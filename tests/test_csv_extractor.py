import pandas as pd

from olist_etl.extractors.csv_extractor import CsvExtractor


def test_extract_csv(tmp_path):
    csv_path = tmp_path / "teste.csv"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_csv(csv_path, index=False)

    extractor = CsvExtractor(str(csv_path))
    df = extractor.extract()

    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]
