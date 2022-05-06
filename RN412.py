import datetime
from datetime import  datetime
from dateutil.relativedelta import *
import copy


class Mensalidade:
    def __init__(self, mensalidade, vigencia):
        self.mensalidade = mensalidade
        self.vigencia = vigencia

class RN412(Mensalidade):
    def __init__(self, mensalidade, vigencia, dt_cancelamento, ultima_mensalidade):
        super().__init__(mensalidade, vigencia)
        self.dt_cancelamento = datetime.strptime(dt_cancelamento, '%d/%m/%Y')
        self.ultima_mensalidade = datetime.strptime(ultima_mensalidade, '%m/%Y')
        self.ultimo_dia_ativo = self.ultimo_dia()
        self.conf_inicial = self.devolucao_inicial()
        self.dias = self.conf_inicial[0]
        self.proporcionalidade = self.conf_inicial[1]
        self.fim_competencia_cance = self.conf_inicial[2]
        self.meses = self.meses_cheios()
        self.valor = self.calculadora_prorata()
    
    def __str__(self):
        return 'R${:.2f}'.format(self.valor)


    def ultimo_dia(self):
        if(self.vigencia == 1):
            ultimo_dia_ativo =  self.ultima_mensalidade + relativedelta(months= +1) + relativedelta(days= -1)          
            return ultimo_dia_ativo
        else:
            data = self.ultima_mensalidade + relativedelta(months= +1)
            ultimo_dia_ativo =  datetime(day = self.vigencia -1, month = data.month, year= data.year)        
            return ultimo_dia_ativo

    def calculadora_prorata(self) -> float:
        if(self.ultimo_dia_ativo<=self.dt_cancelamento):
            return 0
        else:
            return(self.mensalidade * (self.proporcionalidade + self.meses))
            

    def devolucao_inicial(self) -> tuple:
        data = self.dt_cancelamento
        inicio_competencia_cance = datetime(day= self.vigencia, month= data.month, year= data.year)
        if(self.vigencia>self.dt_cancelamento.day):
            inicio_competencia_cance -= relativedelta(months= 1)
        fim_competencia_cance = inicio_competencia_cance + relativedelta(months= 1, days= -1)

        qnt_dias = (fim_competencia_cance - self.dt_cancelamento).days
        proporcionalidade = qnt_dias/((fim_competencia_cance - inicio_competencia_cance).days +1)
        return (qnt_dias, float(proporcionalidade), fim_competencia_cance)
    

    def meses_cheios(self) -> int:
        ultimo_dia_proporcional = self.fim_competencia_cance
        ultimo_dia_ativo = copy.deepcopy(self.ultimo_dia_ativo)
        contagem = 0
        while ultimo_dia_proporcional.year < ultimo_dia_ativo.year or ultimo_dia_proporcional.month < ultimo_dia_ativo.month:
            contagem += 1
            ultimo_dia_ativo -= relativedelta(months= 1)
        
        return contagem

    def getMesCheio(self) -> int:
        return self.meses

    def getDias(self) -> int:
        return self.dias

           




    
        

 """


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
        conclusao = 'Data do cancelamento maior que a cobertura cobrada, não se enquadra em RN412, necessario COBRAR proporcional'

    elif (dt_cancelamento.date() == dt_ultimo_dia_do_faturamento):
        conclusao = 'Não há necessidade de devolução, beneficiario cancelado no ultimo dia de cobertura.'

    #a partir daqui entra em RN412
    #primeira condição quantidade de dias a devolver = a quantidade de dias do mes 
    else :
        qnt_dias_a_maior = (dt_ultimo_dia_do_faturamento - dt_primeiro_dia_a_devolver + timedelta(days= 1)).days 

        if (qnt_dias_a_maior == qnt_dias_mes_cancelamento):
            conclusao = 'Um mês completo a devolver, no valor de R$ {:.2f}'.format(mensalidade)
        
        elif (qnt_dias_a_maior < qnt_dias_mes_cancelamento):
            valor_a_devolver = (mensalidade/qnt_dias_mes_cancelamento)*qnt_dias_a_maior
            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dias'.format(valor_a_devolver, qnt_dias_a_maior)
        
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

            conclusao = 'Valor a ser devolvido R${:.2f} referente a {} dia(s) proporcionais e {} mês(es) cheio(s)'.format(valor_total, qnt_dias_pro_rata, contagem_mes)  

    return conclusao        
    
    
    

    
"""