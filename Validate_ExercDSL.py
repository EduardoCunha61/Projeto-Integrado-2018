# -*- coding: utf-8 -*-
import re
import sys
import unicodedata


# TRATAR DOS ACENTOS!!!!
# Adicionar comentários dentro do código
# Definir mais exercícios para testar
# Fazer import/download do python? Procurar sobre isto
# Definir por email um sistema de submissões! (Mais para a frente!)

# Separa ficheiro de entrada por linhas, sendo dividido por '#]\n'.
# É adicionado o conjunto de caracteres "#]" no final de cada linha não vazia e que não termina em '.'
def split_file(file_exerc):
    new_lines=[]
    delim_final = "#]."
    flag = 0
    with open(file_exerc) as f:
        split_lines = f.read().split('#]\n')
        for line in split_lines:
            end_of_file = re.findall("#].",line)

            if end_of_file:
                aux = line.split(delim_final)
                line = aux[0] + delim_final
                if aux[1]:
                    flag = 2

            if not line.endswith(".") or not line:
                new_lines.append((line+'#'+']'))

            if line.endswith("."):
                new_lines.append(line[:-1])
    
    if not end_of_file:
        flag = 1
    return (new_lines,flag)

# Valida todos os campos do ficheiro de entrada de acordo com a estrutura definida no ficheiro "teste.txt"
def valida_Exerc(file_ex):
    empty_lines = ["Empty"]*4           #Esta lista é concatenada por causa dos indices nas comparações a seguir
    output_lines,flag = split_file(file_ex)
    split_lines = output_lines + empty_lines
    
    res = []

    if flag == 1:
        res.append(-6)
    elif flag == 2:
        res.append(-5)

    if (not bool(re.match('\[\# *[eE]nunciado: *.* \#\]', split_lines[0], re.DOTALL))):
        res.append(-4)

    if(not bool(re.match('\[\# *[tT]emplate: *.*\#\]', split_lines[1], re.DOTALL))):
        res.append(-3)

    if (not bool(re.match('\[\# *[vV]alores de teste: *(\("[^"]*","[^"]*"\),?)+ *\#\]', split_lines[2]))):
        res.append(-2)              
                
    if(not bool(re.match('\[\# *[lL]inguagem: *[a-zA-Z]* *\#\]', split_lines[3]))):
        res.append(-1)

    return res

# Cria uma matriz 2 por numero de campos, sendo que guarda a info neste formato:
# [["Numero Aluno","a71940"],["Resposta","int factorial(int x){int res = 1;...}"]
# Todaos os delimitadores "#]" em cada campo são removidos

def check_lines(file_exec):
    new_lines = split_file(file_exec)[0]
    largura, altura = 2, len(new_lines)
    matrix = [["" for x in range(largura)] for y in range(altura)]

    for line in new_lines:
        i = 0
        sem_delimitadores = remove_delimitador(line)
        str_dividida = sem_delimitadores.split(':')

        str_dividida[0] = check_spaces(str_dividida[0])
        str_dividida[1] = check_spaces(str_dividida[1])      

        if line == new_lines[2]:
            valores = re.findall(r'\"[^"]*\"', str_dividida[1])
            
            matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
            concat = "{\n" 

            while i<(len(valores)):
                concat = concat + "\t\t" + valores[i] + " : " + valores[i+1] + ",\n"
                i = i+2

            concat = concat + "\t}"
            matrix[new_lines.index(line)][1] = concat

        else: 
            matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
            matrix[new_lines.index(line)][1] = "\"" + str_dividida[1] + "\""
    
    return matrix

def check_spaces(stri):
    if stri[:1] == ' ':
        l = list(stri)
        l[0] = ''
        stri = ''.join(l)
    
    if stri[-1:] == ' ':
        l = list(stri)
        l[len(stri)-1] = ''
        stri = ''.join(l)

    return stri

def remove_delimitador(stri):
    first_del = stri.replace("["+"#","")
    snd_del = first_del.replace("#"+"]","")

    return snd_del

# Cria um ficheiro JSON com o formato de exerc.json
def criarJSON(matriz_linhas):
    new_file = sys.argv[2].replace(".txt",".json")
    f = open(new_file,"w+")
    f.write("{\"exercicio\": {\n")

    for line in matriz_linhas:
        if line==matriz_linhas[3]:
            f.write('\t' + line[0] + " : " + line[1] + "\n")
        else:
            f.write('\t' + line[0] + " : " + line[1] + ",\n\n")
    f.write("}}")
    f.close()

if __name__ == '__main__':

    res = valida_Exerc(sys.argv[1])

    if not res:
        criarJSON(check_lines(sys.argv[1]))

    for num in reversed(res):
        if(num==-1):
            print("Invalid language!\n")
        elif(num==-2):
            print("Invalid test values!\n")
        elif(num==-3):
            print("Invalid template!\n")
        elif(num==-4):
            print("Invalid statement!\n")
        elif(num==-5):
            print("There is code after the correct structure of the file!\n")
        elif(num==-6):
            print("File should have ended with '#].'!\n")