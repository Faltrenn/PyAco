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
    
    def __str__(self) -> str:
        return self.chave_primaria


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
    
    def adicionar(self, item: Item) -> None:
        if isinstance(item, self.tipo):
            if not self.pesquisar(chave_primaria = item.chave_primaria):
                self.items.append(item)
                self.salvar()
            else:
                print(f"Já existe um item com a chave primaria {item.chave_primaria}")
        else:
            print(f"O item não é do tipo {self.tipo}")
    
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
                            valor = getattr(item, comando[0])
                            if isinstance(valor, Item):
                                valor = valor.chave_primaria
                            elif isinstance(valor, list):
                                valor = [v.chave_primaria for v in valor]
                            
                            if "contem" in comando[1]:
                                ft = filtros[filtro]
                                if isinstance(ft, list):
                                    for f in ft:
                                        if f in valor:
                                            itens.append(item)
                                            break
                                if isinstance(ft, str) and ft in valor:
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
            itens.remove(removido)

        return itens if len(itens) > 0 else None

    def remover(self, chave_primaria: str, metodo_ci = None) -> None:
        item = self.pesquisar(chave_primaria = chave_primaria)
        if item:
            self.items.remove(item[0])

            Banco.Banco.banco.remover(item, metodo_ci)

            self.salvar()
    
    def editar(self, chave_primaria: str, item: Item) -> None:
        if self.pesquisar(chave_primaria = item.chave_primaria):
            print(f"Já existe um item com a chave primaria {item.chave_primaria}")
            return
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
            for atributo in item.__dict__:
                attr = getattr(item, atributo)
                if isinstance(attr, list):
                    attr = [str(a) for a in attr]
                print(f"{atributo}: {str(attr)}")
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
    
    def __str__(self) -> str:
        return self.nome


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
    def __init__(self, nome: str = "", data: str = "", horario:str = "", atracoes: List[str] = []) -> None:
        super().__init__(nome)
        self.nome = nome
        self.data = data
        self.horario = horario
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
            "horario": self.horario,
            "atracoes": [atracao.chave_primaria for atracao in self.atracoes],
        }
