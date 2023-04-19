import re
import automata

tokens={}
numeros=['1','2','3','4','5','6','7','8','9','0','-1','-2','-3','-4','-5','-6','-7','-8','-9']
operadores=["*","+","|","?"]
variables =['var','let']
noentra=['@','/','!','&','^','%','$','#','[]']
filita=1


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


    

