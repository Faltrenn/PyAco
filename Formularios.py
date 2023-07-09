from Validar import validar_cpf, validar_data, validar_horario

def pegar_cpf() -> str:
    valido = False
    while not valido:
        cpf = input("CPF: ")
        cpf = cpf.replace(".", "").replace("-", "")
        valido = validar_cpf(cpf)
        if not valido:
            print("CPF inválido")
    return cpf

def pegar_data() -> str:
    valido = False
    while not valido:
        data = input("Data(dd/mm/aaaa): ")
        valido = validar_data(data)
        if not valido:
            print("Data inválida")
    return data

def pegar_horario() -> str:
    valido = False
    while not valido:
        horario = input("Horario(hh:mm): ")
        valido = validar_horario(horario)
        if not valido:
            print("Horario inválido")
        horario = horario.split(":")
    return f"{int(horario[0]):02}:{horario[1]}"
