import json
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


class TypeCheckError(Exception):
    pass


class Scope:
    def __init__(self, parent: Optional['Scope'] = None) -> None:
        self.parent = parent
        self.table: Dict[str, str] = {}

    def declare(self, name: str, vartype: str) -> None:
        if name in self.table:
            raise TypeCheckError(f"Variável '{name}' já declarada no escopo atual.")
        self.table[name] = vartype

    def lookup(self, name: str) -> str:
        if name in self.table:
            return self.table[name]
        if self.parent is not None:
            return self.parent.lookup(name)
        raise TypeCheckError(f"Variável '{name}' não declarada.")


@dataclass
class ASTNode:
    pass


@dataclass
class Literal(ASTNode):
    value: Any


@dataclass
class VarRef(ASTNode):
    name: str


@dataclass
class BinaryOp(ASTNode):
    operator: str
    left: ASTNode
    right: ASTNode


@dataclass
class Cast(ASTNode):
    target_type: str
    expression: ASTNode


@dataclass
class VarDecl(ASTNode):
    name: str
    vartype: str
    value: ASTNode


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class If(ASTNode):
    condition: ASTNode
    then_branch: Block
    else_branch: Optional[Block] = None


@dataclass
class Program(ASTNode):
    body: List[ASTNode]


class TypeChecker:
    def __init__(self) -> None:
        self.global_scope = Scope()
        self.current_scope = self.global_scope

    def enter_scope(self) -> None:
        self.current_scope = Scope(parent=self.current_scope)

    def exit_scope(self) -> None:
        if self.current_scope.parent is None:
            raise TypeCheckError("Tentativa de sair do escopo global.")
        self.current_scope = self.current_scope.parent

    def visit(self, node: ASTNode) -> str:
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if method is None:
            raise TypeCheckError(f"Tipo de nó desconhecido: {type(node).__name__}")
        return method(node)

    def visit_Program(self, node: Program) -> str:
        for stmt in node.body:
            self.visit(stmt)
        return "program"

    def visit_Block(self, node: Block) -> str:
        self.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.exit_scope()
        return "block"

    def visit_VarDecl(self, node: VarDecl) -> str:
        value_type = self.visit(node.value)
        if not self.compatible_types(node.vartype, value_type):
            raise TypeCheckError(
                f"Incompatibilidade de tipos na declaração de '{node.name}': "
                f"esperado {node.vartype}, obtido {value_type}."
            )
        self.current_scope.declare(node.name, node.vartype)
        return node.vartype

    def visit_Assignment(self, node: Assignment) -> str:
        value_type = self.visit(node.value)
        variable_type = self.current_scope.lookup(node.name)
        if not self.compatible_types(variable_type, value_type):
            raise TypeCheckError(
                f"Incompatibilidade de tipos na atribuição de '{node.name}': "
                f"esperado {variable_type}, obtido {value_type}."
            )
        return variable_type

    def visit_VarRef(self, node: VarRef) -> str:
        return self.current_scope.lookup(node.name)

    def visit_Literal(self, node: Literal) -> str:
        if isinstance(node.value, bool):
            return "bool"
        if isinstance(node.value, int):
            return "int"
        if isinstance(node.value, float):
            return "float"
        raise TypeCheckError(f"Tipo literal não suportado: {node.value!r}")

    def visit_BinaryOp(self, node: BinaryOp) -> str:
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.operator in {"+", "-", "*", "/"}:
            if left_type == "bool" or right_type == "bool":
                raise TypeCheckError("Operações aritméticas não aceitam bool.")
            if left_type == "float" or right_type == "float":
                return "float"
            return "int"

        if node.operator in {"==", "!=", "<", ">", "<=", ">="}:
            if left_type != right_type and not {
                left_type, right_type
            } == {"int", "float"}:
                raise TypeCheckError(
                    f"Comparação inválida entre {left_type} e {right_type}."
                )
            return "bool"

        raise TypeCheckError(f"Operador desconhecido: {node.operator}")

    def visit_Cast(self, node: Cast) -> str:
        expression_type = self.visit(node.expression)
        if expression_type == node.target_type:
            return node.target_type
        if {expression_type, node.target_type} <= {"int", "float"}:
            return node.target_type
        raise TypeCheckError(
            f"Cast inválido: não é possível converter {expression_type} para {node.target_type}."
        )

    def visit_If(self, node: If) -> str:
        condition_type = self.visit(node.condition)
        if condition_type != "bool":
            raise TypeCheckError("Condição de if deve ser bool.")
        self.visit(node.then_branch)
        if node.else_branch is not None:
            self.visit(node.else_branch)
        return "void"

    @staticmethod
    def compatible_types(expected: str, actual: str) -> bool:
        if expected == actual:
            return True
        if expected == "float" and actual == "int":
            return True
        return False


def parse_node(data: Dict[str, Any]) -> ASTNode:
    node_type = data["type"]
    if node_type == "Program":
        return Program(body=[parse_node(stmt) for stmt in data["body"]])
    if node_type == "Block":
        return Block(statements=[parse_node(stmt) for stmt in data["statements"]])
    if node_type == "VarDecl":
        return VarDecl(name=data["name"], vartype=data["vartype"], value=parse_node(data["value"]))
    if node_type == "Assignment":
        return Assignment(name=data["name"], value=parse_node(data["value"]))
    if node_type == "VarRef":
        return VarRef(name=data["name"])
    if node_type == "Literal":
        return Literal(value=data["value"])
    if node_type == "BinaryOp":
        return BinaryOp(operator=data["operator"], left=parse_node(data["left"]), right=parse_node(data["right"]))
    if node_type == "Cast":
        return Cast(target_type=data["targetType"], expression=parse_node(data["expression"]))
    if node_type == "If":
        return If(
            condition=parse_node(data["condition"]),
            then_branch=parse_node(data["thenBranch"]),
            else_branch=parse_node(data["elseBranch"]) if data.get("elseBranch") else None,
        )
    raise TypeCheckError(f"Tipo de nó JSON inválido: {node_type}")


def load_program(filename: str) -> Program:
    with open(filename, encoding="utf-8") as file:
        data = json.load(file)
    program = parse_node(data)
    if not isinstance(program, Program):
        raise TypeCheckError("O arquivo JSON deve conter um nó Program.")
    return program


def build_sample_program() -> Program:
    return Program(body=[
        VarDecl(name="x", vartype="int", value=Literal(value=2)),
        VarDecl(name="y", vartype="float", value=Literal(value=3.5)),
        Assignment(
            name="x",
            value=BinaryOp(
                operator="+",
                left=VarRef(name="x"),
                right=Cast(target_type="int", expression=VarRef(name="y")),
            ),
        ),
        Assignment(
            name="y",
            value=BinaryOp(
                operator="*",
                left=VarRef(name="x"),
                right=Literal(value=2.0),
            ),
        ),
        If(
            condition=BinaryOp(
                operator=">",
                left=VarRef(name="y"),
                right=Literal(value=4.0),
            ),
            then_branch=Block(statements=[
                Assignment(name="x", value=Literal(value=10)),
            ]),
            else_branch=Block(statements=[
                Assignment(name="x", value=Literal(value=0)),
            ]),
        ),
    ])


def main() -> None:
    if len(sys.argv) == 2:
        program = load_program(sys.argv[1])
    else:
        print("Executando programa de exemplo embutido...\n")
        program = build_sample_program()

    checker = TypeChecker()
    try:
        checker.visit(program)
        print("Verificação de tipos concluída com sucesso: nenhum erro encontrado.")
    except TypeCheckError as error:
        print(f"Erro de verificação de tipos: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
