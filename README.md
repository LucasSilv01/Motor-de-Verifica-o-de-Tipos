[Relatorio_Tecnico_Motor_Verificacao_Tipos_Completo.pdf](https://github.com/user-attachments/files/28730077/Relatorio_Tecnico_Motor_Verificacao_Tipos_Completo.pdf)

# Motor de Verificação de Tipos

Um projeto educacional implementando um **motor de verificação de tipos** em Python com suporte completo a análise semântica, escopos aninhados e coerção de tipos.

## 📋 Descrição

Este motor simula a etapa de **verificação semântica** de um compilador real. Ele processa uma Árvore de Sintaxe Abstrata (AST) representada em JSON e valida:

- ✅ Declaração e escopo de variáveis
- ✅ Compatibilidade de tipos em atribuições
- ✅ Operações aritméticas e comparações
- ✅ Coerção implícita e cast explícito
- ✅ Expressões condicionais

## 🛠️ Requisitos

- **Python 3.10+**
- Dependências opcionais (para gerar PDF): `markdown`, `fpdf`

## 📦 Estrutura do Projeto

```
.
├── type_checker.py       # Motor principal de verificação de tipos
├── examples.json         # Entrada de teste em formato JSON
├── report.md             # Relatório técnico (Markdown)
├── generate_report.py    # Conversor Markdown → PDF
├── requirements.txt      # Dependências Python
└── README.md             # Esta documentação
```

## 🚀 Como Executar

### Opção 1: Usar o Python System (mais rápido)

```powershell
# Navegue para a pasta do projeto
cd caminho/para/o/projeto

python type_checker.py
```

### Opção 2: Usar a Virtualenv (recomendado)

```powershell
# Navegue para a pasta do projeto
cd caminho/para/o/projeto

# Windows
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate

python type_checker.py
```

### Opção 3: Executar com arquivo JSON específico

```powershell
python type_checker.py examples.json
```

> **Nota:** Substitua `caminho/para/o/projeto` pelo diretório onde você clonou ou baixou este repositório.

## 📝 Exemplos de Uso

### Exemplo 1: Programa Válido

Execute sem argumentos para testar o programa embutido:

```powershell
python type_checker.py
```

**Saída esperada:**
```
Executando programa de exemplo embutido...

Verificação de tipos concluída com sucesso: nenhum erro encontrado.
```

### Exemplo 2: Usando Arquivo JSON

```powershell
python type_checker.py examples.json
```

O arquivo `examples.json` contém um programa demonstrando:
- Declaração de variáveis (`int`, `float`)
- Atribuições com operações aritméticas
- Cast explícito entre tipos
- Expressões condicionais

### Exemplo 3: Detectar Erro de Tipo

Modifique `examples.json` para introduzir um erro:

```json
{
  "type": "VarDecl",
  "name": "x",
  "vartype": "int",
  "value": { "type": "Literal", "value": 3.5 }
}
```

**Saída esperada:**
```
Erro de verificação de tipos: Incompatibilidade de tipos na declaração de 'x': esperado int, obtido float.
```

## 🏗️ Estrutura da AST

O motor suporta os seguintes nós de AST (definidos em JSON):

| Nó | Descrição |
|-----|----------|
| `Program` | Raiz contendo lista de comandos |
| `VarDecl` |Navegar para a Pasta do Projeto

```powershell
cd caminho/para/o/projeto
```

### Passo 2: Ativar Virtualenv

**Windows:**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### Passo 3: Instalar Dependências

```powershell
pip install -r requirements.txt
```

### Passo 4: Gerar PDF

```powershell
python generate_report.py
```

**Resultado:** O arquivo `report.pdf` será criado com as seções do relatório técnico.

> **Nota:** Substitua `caminho/para/o/projeto` pelo diretório onde você clonou este repositóri
```powershell
pip install -r requirements.txt
```

### Passo 3: Gerar PDF

```powershell
python generate_report.py
```

Resultado: arquivo `report.pdf` será criado com as seções do relatório técnico.

## ✅ Validação de Tipos

O motor implementa as seguintes regras:

| Operação | Tipos Válidos | Resultado |
|----------|---------------|-----------|
| Aritméticos (+, -, *, /) | `int`, `float` | `int` se ambos `int`, senão `float` |
| Comparação (==, !=, <, >, <=, >=) | `int`, `float` (compatíveis) | `bool` |
| Atribuição | Tipos devem ser compatíveis | Erro se incompatível |
| Cast | `int` ↔ `float` | Conversão explícita |
| Promoção | `int` → `float` | Automática em contextos `float` |

## 📌 Notas Importantes

- **Escopo**: Variáveis são verificadas respeitando escopos aninhados dentro de blocos
- **Coerção**: A conversão de `int` para `float` é automática; o inverso requer `cast` explícito
- **Erro Fatal**: Qualquer erro de tipo encerra a verificação imediatamente
- **Formato JSON**: Certifique-se de que o arquivo JSON segue a estrutura esperada

## 📄 Licença

Projeto educacional para fins acadêmicos.
