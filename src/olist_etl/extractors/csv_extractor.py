# csv_extractor.py
# csv_extractor.py
import pandas as pd
from .base import BaseExtractor


class CsvExtractor(BaseExtractor):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.filepath)


# Extrai dados de um arquivo CSV.
# Unica responsabilidade: extrair de UMA fonte CSV especifica.
# Se amanha for necessario extrair de outra fonte (parquet, api,
# banco de dados), basta criar uma nova classe implementando
# BaseExtractor, sem tocar neste arquivo. Isso e o OCP na pratica.
 