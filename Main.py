# PyAço: Sistema de gestão de circo

from Banco import Banco
from Tabelas import Tabela, Funcionario, Atracao, Papel, Espetaculo, ChaveEstrangeira, Item
from typing import Type


largura = 50

tabela_funcionarios = Tabela("funcionarios", Funcionario)
tabela_atracoes = Tabela("atracoes", Atracao)
tabela_papeis = Tabela("papeis", Papel)
tabela_espetaculos = Tabela("espetaculos", Espetaculo)

banco = Banco("Banco", [tabela_papeis, tabela_funcionarios, tabela_atracoes, tabela_espetaculos])

def cadastrar_funcionario() -> dict:
    nome = input("Nome: ")
    cpf = input("CPF: ")

    papel = None
    while papel == None:
        tabela_papeis.show()
        papel = input("Papel: ")
    telefone = input("Telefone: ")
    funcionario = Funcionario(nome, cpf, papel, telefone)

    tabela_funcionarios.adicionar(funcionario)

def consultar_funcionario():
    tabela_funcionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabela_funcionarios.pesquisar(chave_primaria = chave_primaria)[0]
    print(f"Funcionario: {funcionario.tudo() if funcionario else 'Não encontrado'}")

def editar_funcionario():
    tabela_funcionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabela_funcionarios.pesquisar(chave_primaria)
    if funcionario:
        print(f"Funcionario: {funcionario.tudo()}")

        nome = input("Nome: ")
        cpf = input("CPF: ")
        papel = input("Papel: ")
        telefone = input("Telefone: ")
        funcionario = Funcionario(nome, cpf, papel, telefone)

        tabela_funcionarios.editar(chave_primaria, funcionario)
    else:
        print("Funcionario não encontrado")

def remover_funcionario():
    tabela_funcionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    tabela_funcionarios.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_funcionarios_opcoes = [
    ["Cadastrar funcionário", cadastrar_funcionario],
    ["Consultar funcionário", consultar_funcionario],
    ["Editar funcionário", editar_funcionario],
    ["Remover funcionário", remover_funcionario],
]

def menu_funcionarios():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menu_funcionarios_opcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar: ")
        if opc == "":
            continue
        menu_funcionarios_opcoes[int(opc)-1][1]()


def cadastrar_atracao():
    nome = input("Nome: ")

    tabela_funcionarios.show()

    opc = None
    funcionarios = []
    while opc != "":
        opc = input("Digite a chave primaria do funcionario: ")
        if opc == "":
            continue
        funcionario = tabela_funcionarios.pesquisar(chave_primaria = opc)
        if funcionario:
            funcionarios.append(opc)
        else:
            print("Funcionario não encontrado")
    tabela_atracoes.adicionar(Atracao(nome, funcionarios))

def remover_atracao():
    tabela_atracoes.show()

    chave_primaria = input("Digite a chave primaria da atracao: ")
    
    tabela_atracoes.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_atracoes_opcoes = [
    ["Cadastrar atracão", cadastrar_atracao],
    ["Visualizar atrações", tabela_atracoes.show],
    ["Remover atracão", remover_atracao],
]

def menu_atracoes():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menu_atracoes_opcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar: ")
        if opc == "":
            continue
        menu_atracoes_opcoes[int(opc)-1][1]()

def cadastrar_papel():
    nome = input("Nome: ")
    descricao = input("Descrição: ")
    papel = Papel(nome, descricao)
    tabela_papeis.adicionar(papel)

def consultar_papel():
    tabela_papeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    papel = tabela_papeis.pesquisar(chave_primaria = chave_primaria)
    print(f"Papel: {papel.tudo() if papel else 'Não encontrado'}")

def editar_papel():
    tabela_papeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    papel = tabela_papeis.pesquisar(chave_primaria = chave_primaria)
    if papel:
        print(f"Papel: {papel.tudo()}")

        nome = input("Nome: ")
        papel = Papel(nome)

        tabela_papeis.editar(chave_primaria, papel)
    else:
        print("Papel não encontrado")

def remover_papel():
    tabela_papeis.show()

    chave_primaria = input("Digite a chave primaria do papel: ")
    
    tabela_papeis.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_papel_opcoes = [
    ["Cadastrar papel", cadastrar_papel],
    ["Consultar papel", consultar_papel],
    ["Editar papel", editar_papel],
    ["Remover papel", remover_papel],
]

def menu_papel():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menu_papel_opcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar: ")
        if opc == "":
            continue
        menu_papel_opcoes[int(opc)-1][1]()

def menu_espetaculos():
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

def pegar_tudo(tipo: Type[Item]):
    return banco.tudo(tipo)

menu_relatorios_opcoes = [

]

def menu_relatorios():
    pass

opcoes_menu = [
    ["Menu de funcionários", menu_funcionarios],
    ["Menu de atracões", menu_atracoes],
    ["Menu de espetáculos", menu_espetaculos],
    ["Menu de papel", menu_papel],
    ["Menu de relatórios", menu_relatorios],
    ["Sair", sair],
]

print("=" * largura)
print(f"{' PyAço: Sistema de gestão de circo ':=^{largura}}")
print("=" * largura)

while True:
    for c, opcao in enumerate(opcoes_menu):
        print(f"{c + 1} - {opcao[0]}")

    opcao = int(input("Digite a opção desejada: "))

    opcoes_menu[opcao - 1][1]()
