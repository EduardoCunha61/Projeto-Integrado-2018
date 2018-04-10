import re

#TRATAR DOS ACENTOS!!!!
#ALTERAR VALORES DE RETORNO DA VALIDAÇÃO. TALVEZ FOSSE MELHOR IMPRIMIR VÁRIOS VALORES?
#ADICIONAR END OF FILE DEPOIS DE RECONHECER O '.'

#PRÓXIMA TAREFA: IR BUSCAR NUMERO DE ALUNO E ID DO EXERCICIO PARA GERAR RESULTADO

def split_file(file_subm):
    new_lines=[]

    with open(file_subm) as f:
        for line in f.read().split('},\n'):
            if not line.endswith(".") or not line:
                new_lines.append((line+'}'))
            if line.endswith("."):
                new_lines.append(line[:-1])
                # END OF FILE AQUI
        
    return new_lines
   
def valida_Subm(file_subm):
    split_lines = split_file(file_subm) 

    if(bool(re.match('[nN]umero [aA]luno: *{"[a-zA-Z]?[0-9]{5}"}', split_lines[0]))):                                       
        if (bool(re.match('[rR]esposta: *{".*"\t*}.', split_lines[1], re.DOTALL))): # É preciso rever esta expressão regular (Se adicionarmos um \n ou \t no ficheiro de entrada, dá erro!)
            return 1
        else:
            return -1
    else:
        return -2

# Cria uma matriz 2 por numero de campos, sendo que guarda a info neste formato:
# [["Enunciado","Cria o fatorial de um dado inteiro X"],["Template","ASD"],etc]
# Todas as chavetas usadas para delimitar cada campo são removidas

def check_lines(file_subm):
    new_lines = split_file(file_subm)
    largura, altura = 2, len(new_lines)
    matrix = [["" for x in range(largura)] for y in range(altura)]

    for line in new_lines:
        i = 0
        str_dividida = line.split(":")

        conteudo_campo = remove_chavetas(str_dividida[1])

        matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
        matrix[new_lines.index(line)][1] = conteudo_campo

    return matrix

def remove_chavetas(stri):
    stri = stri.replace("{"+"\"","\"")
    stri = stri.replace("\"" + "}","\"")
    return stri
    
# Cria um ficheiro JSON com o formato de subm.json
def criarJSON(matriz_linhas):
    f = open("submteste.json","w+")
    f.write("{\"submissao\": {\n")
    for line in matriz_linhas:
        f.write('\t' + line[0] + " :" + line[1] + ",\n\n")
    f.write("}}")
    f.close()


if __name__ == '__main__':
    res = valida_Subm('plain.txt')
    
    if(res==1):
        print("Ficheiro corretamente criado!")
        criarJSON(check_lines('plain.txt'))

    elif(res==-1):
        print("RESPOSTA INVALIDA")
    elif(res==-2):
        print("NUMERO DE ALUNO INVALIDO")