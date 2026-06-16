# Reprodutibilidade

## Objetivo

Este documento explica como executar o projeto noutro computador de forma consistente, preservando os dados originais e gerando os artefactos processados por código.

## Requisitos

- Python 3.9 ou superior.
- Dependências listadas em `requirements.txt`.
- Ficheiro original em `data/raw/portugal_listinigs.csv`.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Gerar Dataset Processado

```bash
python3 -m src.data.make_dataset
```

Este comando lê o ficheiro original em `data/raw/`, aplica a preparação inicial e guarda:

```text
data/processed/portugal_listings_initial_clean.csv
```

## Executar Testes

```bash
python3 -m pytest tests
```

## Executar Notebooks Por Linha de Comando

Depois de instalar as dependências, os notebooks numerados podem ser executados com:

```bash
python3 -m jupyter nbconvert --execute --inplace notebooks/01_inicializacao.ipynb
python3 -m jupyter nbconvert --execute --inplace notebooks/02_data_understanding.ipynb
```

## Executar Notebooks

A ordem recomendada é:

1. `notebooks/01_inicializacao.ipynb`
2. `notebooks/02_data_understanding.ipynb`

O notebook `notebooks/archive/inicializacao_legacy.ipynb` foi mantido como referência da primeira exploração, mas os notebooks numerados devem ser usados como fluxo principal.

## Validações Esperadas

Depois de gerar o dataset processado inicial, devem verificar-se os seguintes resultados:

| Validação | Resultado esperado |
|---|---:|
| Linhas no dataset original | 135 536 |
| Colunas no dataset original | 25 |
| Linhas no dataset processado | 126 242 |
| Colunas no dataset processado | 29 |
| Valores em falta em `price` no processado | 0 |
| Duplicados exatos no processado | 0 |
| Valores infinitos em `price_m2` | 0 |
| Valores não positivos em `total_area` | 0 |

## Cuidados

- Não editar manualmente ficheiros em `data/raw/`.
- Regenerar dados processados sempre a partir do código em `src/`.
- Usar caminhos relativos nos notebooks e scripts.
- Não usar `price_m2` como variável explicativa em modelos que preveem `price`.
