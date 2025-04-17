import ply.lex as lex
import ply.yacc as yacc
from transformers import T5Tokenizer, T5ForConditionalGeneration
import gradio as gr

# Lexer
tokens = (
    'NUMBER',
    'PLUS',
    'TIMES',
    'LPAREN',
    'RPAREN',
)

t_PLUS = r'\+'
t_TIMES = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    return f"SCANNING error. ILLEGAL character '{t.value[0]}'"

lexer = lex.lex()

def reset_lexer():
    lexer.input("")
    lexer.lineno = 1

# Parser
precedence = (
    ('left', 'PLUS'),
    ('left', 'TIMES'),
)

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_paren(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    return "Syntax error in input!"
parser = yacc.yacc()


# T5 Model
print("Carregando modelo T5...")
tokenizer = T5Tokenizer.from_pretrained('t5-small')
model = T5ForConditionalGeneration.from_pretrained('t5-small')

def preprocess_expression(expression):
    replacements = {
        'zero': '0',
        'um': '1',
        'dois': '2',
        'três': '3',
        'tres': '3',
        'quatro': '4',
        'cinco': '5',
        'seis': '6',
        'sete': '7',
        'oito': '8',
        'nove': '9',
        'dez': '10',
        'mais': '+',
        'vezes': '*',
        'x': '*',
        'multiplicado por': '*',
        'dividido por': '/',
        'menos': '-',
        'abre parênteses': '(',
        'fecha parênteses': ')'
    }

    for word, replacement in replacements.items():
        expression = expression.replace(word, replacement)
    return expression

def normalize_expression(expression):
    expression = preprocess_expression(expression)
    return expression


def tokenize_and_parse(expression):
    global parser
    reset_lexer()
    lexer.input(expression)
    tokens = []
    for tok in lexer:
        tokens.append(f"{tok.type}({tok.value})")
    try:
        result = parser.parse(expression)
        return tokens, result
    except Exception as e:
        return tokens, str(e)


def interpret_expression(expression):
    try:
        normalized = normalize_expression(expression)
        tokens, result = tokenize_and_parse(normalized)
        return normalized, result, ", ".join(tokens)
    except Exception as e:
        return expression, f"Erro: {str(e)}", "Nenhum token gerado"

# Gradio Interface
# Gradio Interface
print("Iniciando a interface Gradio...")

interface = gr.Interface(
    fn=interpret_expression,
    inputs=gr.Textbox(label="Expressão", placeholder="Ex.: 2 + 3 * 4, dois mais tres, 2+3X4"),
    outputs=[
        gr.Textbox(label="Expressão Normalizada"),
        gr.Textbox(label="Resultado"),
        gr.Textbox(label="Tokens Gerados")
    ],
    title="🎮 Interpretador de Expressões Aritméticas",
    description="Digite uma expressão usando números ou palavras, como 'dois mais três'. '2 + 3 * 4' ",
    submit_btn="🧠 Calcular",
    clear_btn="🧹 Limpar"
)

# Custom CSS (tema retrô estilo Atari)
interface.theme = gr.themes.Base().set(
    body_background_fill="#1a1a1a",  # Fundo escuro
    body_text_color="#f5f5f5",       # Texto claro
    button_primary_background_fill="#ff4c00",  # Botão laranja Atari
    button_primary_text_color="white",
    block_label_text_color="#ff4c00",  # Títulos em laranja
    button_secondary_background_fill="#333333",  # Botão secundário
    button_secondary_text_color="white",
    block_border_color="#ff4c00",
)

interface.launch()
