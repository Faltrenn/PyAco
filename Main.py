# PyAço: Sistema de gestão de circo

largura = 50

banco = {
    "funcionarios": {},
    "atracoes": {},
    "espetaculos": {},
}

def cadastrarFuncionario() -> dict:
    nome = input("Nome: ")
    cpf = input("CPF: ")
    papel = input("Papel: ")
    telefone = input("Telefone: ")
    funcionario = {
        "nome": nome,
        "cpf": cpf,
        "papel": papel,
        "telefone": telefone,
    }
    banco["funcionarios"][cpf] = funcionario

def consultarFuncionario():
    nome = input("Digite o nome do funcionário")
    funcionarios = []
    for cpf, funcionario in banco["funcionarios"].items():
        if nome.upper() in funcionario["nome"].upper():
            funcionarios.append(funcionario)
    for funcionario in funcionarios:
        print("-" * largura)
        print(f"Nome: {funcionario['nome']}")
        print(f"CPF: {funcionario['cpf']}")
        print(f"Papel: {funcionario['papel']}")
        print(f"Telefone: {funcionario['telefone']}")
        print("-" * largura)

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
        menuFuncionariosOpcoes[int(opc)-1][1]()

def menuAtracoes():
    print("Cadastro de atracões")
    print("Nome")
    print("Funcionários")
    print("Consultar atracão")
    print("Nome")

def cadastrarAtracao():
    nome = input("Nome: ")
    funcionarios = []
    while opc != "":
        c = 0
        for funcionario in banco["funcionarios"]:
            if funcionario not in funcionarios:
                print(f"{c + 1} - {funcionario['nome']}")
                c += 1
        opc = input("Digite o número do funcionário ou enter para sair: ")
        if opc != "":
            funcionarios.append(banco["funcionarios"][int(opc) - 1])
    atracao = {
        "nome": nome,
        "funcionarios": funcionarios,
    }
    banco["atracoes"][nome] = atracao

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

for c, opcao in enumerate(opcoesMenu):
    print(f"{c + 1} - {opcao[0]}")

while True:
    opcao = int(input("Digite a opção desejada: "))

    opcoesMenu[opcao - 1][1]()
