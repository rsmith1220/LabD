#Jessica Ortiz 20192

import numpy as np
from copy import deepcopy
from graphviz import Digraph
import re


#stack para hacer las acciones del postfix
class Stack:
     def __init__(self):
         self.items = []

     def empty(self):
         return self.items == []

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def peek(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)


def reescribiendoExpr(regex):
    if re.search(r"\s", regex):
        print("La expresión regular no puede contener espacios.")
        return

    regex = regex.replace('ϵ',' ') 
    # definimos ϵ como vacio
    # y definimos que coloque . donde hay concatenaciones, en el resto no
    newExpr = regex[0]
    for i in range(1,len(regex)):
        if( (((regex[i].isalpha() or regex[i].isdigit() ) 
        and regex[i-1] != '(') or regex[i] == '(') 
        and (regex[i-1] != '|' or regex[i-1] == ')') ):
        
            newExpr += '.'+regex[i]

        else:
            newExpr += regex[i]       
    # print ('Reescribiendo la expresion regular: ' + newExpr)
    return newExpr

def topostfix(regex):
    #definir jerarquia de simbolos
    jerar = {}
    jerar["+"] = 4
    jerar["*"] = 4
    jerar["?"] = 4
    jerar["."] = 3
    jerar["|"] = 2
    jerar["("] = 1
    lista = list(regex)
    output = []

    stack = []

    for item in lista:
        
        if (item.isalpha() or item.isdigit() or item == ' '):
            output.append(item)
        elif (item == '('):
            stack.append(item)
        elif (item == ')'):
            try:
                top = stack.pop()
                while(top != '('):
                    output.append(top)
                    top = stack.pop()
            except IndexError:
                print("Error de sintaxis: paréntesis sin cerrar")
                return
        else:
            while (len(stack) > 0 and jerar[stack[-1]] >= jerar[item]):
                  output.append(stack.pop())
            stack.append(item)
    
    while(len(stack) > 0):
        if stack[-1] in ['(', ')']:
            print("Error de sintaxis: paréntesis sin cerrar")
            return
        output.append(stack.pop())
    
    return ''.join(output)


#termina todo relacionado con postfix

#AFN
class AFN:
    def __init__(self):
        self.estadoInicial = None
        self.estados = set()
        self.estadoFinal = None
        self.transiciones = []

    
    def basic(self, input):
        self.estadoInicial = 0
        self.estadoFinal = 1
        self.estados.add(self.estadoInicial)
        self.estados.add(self.estadoFinal)
        transition = {
            "desde" : self.estadoInicial,
            "=>" : input,
            "hacia" : [self.estadoFinal]
        }
        self.transiciones.append(transition)
        return self

    def display(self):
        object = {
            "estados": self.estados,
            "Estado Inicial": self.estadoInicial,
            "Estado Final": self.estadoFinal,
            "transiciones": self.transiciones
        }
        return object

def basic(input):
    afn = AFN()
    afn.estadoInicial = 0
    afn.estadoFinal = 1
    afn.estados.add(afn.estadoInicial)
    afn.estados.add(afn.estadoFinal)
    transition = {
        "desde" : afn.estadoInicial,
        "=>" : input,
        "hacia" : [afn.estadoFinal]
    }
    afn.transiciones.append(transition)
    return afn

def concat(nfa1, nfa2):
        afn = AFN()
        #trabaja el AFN2
        maximum = max(nfa1.estados)
        for i in range(0,len(nfa2.transiciones)):
            nfa2.transiciones[i]['desde'] += maximum
            nfa2.transiciones[i]['hacia'] = list(np.add(maximum,nfa2.transiciones[i]['hacia']))
        #trabaja el self
        newStates = np.add(maximum, np.array(list(nfa2.estados)))
        newStates = set(set(newStates).union(nfa1.estados))
        afn.estados = newStates
        afn.estadoInicial = nfa1.estadoInicial
        afn.estadoFinal = nfa2.estadoFinal + maximum
        for transition in nfa1.transiciones:
            afn.transiciones.append(transition)
            # print(transition)
        for transition in nfa2.transiciones:
            afn.transiciones.append(transition)
        return afn

def union(nfa1, nfa2):
        afn = AFN()
        #trabaja el AFN1
        newStates1 = np.add(np.array(list(nfa1.estados)),1)
        maximum = max(newStates1)
        nfa1.estadoInicial += 1
        nfa1.estadoFinal += 1
        for i in range(0, len(nfa1.transiciones)):
            nfa1.transiciones[i]['desde']+= 1
            nfa1.transiciones[i]['hacia'] = list(np.add(1, nfa1.transiciones[i]['hacia']))
        #trabaja el AFN2
        nfa2.estadoInicial += maximum + 1
        nfa2.estadoFinal += maximum + 1
        newStates2 = np.add(np.array(list(nfa2.estados)),maximum + 1)
        for i in range(0, len(nfa2.transiciones)):
            nfa2.transiciones[i]['desde']+= maximum + 1
            nfa2.transiciones[i]['hacia'] = list(np.add(maximum + 1, nfa2.transiciones[i]['hacia']))
        #trabaja el self
        afn.estadoInicial = 0
        afn.estadoFinal = nfa2.estadoFinal + 1
        afn.estados.add(afn.estadoInicial)
        for state in newStates1:
            afn.estados.add(state)
        for state in newStates2:
            afn.estados.add(state)
        afn.estados.add(afn.estadoFinal)

        initialTransition = {
            "desde": afn.estadoInicial,
            "=>": " ",
            "hacia": [nfa1.estadoInicial , nfa2.estadoInicial]
        }
        finalTransition1 = {
            "desde": nfa1.estadoFinal,
            "=>": " ",
            "hacia": [afn.estadoFinal]
        }
        finalTransition2 = {
            "desde": nfa2.estadoFinal,
            "=>": " ",
            "hacia": [afn.estadoFinal]
        }
        afn.transiciones.append(initialTransition)
        for transition in nfa1.transiciones:
            afn.transiciones.append(transition)
        for transition in nfa2.transiciones:
            afn.transiciones.append(transition)       
        afn.transiciones.append(finalTransition1)
        afn.transiciones.append(finalTransition2)
        return afn

def kleene(afn):

        nfaMain = AFN()
        nfaMain.estadoInicial = 0
        afn.estados = np.add(np.array(list(afn.estados)),1)
        for i in range(0,len(afn.transiciones)):
            afn.transiciones[i]['desde'] += 1
            afn.transiciones[i]['hacia'] = list(np.add(1,afn.transiciones[i]['hacia']))
        afn.estadoInicial+=1
        afn.estadoFinal+=1
        nfaMain.estadoFinal = afn.estadoFinal + 1
        initialTransition = {
            "desde": nfaMain.estadoInicial,
            "=>":  " ",
            "hacia": [afn.estadoInicial,nfaMain.estadoFinal]
        }
        finalTransition = {
            "desde": afn.estadoFinal,
            "=>": " ",
            "hacia": [afn.estadoInicial, nfaMain.estadoFinal]
        }
        nfaMain.estados.add(nfaMain.estadoInicial)
        nfaMain.estados.add(nfaMain.estadoFinal)
        for state in afn.estados:
            nfaMain.estados.add(state)
        nfaMain.transiciones.append(initialTransition)
        for transition in afn.transiciones:
            nfaMain.transiciones.append(transition)
        nfaMain.transiciones.append(finalTransition)
        return nfaMain

def plus(afn):
    nfa1 = deepcopy(afn)
    nfa2 = deepcopy(afn)
    star = AFN()
    star = kleene(nfa2)
    result = AFN()
    result = concat(nfa1,star)
    return result

def conditional(afn):
    nfa1 = deepcopy(afn)
    epsilon = AFN()
    epsilon = epsilon.basic(' ')
    result = AFN()
    result = union(nfa1,epsilon)
    return result

lista=[]

#convertir postfix a AFN
def evaluatePostfix(regex):

    if(len(regex) == 1):
        afn = AFN()
        afn = afn.basic(regex)
        return afn
    stack = Stack()
    for token in regex:
        if(token.isalpha() or token.isdigit() or token == ' '):
            afn = AFN()
            afn = afn.basic(token)
            stack.push(afn)
        else:
            if(token == '*'):
                afn = stack.pop()
                result = kleene(afn)
                result.display()
                stack.push(result)
            elif(token == '.'):
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = concat(nfa1,nfa2)
                result.display()
                stack.push(result)
            elif(token == '|'):
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                result = union(nfa1,nfa2)
                result.display()
                stack.push(result)
            elif(token == '?'):
                afn = stack.pop()
                result = conditional(afn)
                result.display()
                stack.push(result)
            elif(token == '+'):
                afn = stack.pop()
                result = plus(afn)
                result.display()
                stack.push(result)
    afn = AFN()
    afn = stack.pop()

    #agregando graphviz para hacerlo visual
    # generar archivo DOT
    dot = Digraph()
    dot.attr(rankdir='LR')  # configuración opcional para orientación del grafo
    
    # agregar estados al grafo
    for state in afn.estados:
        if state == afn.estadoInicial:
            dot.node(str(state), "0", shape="circle")
        elif state == afn.estadoFinal:
            dot.node(str(state), shape="doublecircle")
        else:
            dot.node(str(state))

    
    # agregar transiciones al grafo
    for transition in afn.transiciones:
        for hacia in transition["hacia"]:
            if(transition["=>"] == " "):
                epsilon = 'ε'
            else:
                epsilon = str(transition["=>"])
            lista.append(dot.edge(str(transition["desde"]), str(hacia), label=epsilon))
                
    # guardar archivo DOT
    
    dot.render('afnfinal', format='png')
    dot.view()
    

    #print (afn)
    with open('resultadoAFN.txt', 'w') as f:
        for state in afn.estados:
            f.write(str(state)+", ")
        f.write('\n')
        #for loop language
        lang = []
        for i in range(0,len(afn.transiciones)):
            lang.append(str(afn.transiciones[i]['=>']))
        lang = set(lang)
        f.write(str(lang))
        f.write('\n')
        f.write(str(afn.estadoInicial))
        f.write('\n')
        f.write(str(afn.estadoFinal))
        f.write('\n')
        for transition in afn.transiciones:
            f.write(str(transition)+ ", ")

    return afn




#Ejecutar Todo
def ejecutar(regex):
    try:
        print('\nCadena ingresada: ' + regex)
        regexprocess = reescribiendoExpr(regex)
        postfix = topostfix(regexprocess)
        print('Postfix: ' + postfix)
        return evaluatePostfix(postfix)
    except:
        print("La cadena es incorrecta\n")
    
    


# INGRESANDO EXPRESION REGULAR A TRABAJAR
def cadena(lista):
    
    for i in lista:
        ejecutar(i)    

    cadena = ''.join(['(' + item + ')' for item in lista])
    ejecutar(cadena)