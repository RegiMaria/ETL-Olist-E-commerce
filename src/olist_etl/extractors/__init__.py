from .base import BaseExtractor
from .csv_extractor import CsvExtractor
from .parquet_extractor import ParquetExtractor
from .json_extractor import JsonExtractor
from .api_extractor import ApiExtractor
from .factory import ExtractorFactory

# Adicionamos para:
# Ao inves de um bloco de imports gigantes,
# poderemos apenas:
# from olist_etl.extractors import CsvExtractor, JsonExtractor, ParquetExtractor, ApiExtractor