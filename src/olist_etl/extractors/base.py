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



