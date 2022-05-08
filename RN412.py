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
        self.valor = round(self.calculadora_prorata(),2)
    
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

           




    
  