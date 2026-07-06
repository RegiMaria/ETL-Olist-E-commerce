from abc import ABC, abstractmethod

import pandas as pd


class BaseExtractor(ABC):
    """Interface para extratores de dados.

    Cada fonte nova = uma nova classe que implementa extract(),
    sem tocar em nenhuma classe existente. Isso e o OCP na pratica:
    aberto para extensao, fechado para modificacao.
    """

    @abstractmethod
    def extract(self) -> pd.DataFrame:
        ...


# Comentário pedagógico
# Cada extractor concreto recebe apenas os parametros que fazem
# sentido para ele no __init__ (resolvendo o code smell do
# "parametro que nao se aplica a todos os casos", presente na
# versao anterior do Extractor com if/elif).

# O que é ABC
# ABC significa Abstract Base Class (Classe Base Abstrata). 
# É um recurso do Python (do módulo abc) que permite criar uma classe
# que não pode ser instanciada diretamente. 
# Ela serve só como "molde"/contrato pra outras classes seguirem.

# Sem herdar de ABC, BaseExtractor seria uma classe normal, 
# e nada impediria alguém de instanciá-la diretamente,
# o que não faz sentido, porque ela não sabe extrair nada de lugar nenhum,
# só define que deve existir um método extract().

# O que é @abstractmethod
# É um decorador que marca um método como obrigatório para qualquer classe filha.
# Se uma subclasse não implementar esse método, ela também não pode ser instanciada.
# O Python literalmente te impede de criar um extractor incompleto. Isso é uma 
# garantia em tempo de execução (não só uma convenção que alguém pode ignorar)
