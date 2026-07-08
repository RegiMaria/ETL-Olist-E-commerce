"""
Testes para ExtractorFactory.

Cobrem: instanciacao correta por tipo, comportamento do extractor
retornado, e erro para tipo nao suportado.
"""

import pandas as pd
import pytest

from olist_etl.extractors.api_extractor import ApiExtractor
from olist_etl.extractors.csv_extractor import CsvExtractor
from olist_etl.extractors.factory import ExtractorFactory
from olist_etl.extractors.json_extractor import JsonExtractor
from olist_etl.extractors.parquet_extractor import ParquetExtractor


def test_factory_cria_csv_extractor(tmp_path):
    csv_path = tmp_path / "teste.csv"
    pd.DataFrame({"a": [1, 2]}).to_csv(csv_path, index=False)

    extractor = ExtractorFactory.create("csv", str(csv_path))

    assert isinstance(extractor, CsvExtractor)
    df = extractor.extract()
    assert df.shape == (2, 1)


def test_factory_cria_parquet_extractor(tmp_path):
    parquet_path = tmp_path / "teste.parquet"
    pd.DataFrame({"a": [1, 2]}).to_parquet(parquet_path)

    extractor = ExtractorFactory.create("parquet", str(parquet_path))

    assert isinstance(extractor, ParquetExtractor)
    df = extractor.extract()
    assert df.shape == (2, 1)


def test_factory_cria_json_extractor(tmp_path):
    json_path = tmp_path / "teste.json"
    pd.DataFrame({"a": [1, 2]}).to_json(json_path)

    extractor = ExtractorFactory.create("json", str(json_path))

    assert isinstance(extractor, JsonExtractor)
    df = extractor.extract()
    assert df.shape == (2, 1)


def test_factory_cria_api_extractor_sem_filepath():
    extractor = ExtractorFactory.create("api")

    assert isinstance(extractor, ApiExtractor)
    df = extractor.extract()
    assert df.shape == (2, 2)
    assert list(df.columns) == ["id", "valor"]


def test_factory_tipo_nao_suportado():
    with pytest.raises(ValueError):
        ExtractorFactory.create("xml", "qualquer_caminho.xml")