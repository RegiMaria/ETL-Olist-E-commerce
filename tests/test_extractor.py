import pandas as pd
import pytest

from olist_etl.extractors.extractor import Extractor


def test_extract_csv(tmp_path):
    # arrange: cria um CSV temporario
    csv_path = tmp_path / "teste.csv"
    pd.DataFrame({"a": [1, 2], "b": [3, 4]}).to_csv(csv_path, index=False)

    # act
    extractor = Extractor()
    df = extractor.extract("csv", str(csv_path))

    # assert
    assert df.shape == (2, 2)
    assert list(df.columns) == ["a", "b"]


def test_extract_tipo_nao_suportado():
    extractor = Extractor()

    with pytest.raises(ValueError):
        extractor.extract("xml", "qualquer_caminho.xml")

"""
Checagem rápida no terminal:

python3 -c "
from src.olist_etl.extractors.extractor import Extractor

extractor = Extractor()
orders = extractor.extract('csv', 'data/raw/olist_orders_dataset.csv')
print(orders.shape)
print(orders.head())
"
"""
"""
Usamos python3 -c confirmar que o Extractor conseguia ler um CSV real do Olist 
e funcionar corretamente, sem precisar criar um arquivo temporário só pra isso
e depois ter que lembrar de apagar.
"""