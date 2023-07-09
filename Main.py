# PyAço: Sistema de gestão de circo

from Banco import Banco
from Tabelas import Tabela, Funcionario, Atracao, Papel, Apresentacao, ChaveEstrangeira

from Formularios import pegar_cpf, pegar_data, pegar_horario


largura = 50

tabela_papeis = Tabela("papeis", Papel)
tabela_funcionarios = Tabela("funcionarios", Funcionario)
tabela_atracoes = Tabela("atracoes", Atracao)
tabela_apresentacoes = Tabela("apresentacoes", Apresentacao)

banco = Banco("Banco", [tabela_papeis, tabela_funcionarios, tabela_atracoes, tabela_apresentacoes])


def cadastrar_funcionario():
    nome = input("Nome: ")
    cpf = pegar_cpf()

    papel = None
    while papel == None:
        tabela_papeis.show()
        papel = input("Papel: ")
        existe = tabela_papeis.pesquisar(chave_primaria = papel)
        if not existe:
            print("Papel inválido")
            papel = None
    telefone = input("Telefone: ")
    funcionario = Funcionario(nome, cpf, papel, telefone)

    tabela_funcionarios.adicionar(funcionario)

def editar_funcionario():
    tabela_funcionarios.show()

    chave_primaria = input("Digite a chave primaria do funcionario: ")
    
    funcionario = tabela_funcionarios.pesquisar(chave_primaria)
    if funcionario:
        print(f"Funcionario: {funcionario.tudo()}")

        nome = input("Nome: ")
        cpf = pegar_cpf()

        tabela_papeis.show()

        existe = None
        while existe == None:
            papel = input("Papel: ")
            existe = tabela_papeis.pesquisar(chave_primaria = papel)
            if not existe:
                print("Papel inválido")

        telefone = input("Telefone: ")
        funcionario = Funcionario(nome, cpf, papel, telefone)

        tabela_funcionarios.editar(chave_primaria, funcionario)
    else:
        print("Funcionario não encontrado")

def remover_funcionario():
    tabela_funcionarios.show()

    existe = None
    while not existe:
        chave_primaria = input("Digite a chave primaria do funcionario, enter para sair: ")
        if chave_primaria == "":
            return
        existe = tabela_funcionarios.pesquisar(chave_primaria = chave_primaria)
        if not existe:
            print("Funcionario inválido")
    
    tabela_funcionarios.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_funcionarios_opcoes = [
    ["Cadastrar funcionário", cadastrar_funcionario],
    ["Mostrar funcionário", tabela_funcionarios.show],
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
        opc = input("Digite a chave primaria do funcionario, enter para parar: ")
        if opc == "":
            if len(funcionarios) == 0:
                print("É necessário ter pelo menos um funcionário")
                opc = None
            continue
        funcionario = tabela_funcionarios.pesquisar(chave_primaria = opc)
        if funcionario:
            funcionarios.append(opc)
        else:
            print("Funcionario não encontrado")
    tabela_atracoes.adicionar(Atracao(nome, funcionarios))

def remover_atracao():
    tabela_atracoes.show()

    existe = None
    while not existe:
        chave_primaria = input("Digite a chave primaria da atracao, enter para sair: ")
        if chave_primaria == "":
            return
        existe = tabela_atracoes.pesquisar(chave_primaria = chave_primaria)
        if not existe:
            print("Atracao inválida")
    
    tabela_atracoes.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_atracoes_opcoes = [
    ["Cadastrar atracão", cadastrar_atracao],
    ["Mostrar atrações", tabela_atracoes.show],
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

    existe = None
    while not existe:
        chave_primaria = input("Digite a chave primaria do papel, enter para sair: ")
        if chave_primaria == "":
            return
        existe = tabela_papeis.pesquisar(chave_primaria = chave_primaria)
        if not existe:
            print("Papel inválido")
    
    tabela_papeis.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_papel_opcoes = [
    ["Cadastrar papel", cadastrar_papel],
    ["Mostrar papel", tabela_papeis.show],
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

def menu_relatorios():
    for c, tabela in enumerate(banco.tabelas):
        print(f"{c + 1} - {tabela.nome}")
    opc = input("Escolha a tabela que deseja filtrar, ou enter para voltar: ")
    if opc == "":
        return
    opc = int(opc)
    if opc > len(banco.tabelas) or opc < 1:
        print("Opção inválida")
    tabela = banco.tabelas[opc - 1]
    aux = tabela.tipo()
    for atributo in aux.__dict__:
        print(f"{atributo}")
    opc = input("Escolha os atributos que deseja filtrar(atributo1,atributo2...), ou enter para voltar: ")
    if opc == "":
        return
    opcs = opc.split(",")
    filtros = {}
    for opc in opcs:
        opc = opc.strip()
        if opc not in aux.__dict__:
            print(f"{opc} não é um atributo válido")
            return

        valor = ""
        while valor == "":
            valor = input(f"{opc}: ")
            valores = valor.split(",")
        print(f"Que tipo de filtro deseja aplicar em {opc}?")
        print("1 - Igual")
        print("2 - Contém")
        tipo = ""
        while tipo not in ["1", "2"]:
            tipo = input("Digite a opção desejada: ")
        if tipo == "1":
            filtros[opc] = valores if len(valores) > 1 else valores[0]
        elif tipo == "2":
            filtros[f"{opc}_contem"] = valores if len(valores) > 1 else valores[0]
    itens = tabela.pesquisar(**filtros)
    if itens:
        for item in itens:
            print(item.tudo())
    else:
        print("Nenhum item encontrado")

def cadastrar_apresentacao():
    nome = input("Nome: ")
    atracoes = []
    tabela_atracoes.show()

    opc = None
    while opc != "":
        opc = input("Digite a chave primaria da atracao, enter para parar: ")
        if opc == "":
            if len(atracoes) == 0:
                print("É necessário ter pelo menos uma atração")
                opc = None
            continue
        atracao = tabela_atracoes.pesquisar(chave_primaria = opc)
        if atracao:
            atracoes.append(opc)
        else:
            print("Atracao não encontrada")
    
    data = pegar_data()
    horario = pegar_horario()

    tabela_apresentacoes.adicionar(Apresentacao(nome, data, horario, atracoes))

def remover_apresentacao():
    tabela_apresentacoes.show()

    existe = None
    while not existe:
        chave_primaria = input("Digite a chave primaria da apresentacao, enter para sair: ")
        if chave_primaria == "":
            return
        existe = tabela_apresentacoes.pesquisar(chave_primaria = chave_primaria)
        if not existe:
            print("Apresentacao inválida")
    
    tabela_apresentacoes.remover(chave_primaria, ChaveEstrangeira.Metodos.remocao)

menu_apresentacoes_opcoes = [
    ["Cadastrar apresentação", cadastrar_apresentacao],
    ["Mostrar apresentações", tabela_apresentacoes.show],
    ["Remover apresentação", remover_apresentacao],
]

def menu_apresentacoes():
    opc = None
    while opc != "":
        for c, opcao in enumerate(menu_apresentacoes_opcoes):
            print(f"{c + 1} - {opcao[0]}")
        opc = input("Digite a opção desejada, ou enter para voltar: ")
        if opc == "":
            continue
        menu_apresentacoes_opcoes[int(opc)-1][1]()

opcoes_menu = [
    ["Menu de papel", menu_papel],
    ["Menu de funcionários", menu_funcionarios],
    ["Menu de atracões", menu_atracoes],
    ["Menu de apresentações", menu_apresentacoes],
    ["Menu de relatórios", menu_relatorios],
]

print("=" * largura)
print(f"{' PyAço: Sistema de gestão de circo ':=^{largura}}")
print("=" * largura)

opcao = None
while opcao != "":
    for c, opcao in enumerate(opcoes_menu):
        print(f"{c + 1} - {opcao[0]}")

    opcao = input("Digite a opção desejada, pressione ENTER para sair: ")

    if opcao == "":
        continue

    opcoes_menu[int(opcao) - 1][1]()
    opcao = None

banco.salvar()
