"""
ApiExtractor - simula a extracao de dados de uma API (sem rede real).

Reparamos que essa classe NAO precisa de filepath. Na versao "antes OCP",
esse parametro existia no metodo extract() mesmo sem fazer sentido
para essa fonte. Aqui, cada classe so tem os parametros que de fato
usa.
"""

import pandas as pd

from .base import BaseExtractor


class ApiExtractor(BaseExtractor):
    """Extrai dados simulados de uma API."""

    def extract(self) -> pd.DataFrame:
        dados_fake = {"id": [1, 2], "valor": [100, 200]}
        return pd.DataFrame(dados_fake)