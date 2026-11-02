import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from src import main
from src.aluno import Aluno
from src.armazenamento import ArmazenamentoError
from src.erros import DadoInvalidoError


def digitando(*respostas):
    """Simula o professor digitando as respostas, uma por pergunta."""
    return patch("builtins.input", side_effect=list(respostas))


class TestLeituraEBusca(unittest.TestCase):
    def test_ler_numero_aceita_virgula(self):
        with digitando("8,5"):
            self.assertEqual(main.ler_numero("Nota: "), 8.5)

    def test_ler_numero_inteiro(self):
        with digitando("50"):
            self.assertEqual(main.ler_numero("Aulas: ", int), 50)

    def test_ler_numero_com_texto_gera_erro(self):
        with digitando("sete"), self.assertRaises(DadoInvalidoError):
            main.ler_numero("Nota: ")

    def test_buscar_aluno_ignora_maiusculas_e_espacos(self):
        maria = Aluno(nome="Maria", turma="9A")
        self.assertIs(main.buscar_aluno([maria], "  maria "), maria)

    def test_buscar_aluno_inexistente_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            main.buscar_aluno([], "Joao")


class TestOpcoesDoMenu(unittest.TestCase):
    def setUp(self):
        self.alunos = []
        self.saida = io.StringIO()

    def executar(self, opcao, *respostas):
        with digitando(*respostas), redirect_stdout(self.saida):
            opcao(self.alunos)

    def test_cadastrar(self):
        self.executar(main.cadastrar, "Maria", "9A")
        self.assertEqual(self.alunos[0].nome, "Maria")

    def test_cadastrar_nome_repetido_gera_erro(self):
        self.executar(main.cadastrar, "Maria", "9A")
        with self.assertRaises(DadoInvalidoError):
            self.executar(main.cadastrar, "MARIA", "9B")

    def test_lancar_nota_faltas_e_ver_boletim(self):
        self.executar(main.cadastrar, "Maria", "9A")
        for nota in ("7", "8,5", "6"):
            self.executar(main.lancar_nota, "Maria", nota)
        self.executar(main.lancar_faltas, "Maria", "50", "4")
        self.executar(main.ver_boletim, "Maria")
        texto = self.saida.getvalue()
        self.assertIn("Média: 7.2", texto)
        self.assertIn("Frequência: 92%", texto)
        self.assertIn("Situação: APROVADO", texto)

    def test_relatorio_da_turma(self):
        self.executar(main.cadastrar, "Maria", "9A")
        self.executar(main.cadastrar, "Joao", "9A")
        self.executar(main.lancar_nota, "Maria", "3")
        self.executar(main.lancar_faltas, "Maria", "40", "0")
        self.executar(main.relatorio_turma, "9a")
        texto = self.saida.getvalue()
        self.assertIn("REPROVADO", texto)
        self.assertIn("Joao", texto)
        self.assertIn("sem notas ou frequência lançadas", texto)

    def test_relatorio_de_turma_vazia_gera_erro(self):
        with self.assertRaises(DadoInvalidoError):
            self.executar(main.relatorio_turma, "7B")


class TestProgramaPrincipal(unittest.TestCase):
    def rodar(self, *respostas, carregar=None):
        saida = io.StringIO()
        carregar = carregar or patch.object(main, "carregar_alunos", return_value=[])
        with carregar, patch.object(main, "salvar_alunos") as salvar, \
                digitando(*respostas), redirect_stdout(saida):
            main.main()
        return saida.getvalue(), salvar

    def test_fluxo_completo_com_erro_e_opcao_invalida(self):
        texto, salvar = self.rodar("1", "Maria", "9A", "2", "Maria", "12", "9", "0")
        self.assertIn("Aluno cadastrado.", texto)
        self.assertIn("Erro: A nota deve estar entre 0 e 10.", texto)
        self.assertIn("Opção inválida.", texto)
        self.assertIn("Até logo!", texto)
        self.assertEqual(salvar.call_count, 1)  # só salva quando a ação deu certo

    def test_arquivo_corrompido_encerra_com_mensagem(self):
        quebrado = patch.object(main, "carregar_alunos", side_effect=ArmazenamentoError("arquivo corrompido"))
        texto, _ = self.rodar(carregar=quebrado)
        self.assertIn("Erro: arquivo corrompido", texto)


if __name__ == "__main__":
    unittest.main()
