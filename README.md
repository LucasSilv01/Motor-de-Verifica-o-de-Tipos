# Motor de Verificação de Tipos

Este projeto implementa um **motor de verificação de tipos** em Python, com suporte a AST, escopos aninhados, declaração de variáveis, atribuições, expressões binárias e coerções de tipo (cast).

## Requisitos

- Python 3.10+
- Dependências opcionais para gerar o relatório PDF: `markdown`, `fpdf`

## Como executar

1. Abra um terminal em `c:\Users\josel\Compiladores`
2. Execute:

```powershell
C:/Users/josel/AppData/Roaming/uv/python/cpython-3.14.5-windows-x86_64-none/python.exe type_checker.py examples.json
```

3. Para ver um exemplo incorporado sem arquivo JSON, execute:

```powershell
C:/Users/josel/AppData/Roaming/uv/python/cpython-3.14.5-windows-x86_64-none/python.exe type_checker.py
```

## Testes

O arquivo `examples.json` contém um programa de exemplo que demonstra:

- declaração de variáveis
- atribuição
- operações aritméticas e de comparação
- coerção de tipos com `cast`

## Gerar relatório PDF (opcional)

1. Instale dependências:

```powershell
C:/Users/josel/AppData/Roaming/uv/python/cpython-3.14.5-windows-x86_64-none/python.exe -m pip install -r requirements.txt
```

2. Execute:

```powershell
C:/Users/josel/AppData/Roaming/uv/python/cpython-3.14.5-windows-x86_64-none/python.exe generate_report.py
```

Se faltar uma dependência, o script avisará qual módulo está ausente.

O arquivo `report.pdf` será gerado a partir de `report.md`.
