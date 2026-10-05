import unittest

from src.erros import DadoInvalidoError


class TestDadoInvalidoError(unittest.TestCase):
    def test_e_um_erro_de_valor(self):
        self.assertTrue(issubclass(DadoInvalidoError, ValueError))

    def test_guarda_a_mensagem(self):
        erro = DadoInvalidoError("nota inválida")
        self.assertEqual(str(erro), "nota inválida")


if __name__ == "__main__":
    unittest.main()
