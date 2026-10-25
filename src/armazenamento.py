"""Leitura e gravação dos alunos em arquivo JSON."""

import json
from pathlib import Path

from src.aluno import Aluno

ARQUIVO_PADRAO = Path("dados.json")


class ArmazenamentoError(Exception):
    """Erro ao ler ou gravar o arquivo de dados."""


def carregar_alunos(caminho=ARQUIVO_PADRAO):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    try:
        registros = json.loads(caminho.read_text(encoding="utf-8"))
        return [Aluno(**registro) for registro in registros]
    except (json.JSONDecodeError, TypeError) as erro:
        raise ArmazenamentoError(
            f"O arquivo {caminho} está corrompido e não pôde ser lido."
        ) from erro


def salvar_alunos(alunos, caminho=ARQUIVO_PADRAO):
    registros = [aluno.para_dicionario() for aluno in alunos]
    try:
        Path(caminho).write_text(
            json.dumps(registros, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except OSError as erro:
        raise ArmazenamentoError(f"Não foi possível gravar em {caminho}.") from erro
