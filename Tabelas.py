from typing import List, Type
import Banco


class Item:
    dependencias = []
    def __init__(self, chave_primaria: str) -> None:
        self.chave_primaria = chave_primaria
    
    def get_dependencias(self) -> dict:
        return None

    def tudo(self):
        pass
    
    def substituir(self, item: "Item") -> None:
        for atributo in item.__dict__:
            setattr(self, atributo, getattr(item, atributo))


class ChaveEstrangeira:
    class Metodos:
        destruicao = 0
        remocao = 1


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
    
    def pesquisar(self, **filtros) -> Item:
        items = []
        if "item" in filtros:
            if isinstance(filtros["item"], self.tipo):
                for item in self.items:
                    if item.chave_primaria == filtros["item"].chave_primaria:
                        return item
            return None
        
        for item in self.items:
            for atributo, valor in filtros.items():
                if hasattr(item, atributo) and getattr(item, atributo) == valor:
                    items.append(item)
                else:
                    if item in items:
                        items.remove(item)
                    break
            

        return items[0] if len(items) > 0 else None

        # for item in self.items:
        #     if item.chave_primaria == chave_primaria:
        #         return item
        # return None

    def remover(self, chave_primaria: str, metodo_ci = None) -> None:
        item = self.pesquisar(chave_primaria)
        if item in self.items:
            self.items.remove(item)

            Banco.Banco.banco.remover(item, metodo_ci)

            self.salvar()
    
    def editar(self, chave_primaria: str, item: Item) -> None:
        if isinstance(item, self.tipo):
            for item2 in self.items:
                if item2.chave_primaria == chave_primaria:
                    item2.substituir(item)
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

    def tudo(self) -> list:
        data = []
        for item in self.items:
            data.append(item.tudo())
        return data
    
    def show(self) -> None:
        print(f"Tabela: {self.nome}")
        for item in self.items:
            print("-" * 60)
            print(f"{item.chave_primaria}: {item.tudo()}")
            print("-" * 60)
        print()


class Papel(Item):
    def __init__(self, nome: str = "nome", descricao: str = "descricao") -> None:
        super().__init__(nome)
        self.nome = nome
        self.descricao = descricao
    
    def tudo(self):
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
            Papel: ["papel", self.papel]
        }
    
    def tudo(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "papel": self.papel.chave_primaria if self.papel else None,
            "telefone": self.telefone,
        }


class Atracao(Item):
    dependencias = [Funcionario]
    def __init__(self, nome: str = "nome", funcionarios: List[str] = []) -> None:
        super().__init__(nome)
        self.nome = nome
        self.funcionarios = [Banco.Banco.banco.pesquisar(Funcionario(cpf=funcionario)) for funcionario in funcionarios]
    
    def get_dependencias(self) -> dict:
        return {
            Funcionario: ["funcionarios", self.funcionarios]
        }

    def tudo(self):
        return {
            "nome": self.nome,
            "funcionarios": [funcionario.chave_primaria for funcionario in self.funcionarios],
        }


class Apresentacao(Item):
    dependencias = [Atracao]
    def __init__(self, nome: str, data: str, atracoes: List[str]) -> None:
        super().__init__(nome)
        self.nome = nome
        self.data = data
        self.atracoes = [Banco.Banco.banco.pesquisar(Atracao(nome=atracao)) for atracao in atracoes]

    def get_dependencias(self) -> dict:
        return {
            Atracao: ["atracoes", self.atracoes]
        }

    def tudo(self):
        return {
            "nome": self.nome,
            "data": self.data,
            "atracoes": [atracao.chave_primaria for atracao in self.atracoes],
        }


class Espetaculo(Item):
    dependencias = [Atracao]
    def __init__(self, cidade: str, data: str, apresentacoes: List[str]) -> None:
        super().__init__(data)
        self.cidade = cidade
        self.data = data
        self.apresentacoes = [Banco.Banco.banco.pesquisar(Apresentacao(nome=apresentacao)) for apresentacao in apresentacoes]

    def get_dependencias(self) -> dict:
        return {
            Apresentacao: ["apresentacoes", self.apresentacoes]
        }

    def tudo(self):
        return {
            "cidade": self.cidade,
            "data": self.data,
            "apresentacoes": [apresentacao.chave_primaria for apresentacao in self.apresentacoes],
        }
