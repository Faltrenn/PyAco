from datetime import datetime


invalidos = ["0"*11, "1"*11, "2"*11, "3"*11, "4"*11, "5"*11, "6"*11, "7"*11, "8"*11, "9"*11]
hoje = datetime.now()
fevereiro = 29 if hoje.year % 4 == 0 or (hoje.year % 4 == 0 and hoje.year % 100 == 0 and hoje.year % 400 == 0) else 28
meses = [31, fevereiro, 31, 30, 31, 30, 31, 31, 30, 31 ,30, 31]

def validar_cpf(cpf: str) -> bool:
    if len(cpf) != 11:
        return False
    if not cpf.isnumeric():
        return False
    if cpf in invalidos:
        return False
    validacao = cpf[:-2]
    verificador = cpf[-2:]
    soma = 0
    for c, numero in enumerate(validacao):
        soma += int(numero) * (10 - c)
    digito1 = (soma * 10) % 11
    digito1 = 0 if digito1 == 10 else digito1
    if digito1 != int(verificador[0]):
        return False
    soma = 0
    for c, numero in enumerate(validacao + verificador[0]):
        soma += int(numero) * (11 - c)
    digito2 = (soma * 10) % 11
    digito2 = 0 if digito2 == 10 else digito2
    if digito2 != int(verificador[1]):
        return False
    return True

def validar_data(data: str) -> bool:
    partes = data.split("/")
    if len(partes) != 3:
        return False
    if not partes[0].isnumeric() or not partes[1].isnumeric() or not partes[2].isnumeric():
        return False
    dia = int(partes[0])
    mes = int(partes[1])
    ano = int(partes[2])
    if dia < 1 or dia > meses[mes - 1]:
        return False
    if mes < 1 or mes > 12:
        return False
    if ano < hoje.year:
        return False
    if ano == hoje.year and mes < hoje.month:
        return False
    if ano == hoje.year and mes == hoje.month and dia < hoje.day:
        return False
    
    return True

def validar_horario(horario: str) -> bool: #formato hora:minuto
    partes = horario.split(":")
    if len(partes) != 2:
        return False
    if not partes[0].isnumeric() or not partes[1].isnumeric():
        return False
    if len(partes[1]) != 2:
        return False
    hora = int(partes[0])
    minuto = int(partes[1])
    if hora < 0 or hora > 23:
        return False
    if minuto < 0 or minuto > 59:
        return False
    return True
