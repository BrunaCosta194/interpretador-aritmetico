# Mini Compilador / Interpretador de Expressões Aritméticas

Este projeto é um **mini compilador e interpretador** de expressões aritméticas, desenvolvido em Python utilizando a biblioteca **PLY** (Python Lex-Yacc). Ele realiza a análise léxica, sintática e semântica de expressões numéricas, respeitando a precedência de operadores e o uso de parênteses.

## 🎯 Funcionalidades

- ✅ Análise léxica: reconhecimento de números, operadores e parênteses.
- ✅ Análise sintática: validação da estrutura das expressões com base em uma gramática livre de contexto.
- ✅ Análise semântica: interpretação e cálculo imediato do valor das expressões.
- ✅ Suporte a operações: soma (+), subtração (-), multiplicação (*), divisão (/).
- ✅ Suporte a expressões aninhadas com parênteses.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **PLY (Python Lex-Yacc)**

## 📚 Conceitos de Compiladores Aplicados

- **Analisador Léxico (Scanner):** separa a expressão em tokens.
- **Analisador Sintático (Parser):** valida a ordem e combinação dos tokens segundo uma gramática.
- **Analisador Semântico:** executa operações e calcula os resultados.
  
Embora não gere código executável, o projeto segue as etapas iniciais de um compilador, funcionando como um **interpretador**.

## 📄 Estrutura do Projeto

interpretador/
├── interpretador.py # Arquivo principal com as regras léxicas e sintáticas
├── parsetab.py # Arquivo gerado automaticamente pelo PLY
└── README.md # Este documento

## 🚀 Como Executar

1. **Clone o repositório:**

```bash
git clone https://github.com/seuusuario/interpretador-aritmetico.git
cd interpretador-aritmetico

Instale a biblioteca PLY
pip install ply
Execute o interpretador
python interpretador.py

Digite expressões:
Digite uma expressão: (2 + 3) * 4
Resultado: 20
🧩 Exemplo de Entrada e Saída
Entrada: (5 + 10) * 3 - 8 / 2  
Resultado: 40.0  

README.md: Esta documentação.



