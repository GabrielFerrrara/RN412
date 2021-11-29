import datetime
import calendar
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *

# Este programa foi feito para calcular pro-rata, podendo basear-se para valorização de devolução de casos da RN412 - Resolucao normativa de regras para cancelamento de plano de saude
# Podendo inputar os dados em lote ou unitariamente.
# programa ainda não calcula corretamente caso valor da mensalidade mude entre as datas inputadas
# por regra de negocios, não faz sentido haver vigencia superior a 25 (exemplo contando de 26 de um mes até o dia 25 de outro mes)
#inputs


def calculo_rn412(mensalidade, vigencia, dt_cancelamento, ultimo_mes_faturamento):
    #nome = input("Nome: ")
    #mensalidade = float(input("Valor da mensalidade(R$xxxx.xx): "))
    #vigencia = int(input("Dia de vigencia: "))
    #dt_cancelamento = input("Dia de cancelamento (DD/MM/AAAA): ")
    #ultimo_mes_faturamento = input("Ultimo mes de faturamento (MM/AAAA): ")

    #conversao para data do cancelamento
    dt_cancelamento_separado = dt_cancelamento.split(sep="/")
    dia_cancelamento = int(dt_cancelamento_separado[0])
    mes_cancelamento = int(dt_cancelamento_separado[1])
    ano_cancelamento = int(dt_cancelamento_separado[2])
    dt_cancelamento = date(ano_cancelamento, mes_cancelamento, dia_cancelamento)
    #calculando quantidade de dias do mes referente a competencia do cancelamento
    if (dia_cancelamento < vigencia):
        ano_mes_de_cancelamento_correspondente_a_vigencia = dt_cancelamento + relativedelta(months= -1)
        qnt_dias_mes_cancelamento = calendar.monthrange(ano_mes_de_cancelamento_correspondente_a_vigencia.year, ano_mes_de_cancelamento_correspondente_a_vigencia.month)[1]
    else:
        qnt_dias_mes_cancelamento = calendar.monthrange(dt_cancelamento.year, dt_cancelamento.month)[1]



    #data do primeiro dia a ser devolvido
    if (dia_cancelamento == qnt_dias_mes_cancelamento):
        dt_primeiro_dia_a_devolver = date(ano_cancelamento, mes_cancelamento+1, 1)
    else :
        dt_primeiro_dia_a_devolver = date(ano_cancelamento, mes_cancelamento, dia_cancelamento+1)


    #conversao para data ultimo faturamento
    dt_ultimo_separado = ultimo_mes_faturamento.split(sep="/")
    mes_ultimo = int(dt_ultimo_separado[0])
    ano_ultimo = int(dt_ultimo_separado[1])
    dt_ultimo_primeiro_dia_do_faturamento = date(ano_ultimo, mes_ultimo, vigencia) #primeiro dia do ultimo mes de cobranca, de acordo com a vigencia
    qnt_dias_mes_faturamento = calendar.monthrange(dt_ultimo_primeiro_dia_do_faturamento.year, dt_ultimo_primeiro_dia_do_faturamento.month)[1]

    #definindo ultimo dia com cobertura do plano
    if (vigencia == 1):
        dt_ultimo_dia_do_faturamento = date(ano_ultimo, mes_ultimo, qnt_dias_mes_faturamento)
    else :
        dt_ultimo_dia_do_faturamento = date(ano_ultimo, mes_ultimo, vigencia -1) + relativedelta(months= +1)



    #definindo o ultimo dia para calculo de pro-rata do mes do cancelamento
    if (vigencia == 1):
        dt_ultimo_dia_da_prorata = date(ano_cancelamento, mes_cancelamento, qnt_dias_mes_cancelamento)
    else :
        dt_ultimo_dia_da_prorata = date(ano_cancelamento, mes_cancelamento, vigencia -1 ) + relativedelta(months= +1)


    #as duas primeiras condições não se enquadram em RN412
    if (dt_cancelamento > dt_ultimo_dia_do_faturamento):
        conclusao = 'Data do cancelamento maior que a cobertura cobrada, não se enquadra em RN412, necessario COBRAR proporcional'

    elif (dt_cancelamento == dt_ultimo_dia_do_faturamento):
        conclusao = 'Não há necessidade de devolução, beneficiario cancelado no ultimo dia de cobertura.'
    #a partir daqui entra em RN412
    #primeira condição quantidade de dias a devolver = a quantidade de dias do mes 
    else :
        qnt_dias_a_maior = (dt_ultimo_dia_do_faturamento - dt_primeiro_dia_a_devolver + timedelta(days= 1)).days ###preciso transformar esse cara em int.

        if (qnt_dias_a_maior == qnt_dias_mes_cancelamento):
            conclusao = 'Um mês completo a devolver, no valor de R$ {:.2f}'.format(mensalidade)
        
        elif (qnt_dias_a_maior < qnt_dias_mes_cancelamento):
            valor_a_devolver = (mensalidade/qnt_dias_mes_cancelamento)*qnt_dias_a_maior
            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dias'.format(valor_a_devolver, qnt_dias_a_maior)
        
        else :
            qnt_dias_pro_rata = (dt_ultimo_dia_da_prorata - dt_cancelamento).days
            valor_pro_rata = (mensalidade/qnt_dias_mes_cancelamento) * qnt_dias_pro_rata
            
            #primeiro dia apos o mes da pro-rata, primeiro dia do(s) mes(es) cheio(s)
            dt_primeiro_dia_mes_cheio = dt_ultimo_dia_da_prorata + timedelta(days= 1)
            valor = 0
            contagem_mes = 0
            while dt_primeiro_dia_mes_cheio < dt_ultimo_dia_do_faturamento:
                contagem_mes += 1
                valor = valor + mensalidade
                dt_primeiro_dia_mes_cheio += relativedelta(months= +1)
            valor_total = valor_pro_rata + valor 

            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dia(s) proporcionais e {} mês(es) cheio(s)'.format(valor_total, qnt_dias_pro_rata, contagem_mes)  

    return conclusao        




    


    
    
    

    


# NOW WE DEFINE THE FILE TO SAVE OUTPUT INTO
# WE USE THE "a" OPTION TO APPEND TO THE FILE
# OTHERWISE EACH INPUT WOULD OVERWRITE THE
# PREVIOUS INPUT

###file = open(nome + ".txt", "a")

# WE USE A NUMBER OF file.write STATEMENTS TO WRITE THE OUTPUT IN A FORMAT


#file.write('Prezado(a),' + input1 + '\n')
#file.write('Você utilizou ' + + 'dias da mensalidade. \n')
#file.write('Valor a pagar: R$ ' + )
#file.write("---" + "\n")
#file.close()