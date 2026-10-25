"""Regras de negócio da frequência e da situação final do aluno."""

from src.erros import DadoInvalidoError

MEDIA_APROVACAO = 6.0
MEDIA_RECUPERACAO = 4.0
FREQUENCIA_MINIMA = 75.0


def calcular_frequencia(total_aulas, faltas):
    if total_aulas <= 0:
        raise DadoInvalidoError("O total de aulas deve ser maior que zero.")
    if faltas < 0:
        raise DadoInvalidoError("O número de faltas não pode ser negativo.")
    if faltas > total_aulas:
        raise DadoInvalidoError("As faltas não podem superar o total de aulas.")
    return round((total_aulas - faltas) / total_aulas * 100, 1)


def definir_situacao(media, frequencia):
    if frequencia < FREQUENCIA_MINIMA:
        return "REPROVADO POR FALTA"
    if media >= MEDIA_APROVACAO:
        return "APROVADO"
    if media >= MEDIA_RECUPERACAO:
        return "RECUPERAÇÃO"
    return "REPROVADO"
