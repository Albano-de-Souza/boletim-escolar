"""Menu do Boletim Escolar (aplicação console)."""

from src.aluno import criar_aluno
from src.armazenamento import ArmazenamentoError, carregar_alunos, salvar_alunos
from src.erros import DadoInvalidoError

MENU = """
=== BOLETIM ESCOLAR ===
1. Cadastrar aluno
2. Lançar nota
3. Lançar faltas
4. Ver boletim do aluno
5. Relatório da turma
0. Sair
"""


def ler_numero(mensagem, tipo=float):
    texto = input(mensagem).strip().replace(",", ".")
    try:
        return tipo(texto)
    except ValueError:
        raise DadoInvalidoError("Digite um número válido.") from None


def buscar_aluno(alunos, nome):
    for aluno in alunos:
        if aluno.nome.lower() == nome.strip().lower():
            return aluno
    raise DadoInvalidoError(f"Aluno '{nome.strip()}' não encontrado.")


def cadastrar(alunos):
    novo = criar_aluno(input("Nome do aluno: "), input("Turma: "))
    if any(a.nome.lower() == novo.nome.lower() for a in alunos):
        raise DadoInvalidoError("Já existe um aluno com esse nome.")
    alunos.append(novo)
    print("Aluno cadastrado.")


def lancar_nota(alunos):
    aluno = buscar_aluno(alunos, input("Nome do aluno: "))
    aluno.adicionar_nota(ler_numero("Nota (0 a 10): "))
    print("Nota lançada.")


def lancar_faltas(alunos):
    aluno = buscar_aluno(alunos, input("Nome do aluno: "))
    total = ler_numero("Total de aulas dadas: ", int)
    faltas = ler_numero("Número de faltas: ", int)
    aluno.registrar_frequencia(total, faltas)
    print("Frequência registrada.")


def formatar_boletim(dados):
    notas = " | ".join(f"{nota:.1f}" for nota in dados["notas"])
    return (
        f"Aluno: {dados['nome']}    Turma: {dados['turma']}\n"
        f"Notas: {notas}    Média: {dados['media']:.1f}\n"
        f"Frequência: {dados['frequencia']:.0f}%\n"
        f"Situação: {dados['situacao']}"
    )


def ver_boletim(alunos):
    aluno = buscar_aluno(alunos, input("Nome do aluno: "))
    print(formatar_boletim(aluno.boletim()))


def relatorio_turma(alunos):
    turma = input("Turma: ").strip().lower()
    da_turma = [a for a in alunos if a.turma.lower() == turma]
    if not da_turma:
        raise DadoInvalidoError("Nenhum aluno cadastrado nessa turma.")
    for aluno in da_turma:
        try:
            dados = aluno.boletim()
            print(f"{dados['nome']:<30} média {dados['media']:>4.1f}  "
                  f"freq. {dados['frequencia']:>3.0f}%  {dados['situacao']}")
        except DadoInvalidoError:
            print(f"{aluno.nome:<30} sem notas ou frequência lançadas")


OPCOES = {
    "1": cadastrar,
    "2": lancar_nota,
    "3": lancar_faltas,
    "4": ver_boletim,
    "5": relatorio_turma,
}


def main():
    try:
        alunos = carregar_alunos()
    except ArmazenamentoError as erro:
        print(f"Erro: {erro}")
        return

    while True:
        print(MENU)
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até logo!")
            break
        acao = OPCOES.get(opcao)
        if acao is None:
            print("Opção inválida.")
            continue
        try:
            acao(alunos)
            salvar_alunos(alunos)
        except (DadoInvalidoError, ArmazenamentoError) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
