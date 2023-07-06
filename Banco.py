from typing import List, Type
from json import dumps, loads
import Tabelas
    

class Banco:
    banco = None
    def __init__(self, nome: str, tabelas: List[Tabelas.Tabela]) -> None:
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
    
    def remover(self, item: Tabelas.Item, metodo_ci: Tabelas.ChaveEstrangeira.Metodos) -> None:
        for tabela in self.tabelas:
            for dependencia in tabela.tipo.dependencias:
                if isinstance(item, dependencia):
                    for i in tabela.items:
                        for dep, dep_item in i.get_dependencias().items():
                            if isinstance(item, dep):
                                if isinstance(dep_item[1], list):
                                    for j in dep_item[1]:
                                        if j.chave_primaria == item.chave_primaria:
                                            match metodo_ci:
                                                case Tabelas.ChaveEstrangeira.Metodos.destruicao:
                                                    tabela.remover(item.chave_primaria)
                                                case Tabelas.ChaveEstrangeira.Metodos.remocao:
                                                    getattr(i, dep_item[0]).remove(j)
                                            break
                                else:
                                    match metodo_ci:
                                        case Tabelas.ChaveEstrangeira.Metodos.destruicao:
                                            tabela.remover(i.chave_primaria)
                                        case Tabelas.ChaveEstrangeira.Metodos.remocao:
                                            setattr(i, dep_item[0], None)
                                    break
    
    def pesquisar(self, item: Tabelas.Item) -> Tabelas.Item:
        for tabela in self.tabelas:
            if isinstance(item, tabela.tipo):
                return tabela.pesquisar(item = item)
        return None

    def tudo(self, tipo: Type[Tabelas.Item] = None):
        if tipo:
            for tabela in self.tabelas:
                if tabela.tipo == tipo:
                    return tabela.tudo()
            return None
        else:
            data = {}
            for tabela in self.tabelas:
                data[tabela.nome] = tabela.tudo()
            return data
    
    def salvar(self) -> None:
        with open(f"{self.nome}.json", "w") as arquivo:
            arquivo.write(dumps(self.tudo(), indent=4))
