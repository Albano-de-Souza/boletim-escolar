import tempfile
import unittest
from pathlib import Path

from src.aluno import Aluno
from src.armazenamento import ArmazenamentoError, carregar_alunos, salvar_alunos


class TestArmazenamento(unittest.TestCase):
    def setUp(self):
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "dados.json"

    def tearDown(self):
        self.pasta.cleanup()

    def test_arquivo_inexistente_devolve_lista_vazia(self):
        self.assertEqual(carregar_alunos(self.arquivo), [])

    def test_salvar_e_carregar_de_volta(self):
        maria = Aluno(nome="Maria", turma="9A", notas=[7.0, 8.5], total_aulas=50, faltas=4)
        salvar_alunos([maria], self.arquivo)
        self.assertEqual(carregar_alunos(self.arquivo), [maria])

    def test_acentos_sao_preservados(self):
        salvar_alunos([Aluno(nome="João", turma="9A")], self.arquivo)
        self.assertIn("João", self.arquivo.read_text(encoding="utf-8"))

    def test_arquivo_corrompido_gera_erro(self):
        self.arquivo.write_text("isto não é JSON", encoding="utf-8")
        with self.assertRaises(ArmazenamentoError):
            carregar_alunos(self.arquivo)

    def test_campos_errados_geram_erro(self):
        self.arquivo.write_text('[{"apelido": "Mari"}]', encoding="utf-8")
        with self.assertRaises(ArmazenamentoError):
            carregar_alunos(self.arquivo)

    def test_falha_ao_gravar_gera_erro(self):
        with self.assertRaises(ArmazenamentoError):
            salvar_alunos([], self.pasta.name)  # uma pasta não pode ser gravada como arquivo


if __name__ == "__main__":
    unittest.main()
