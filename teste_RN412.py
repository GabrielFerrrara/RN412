from RN412 import calculo_rn412


#teste 1
if ('Valor a ser devolvido R$1006.45 referente a 11 dia(s) proporcionais e 3 mês(es) cheio(s)' == calculo_rn412(300, 1, '20/01/2021', '04/2021')):
    print('Teste 1 ok')
else :
    print('Teste 1 falhou')

#teste 2
if ('Valor a ser devolvido R$137.50 referente a 15 dias' == calculo_rn412(275, 15, '29/09/2021', '09/2021')):
    print('Teste 2 ok')
else :
    print('Teste 2 falhou')

#teste 3

if ('Valor a ser devolvido R$192.93 referente a 8 dias' == calculo_rn412(723.5, 10, '01/10/2021', '09/2021')):
    print('Teste 3 ok')
else :
    print('Teste 3 falhou')

#teste 4

if ('Não há necessidade de devolução, beneficiario cancelado no ultimo dia de cobertura.' == calculo_rn412(250, 20, '19/10/2021', '09/2021')):
    print('Teste 4 ok')
else :
    print('Teste 4 falhou')


#teste 5

if ('Valor a ser devolvido R$70.97 referente a 11 dias' == calculo_rn412(200, 1, '20/01/2021', '01/2021')):
    print('Teste 5 ok')
else :
    print('Teste 5 falhou')

#teste 6

if ('Data do cancelamento maior que a cobertura cobrada, não se enquadra em RN412, necessario COBRAR proporcional' == calculo_rn412(800, 10, '27/11/2021', '10/2021')):
    print('Teste 6 ok')
else :
    print('Teste 6 falhou')