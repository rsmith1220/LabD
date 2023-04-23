tokens={}
numeros=['1','2','3','4','5','6','7','8','9','0','-1','-2','-3','-4','-5','-6','-7','-8','-9']
operadores=["*","+","|","?","^"]
variables =['var','let']
noentra=['@','!','&','%','$','#','[]']
abece=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','r','s','t','u','v','w','x','y','z']
filita=1
open('resultado.txt','w')

with open('yalex1.txt', 'r') as file:
    for line in file:
        text=line
        inside_block_comment = False  # flag to keep track of whether we're inside a block comment or not
        filita+=1
        with open('resultado.txt', 'a') as f:
            tickets = line.split()
            # print(tickets)
            for token in tickets:
                for i in noentra:
                    if i in text:
                        print("\n!!!!!!!!\nerror en la linea ",filita," no se puede identificar el token",i,'\n')
                        f.write(i+' --> error\n')

                if any(op in token for op in operadores):
                    for char in  token:
                        if char in abece:
                            f.write(char+' --> letra\n')
                        elif char in operadores:
                            if char == '+':
                                f.write(char+' --> operador de suma\n')
                            elif char == '*':
                                f.write(char+' --> operador kleene\n')
                            elif char == '|':
                                f.write(char+' --> operador or\n')
                            elif char == '?':
                                f.write(char+' --> operador desicion\n')
                            elif char == '^':
                                f.write(char+' --> operador de potencia\n')
                        elif '.' in token and any(char.isdigit() for char in token):
                            # check if token has decimal point and contains at least one digit
                            f.write(token + ' --> numero decimal\n')
                        elif char in numeros:
                            # check if token is a regular integer
                            f.write(char + ' --> numero\n')
                        else:
                            pass
                elif token == 'IF' or token =='if' or token =='If':
                    f.write(token+' --> IF\n')
                elif token == 'FOR' or token =='for' or token =='For':
                    f.write(token+' --> FOR\n')
                elif token == 'WHILE' or token =='while' or token =='While':
                    f.write(token+' --> WHILE\n')
                
                elif token == "=":
                    f.write(token+' --> operador de asignacion\n')
                elif any(var in token for var in variables):
                    f.write(token+' --> identificador\n')


                # aqui verifica si es un comentario
                elif line.startswith("/*") or line.startswith("(*"):
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
                    f.write(token+' --> variable asignada\n')
              