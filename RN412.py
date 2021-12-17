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

    dt_cancelamento = datetime.strptime(dt_cancelamento, '%d/%m/%Y')
    #calculando quantidade de dias do mes referente a competencia do cancelamento
    if (dt_cancelamento.day < vigencia):
        ano_mes_de_cancelamento_correspondente_a_vigencia = dt_cancelamento + relativedelta(months= -1)
        qnt_dias_mes_cancelamento = calendar.monthrange(ano_mes_de_cancelamento_correspondente_a_vigencia.year, ano_mes_de_cancelamento_correspondente_a_vigencia.month)[1]
    else:
        qnt_dias_mes_cancelamento = calendar.monthrange(dt_cancelamento.year, dt_cancelamento.month)[1]


    #data do primeiro dia a ser devolvido
    if (dt_cancelamento.day == qnt_dias_mes_cancelamento):
        dt_primeiro_dia_a_devolver = date(dt_cancelamento.year, dt_cancelamento.month+1, 1)
    else :
        dt_primeiro_dia_a_devolver = date(dt_cancelamento.year, dt_cancelamento.month, dt_cancelamento.day+1)

    #conversao para data ultimo faturamento, parametros de ultimos dias de vigencia do plano.
    dt_ultimo_mes_faturamento = datetime.strptime(ultimo_mes_faturamento, '%m/%Y')
    dt_ultimo_primeiro_dia_do_faturamento = date(dt_ultimo_mes_faturamento.year, dt_ultimo_mes_faturamento.month, vigencia) #primeiro dia do ultimo mes de cobranca, de acordo com a vigencia
    qnt_dias_mes_faturamento = calendar.monthrange(dt_ultimo_primeiro_dia_do_faturamento.year, dt_ultimo_primeiro_dia_do_faturamento.month)[1]

    #definindo ultimo dia com cobertura do plano
    if (vigencia == 1):
        dt_ultimo_dia_do_faturamento = date(dt_ultimo_mes_faturamento.year, dt_ultimo_mes_faturamento.month, qnt_dias_mes_faturamento)
    else :
        dt_ultimo_dia_do_faturamento = date(dt_ultimo_mes_faturamento.year, dt_ultimo_mes_faturamento.month, vigencia -1) + relativedelta(months= +1)



    #definindo o ultimo dia para calculo de pro-rata do mes do cancelamento
    if (vigencia == 1):
        dt_ultimo_dia_da_prorata = date(dt_cancelamento.year, dt_cancelamento.month, qnt_dias_mes_cancelamento)
    else :
        dt_ultimo_dia_da_prorata = date(dt_cancelamento.year, dt_cancelamento.month, vigencia -1 ) + relativedelta(months= +1)


    #as duas primeiras condições não se enquadram em RN412
    if (dt_cancelamento.date() > dt_ultimo_dia_do_faturamento):
        conclusao = 'Data do cancelamento maior que a cobertura cobrada, não se enquadra em RN412, necessario COBRAR proporcional  \n'

    elif (dt_cancelamento.date() == dt_ultimo_dia_do_faturamento):
        conclusao = 'Não há necessidade de devolução, beneficiario cancelado no ultimo dia de cobertura. \n'

    #a partir daqui entra em RN412
    #primeira condição quantidade de dias a devolver = a quantidade de dias do mes 
    else :
        qnt_dias_a_maior = (dt_ultimo_dia_do_faturamento - dt_primeiro_dia_a_devolver + timedelta(days= 1)).days 

        if (qnt_dias_a_maior == qnt_dias_mes_cancelamento):
            conclusao = 'Um mês completo a devolver, no valor de R$ {:.2f} \n'.format(mensalidade)
        
        elif (qnt_dias_a_maior < qnt_dias_mes_cancelamento):
            valor_a_devolver = (mensalidade/qnt_dias_mes_cancelamento)*qnt_dias_a_maior
            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dias  \n'.format(valor_a_devolver, qnt_dias_a_maior)
        
        else :
            qnt_dias_pro_rata = (dt_ultimo_dia_da_prorata - dt_cancelamento.date()).days
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

            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dia(s) proporcionais e {} mês(es) cheio(s)  \n'.format(valor_total, qnt_dias_pro_rata, contagem_mes)  

    return conclusao        
    
    
    

    
