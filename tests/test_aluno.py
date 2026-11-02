import unittest

from src.aluno import Aluno, criar_aluno
from src.erros import DadoInvalidoError


class TestCriarAluno(unittest.TestCase):
    def test_cria_aluno_sem_espacos_sobrando(self):
        aluno = criar_aluno("  Maria  ", " 9A ")
        self.assertEqual(aluno.nome, "Maria")
        self.assertEqual(aluno.turma, "9A")

    def test_nome_vazio_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            criar_aluno("   ", "9A")

    def test_turma_vazia_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            criar_aluno("Maria", "")


class TestAluno(unittest.TestCase):
    def setUp(self):
        self.aluno = Aluno(nome="Maria", turma="9A")

    def test_aluno_novo_comeca_sem_notas_e_sem_faltas(self):
        self.assertEqual(self.aluno.notas, [])
        self.assertEqual(self.aluno.faltas, 0)

    def test_cada_aluno_tem_a_sua_lista_de_notas(self):
        outro = Aluno(nome="Joao", turma="9A")
        self.aluno.adicionar_nota(8)
        self.assertEqual(outro.notas, [])

    def test_adicionar_nota_valida(self):
        self.aluno.adicionar_nota(7)
        self.assertEqual(self.aluno.notas, [7.0])

    def test_adicionar_nota_invalida_nao_grava(self):
        with self.assertRaises(DadoInvalidoError):
            self.aluno.adicionar_nota(12)
        self.assertEqual(self.aluno.notas, [])

    def test_registrar_frequencia_valida(self):
        self.aluno.registrar_frequencia(50, 4)
        self.assertEqual((self.aluno.total_aulas, self.aluno.faltas), (50, 4))

    def test_registrar_frequencia_invalida_nao_grava(self):
        with self.assertRaises(DadoInvalidoError):
            self.aluno.registrar_frequencia(40, 41)
        self.assertEqual((self.aluno.total_aulas, self.aluno.faltas), (0, 0))

    def test_boletim_completo(self):
        for nota in (7, 8.5, 6):
            self.aluno.adicionar_nota(nota)
        self.aluno.registrar_frequencia(50, 4)
        boletim = self.aluno.boletim()
        self.assertEqual(boletim["media"], 7.2)
        self.assertEqual(boletim["frequencia"], 92.0)
        self.assertEqual(boletim["situacao"], "APROVADO")

    def test_boletim_sem_notas_gera_erro(self):
        self.aluno.registrar_frequencia(50, 4)
        with self.assertRaises(DadoInvalidoError):
            self.aluno.boletim()

    def test_para_dicionario(self):
        self.aluno.adicionar_nota(9)
        self.assertEqual(self.aluno.para_dicionario(), {
            "nome": "Maria", "turma": "9A", "notas": [9.0], "total_aulas": 0, "faltas": 0})


if __name__ == "__main__":
    unittest.main()
