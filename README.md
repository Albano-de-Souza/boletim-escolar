# Boletim Escolar

Trabalho A3 de Gestão e Qualidade de Software (UNA).

Aplicação console em Python para o professor registrar notas e faltas e obter
automaticamente a média, a frequência e a situação de cada aluno.

**ODS 4 – Educação de Qualidade:** o relatório da turma mostra cedo quem está em
risco de reprovação, permitindo intervir antes do fim do período.

## Equipe

| Nome | RA |
|---|---|
| Albano de Souza | 32516336 |
| Ana Carolina de Sousa Freitas | 325132932 |
| Alice Fernandes Barbosa | 326128348 |

## Regras de negócio

- **Média:** média aritmética das notas (cada nota de 0 a 10).
- **Frequência:** (aulas dadas − faltas) ÷ aulas dadas × 100.
- **Situação:**
  - frequência abaixo de 75%: REPROVADO POR FALTA
  - média a partir de 6,0: APROVADO
  - média de 4,0 a 5,9: RECUPERAÇÃO
  - média abaixo de 4,0: REPROVADO

## Como executar

Requer Python 3.10 ou superior. Não há dependências externas.

```
python -m src.main
```

## Como rodar os testes

```
python -m unittest discover -s tests -t . -v
```

## Organização do repositório

- Git Flow: `main` (versão estável), `develop` (integração) e `feature/*` (uma por funcionalidade).
- Commits semânticos: `feat:`, `fix:`, `test:`, `refactor:`, `docs:`, `ci:`.
- CI: GitHub Actions executa os testes a cada push e pull request.
