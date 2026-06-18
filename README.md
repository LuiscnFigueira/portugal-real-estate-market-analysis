# Análise e Previsão Local de Preços de Imóveis em Portugal

## Descrição

Este projeto de Ciência de Dados tem como objetivo analisar anúncios imobiliários em Portugal e preparar uma base consistente para a previsão local de preços de imóveis. O trabalho segue a metodologia CRISP-DM e privilegia um fluxo reprodutível, documentado e executável localmente, sem recurso a APIs externas de inteligência artificial.

A fase atual corresponde à preparação e feature engineering do projeto: carregamento do dataset, normalização de variáveis, conversão de tipos, validação conservadora, criação de variáveis derivadas, geração de datasets processados e documentação das decisões necessárias para modelação futura.

## Objetivos

- Compreender a estrutura do mercado imobiliário português a partir de dados de anúncios.
- Identificar fatores potencialmente associados ao preço anunciado dos imóveis.
- Preparar dados coerentes para análise exploratória, preparação final e modelação.
- Evitar fuga de informação entre variáveis derivadas e variável alvo.
- Desenvolver, numa fase posterior, modelos locais de machine learning para estimar preços.

## Dataset

| Campo | Informação |
|---|---|
| Nome | Portugal Real Estate 2024 |
| Fonte | Kaggle |
| Ficheiro original | `data/raw/portugal_listinigs.csv` |
| Observações iniciais | 135 536 anúncios |
| Variáveis originais | 25 |
| Variável alvo | `price` |

O ficheiro em `data/raw/` é tratado como fonte original e não deve ser alterado. Dados preparados deverão ser guardados em `data/processed/`.

## Artefactos Atuais

| Artefacto | Estado |
|---|---|
| Dataset original | `data/raw/portugal_listinigs.csv` |
| Dataset processado inicial | `data/processed/portugal_listings_initial_clean.csv` |
| Dataset preparado | `data/processed/portugal_listings_prepared.csv.gz` |
| Dataset com features | `data/processed/portugal_listings_features.csv.gz` |
| Pipeline de preparação | `src/data/make_dataset.py` |
| Funções reutilizáveis | `src/data/preprocess.py`, `src/data/prepare.py`, `src/features/build_features.py` |
| Notebooks organizados | `notebooks/01_inicializacao.ipynb`, `notebooks/02_data_understanding.ipynb`, `notebooks/03_data_preparation.ipynb`, `notebooks/04_feature_engineering.ipynb` |
| Testes | `tests/test_preprocess.py` |

## Metodologia

O projeto segue a metodologia CRISP-DM:

1. Compreensão do negócio
2. Compreensão dos dados
3. Preparação dos dados
4. Modelação
5. Avaliação
6. Apresentação e utilização local dos resultados

Até à fase 04, o foco está na compreensão dos dados, preparação estruturada e criação de features. Ainda não existem resultados de modelação a reportar.

## Estrutura do Projeto

| Pasta/Ficheiro | Finalidade |
|---|---|
| `data/raw/` | Dados originais, sem alterações manuais |
| `data/processed/` | Dados tratados e versões intermédias |
| `docs/` | Documentação técnica do projeto |
| `notebooks/` | Notebooks por fase de trabalho |
| `reports/figures/` | Gráficos e outputs visuais |
| `src/` | Código reutilizável, a estruturar nas próximas fases |
| `tests/` | Testes simples para funções reutilizáveis |
| `requirements.txt` | Dependências do ambiente |

## Execução Local

Instalar dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Gerar o dataset processado inicial:

```bash
python3 -m src.data.make_dataset
```

Executar testes:

```bash
python3 -m pytest tests
```

## Notebooks

| Notebook | Finalidade |
|---|---|
| `notebooks/01_inicializacao.ipynb` | Inicialização, preparação inicial e geração do dataset processado |
| `notebooks/02_data_understanding.ipynb` | Compreensão dos dados, qualidade, descritivas e agregações iniciais |
| `notebooks/03_data_preparation.ipynb` | Preparação estruturada, missing indicators e flags de outliers |
| `notebooks/04_feature_engineering.ipynb` | Criação de features candidatas e política de leakage |
| `notebooks/archive/inicializacao_legacy.ipynb` | Notebook original arquivado como referência da primeira exploração |

## Documentação

- `docs/01_project_overview.md` - visão geral do projeto
- `docs/02_business_understanding.md` - problema, objetivos e critérios de sucesso
- `docs/03_data_understanding.md` - compreensão dos dados
- `docs/04_data_dictionary.md` - dicionário de variáveis
- `docs/05_data_quality.md` - qualidade dos dados
- `docs/06_data_preparation.md` - preparação inicial dos dados
- `docs/07_feature_engineering.md` - variáveis derivadas e risco de fuga de informação
- `docs/08_next_steps.md` - plano de trabalho recomendado
- `docs/09_statistical_validation.md` - validação estatística e cuidados de interpretação
- `docs/10_reproducibility.md` - instruções de reprodutibilidade
- `docs/11_processed_data_audit.md` - auditoria do dataset processado

## Estado Atual

O projeto já contém notebooks executados até à fase de feature engineering, datasets processados comprimidos para GitHub/Kaggle, código reutilizável em `src/` e testes automatizados. O próximo passo recomendado é validação estatística e baseline de machine learning com pipelines locais.

## Autor

Luís Figueira

Última atualização: 18/06/2026
