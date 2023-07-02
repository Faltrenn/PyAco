from typing import List, Type
import Banco


class Item:
    dependencias = []
    def __init__(self, chave_primaria: str) -> None:
        self.chave_primaria = chave_primaria
    
    def get_dependencias(self) -> dict:
        return None

    def get_data(self):
        pass


class Tabela:
    def __init__(self, nome: str, tipo: Type[Item]) -> None:
        self.nome = nome
        self.items: List[Item] = []
        self.tipo = tipo
    
    def salvar(self) -> None:
        if Banco.Banco.banco:
            Banco.Banco.banco.salvar()
    
    def adicionar(self, item: Item):
        self.items.append(item)

        self.salvar()
    
    def pesquisar(self, chave_primaria: str) -> Item:
        for item in self.items:
            if item.chave_primaria == chave_primaria:
                return item
        return None

    def remover(self, chave_primaria: str) -> None:
        item = self.pesquisar(chave_primaria)
        if item in self.items:
            self.items.remove(item)

            Banco.Banco.banco.remover(item)

            self.salvar()
    
    def editar(self, chave_primaria: str, item: Item) -> None:
        if isinstance(item, self.tipo):
            for item2 in self.items:
                if item2.chave_primaria == chave_primaria:
                    self.items.remove(item2)
                    self.items.append(item)
                    break

            self.salvar()

    def set_items(self, items: List[dict]) -> None:
        self.items = []
        self.objeto = self.tipo()
        atributos = {}
        for item in items:
            for atributo in item:
                if hasattr(self.objeto, atributo):
                    atributos[atributo] = item[atributo]
            self.items.append(self.tipo(**atributos))

    def get_data(self) -> list:
        data = []
        for item in self.items:
            data.append(item.get_data())
        return data
    
    def show(self) -> None:
        print(f"Tabela: {self.nome}")
        for item in self.items:
            print("-" * 60)
            print(f"{item.chave_primaria}: {item.get_data()}")
            print("-" * 60)
        print()


class Papel(Item):
    def __init__(self, nome: str = "nome", descricao: str = "descricao") -> None:
        super().__init__(nome)
        self.nome = nome
        self.descricao = descricao
    
    def get_data(self):
        return {
            "nome": self.nome,
            "descricao": self.descricao,
        }

    def __str__(self) -> str:
        return self.nome


class Funcionario(Item):
    dependencias = [Papel]
    def __init__(self, nome: str = "nome", cpf: str = "cpf", papel: str = "nome", telefone: str = "telefone") -> None:
        super().__init__(cpf)
        self.nome = nome
        self.cpf = cpf
        self.papel = Banco.Banco.banco.pesquisar(Papel(papel))
        self.telefone = telefone
    
    def get_dependencias(self) -> dict:
        return {
            Papel: self.papel
        }
    
    def get_data(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "papel": self.papel.chave_primaria,
            "telefone": self.telefone,
        }


class Atracao(Item):
    dependencias = [Funcionario]
    def __init__(self, nome: str = "nome", funcionarios: List[str] = []) -> None:
        super().__init__(nome)
        self.nome = nome
        self.funcionarios = [Banco.Banco.banco.pesquisar(Funcionario(cpf=funcionario)) for funcionario in funcionarios]
    
    def get_data(self):
        return {
            "nome": self.nome,
            "funcionarios": [funcionario.chave_primaria for funcionario in self.funcionarios],
        }
