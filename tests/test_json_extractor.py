import pandas as pd

from olist_etl.extractors.json_extractor import JsonExtractor


def test_extract_json(tmp_path):
    json_path = tmp_path / "teste.json"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_json(json_path)

    extractor = JsonExtractor(str(json_path))
    df = extractor.extract()

    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]
