import unittest
from RN412 import RN412
from unittest import TestCase

class TestRN412(TestCase):

    def teste_dias_proporcionais_com_mes_cheio_vigencia_1(self):
        teste = RN412(300, 1, '20/01/2021', '04/2021')
        valor_esperado = 1006.45
        meses_esperado = 3
        dias_esperado = 11

        self.assertEqual(valor_esperado, teste.valor)
        self.assertEqual(meses_esperado, teste.meses)
        self.assertEqual(dias_esperado, teste.dias)

    def teste_dias_proporcionais_com_mes_cheio_vigencia_dif_1(self):
        teste = RN412(275, 15, '29/09/2021', '01/2022')
        valor_esperado = 1237.50
        meses_esperado = 4
        dias_esperado = 15

        self.assertEqual(valor_esperado, teste.valor)
        self.assertEqual(meses_esperado, teste.meses)
        self.assertEqual(dias_esperado, teste.dias)
        
    def teste_somente_dias_vigencia_1(self):
        teste = RN412(723.5, 1, '01/09/2021', '09/2021')
        valor_esperado = 699.38
        meses_esperado = 0
        dias_esperado = 29

        self.assertEqual(valor_esperado, teste.valor)
        self.assertEqual(meses_esperado, teste.meses)
        self.assertEqual(dias_esperado, teste.dias)
        
    def teste_somente_dias_vigencia_dif_1(self):
        teste = RN412(723.5, 10, '01/10/2021', '09/2021')
        valor_esperado = 192.93
        meses_esperado = 0
        dias_esperado = 8

        self.assertEqual(valor_esperado, teste.valor)
        self.assertEqual(meses_esperado, teste.meses)
        self.assertEqual(dias_esperado, teste.dias)
        
    def teste_dev_ultimo_dia_cobertura(self):
        teste = RN412(250, 20, '19/10/2021', '09/2021')
        valor_esperado = 0

        self.assertEqual(valor_esperado, teste.valor)

        
    def teste_data_cancelamento_maior_cobertura(self):
        teste = RN412(800, 10, '27/11/2021', '10/2021')
        valor_esperado = 0

        self.assertEqual(valor_esperado, teste.valor)

        
if __name__ == '__main__':
    unittest.main()
