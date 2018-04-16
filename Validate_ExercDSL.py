import re

#TRATAR DOS ACENTOS!!!!
#INDEX DA LISTA AO VERIFICAR PODE DAR ERRO (CASO NÃO SEJAM DIVIDIDAS EM 2 LINHAS (neste caso))

#PRÓXIMA TAREFA: IR BUSCAR OS VALORES DE TESTE PARA VALIDAR FUNÇÃO

# Separa ficheiro de entrada por linhas, sendo dividido por '},\n'.
# É adicionado o caractér '}' no final de cada linha não vazia e que não termina em '.'
def split_file(file_exerc):
    new_lines=[]
    delim_final = "}."
    flag = 0
    with open(file_exerc) as f:
        split_lines = f.read().split('},\n')
        for line in split_lines:
            end_of_file = re.findall("}\.",line)

            if end_of_file:
                aux = line.split(delim_final)
                line = aux[0] + delim_final
                if aux[1]:
                    flag = 2
            if not line.endswith(".") or not line:
                new_lines.append((line+'}'+','))
            if line.endswith("."):
                new_lines.append(line[:-1])
    if not end_of_file:
        flag = 1
    return (new_lines,flag)

# Valida todos os campos do ficheiro de entrada de acordo com a estrutura definida no ficheiro "teste.txt"
# Esta função tem que ser optimizada, visto que, só retorna um erro de cada vez (Era fixe retornar todos)
def valida_Exerc(file_ex):
    empty_lines = ["Empty"]*4           #Esta lista é concatenada por causa dos indices nas comporações a seguir
    output_lines,flag = split_file(file_ex)
    split_lines = output_lines + empty_lines
    
    res = []

    if flag == 1:
        res.append(-6)
    elif flag == 2:
        res.append(-5)

    if (not bool(re.match('Enunciado: *{".*"},', split_lines[0], re.DOTALL))):
        res.append(-4)

    if(not bool(re.match('Template: *{".*"\t*},', split_lines[1], re.DOTALL))):
        res.append(-3)

    if (not bool(re.match('Valores de teste: *{(\("[^"]*","[^"]*"\),?)+},', split_lines[2]))):
        res.append(-2)              
                
    if(not bool(re.match('Linguagem: *{"[a-zA-Z]*"}', split_lines[3]))):
        res.append(-1)

    return res

# Cria uma matriz 2 por numero de campos, sendo que guarda a info neste formato:
# [["Numero Aluno","a71940"],["Resposta","int factorial(int x){int res = 1;...}"]
# Todas as chavetas usadas para delimitar cada campo são removidas

def check_lines(file_exec):
    new_lines = split_file(file_exec)[0]
    largura, altura = 2, len(new_lines)
    matrix = [["" for x in range(largura)] for y in range(altura)]

    for line in new_lines:
        i = 0
        str_dividida = line.split(':')

        if line==new_lines[2]:
            valores = re.findall(r'\"[^"]*\"', str_dividida[1])
            
            matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
            concat = " {\n"

            while i<(len(valores)):
                concat = concat + "\t\t" + valores[i] + " : " + valores[i+1] + ",\n"
                i = i+2

            concat = concat + "\t}"
            matrix[new_lines.index(line)][1] = concat

        else: 
            conteudo_campo = remove_chavetas(str_dividida[1])
        
            matrix[new_lines.index(line)][0] = "\"" + str_dividida[0] + "\""
            matrix[new_lines.index(line)][1] = conteudo_campo
    
    return matrix

def remove_chavetas(stri):
    stri = stri.replace("{"+"\"","\"")

    if stri.endswith("\"},"):
        stri = stri.replace("\"" + "}" + ",","\"")
    elif stri.endswith("\"}"):
        stri = stri.replace("\"" + "}","\"")

    return stri

# Cria um ficheiro JSON com o formato de exerc.json
def criarJSON(matriz_linhas):
    f = open("testeaux.json","w+")
    f.write("{\"exercicio\": {\n")

    for line in matriz_linhas:
        if line==matriz_linhas[3]:
            f.write('\t' + line[0] + " :" + line[1] + "\n")
        else:
            f.write('\t' + line[0] + " :" + line[1] + ",\n\n")
    f.write("}}")
    f.close()

if __name__ == '__main__':

    res = valida_Exerc('teste.txt')

    if not res:
        print("Ficheiro correto!")
        criarJSON(check_lines('teste.txt'))

    for num in reversed(res):
        print(num)
        if(num==-1):
            print("LINGUAGEM INVALIDA")
        elif(num==-2):
            print("VALORES DE TESTE INVALIDOS")
        elif(num==-3):
            print("TEMPLATE INVALIDO")
        elif(num==-4):
            print("ENUNCIADO INVALIDO")
        elif(num==-5):
            print("Existe codigo posterior a estrutura do ficheiro correta!")
        elif(num==-6):
            print("Ficheiro nao terminado como esperado! ('}.')")