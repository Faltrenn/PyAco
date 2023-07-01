from typing import List, Type
from pickle import dump, load
    
class Item:
    dependencias = []
    def __init__(self, chave_primaria: str) -> None:
        self.chave_primaria = chave_primaria
    
    def get_dependencias(self) -> dict:
        return None

    def get_data(self):
        pass


class Papel(Item):
    def __init__(self, nome: str, descricao: str) -> None:
        Item.__init__(self, nome)
        self.nome = nome
        self.descricao = descricao
    
    def get_data(self):
        return {
            "descricao": self.descricao
        }

    def __str__(self) -> str:
        return self.nome


class Funcionario(Item):
    dependencias = [Papel]
    def __init__(self, nome: str, cpf: str, papel: Papel, telefone: str) -> None:
        Item.__init__(self, cpf)
        self.nome = nome
        self.cpf = cpf
        self.papel = papel
        self.telefone = telefone
    
    def get_dependencias(self) -> dict:
        return {
            Papel: self.papel
        }
    
    def get_data(self):
        return {
            "nome": self.nome,
            "papel": str(self.papel),
            "telefone": self.telefone
        }


class Atracao(Item):
    dependencias = [Funcionario]
    def __init__(self, nome: str, funcionarios: List[Funcionario]) -> None:
        Item.__init__(self, nome)
        self.nome = nome
        self.funcionarios = funcionarios
    
    def get_data(self):
        return {
            "funcionarios": [funcionario.get_data() for funcionario in self.funcionarios]
        }


class Tabela:
    def __init__(self, nome: str, tipo: Type[Item]) -> None:
        self.nome = nome
        self.items: List[Item] = []
        self.banco: Banco = None
        self.tipo = tipo
    
    def salvar(self) -> None:
        if self.banco:
            self.banco.salvar()
    
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

            self.banco.remover(item)

            self.salvar()
    
    def editar(self, chave_primaria: str, item: Item) -> None:
        if isinstance(item, self.tipo):
            for item2 in self.items:
                if item2.chave_primaria == chave_primaria:
                    self.items.remove(item2)
                    self.items.append(item)
                    break

            self.salvar()

    def set_items(self, items: List[Item]) -> None:
        self.items = items

    def get_data(self) -> dict:
        data = {}
        for item in self.items:
            data[item.chave_primaria] = item.get_data()
        return data
    
    def show(self) -> None:
        print(f"Tabela: {self.nome}")
        for item in self.items:
            print("-" * 60)
            print(f"{item.chave_primaria}: {item.get_data()}")
            print("-" * 60)
        print()


class Banco:
    def __init__(self, nome: str, tabelas: List[Tabela]) -> None:
        self.nome = nome
        self.tabelas = tabelas
        for tabela in self.tabelas:
            tabela.banco = self

        try:
            with open(f"{self.nome}", "rb") as banco:
                tabelas = load(banco)
                for tabela in tabelas.values():
                    for tabela2 in self.tabelas:
                        if tabela.nome == tabela2.nome:
                            tabela2.set_items(tabela.items)
                            break
        except FileNotFoundError:
            pass
    
    def remover(self, item: Item) -> None:
        for tabela in self.tabelas:
            for dependencia in tabela.tipo.dependencias:
                if isinstance(item, dependencia):
                    for i in tabela.items:
                        for dep, dep_item in i.get_dependencias().items():
                            print(i.get_data())
                            if isinstance(item, dep) and dep_item.chave_primaria == item.chave_primaria:
                                tabela.remover(i.chave_primaria)
                                break

    def salvar(self) -> None:
        data = {}

        for tabela in self.tabelas:
            data[tabela.nome] = tabela

        with open(self.nome, "wb") as banco:
            dump(data, banco)
