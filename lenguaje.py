import re

class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __str__(self):
        return f"{self.tipo}({self.valor}) en línea {self.linea}, columna {self.columna}"

# Palabras reservadas
keywords = {
    "varier", "laisser", "constant", "entier", "flottant", "chaine", "booleen",
    "si", "sinon", "sinonSi", "choisir", "cas", "parDefaut",
    "tantQue", "faire", "fonction", "retour", "afficher"
}

# Lista de especificaciones de tokens: (tipo, patrón regex)
token_specification = [
    ('COMMENT2',  r':\)\[.*?\]:\)'),               # Comentario multilínea
    ('COMMENT1',  r':\).*'),                       # Comentario una línea
    ('STRING',    r'"[^"\n]*"'),                   # Cadena entre comillas
    ('FLOAT',     r'\d+\.\d+'),                    # Números flotantes
    ('INT',       r'\d+'),                         # Números enteros
    ('ID',        r'[a-zA-Z_]\w*'),                # Identificadores
    ('EQ',        r'=='),                          # Igualdad
    ('NEQ',       r'!='),                          # Diferente
    ('GE',        r'>='),                          # Mayor o igual
    ('LE',        r'<='),                          # Menor o igual
    ('GT',        r'>'),                           # Mayor
    ('LT',        r'<'),                           # Menor
    ('ASSIGN',    r'='),                           # Asignación
    ('PLUS',      r'\+'),                          # Suma
    ('MINUS',     r'-'),                           # Resta
    ('MULT',      r'\*'),                          # Multiplicación
    ('DIV',       r'/'),                           # División
    ('LPAREN',    r'\('),                          # (
    ('RPAREN',    r'\)'),                          # )
    ('LBRACE',    r'\{'),                          # {
    ('RBRACE',    r'\}'),                          # }
    ('LBRACK',    r'\['),                          # [
    ('RBRACK',    r'\]'),                          # ]
    ('NEWLINE',   r'\n'),                          # Saltos de línea
    ('SKIP',      r'[ \t]+'),                      # Espacios y tabulaciones
    ('MISMATCH',  r'.'),                           # Cualquier otro (error)
]


# Compilar expresión regular general
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
get_token = re.compile(tok_regex).match

def lexer(texto):
    linea = 1
    columna = 1
    pos = 0
    tokens = []

    while pos < len(texto):
        match = get_token(texto, pos)
        if not match:
            print(f"Error léxico en línea {linea}, columna {columna}: {texto[pos]!r}")
            pos += 1
            columna += 1
            continue

        tipo = match.lastgroup
        lexema = match.group(tipo)

        if tipo == 'NEWLINE':
            linea += 1
            columna = 1
            pos = match.end()
            continue
        elif tipo == 'SKIP':
            columna += len(lexema)
            pos = match.end()
            continue
        elif tipo == 'MISMATCH':
            print(f"Error léxico en línea {linea}, columna {columna}: {lexema!r}")
            pos = match.end()
            columna += len(lexema)
            continue
        elif tipo == 'ID' and lexema in keywords:
            tipo = 'PALABRA_RESERVADA'

        tokens.append(Token(tipo, lexema, linea, columna))
        pos = match.end()
        columna += len(lexema)

    return tokens

# Ejecución principal
if __name__ == '__main__':
    with open("archivo_fuente.txt", "r", encoding="utf-8") as f:
        contenido = f.read()

    tokens = lexer(contenido)
    with open("salida_tokens.txt", "w", encoding="utf-8") as salida:
        for token in tokens:
            salida.write(str(token) + "\n")