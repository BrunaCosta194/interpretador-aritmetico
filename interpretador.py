import ply.lex as lex
import ply.yacc as yacc
# Se você decidir não usar T5 por enquanto e quiser acelerar o início, 
# pode comentar as duas linhas seguintes (e as de carregamento do T5 mais abaixo)
from transformers import T5Tokenizer, T5ForConditionalGeneration 
import gradio as gr

modern_tech_theme = gr.themes.Base(
    font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "ui-monospace", "Consolas", "monospace"],
).set(
    # Cores de Fundo
    body_background_fill="#171A1D",
    block_background_fill="#22262A",
    input_background_fill="#2C3034",
    
    # Cores de Texto
    body_text_color="#E8EAED",
    block_label_text_color="#00CFE8",
    block_title_text_color="#00CFE8",
    body_text_color_subdued="#909399",

    button_primary_background_fill="#00A9E0",
    button_primary_background_fill_hover="#0095C7",
    button_primary_text_color="#FFFFFF",
    
    button_secondary_background_fill="#3A3F44",
    button_secondary_background_fill_hover="#4A4F54",
    button_secondary_text_color="#E8EAED",
   
    # Bordas
    block_border_width="1px",
    block_border_color="#3A3F44",
    input_border_width="1px",
    input_border_color="#4A4F54",

    # Cores de Destaque (Accent)
    color_accent="#00CFE8",
    color_accent_soft="rgba(0, 207, 232, 0.1)",

)
# --- Lexer ---
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN',
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    error_message = f"Caractere ilegal '{t.value[0]}' na expressão normalizada ('{t.lexer.lexdata}'), linha {t.lineno}"
    print(error_message) 
    t.lexer.skip(1)

lexer = lex.lex()

# --- Parser ---
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    if p[3] == 0:
        raise ZeroDivisionError("Erro: Divisão por zero!")
    p[0] = p[1] / p[3]

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
    if p:
        # Este é o erro que será retornado para a interface se houver erro de sintaxe
        p.lexer.error_message = f"Erro de sintaxe próximo a '{p.value}'" 
    else:
        p.lexer.error_message = "Erro de sintaxe: Expressão incompleta ou inválida."
    # Não retornamos nada aqui, o parser do PLY lida com a recuperação de erro ou para.
    # A mensagem de erro customizada é atribuída para ser usada depois.

parser = yacc.yacc()

# --- Modelos T5 (Carregados mas não usados ativamente na abordagem de regras para NLP) ---
# Se decidir não usar T5, pode comentar estas linhas e o import lá em cima.
print("Carregando modelo T5 (pode ser removido se não usado)...")

def preprocess_expression(expression_text):
    replacements = {
        'zero': '0', 'um': '1', 'dois': '2', 'três': '3', 'tres': '3', 
        'quatro': '4', 'cinco': '5', 'seis': '6', 'sete': '7', 'oito': '8', 
        'nove': '9', 'dez': '10', 'onze': '11', 'doze': '12', 'treze': '13', 
        'quatorze': '14', 'quinze': '15', 'dezesseis': '16', 'dezessete': '17', 
        'dezoito': '18', 'dezenove': '19', 'vinte': '20', 'vinte e um': '21',
        'trinta': '30', 'quarenta': '40', 'cinquenta': '50',
        'mais': '+', 'vezes': '*', 'x': '*', 'multiplicado por': '*',
        'dividido por': '/', 'menos': '-',
        'abre parênteses': '(', 'fecha parênteses': ')'
    }
    sorted_words = sorted(replacements.keys(), key=len, reverse=True)
    for word in sorted_words:
        replacement = replacements[word]
        expression_text = expression_text.replace(word, replacement)
    return expression_text.strip()

def normalize_phrase_and_convert_to_math(natural_language_input):
    text = natural_language_input.lower()
    
    fillers_to_remove_at_start = [
        "converta a seguinte frase para uma expressão matemática simples (apenas números e operadores em palavras):",
        "qual é o resultado de", "qual o resultado de", "resultado de",
        "calcule para mim", "calcule",
        "me diga quanto é", "quanto é", "quanto dá",
        "por favor calcule",
    ]
    
    # Remover aspas do input se presentes
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
        
    original_text_for_debug = text 
    
    for filler in fillers_to_remove_at_start:
        if text.startswith(filler):
            text = text.replace(filler, "", 1).strip()
            break 
            
    print(f"Texto original (após lower e aspas): '{original_text_for_debug}'")
    print(f"Texto após remoção de fillers: '{text}'")

    final_normalized_expression = preprocess_expression(text)
    print(f"Expressão após preprocess_expression (regras): '{final_normalized_expression}'")
    
    return final_normalized_expression

def tokenize_and_parse(expression_to_parse):
    lexer.input(expression_to_parse)
    lexer.error_message = None # Reseta a mensagem de erro customizada
    
    tokens_generated = []
    while True:
        tok = lexer.token()
        if not tok: 
            break
        tokens_generated.append(f"{tok.type}({tok.value})")

    if not tokens_generated and expression_to_parse.strip():
        
        return tokens_generated, "Erro: A expressão contém apenas caracteres não reconhecidos."

    try:
        # O parser usa o estado do lexer (que já teve lexer.input(expression_to_parse))
        result = parser.parse(expression_to_parse, lexer=lexer) # Passar o lexer explicitamente

        if lexer.error_message: # Verifica se p_error definiu uma mensagem
             return tokens_generated, lexer.error_message
        
        if result is None and not expression_to_parse.strip() == "":
            if tokens_generated : 
                 return tokens_generated, "Erro de sintaxe: Expressão mal formada ou não calculável."
            

        return tokens_generated, result
    except ZeroDivisionError as zde:
        return tokens_generated, str(zde)
    except Exception as e: # Outros erros inesperados durante o parsing
        print(f"Exceção em tokenize_and_parse: {e}")
        return tokens_generated, f"Erro de parsing: {e}"

def interpret_expression(expression_input_by_user):
    try:
        if not expression_input_by_user or not expression_input_by_user.strip():
            return "N/A", "Por favor, digite uma expressão.", "N/A"

        normalized_expression_for_ply = normalize_phrase_and_convert_to_math(expression_input_by_user)
        
        if not normalized_expression_for_ply.strip():
            return expression_input_by_user, "A normalização resultou em uma expressão vazia.", "Nenhum token gerado"

        tokens_display_list, calculation_result = tokenize_and_parse(normalized_expression_for_ply)
        
        result_display_str = ""
        if isinstance(calculation_result, (int, float)):
            result_display_str = str(calculation_result)
        elif isinstance(calculation_result, str): # Mensagem de erro do parser/lexer
            result_display_str = calculation_result
        elif calculation_result is None:
        
            result_display_str = "Erro: Não foi possível calcular um resultado."
            if not tokens_display_list and normalized_expression_for_ply:
                 result_display_str = "Erro: Caracteres não reconhecidos na expressão."

        else: # Caso inesperado para o tipo de resultado
            result_display_str = f"Tipo de resultado inesperado: {type(calculation_result)}"

        return normalized_expression_for_ply, result_display_str, ", ".join(tokens_display_list)
    
    except Exception as e:
        print(f"Erro crítico em interpret_expression: {e}") 
        return expression_input_by_user, f"Erro crítico no sistema: {str(e)}", "Nenhum token gerado"

# --- Gradio Interface ---
print("Iniciando a interface Gradio...")

interface = gr.Interface(
    fn=interpret_expression,
    inputs=gr.Textbox(lines=2, label="Expressão", placeholder="Ex.: 2 + 3 * 4, dois mais tres, quanto é 5 x quatro"),
    outputs=[
        gr.Textbox(label="Expressão Normalizada (Alimentada ao Parser)"),
        gr.Textbox(label="Resultado do Cálculo"),
        gr.Textbox(label="Tokens Gerados pelo Lexer")
    ],
    title="🤖 Interpretador de Expressões Aritméticas com NLP",
    description="Digite uma expressão matemática usando números, palavras (ex: 'dois mais três') ou frases (ex: 'quanto é cinco vezes quatro'). O sistema tentará normalizar e calcular.",
    theme=modern_tech_theme, 
    submit_btn="Calcular 🧮",
    clear_btn="Limpar 🧹"
)

if __name__ == '__main__':
    interface.launch()