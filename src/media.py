"""Regras de negócio das notas: validação e cálculo da média."""

from src.erros import DadoInvalidoError

NOTA_MINIMA = 0.0
NOTA_MAXIMA = 10.0


def validar_nota(nota):
    if isinstance(nota, bool) or not isinstance(nota, (int, float)):
        raise DadoInvalidoError("A nota deve ser um número.")
    if nota < NOTA_MINIMA or nota > NOTA_MAXIMA:
        raise DadoInvalidoError("A nota deve estar entre 0 e 10.")
    return float(nota)


def calcular_media(notas):
    if not notas:
        raise DadoInvalidoError("O aluno não possui notas lançadas.")
    validas = [validar_nota(nota) for nota in notas]
    return round(sum(validas) / len(validas), 1)
