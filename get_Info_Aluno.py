 import re

def read_file(file_json):
    splitted_file = []
    with open(file_json) as f:
        file_r = f.read()
    
    return file_r

def get_numero_aluno(file_json):
    file_r = read_file(file_json)
    linha_numero = re.findall('"[nN]umero [aA]luno" : .*\",', file_r, re.DOTALL)
    numero = re.findall("[a-zA-Z]?[0-9]{5}",linha_numero[0])

    return numero

def get_resposta(file_json):
   file_r = read_file(file_json)
   linha_resposta = re.findall('"[rR]esposta" : .*}\"', file_r, re.DOTALL)
   #SPLIT "RESPOSTA" DO CÓDIGO! CUIDADO QUE PODE EXISTIR ':' NO MEIO DO CÓDIGO

   return linha_resposta

if __name__ == '__main__':
    num = get_numero_aluno('submteste.json')
    resp = get_resposta('submteste.json')

    final = num + resp
    print(final)