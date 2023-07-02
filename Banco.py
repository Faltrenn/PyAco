from typing import List, Type
from json import dumps, loads
    
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
        if Banco.banco:
            Banco.banco.salvar()
    
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

            Banco.banco.remover(item)

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


class Banco:
    banco = None
    def __init__(self, nome: str, tabelas: List[Tabela]) -> None:
        Banco.banco = self

        self.nome = nome
        self.tabelas = tabelas
        
        self.carregar()
    
    def carregar(self) -> None:
        try:
            with open(f"{self.nome}.json", "r") as arquivo:
                data = loads(arquivo.read())
                for tabela in self.tabelas:
                    if tabela.nome in data:
                        tabela.set_items(data[tabela.nome])
        except Exception as error:
            print(error)
    
    def remover(self, item: Item) -> None:
        for tabela in self.tabelas:
            for dependencia in tabela.tipo.dependencias:
                if isinstance(item, dependencia):
                    for i in tabela.items:
                        for dep, dep_item in i.get_dependencias().items():
                            if isinstance(item, dep) and dep_item.chave_primaria == item.chave_primaria:
                                tabela.remover(i.chave_primaria)
                                break
    
    def pesquisar(self, item: Item) -> Item:
        for tabela in self.tabelas:
            if isinstance(item, tabela.tipo):
                return tabela.pesquisar(item.chave_primaria)
        return None
    
    def get_data(self) -> dict:
        data = {}
        for tabela in self.tabelas:
            data[tabela.nome] = tabela.get_data()
        return data
    
    def salvar(self) -> None:
        with open(f"{self.nome}.json", "w") as arquivo:
            arquivo.write(dumps(self.get_data(), indent=4))


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
    def __init__(self, nome: str = "nome", cpf: str = "cpf", papel: str = "nome") -> None:
        super().__init__(cpf)
        self.nome = nome
        self.cpf = cpf
        self.papel = Banco.banco.pesquisar(Papel(papel))
    
    def get_dependencias(self) -> dict:
        return {
            Papel: self.papel
        }
    
    def get_data(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "papel": self.papel.chave_primaria,
        }


class Atracao(Item):
    dependencias = [Funcionario]
    def __init__(self, nome: str = "nome", funcionarios: List[str] = []) -> None:
        super().__init__(nome)
        self.nome = nome
        self.funcionarios = [Banco.banco.pesquisar(Funcionario(cpf=funcionario)) for funcionario in funcionarios]
    
    def get_data(self):
        return {
            "nome": self.nome,
            "funcionarios": [funcionario.chave_primaria for funcionario in self.funcionarios],
        }
