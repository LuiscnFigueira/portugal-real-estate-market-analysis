# Próximos Passos

Este documento organiza as próximas etapas recomendadas após a fase inicial de documentação e preparação preliminar.

## Prioridades Imediatas

| Prioridade | Ação | Resultado esperado |
|---|---|---|
| 1 | Validar a versão processada inicial | Confirmar se serve de base para análise exploratória |
| 2 | Separar notebooks por fase CRISP-DM | Fluxo de trabalho mais claro |
| 3 | Expandir funções reutilizáveis em `src/` | Transformações reprodutíveis |
| 4 | Definir regras finais de limpeza | Dataset pronto para modelação |
| 5 | Criar baseline local | Referência mínima de desempenho |

## 1. Guardar Dataset Processado

Já existe uma primeira versão processada do dataset:

`data/processed/portugal_listings_initial_clean.csv`

Esta versão é gerada por código através de:

```bash
python3 -m src.data.make_dataset
```

O ficheiro original em `data/raw/` permanece intacto.

## 2. Organizar Notebooks por Fase

Estrutura recomendada:

| Notebook | Finalidade |
|---|---|
| `01_inicializacao.ipynb` | Carregamento, configuração e preparação inicial |
| `02_data_understanding.ipynb` | Compreensão dos dados e análise preliminar |
| `03_data_preparation.ipynb` | Limpeza, tratamento e dataset final |
| `04_modeling.ipynb` | Baselines e modelos de regressão |
| `05_evaluation.ipynb` | Avaliação, comparação e interpretação |

## 3. Criar Código Reutilizável

Mover transformações repetíveis para `src/`, mantendo os notebooks mais focados em análise e decisões. Estrutura sugerida:

| Caminho | Finalidade |
|---|---|
| `src/config.py` | Caminhos e parâmetros gerais |
| `src/data/preprocess.py` | Leitura, renomeação, tipos e limpeza |
| `src/features/build_features.py` | Criação de variáveis derivadas |
| `src/models/train_model.py` | Treino de modelos locais |
| `src/models/evaluate_model.py` | Métricas e avaliação |

## 4. Definir Tratamento Final de Dados

Antes da modelação, devem ficar documentadas as decisões sobre:

- Valores em falta por variável.
- Outliers a remover, transformar ou manter.
- Variáveis a excluir.
- Variáveis permitidas no treino.
- Estratégia de encoding.
- Separação entre treino, validação e teste.

## 5. Criar Baselines

Antes de modelos mais complexos, criar referências simples:

| Baseline | Utilidade |
|---|---|
| Mediana do preço | Define um desempenho mínimo |
| Regressão linear simples | Testa relação inicial com poucas variáveis |
| Regressão regularizada | Avalia melhoria com controlo de complexidade |

## 6. Preparar Modelação Local

Modelos candidatos para uma primeira iteração:

- Linear Regression
- Ridge Regression
- Random Forest Regressor
- Gradient Boosting Regressor

Métricas recomendadas:

| Métrica | Interpretação |
|---|---|
| MAE | Erro médio absoluto em euros |
| RMSE | Penaliza erros grandes com mais intensidade |
| R2 | Percentagem de variância explicada pelo modelo |

## 7. Preparar Outputs

Quando a análise exploratória estiver concluída, guardar gráficos relevantes em `reports/figures/` e referenciá-los na documentação. As conclusões devem ser escritas apenas quando estiverem suportadas por resultados verificados.
