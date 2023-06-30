# PyAço: Sistema de gestão de circo

from Banco import Banco, Tabela, Funcionario, Atracao


largura = 50

tabelaFuncionarios = Tabela("funcionarios")
tabelaAtracoes = Tabela("atracoes")

banco = Banco("Banco", [tabelaFuncionarios, tabelaAtracoes])

def cadastrarFuncionario() -> dict:
    nome = input("Nome: ")
    cpf = input("CPF: ")
    papel = input("Papel: ")
    telefone = input("Telefone: ")
    funcionario = Funcionario(nome, cpf, papel, telefone)

    tabelaFuncionarios.adicionar(funcionario)

def consultarFuncionario():
    tabelaFuncionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabelaFuncionarios.pesquisar(chave_primaria)
    print(f"Funcionario: {funcionario.get_data() if funcionario else 'Não encontrado'}")

menuFuncionariosOpcoes = [
    ["Cadastrar funcionário", cadastrarFuncionario],
    ["Consultar funcionário", consultarFuncionario],
]

def menuFuncionarios():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menuFuncionariosOpcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar:")
        if opc == "":
            continue
        menuFuncionariosOpcoes[int(opc)-1][1]()


def cadastrarAtracao():
    nome = input("Nome: ")

    tabelaFuncionarios.show()

    opc = None
    funcionarios = []
    while opc != "":
        opc = input("Digite a chave primaria do funcionario: ")
        if opc == "":
            continue
        funcionario = tabelaFuncionarios.pesquisar(opc)
        if funcionario:
            funcionarios.append(funcionario)
        else:
            print("Funcionario não encontrado")
    tabelaAtracoes.adicionar(Atracao(nome, funcionarios))


menuAtracoesOpcoes = [
    ["Cadastrar atracão", cadastrarAtracao],
    ["Visualizar atrações", tabelaAtracoes.show],
]

def menuAtracoes():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menuAtracoesOpcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar:")
        if opc == "":
            continue
        menuAtracoesOpcoes[int(opc)-1][1]()


def menuEspetaculos():
    print("Cadastro de espetáculos")
    print("Cidade")
    print("Local")
    print("Data")
    print("Horário")
    print("Consultar espetáculo")
    print("Cidade")

def sair():
    print("Sair")
    banco.salvar()
    exit()

opcoesMenu = [
    ["Menu de funcionários", menuFuncionarios],
    ["Menu de atracões", menuAtracoes],
    ["Menu de espetáculos", menuEspetaculos],
    ["Sair", sair],
]

print("=" * largura)
print(f"{' PyAço: Sistema de gestão de circo ':=^{largura}}")
print("=" * largura)

while True:
    for c, opcao in enumerate(opcoesMenu):
        print(f"{c + 1} - {opcao[0]}")

    opcao = int(input("Digite a opção desejada: "))

    opcoesMenu[opcao - 1][1]()
