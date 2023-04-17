import re
with open('ejemplo.txt', 'r') as file:
    for line in file:
        text=line
        # Input text
        # text = "let token1 = 'a'|'b'\nlet token2 = 'c'*
        regex = r'^let\s+(\w+)\s+=\s+(.*)$'

        matches = re.findall(regex, text, re.MULTILINE)

        for match in matches:
            name = match[0]
            value = match[1].strip()
            print(name, value)
        

        