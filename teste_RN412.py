from RN412 import calculo_rn412
from pintura import *


#teste 1
if ('Valor a ser devolvido R$1006.45 referente a 11 dia(s) proporcionais e 3 mês(es) cheio(s)' == calculo_rn412(300, 1, '20/01/2021', '04/2021')):
    prCyan('Teste 1 ok\n')
else :
    prRed('Teste 1 falhou\n')

#teste 2
if ('Valor a ser devolvido R$137.50 referente a 15 dias' == calculo_rn412(275, 15, '29/09/2021', '09/2021')):
    prCyan('Teste 2 ok\n')
else :
    prRed('Teste 2 falhou\n')

#teste 3

if ('Valor a ser devolvido R$192.93 referente a 8 dias' == calculo_rn412(723.5, 10, '01/10/2021', '09/2021')):
    prCyan('Teste 3 ok\n')
else :
    prRed('Teste 3 falhou\n')

#teste 4

if ('Não há necessidade de devolução, beneficiario cancelado no ultimo dia de cobertura.' == calculo_rn412(250, 20, '19/10/2021', '09/2021')):
    prCyan('Teste 4 ok\n')
else :
    prRed('Teste 4 falhou\n')


#teste 5

if ('Valor a ser devolvido R$70.97 referente a 11 dias' == calculo_rn412(200, 1, '20/01/2021', '01/2021')):
    prCyan('Teste 5 ok\n')
else :
    prRed('Teste 5 falhou\n')

#teste 6

if ('Data do cancelamento maior que a cobertura cobrada, não se enquadra em RN412, necessario COBRAR proporcional' == calculo_rn412(800, 10, '27/11/2021', '10/2021')):
    prCyan('Teste 6 ok\n')
else :
    prRed('Teste 6 falhou')