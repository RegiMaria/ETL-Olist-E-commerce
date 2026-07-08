"""
ExtractorFactory - decide qual Extractor concreto instanciar.

Sem essa classe, o codigo que consome os extractors (ex: um pipeline
ou um main.py) precisaria de um if/elif proprio pra saber qual classe
usar - recriando, fora das classes de extracao, o mesmo problema que
o OCP resolveu dentro delas.

A Factory concentra essa decisao em um unico lugar. Adicionar uma
fonte nova exige registrar uma entrada aqui, mas nao exige tocar em
nenhuma classe de extracao ja existente (CsvExtractor, JsonExtractor
etc. continuam intocadas).
"""

from .api_extractor import ApiExtractor
from .base import BaseExtractor
from .csv_extractor import CsvExtractor
from .json_extractor import JsonExtractor
from .parquet_extractor import ParquetExtractor


class ExtractorFactory:
    """Fabrica de extratores: mapeia um tipo de fonte para a classe."""

    _extractors = {
        "csv": CsvExtractor,
        "parquet": ParquetExtractor,
        "json": JsonExtractor,
        "api": ApiExtractor,
    }

    # Fontes que nao precisam de filepath (o construtor nao recebe
    # argumentos). Mantido separado do dict acima pra deixar explicito
    # o motivo, em vez de inferir por convencao.
    _sem_filepath = {"api"}

    @classmethod
    def create(cls, source_type: str, filepath: str = None) -> BaseExtractor:
        """Instancia o Extractor correto para o tipo de fonte informado.

        Args:
            source_type: tipo da fonte de dados ("csv", "parquet",
                "json", "api").
            filepath: caminho do arquivo. Nao e usado para fontes que
                nao dependem de arquivo (ex: "api").

        Raises:
            ValueError: se source_type nao estiver registrado.
        """
        extractor_class = cls._extractors.get(source_type)

        if extractor_class is None:
            raise ValueError(f"Tipo de fonte nao suportado: {source_type}")

        if source_type in cls._sem_filepath:
            return extractor_class()

        return extractor_class(filepath)
