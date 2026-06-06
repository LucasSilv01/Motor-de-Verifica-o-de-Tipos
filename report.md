# Introdução

Este relatório descreve o desenvolvimento de um **Motor de Verificação de Tipos** simples para um compilador educacional. O sistema valida programas representados como uma Árvore de Sintaxe Abstrata (AST) em JSON, identificando inconsistências de tipos em declarações, atribuições e expressões.

# Metodologia de Implementação

O motor foi implementado em Python com as seguintes estruturas:

- `Scope`: controla escopos aninhados usando dicionários (`Hash Tables`) e permite `declarar` e `buscar` variáveis.
- `ASTNode` e subclasses: modelos para expressões e comandos como `Literal`, `VarRef`, `BinaryOp`, `Cast`, `VarDecl`, `Assignment`, `Block`, `If` e `Program`.
- `TypeChecker`: percorre a AST usando métodos `visit_*` e aplica regras de tipo para operações aritméticas, comparações e coerção.

A análise de tipo considera:

- `int`, `float` e `bool`
- promoção implícita de `int` para `float`
- cast explícito entre `int` e `float`
- verificação de compatibilidade em declarações e atribuições
- validação de condições de `if` como `bool`

# Casos de Teste

## Caso de Teste 1: Programa de Exemplo

Entrada (`examples.json`):

```json
{
  "type": "Program",
  "body": [
    {
      "type": "VarDecl",
      "name": "x",
      "vartype": "int",
      "value": { "type": "Literal", "value": 2 }
    },
    {
      "type": "VarDecl",
      "name": "y",
      "vartype": "float",
      "value": { "type": "Literal", "value": 3.5 }
    },
    {
      "type": "Assignment",
      "name": "x",
      "value": {
        "type": "BinaryOp",
        "operator": "+",
        "left": { "type": "VarRef", "name": "x" },
        "right": {
          "type": "Cast",
          "targetType": "int",
          "expression": { "type": "VarRef", "name": "y" }
        }
      }
    }
  ]
}
```

Saída esperada:

```
Verificação de tipos concluída com sucesso: nenhum erro encontrado.
```

## Caso de Teste 2: Atribuição com erro de tipo

Entrada:

```json
{
  "type": "Program",
  "body": [
    {
      "type": "VarDecl",
      "name": "x",
      "vartype": "int",
      "value": { "type": "Literal", "value": 2 }
    },
    {
      "type": "Assignment",
      "name": "x",
      "value": { "type": "Literal", "value": 3.5 }
    }
  ]
}
```

Saída esperada:

```
Erro de verificação de tipos: Incompatibilidade de tipos na atribuição de 'x': esperado int, obtido float.
```

## Execução direta com programa embutido

Comando:

```powershell

```

Saída esperada:

```
Executando programa de exemplo embutido...

Verificação de tipos concluída com sucesso: nenhum erro encontrado.
```
