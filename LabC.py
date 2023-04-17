import re
import automata

tokens={}
numeros=['1','2','3','4','5','6','7','8','9','0','-1','-2','-3','-4','-5','-6','-7','-8','-9']
operadores=["*","+","|","?"]
variables =['var','let']
noentra=['@','/','!','&','^','%','$','#','[]']
filita=1
""" with open('entrada1.txt', 'r') as file:
    for line in file:
        text=line
        inside_block_comment = False  # flag to keep track of whether we're inside a block comment or not
        filita+=1
        
        # print("Identificador")
        # fila = "var + 5 * -11 = otraVariable + 2"
        tickets = line.split()
        # print(tickets)
        for token in tickets:
            
            if any(op in token for op in operadores):
                print("Operador")
            elif any(num in token for num in numeros):
                print("Numero")
            elif token == "=":
                print("Operador de asignacion")
            elif any(var in token for var in variables):
                print("Identificador")
            elif token in noentra:
                print("\n!!!!!!!!\nerror en la linea ",filita," no se puede identificar el token")
                print("Terminando programa\n")
                exit()

            # aqui verifica si es un comentario
            elif line.startswith("/*"):
                if inside_block_comment:
                    #si estamos en un bloque de comentario, revisar si alli termina o sigue
                    if '*/' in line and inside_block_comment or '*)' in line and inside_block_comment:
                        inside_block_comment = False  # found the end of the comment
                else:
                    #revisar si comienza el bloque de comentario
                    if '/*' in line or '(*' in line:
                        inside_block_comment = True  # found the start of a comment
                    else:
                        #si no se esta en un comentario, continuar
                        pass
            else:
                pass
            # elif line.startswith(numeros):
            #     print("Error lexico, token no reconocido")
            #     exit() """

with open('ejemplo.txt', 'r') as file:
    for line in file:
        text=line
        for char in noentra:
            if char in line:
                print("Error en la linea", filita,"\nEl programa se cerrara")
                exit()
        # Input text
        # text = "let token1 = 'a'|'b'\nlet token2 = 'c'*
        regex = r'^let\s+(\w+)\s+=\s+(.*)$'

        matches = re.findall(regex, text, re.MULTILINE)

        for match in matches:
            name = match[0]
            value = match[1].strip()
            tokens[name]=value
            # print(tokens)
            filita+=1


    acepta = ['ε','1','2','3','4','5','6','7','8','9','*','+','|','?','(',')']

    #se itera para verificar cuales son las variables que no tienen un valor especifico
    for key in ['numero', 'identificador']:
        
        pattern = tokens[key][1:-1]  
        pattern = re.sub(r'digito', tokens['digito'][1:-1], pattern)
        pattern = re.sub(r'letra', tokens['letra'][1:-1], pattern)
        
        tokens[key] = f'"{pattern}"'

print(tokens)
construir=[]
s=''
for key, value in tokens.items():
    s = f' {value}'
    s = s.replace('"', '')
    s=s.strip()
    construir.append(s)



#se regresa el diccionario con sus respectivos valores
print(construir)
automata.cadena(construir)   


    

