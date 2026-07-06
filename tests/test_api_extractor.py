from olist_etl.extractors.api_extractor import ApiExtractor


def test_extract_api():
    extractor = ApiExtractor()
    df = extractor.extract()

    assert df.shape == (2, 2)
    assert list(df.columns) == ["id", "valor"]
