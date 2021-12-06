import csv
from RN412 import calculo_rn412
import csv
import pandas as pd

#Arquivo deverá conter da coluna A até a E os seguintes cabeçalhos: NOME, MENSALIDADE, VIGENCIA, DT_CANCELAMENTO, ULTIMO_MES_FATURAMENTO
#se atentar ao colocar a coluna valor separando decimais com "." ao inves de "," e deixar como texto as colunas "D" e "E" (DT_CANCELAMENTO e ULTIMO_MES_FATURAMENTO)

arquivo_leitura = pd.read_csv(r'/home/gabsferrara/projects/RN412/RN412.CSV', sep=';', encoding='iso8859-1')
#Ao ler o arquivo a biblioteca do pandas entende object = string

tuples = [tuple(x) for x in arquivo_leitura.values]

arquivo_retorno = open('/home/gabsferrara/projects/RN412/arquivo_retorno.csv', 'w', newline='', encoding='iso8859-1')

objeto_gravacao = csv.writer(arquivo_retorno)

for linhas in tuples:
    calculo = calculo_rn412(linhas[1],linhas[2],linhas[3],linhas[4])
    nome = linhas [0] 
    objeto_gravacao.writerow((nome,calculo))   
arquivo_retorno.close()