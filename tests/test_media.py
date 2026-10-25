import unittest

from src.erros import DadoInvalidoError
from src.media import calcular_media


class TestCalcularMedia(unittest.TestCase):
    def test_media_de_tres_notas(self):
        self.assertEqual(calcular_media([7.0, 8.5, 6.0]), 7.2)

    def test_lista_vazia_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_media([])

    def test_nota_acima_de_dez_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_media([7.0, 11.0])

    def test_nota_negativa_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_media([-1.0])

    def test_nota_em_texto_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            calcular_media(["sete"])

if __name__ == "__main__":
    unittest.main()
