# PyAço: Sistema de gestão de circo

from Banco import Banco
from Tabelas import Tabela, Funcionario, Atracao, Papel, Espetaculo, ChaveEstrangeira

largura = 50

tabelaFuncionarios = Tabela("funcionarios", Funcionario)
tabelaAtracoes = Tabela("atracoes", Atracao)
tabelaPapeis = Tabela("papeis", Papel)
tabelaEspetaculos = Tabela("espetaculos", Espetaculo)

banco = Banco("Banco", [tabelaPapeis, tabelaFuncionarios, tabelaAtracoes, tabelaEspetaculos])

def cadastrarFuncionario() -> dict:
    nome = input("Nome: ")
    cpf = input("CPF: ")

    papel = None
    while papel == None:
        tabelaPapeis.show()
        papel = input("Papel: ")
    telefone = input("Telefone: ")
    funcionario = Funcionario(nome, cpf, papel, telefone)

    tabelaFuncionarios.adicionar(funcionario)

def consultarFuncionario():
    tabelaFuncionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabelaFuncionarios.pesquisar(chave_primaria)
    print(f"Funcionario: {funcionario.get_data() if funcionario else 'Não encontrado'}")

def editarFuncionario():
    tabelaFuncionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabelaFuncionarios.pesquisar(chave_primaria)
    if funcionario:
        print(f"Funcionario: {funcionario.get_data()}")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        papel = input("Papel: ")
        telefone = input("Telefone: ")
        funcionario = Funcionario(nome, cpf, papel, telefone)

        tabelaFuncionarios.editar(chave_primaria, funcionario)
    else:
        print("Funcionario não encontrado")

def removerFuncionario():
    tabelaFuncionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    tabelaFuncionarios.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menuFuncionariosOpcoes = [
    ["Cadastrar funcionário", cadastrarFuncionario],
    ["Consultar funcionário", consultarFuncionario],
    ["Editar funcionário", editarFuncionario],
    ["Remover funcionário", removerFuncionario],
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
            funcionarios.append(opc)
        else:
            print("Funcionario não encontrado")
    tabelaAtracoes.adicionar(Atracao(nome, funcionarios))

def removerAtracao():
    tabelaAtracoes.show()

    chave_primaria = input("Digite a chave primaria da atracao: ")
    
    tabelaAtracoes.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menuAtracoesOpcoes = [
    ["Cadastrar atracão", cadastrarAtracao],
    ["Visualizar atrações", tabelaAtracoes.show],
    ["Remover atracão", removerAtracao],
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

def cadastrarPapel():
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    papel = Papel(nome, descricao)
    tabelaPapeis.adicionar(papel)

def consultarPapel():
    tabelaPapeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    papel = tabelaPapeis.pesquisar(chave_primaria)
    print(f"Papel: {papel.get_data() if papel else 'Não encontrado'}")

def editarPapel():
    tabelaPapeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    papel = tabelaPapeis.pesquisar(chave_primaria)
    if papel:
        print(f"Papel: {papel.get_data()}")

        nome = input("Nome: ")
        papel = Papel(nome)

        tabelaPapeis.editar(chave_primaria, papel)
    else:
        print("Papel não encontrado")

def removerPapel():
    tabelaPapeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    tabelaPapeis.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menuPapelOpcoes = [
    ["Cadastrar papel", cadastrarPapel],
    ["Consultar papel", consultarPapel],
    ["Editar papel", editarPapel],
    ["Remover papel", removerPapel],
]

def menuPapel():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menuPapelOpcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar:")
        if opc == "":
            continue
        menuPapelOpcoes[int(opc)-1][1]()

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
    ["Menu de papel", menuPapel],
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
