"""Representação de um aluno e do seu boletim."""

from dataclasses import dataclass, field, asdict

from src.erros import DadoInvalidoError
from src.frequencia import calcular_frequencia, definir_situacao
from src.media import calcular_media, validar_nota


@dataclass
class Aluno:
    nome: str
    turma: str
    notas: list = field(default_factory=list)
    total_aulas: int = 0
    faltas: int = 0

    def adicionar_nota(self, nota):
        self.notas.append(validar_nota(nota))

    def registrar_frequencia(self, total_aulas, faltas):
        calcular_frequencia(total_aulas, faltas)  # valida antes de gravar
        self.total_aulas = total_aulas
        self.faltas = faltas

    def boletim(self):
        media = calcular_media(self.notas)
        frequencia = calcular_frequencia(self.total_aulas, self.faltas)
        return {
            "nome": self.nome,
            "turma": self.turma,
            "notas": self.notas,
            "media": media,
            "frequencia": frequencia,
            "situacao": definir_situacao(media, frequencia),
        }

    def para_dicionario(self):
        return asdict(self)


def criar_aluno(nome, turma):
    nome, turma = nome.strip(), turma.strip()
    if not nome:
        raise DadoInvalidoError("O nome do aluno não pode ficar vazio.")
    if not turma:
        raise DadoInvalidoError("A turma não pode ficar vazia.")
    return Aluno(nome=nome, turma=turma)
