# Olist ETL - Estudo de Princípios SOLID

Projeto de estudo prático dos princípios SOLID (SRP e OCP) aplicados a um pipeline
ETL em Python, usando o dataset público **Brazilian E-Commerce by Olist**
(Kaggle).

O objetivo não é construir um pipeline de produção, e sim demonstrar de forma
didática:

1. Como aplicar o **SRP (Single Responsibility Principle)** desde o início,
   separando claramente extração, transformação e carga.
2. Como uma implementação inicial pode **violar o OCP (Open/Closed Principle)**
   mesmo respeitando o SRP.
3. Como refatorar essa implementação para respeitar o OCP, usando abstrações
   (classes abstratas / interfaces) que permitem estender o pipeline sem
   modificar código existente.

## OCP é o Open/Closed Principle - o "O" do SOLID. A ideia central:

> Uma entidade de software (classe, módulo, função) deve estar aberta para extensão, mas fechada para modificação.

Ou seja: quando você precisa adicionar um comportamento novo, você deve conseguir fazer isso criando código novo, sem precisar alterar o código que já existe e já está testado/funcionando.

Por que isso importa?
Toda vez que você modifica uma classe que já está em produção, você corre o risco de quebrar algo que já funcionava. O OCP existe pra reduzir esse risco: se o comportamento novo entra por extensão (uma classe nova implementando uma interface), o código antigo nunca é tocado, logo, nunca quebra.

## Sobre o dataset

**Brazilian E-Commerce Public Dataset by Olist**
Fonte: [kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Conjunto de ~9 arquivos CSV com dados reais (anonimizados) de pedidos de um
marketplace brasileiro entre 2016 e 2018: pedidos, itens, clientes, produtos,
pagamentos, avaliações, vendedores e geolocalização.

Principais arquivos:

| Arquivo | Descrição |
|---|---|
| `olist_orders_dataset.csv` | Pedidos e seus status/datas |
| `olist_order_items_dataset.csv` | Itens de cada pedido |
| `olist_customers_dataset.csv` | Clientes |
| `olist_products_dataset.csv` | Produtos |
| `olist_order_payments_dataset.csv` | Pagamentos |
| `olist_order_reviews_dataset.csv` | Avaliações |
| `olist_sellers_dataset.csv` | Vendedores |
| `olist_geolocation_dataset.csv` | Geolocalização por CEP |
| `product_category_name_translation.csv` | Tradução de categorias PT → EN |

> Os arquivos originais **não são versionados** neste repositório. Baixe-os do
> Kaggle e coloque em `data/raw/` (veja [Como rodar](#como-rodar)).🌻

## Arquitetura

Pipeline ETL organizado em camadas **Bronze → Silver → Gold** (medallion
architecture), com responsabilidades bem separadas:

```
olist-etl/
├── data/
│   ├── raw/              # CSVs originais do Kaggle (não versionado)
│   ├── bronze/           # dados brutos ingeridos, sem transformação
│   ├── silver/           # dados limpos e padronizados
│   └── gold/             # dados agregados, prontos para consumo/análise
├── notebooks/
│   └── 01_eda.ipynb      # análise exploratória inicial
├── src/
│   └── olist_etl/
│       ├── extractors/   # responsáveis por extrair dados de uma origem
│       ├── transformers/ # responsáveis por transformar dados (bronze/silver/gold)
│       ├── loaders/      # responsáveis por carregar dados em um destino
│       └── pipeline.py   # orquestra extract → transform → load
├── tests/
├── pyproject.toml
└── README.md
```

### SRP (Single Responsibility Principle)

Cada classe tem uma única responsabilidade:

A ser criado

### OCP (Open/Closed Principle)

A ser criado

## Como rodar

### 1. Pré-requisitos

- Python 3.11+
- [Kaggle API](https://github.com/Kaggle/kaggle-api) configurada (opcional,
  para baixar o dataset via linha de comando) ou download manual pelo site.

### 2. Instalar dependências

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

### 3. Baixar o dataset

Opção A - via Kaggle API:

```bash
kaggle datasets download -d olistbr/brazilian-ecommerce -p data/raw --unzip
```

Opção B — manual: baixe o `.zip` em
[kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
e extraia o conteúdo em `data/raw/`.

### 4. Rodar a EDA

```bash
jupyter notebook notebooks/01_eda.ipynb # Colocar nome
```

### 5. Rodar o pipeline ETL

```bash
python -m olist_etl.pipeline
```

## Testes

```bash
pytest tests/
```

## Roadmap de estudo

- [ ] Setup do projeto e organização em camadas bronze/silver/gold
- [ ] EDA inicial do dataset Olist
- [ ] Pipeline "antes OCP" (SRP aplicado, OCP violado)
- [ ] Pipeline "depois OCP" (abstrações e extensibilidade)
- [ ] Aplicação do Liskov Substitution Principle (LSP)
- [ ] Aplicação do Interface Segregation Principle (ISP)
- [ ] Aplicação do Dependency Inversion Principle (DIP)

## Licença dos dados

O dataset é disponibilizado pela Olist sob licença [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/),
para uso não comercial. Este projeto é de finalidade exclusivamente
educacional.
