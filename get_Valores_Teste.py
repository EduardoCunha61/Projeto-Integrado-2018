import re

def get_Valores_Teste(file_json):
    valores_finais = []
    with open(file_json) as f:
        file_r = f.read()
        campo_valores = re.findall('"Valores de teste" :.*},',file_r,re.DOTALL)
        valores_chaveta = re.findall('{.*\".*\" : \".*\".*},',campo_valores[0],re.DOTALL)
        valores = re.findall('\"[^"]*\" : \"[^"]*\"',valores_chaveta[0])
        
        for par_valores in valores:
            par_valores = par_valores.replace("\"","")
            valores_sep = par_valores.split(' : ')
            valores_finais.append((valores_sep[0],valores_sep[1]))
    
    return valores_finais

if __name__ == '__main__':
    print(get_Valores_Teste('exerc.json'))