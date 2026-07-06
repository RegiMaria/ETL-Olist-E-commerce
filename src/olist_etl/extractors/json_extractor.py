"""
JsonExtractor - para extrai dados de um arquivo JSON.
"""

import pandas as pd

from .base import BaseExtractor


class JsonExtractor(BaseExtractor):
    """Extrai dados de um arquivo JSON."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract(self) -> pd.DataFrame:
        return pd.read_json(self.filepath)