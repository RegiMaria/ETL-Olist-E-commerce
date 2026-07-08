# etl-olist-ecommerce

Projeto de estudo aplicado sobre os princípios **SOLID**, usando como
contexto prático um extrator de dados do [dataset público da Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
(e-commerce brasileiro).

> **Aviso de escopo:** apesar do nome, este projeto **não** implementa
> um pipeline de ETL completo (Extract-Transform-Load). O foco é
> estudar, na prática, como um princípio de design de software (o OCP)
> se manifesta em código real - usando a etapa de *Extract* como
> estudo de caso. Transform e Load podem vir depois, mas não são o
> objetivo principal aqui.

## Objetivo

Comparar duas versões de uma mesma classe `Extractor`, responsável por
ler dados de diferentes origens (CSV, Parquet, JSON, API simulada):

1. **Antes do OCP** - respeita o SRP, mas viola o OCP.
2. **Depois do OCP** - respeita SRP *e* OCP, com uma *Factory* para
   centralizar a escolha do extractor certo.

A ideia é tornar tangível a diferença entre "só funciona" e "está bem
projetado", e mostrar o motivo prático por trás do princípio, não só a
definição de livro.

## Os princípios que vamos trabalhar

### SRP - Single Responsibility Principle

> Uma classe deve ter um, e somente um, motivo para mudar.

Nas duas versões do `Extractor`, o SRP é respeitado: a única
responsabilidade da classe é extrair dados de uma origem. Ela não
transforma dados, não valida regras de negócio, não salva nada, só
extrai.

### OCP - Open/Closed Principle

> Entidades de software devem estar abertas para extensão, mas
> fechadas para modificação.

É aqui que as duas versões divergem.🧚🏾‍♀️

## Versão 1: "antes OCP"

📁 `src/olist_etl/extractors/extractor.py`

Uma única classe `Extractor`, com um único método `extract()`, que usa
uma cadeia de `if/elif` para decidir o comportamento com base no tipo
de fonte:

```python
class Extractor:
    def extract(self, source_type: str, filepath: str = None) -> pd.DataFrame:
        if source_type == "csv":
            return pd.read_csv(filepath)
        elif source_type == "parquet":
            return pd.read_parquet(filepath)
        elif source_type == "json":
            return pd.read_json(filepath)
        elif source_type == "api":
            dados_fake = {"id": [1, 2], "valor": [100, 200]}
            return pd.DataFrame(dados_fake)
        else:
            raise ValueError(f"Tipo de fonte nao suportado: {source_type}")
```

**Problema:** toda vez que uma fonte nova precisa ser suportada, é
necessário **modificar** o método `extract()` já existente, adicionando
mais um `elif`. Isso violou o OCP na prática, quando adicionamos a
fonte `"api"`: precisamos editar uma classe já pronta e já testada,
com risco de quebrar o que já funcionava.

Além disso, esse processo revelou um segundo problema de design: o
parâmetro `filepath` faz sentido para `csv`/`parquet`/`json`, mas é
inútil para `api` — um sintoma de que o método está tentando fazer
coisas demais dentro de uma única assinatura (um cheiro de código
relacionado ao Interface Segregation Principle, o "I" do SOLID).

## Versão 2: "depois OCP"

📁 `src/olist_etl/extractors/`

```
extractors/
├── base.py               # BaseExtractor (interface abstrata)
├── csv_extractor.py       # CsvExtractor
├── parquet_extractor.py   # ParquetExtractor
├── json_extractor.py      # JsonExtractor
├── api_extractor.py       # ApiExtractor
└── factory.py             # ExtractorFactory
```

Cada fonte de dados vira uma classe própria, que implementa a
interface `BaseExtractor`:

```python
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self) -> pd.DataFrame:
        ...


class CsvExtractor(BaseExtractor):
    def __init__(self, filepath: str):
        self.filepath = filepath

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.filepath)


class ApiExtractor(BaseExtractor):
    def extract(self) -> pd.DataFrame:
        dados_fake = {"id": [1, 2], "valor": [100, 200]}
        return pd.DataFrame(dados_fake)
```

**Resultado:** adicionar uma fonte nova significa **criar um arquivo
novo** implementando `BaseExtractor`, sem tocar em nenhum arquivo já
existente. O sistema fica aberto para extensão e fechado para
modificação, o OCP na prática.

Como bônus, o segundo problema também desaparece: cada classe concreta
só tem os parâmetros que realmente faz sentido para ela (`ApiExtractor`
nem precisa de `filepath`).

## A ExtractorFactory

### O problema que a Factory resolve

Ter várias classes (`CsvExtractor`, `ParquetExtractor`, `ApiExtractor`...)
resolve o problema *dentro* de cada extractor, mas cria uma pergunta
nova: **quem decide qual classe instanciar?**

Sem uma resposta pra isso, o código que consome os extractors acabaria
assim:

```python
if tipo == "csv":
    extractor = CsvExtractor(caminho)
elif tipo == "parquet":
    extractor = ParquetExtractor(caminho)
elif tipo == "api":
    extractor = ApiExtractor()
```

Ou seja: o `if/elif` que tirei de dentro do `Extractor.extract()`
simplesmente **migrou** para outro lugar do código (um `main.py`, um
`pipeline.py`). A violação do OCP não desapareceu, só mudou de
endereço.

### O que é a Factory

**Factory** (fábrica) é um padrão de projeto cuja única
responsabilidade é: dado um tipo de fonte, devolver a instância certa
da classe certa. Ela concentra essa decisão em um único lugar, ao invés
de espalhar `if/elif` por todo o código que precisa de um extractor.

```python
class ExtractorFactory:
    _extractors = {
        "csv": CsvExtractor,
        "parquet": ParquetExtractor,
        "json": JsonExtractor,
        "api": ApiExtractor,
    }

    _sem_filepath = {"api"}

    @classmethod
    def create(cls, source_type: str, filepath: str = None) -> BaseExtractor:
        extractor_class = cls._extractors.get(source_type)

        if extractor_class is None:
            raise ValueError(f"Tipo de fonte nao suportado: {source_type}")

        if source_type in cls._sem_filepath:
            return extractor_class()

        return extractor_class(filepath)
```

Uso:

```python
extractor = ExtractorFactory.create("csv", "data/raw/pedidos.csv")
df = extractor.extract()
```

Quem consome a Factory não precisa saber qual classe concreta veio de
volta, só que ela cumpre o contrato de `BaseExtractor` (tem um
`.extract()`). Isso é polimorfismo em ação.

> **Nota:** a Factory ainda tem um `if` internamente
> (`_sem_filepath`). Isso não é uma violação do OCP — é o mapeamento
> mínimo necessário para traduzir uma string em uma classe. O ganho
> real do OCP aqui é que esse `if` fica isolado em **um único lugar**,
> e adicionar uma fonte nova não exige tocar nas classes de extração
> já existentes.

## Resumo

* **Antes OCP:** um método gigante decidindo comportamento por tipo.
* **Depois OCP:** várias classes, cada uma resolvendo seu próprio
  comportamento.
* **Factory:** a peça que decide qual dessas classes instanciar,
  centralizando essa decisão num único lugar (ao invés de espalhar
  `if/elif` pelo código que consome os extractors).

## Comparação rápida

| | Antes OCP | Depois OCP |
|---|---|---|
| SRP respeitado? | ✅ | ✅ |
| OCP respeitado? | ❌ | ✅ |
| Adicionar fonte nova | Editar método existente | Criar arquivo novo + registrar na Factory |
| Parâmetros "que não se aplicam" | Sim (`filepath` em `api`) | Não |
| Risco ao adicionar fonte | Quebrar fontes já testadas | Nenhum (isolado) |
| Quem decide qual classe usar | N/A (é uma classe só) | `ExtractorFactory` |

## Testes

```bash
pytest tests/ -v
```

- `tests/test_extractor.py` - cobre a versão "antes OCP"
- `tests/test_csv_extractor.py` - `CsvExtractor`
- `tests/test_parquet_extractor.py` - `ParquetExtractor`
- `tests/test_json_extractor.py` - `JsonExtractor`
- `tests/test_api_extractor.py` - `ApiExtractor`
- `tests/test_factory.py` - `ExtractorFactory`

## Estrutura do projeto

```
etl-olist-ecommerce/
├── src/
│   └── olist_etl/
│       └── extractors/
│           ├── extractor.py          # versao "antes OCP"
│           ├── base.py               # versao "depois OCP"
│           ├── csv_extractor.py
│           ├── parquet_extractor.py
│           ├── json_extractor.py
│           ├── api_extractor.py
│           └── factory.py            # ExtractorFactory
├── tests/
│   ├── test_extractor.py
│   ├── test_csv_extractor.py
│   ├── test_parquet_extractor.py
│   ├── test_json_extractor.py
│   ├── test_api_extractor.py
│   └── test_factory.py
└── data/
    └── raw/                          # dataset da Olist (nao versionado)
```

## Próximos passos possíveis

- [ ] Documentar outros princípios SOLID (LSP, ISP, DIP) usando o
      mesmo estudo de caso.
- [ ] (Opcional, fora do escopo principal) Etapas de Transform e Load.

## Referências

- Robert C. Martin, *Clean Architecture* - capítulo sobre OCP.

- [Dataset Olist Brazilian E-Commerce (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)