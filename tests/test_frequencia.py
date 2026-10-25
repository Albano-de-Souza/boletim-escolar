import unittest

from src.erros import DadoInvalidoError
from src.frequencia import calcular_frequencia, definir_situacao


class TestCalcularFrequencia(unittest.TestCase):
    def test_frequencia_normal(self):
        self.assertEqual(calcular_frequencia(50, 4), 92.0)

    def test_sem_faltas(self):
        self.assertEqual(calcular_frequencia(40, 0), 100.0)

    def test_faltas_negativas_geram_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_frequencia(40, -1)

    def test_faltas_maiores_que_aulas_geram_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_frequencia(40, 41)

    def test_total_de_aulas_zero_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_frequencia(0, 0)


class TestDefinirSituacao(unittest.TestCase):
    def test_aprovado(self):
        self.assertEqual(definir_situacao(7.2, 92.0), "APROVADO")

    def test_aprovado_no_limite(self):
        self.assertEqual(definir_situacao(6.0, 75.0), "APROVADO")

    def test_recuperacao(self):
        self.assertEqual(definir_situacao(5.0, 90.0), "RECUPERAÇÃO")

    def test_reprovado_por_nota(self):
        self.assertEqual(definir_situacao(3.9, 90.0), "REPROVADO")

    def test_reprovado_por_falta_mesmo_com_media_alta(self):
        self.assertEqual(definir_situacao(9.0, 74.9), "REPROVADO POR FALTA")

if __name__ == "__main__":
    unittest.main()
