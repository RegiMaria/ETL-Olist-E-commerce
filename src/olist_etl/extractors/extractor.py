"""
Extractor - versao "antes OCP".

Este modulo respeita o SRP: a classe tem UMA ÚNICA responsabilidade,
que e extrair dados de uma origem.

Porem, ele viola o OCP (Open/Closed Principle): toda vez que uma nova
fonte de dados precisar ser suportada (ex: parquet, API, banco de dados),
sera necessario MODIFICAR o metodo extract() abaixo, adicionando mais um
bloco elif. Isso torna a classe fechada para extensão e aberta para
modificacao - exatamente o oposto do que o OCP recomenda.

Compare com a versao "depois OCP" (extractors/base.py + implementacoes
especificas), onde novas fontes sao adicionadas criando uma classe nova,
sem tocar em nenhum código existente.
"""

import pandas as pd


class Extractor:
    """Extrai dados de diferentes origens com base em um tipo informado.

    Respeita o SRP (so faz extracao), mas viola o OCP: adicionar uma
    fonte nova exige editar o metodo extract().
    """

    def extract(self, source_type: str, filepath: str) -> pd.DataFrame:
        if source_type == "csv":
            return pd.read_csv(filepath)

        elif source_type == "parquet":
            return pd.read_parquet(filepath)

        elif source_type == "json":
            return pd.read_json(filepath)

        # Cada fonte nova exige mais um elif aqui.
        # Isso é a violacao do OCP: a classe nunca fica "fechada".
        else:
            raise ValueError(f"Tipo de fonte nao suportado: {source_type}")
