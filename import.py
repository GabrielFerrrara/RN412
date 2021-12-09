import csv
from RN412 import calculo_rn412

import pandas as pd

#Arquivo deverá conter da coluna A até a E os seguintes cabeçalhos: NOME, MENSALIDADE, VIGENCIA, DT_CANCELAMENTO, ULTIMO_MES_FATURAMENTO
#se atentar ao colocar a coluna valor separando decimais com "." ao inves de "," e deixar como texto as colunas "D" e "E" (DT_CANCELAMENTO e ULTIMO_MES_FATURAMENTO)

tipo_analise = 'None'
erro = 0


while (tipo_analise != 'L' and tipo_analise != 'I'):    
    if(erro == 0):
        tipo_analise = input('Deseja calcular individual (I) ou em lote (L): ').upper()
        erro += 1
    else:
        print('Entrada incorreta')
        tipo_analise = input('Deseja calcular individual (I) ou em lote (L): ').upper()


def analise_individual():

    mensalidade = float(input('Informe o valor da mensalidade R$####.##: '))
    vigencia = int(input('Informe a vigencia: '))
    dt_cancelamento = input('Informe a data de cancalemnto ##/##/####: ')
    ultimo_mes_faturamento = input('Informe a ultima competencia faturada ##/####: ')

    return print(calculo_rn412(mensalidade, vigencia, dt_cancelamento, ultimo_mes_faturamento))

def analise_lote():
    
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
    print('Processo concluido')

if(tipo_analise == 'I'):
    analise_individual()
else:
    analise_lote()
