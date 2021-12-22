import sys
import csv
import datetime
import pandas as pd
from RN412 import calculo_rn412
from pintura import *
from datetime import datetime



#Arquivo deverá conter da coluna A até a E os seguintes cabeçalhos: NOME, MENSALIDADE, VIGENCIA, DT_CANCELAMENTO, ULTIMO_MES_FATURAMENTO
#se atentar ao colocar a coluna valor separando decimais com "." ao inves de "," e deixar como texto as colunas "D" e "E" (DT_CANCELAMENTO e ULTIMO_MES_FATURAMENTO)


def analise_individual():
    if(len(sys.argv) == 5):
        mensalidade = float(sys.argv[1])
        vigencia = int(sys.argv[2])
        dt_cancelamento = sys.argv[3]
        ultimo_mes_faturamento = sys.argv[4]
    else:

        while True:
            try:
                mensalidade = float(input('Informe o valor da mensalidade R$####.##: '))
                vigencia = int(input('Informe a vigencia: '))
                break
            except (NameError, ValueError):
                prRed('Campo mensalidade tem que ser um numero e caso seja decimal o separador é . (ponto)\n')
                prRed('Campo vigencia tem que ser um numero inteiro\n')
                prRed('Tente novamente\n')
        while True:
            try:
                dt_cancelamento = input('Informe a data de cancalemnto ##/##/####: ')
                conversao_data_cancelamento = datetime.strptime(dt_cancelamento, '%d/%m/%Y')
                ultimo_mes_faturamento = input('Informe a ultima competencia faturada ##/####: ')
                consersao_ultimo_mes_faturamento = datetime.strptime(ultimo_mes_faturamento, '%m/%Y')
                break
            
            except (NameError, ValueError):
            
                prRed('Campo data de cancelamento tem que ser uma data com dia/mês/ano \n')
                prRed('Campo ultima competencia tem que ser uma data com mês/ano\n')
                prRed('Tente novamente\n')
            

    
    return prLightPurple(calculo_rn412(mensalidade, vigencia, dt_cancelamento, ultimo_mes_faturamento))

def analise_lote():
    if(len(sys.argv) == 3):
        diretorio = sys.argv[1]
        diretorio_retorno = sys.argv[2]
    else:
        diretorio = input('Informar diretorio + nome_arquivo.csv :')
        diretorio_retorno = input('Informar diretorio retorno + nome_arquivo_retorno.csv :')
        
    arquivo_leitura = pd.read_csv(diretorio, sep=';', encoding='iso8859-1')
    #Ao ler o arquivo a biblioteca do pandas entende object = string

    tuples = [tuple(x) for x in arquivo_leitura.values]

    arquivo_retorno = open(diretorio_retorno, 'w', newline='', encoding='iso8859-1')

    objeto_gravacao = csv.writer(arquivo_retorno)

    for linhas in tuples:
        calculo = calculo_rn412(linhas[1],linhas[2],linhas[3],linhas[4])
        nome = linhas [0] 
        objeto_gravacao.writerow((nome,calculo))   
    arquivo_retorno.close()
    prLightPurple('Processo concluido')


def rodando_usuario():

    tipo_analise = 'None'
    erro = 0

    while (tipo_analise != 'L' and tipo_analise != 'I'):    
        if(erro == 0):
            tipo_analise = input('Deseja calcular individual (I) ou em lote (L): ').upper()
            erro += 1
        else:
            prRed('Entrada incorreta')
            tipo_analise = input('Deseja calcular individual (I) ou em lote (L): ').upper()
    if(tipo_analise == 'I'):
        analise_individual()
    else:
        analise_lote()



if(len(sys.argv)<2):
    rodando_usuario()

elif(sys.argv[1] == '--help'):
    prCyan('Para utilizar o programa através de parametros inputados diretamente no console voce tem duas opções: \n')
    prGreen('1) Lote - com isso os parametros são ');prRed('<diretorio/nome_arquivo.csv> '); prGreen('e '); prRed('<diretorio_retorno/nome_arquivo_retorno.csv>\n')
    prGreen('2) Indidual - com isso os parametros são: \n')
    prRed('<mensalidade(####.##)>');prGreen(', ');prRed('<vigencia(##)>');prGreen(', ');prRed(' <dt_cancelamento(##/##/####)>');prGreen(' e ');prRed('<ultimo_mes_faturamento(##/####)>\n')




elif(len(sys.argv) == 3):
    analise_lote()

elif(len(sys.argv) == 5):
    analise_individual()

else:
    prYellow('Parametros invalidos, consulte --help  \n')
