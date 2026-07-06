import pandas as pd

from olist_etl.extractors.parquet_extractor import ParquetExtractor


def test_extract_parquet(tmp_path):
    parquet_path = tmp_path / "teste.parquet"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_parquet(parquet_path)

    extractor = ParquetExtractor(str(parquet_path))
    df = extractor.extract()

    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]
