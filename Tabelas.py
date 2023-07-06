from typing import List, Type
import Banco

tipos_comandos = ["contem"]

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
    
    def pesquisar(self, **filtros) -> List[Item]:
        itens = []
        removidos = []
        for c, filtro in enumerate(filtros):
            aux = filtro.split("_")
            comando = aux
            if len(aux) > 1:
                comando = ["_".join(comando) if comando[-1] not in tipos_comandos else "_".join(comando[:-1])]
                comando.append(aux[-1]) if aux[-1] in tipos_comandos else None
            if c == 0:
                if len(comando) == 1:
                    for item in self.items:
                        if hasattr(item, comando[0]) and str(getattr(item, comando[0])) == str(filtros[filtro]):
                            itens.append(item)
                else:
                    for item in self.items:
                        if hasattr(item, comando[0]):
                            valor = str(getattr(item, comando[0]))
                            if len(comando) > 1:
                                if "contem" in comando[1] and filtros[filtro] in valor:
                                    itens.append(item)
                            else:
                                if filtros[filtro] == valor:
                                    itens.append(item)
            else:
                for item in itens:
                    if hasattr(item, comando[0]):
                        valor = str(getattr(item, comando[0]))
                    if len(comando) > 1:
                        if "contem" in comando[1] and filtros[filtro] not in valor:
                            removidos.append(item)
                    else:
                        if filtros[filtro] != valor:
                            removidos.append(item)

        for removido in removidos:
            print("removidos", removido.tudo())
            itens.remove(removido)

        # for item in self.items:
        #     for atributo, valor in filtros.items():
        #         if hasattr(item, atributo) and getattr(item, atributo) == valor:
        #             items.append(item)
        #         else:
        #             if item in items:
        #                 items.remove(item)
        #             break
            
        # quantidade = len(itens)
        # if quantidade == 1:
        #     return itens[0]
        # elif quantidade > 1:
        #     return itens
        # else:
        #     return None

        return itens if len(itens) > 0 else None

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
        p = Banco.Banco.banco.pesquisar(Papel(papel))
        self.papel = p[0] if p else None
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
        self.funcionarios = []
        for funcionario in funcionarios:
            func = Banco.Banco.banco.pesquisar(Funcionario(cpf=funcionario))
            self.funcionarios.append(func[0]) if func else None

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
        self.atracoes = []
        for atracao in atracoes:
            atra = Banco.Banco.banco.pesquisar(Atracao(nome=atracao))
            self.atracoes.append(atra[0]) if atra else None

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
        self.apresentacoes = []
        for apresentacao in apresentacoes:
            apre = Banco.Banco.banco.pesquisar(Apresentacao(nome=apresentacao))
            self.apresentacoes.append(apre[0]) if apre else None

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
