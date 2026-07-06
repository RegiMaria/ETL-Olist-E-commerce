"""
ParquetExtractor - extrai dados de um arquivo Parquet.
"""

import pandas as pd

from .base import BaseExtractor


class ParquetExtractor(BaseExtractor):
    """Extrai dados de um arquivo Parquet."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract(self) -> pd.DataFrame:
        return pd.read_parquet(self.filepath)
    


# Não tenho arquivo parquet
# Então gera um só pra avaliar:

""" python3 -c "
import pandas as pd
from src.olist_etl.extractors.parquet_extractor import ParquetExtractor

# cria um parquet de teste
pd.DataFrame({'a': [1, 2], 'b': [3, 4]}).to_parquet('/tmp/teste.parquet')

extractor = ParquetExtractor('/tmp/teste.parquet')
df = extractor.extract()
print(df)
"""