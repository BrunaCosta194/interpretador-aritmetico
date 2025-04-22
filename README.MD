Interpretador de Expressões Aritméticas

Introdução

Este projeto é um interpretador de expressões aritméticas desenvolvido para a disciplina de Linguagens Formais e Autômatos. Ele utiliza conceitos de autômatos finitos e gramáticas livres de contexto para processar expressões aritméticas, tanto em formato numérico (ex.: 2 + 3 * 4) quanto em linguagem natural (ex.: dois mais três). O interpretador também integra inteligência artificial (modelo T5) para normalizar entradas em linguagem natural e uma interface gráfica (Gradio) para interação com o usuário.

Funcionalidades





Processa expressões aritméticas simples com operadores + e *.



Suporta parênteses para definir precedência (ex.: (1 + 2) * 3).



Converte linguagem natural em expressões aritméticas (ex.: dois mais três → 2 + 3).



Exibe os tokens gerados pelo lexer (ex.: NUMBER(2), PLUS, NUMBER(3)).



Interface visual com Gradio para facilitar a interação.



Requisitos

Pré-requisitos





Python 3.12 (ou superior, mas 3.12 é recomendado para compatibilidade com as bibliotecas).



Git (para clonar o repositório).



Um ambiente virtual (venv) é recomendado para gerenciar as dependências.

Bibliotecas Necessárias





ply==3.11



transformers==4.51.3



torch==2.6.0



sentencepiece==0.2.0



gradio==5.25.1



Instalação

Siga os passos abaixo para configurar o projeto no seu computador:





Clone o repositório do GitHub:

git clone https://github.com/BrunaCosta194/interpretador-aritmetico
cd interpretador_aritmetico



Crie e ative um ambiente virtual:

python -m venv venv
.\venv\Scripts\activate  # No Windows
# ou
source venv/bin/activate  # No Linux/Mac



Instale as dependências:

pip install ply==3.11 transformers==4.51.3 torch==2.6.0 sentencepiece==0.2.0 gradio==5.25.1



Execute o interpretador:

python interpretador.py



Acesse a interface Gradio:





Após executar o comando acima, o terminal mostrará um link como:

Running on local URL: http://127.0.0.1:7860



Abra o link no seu navegador para usar a interface.



Como Usar





Digite uma expressão aritmética:





No campo "Expressão" da interface Gradio, digite uma expressão como:





2 + 3 * 4



dois mais três



(1 + 2) * 3



Clique em "Enviar":





A interface mostrará:





Expressão Normalizada: A expressão após ser processada (ex.: dois mais três → 2 + 3).



Resultado: O valor calculado (ex.: 5 para 2 + 3).



Tokens Gerados: Os tokens identificados pelo lexer (ex.: NUMBER(2), PLUS, NUMBER(3)).

Exemplos







Entrada



Expressão Normalizada



Resultado



Tokens Gerados





2 + 3 * 4



2 + 3 * 4



14



NUMBER(2), PLUS, NUMBER(3), TIMES, NUMBER(4)





dois mais três



2 + 3



5



NUMBER(2), PLUS, NUMBER(3)





(1 + 2) * 3



(1 + 2) * 3



9



LPAREN, NUMBER(1), PLUS, NUMBER(2), RPAREN, TIMES, NUMBER(3)



Conceitos Teóricos

Este projeto integra conceitos de Linguagens Formais e Autômatos com inteligência artificial e interface gráfica:

Lexer (Autômato Finito)





O lexer, implementado com ply.lex, é um autômato finito que converte a entrada (ex.: 2 + 3) em uma sequência de tokens (ex.: NUMBER(2), PLUS, NUMBER(3)).



Ele reconhece números, operadores (+, *) e parênteses ((, )).

Parser (Gramática Livre de Contexto)





O parser, implementado com ply.yacc, usa uma gramática livre de contexto para avaliar a estrutura da expressão e calcular o resultado.



Exemplo de gramática:

expression : expression PLUS term
           | term
term       : term TIMES factor
           | factor
factor     : NUMBER
           | LPAREN expression RPAREN

Inteligência Artificial (T5)





O modelo T5 (t5-small) da Hugging Face é usado para normalizar entradas em linguagem natural (ex.: dois mais três → 2 + 3).



Pré-processamento manual foi adicionado para melhorar a precisão do T5 (ex.: substituição de "dois" por 2).

Interface Gradio





A biblioteca gradio fornece uma interface web para interagir com o interpretador, exibindo a expressão normalizada, o resultado e os tokens gerados.



Aplicações Práticas

Este interpretador pode ser usado em:





Calculadoras Inteligentes: Processar expressões aritméticas em linguagem natural.



Ferramentas Educacionais: Ensinar conceitos de matemática e linguagens formais.



Automação de Tarefas: Resolver expressões aritméticas em sistemas que processam linguagem natural.



Estrutura do Projeto





interpretador.py: Código principal com o lexer, parser, integração com T5 e interface Gradio.



test_libs.py: Script para testar a instalação das bibliotecas.



.gitignore: Ignora arquivos desnecessários (ex.: ambiente virtual, arquivos temporários).



README.md: Esta documentação.



