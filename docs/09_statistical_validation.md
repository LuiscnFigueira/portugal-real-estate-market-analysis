# 09 - Validação Estatística

## Objetivo

Validar estatisticamente o dataset com features antes da modelação, avaliando a distribuição da variável alvo, associações numéricas, diferenças entre grupos e multicolinearidade.

Esta fase é implementada no notebook `notebooks/05_statistical_validation.ipynb` e no módulo reutilizável `src/analysis/statistical_validation.py`.

## Base Validada

| Indicador | Valor |
|---|---:|
| Dataset | `data/processed/portugal_listings_features.csv.gz` |
| Linhas | 126 242 |
| Colunas | 71 |
| Variável alvo | `price` |
| Alvo transformado | `log_price` |
| Valores em falta em `price` | 0 |
| Valores em falta em `log_price` | 0 |

A validação foi feita sobre a versão com features criada na fase 04. Os resultados devem ser lidos como suporte à modelação, não como prova causal sobre o mercado imobiliário.

## Distribuição de `price`

| Estatística | Valor |
|---|---:|
| Média | 370 785,56 |
| Desvio-padrão | 3 935 295 |
| Mínimo | 1 |
| Percentil 1 | 5 999,41 |
| Percentil 5 | 20 000 |
| Percentil 25 | 85 000 |
| Mediana | 210 000 |
| Percentil 75 | 390 000 |
| Percentil 90 | 750 000 |
| Percentil 95 | 1 198 947 |
| Percentil 99 | 2 750 000 |
| Máximo | 1 380 000 000 |
| Assimetria | 341,37 |
| Curtose | 119 660,5 |

A distribuição de `price` continua extremamente assimétrica à direita. A média é bastante superior à mediana e o máximo continua a dominar estatísticas sensíveis a valores extremos.

Recomendação:

- comunicar resultados com mediana, quartis e percentis;
- usar `log_price` como candidato forte para alvo transformado na modelação;
- não remover outliers automaticamente sem análise por contexto.

## Associações Numéricas com `log_price`

As correlações foram calculadas com Pearson e Spearman. A ordenação abaixo usa Spearman, por ser mais adequada a relações monotónicas e menos sensível a extremos.

| Variável | Pares válidos | Pearson | Spearman |
|---|---:|---:|---:|
| `number_of_bathrooms` | 119 743 | 0,504 | 0,594 |
| `amenity_count` | 126 242 | 0,387 | 0,446 |
| `number_of_bedrooms` | 43 656 | 0,424 | 0,435 |
| `total_rooms` | 68 605 | 0,085 | 0,430 |
| `bathrooms_per_bedroom` | 39 320 | 0,184 | 0,419 |
| `parking` | 126 096 | 0,322 | 0,377 |
| `construction_year` | 83 118 | 0,314 | 0,370 |
| `property_age` | 83 118 | -0,314 | -0,370 |
| `construction_decade` | 83 118 | 0,314 | 0,364 |
| `rooms_per_bathroom` | 59 085 | -0,206 | -0,297 |
| `missing_core_feature_count` | 126 242 | -0,279 | -0,282 |
| `bedrooms_per_room` | 20 512 | 0,237 | 0,275 |

Interpretação:

- casas de banho, quartos, divisões, estacionamento e amenidades apresentam associação positiva com `log_price`;
- imóveis mais recentes tendem a apresentar preços anunciados superiores, enquanto `property_age` tem associação negativa;
- maior falta de informação em variáveis centrais está associada a preços mais baixos, o que pode indicar segmentos menos completos ou anúncios de menor qualidade;
- estas associações não devem ser interpretadas como efeitos causais.

## Diferenças Entre Grupos

Foi usado o teste de Kruskal-Wallis sobre `log_price`, com grupos de dimensão mínima adequada. Os valores-p são muito pequenos devido ao tamanho da amostra, por isso a interpretação deve privilegiar `epsilon_squared`.

| Variável categórica | Grupos | N | Epsilon squared | Interpretação |
|---|---:|---:|---:|---|
| `type` | 14 | 125 528 | 0,257 | Diferenças relevantes por tipologia |
| `energy_certificate` | 10 | 126 170 | 0,224 | Diferenças relevantes por certificação energética |
| `district` | 17 | 125 755 | 0,198 | Diferenças relevantes por distrito |
| `property_age_group` | 5 | 83 118 | 0,138 | Diferenças moderadas por grupo de idade |

Conclusão:

- `type`, `district` e `energy_certificate` devem ser considerados variáveis importantes para modelação;
- a codificação destas categorias deve ser feita dentro da pipeline de treino;
- categorias raras devem ser agregadas ou tratadas antes de modelos sensíveis a alta cardinalidade.

## Multicolinearidade

Foi calculado VIF para variáveis numéricas candidatas. Nos campos avaliados, os maiores valores ficaram abaixo de 2,5:

| Variável | VIF |
|---|---:|
| `number_of_bathrooms` | 2,23 |
| `log_living_area` | 1,95 |
| `log_total_area` | 1,79 |
| `living_area` | 1,76 |
| `total_rooms` | 1,70 |
| `missing_core_feature_count` | 1,55 |
| `number_of_bedrooms` | 1,52 |
| `rooms_per_bathroom` | 1,50 |

Não há sinal forte de multicolinearidade problemática neste conjunto reduzido de variáveis. Ainda assim, áreas originais, áreas logarítmicas e rácios devem ser usados com cuidado em modelos lineares, porque podem representar informação parcialmente redundante.

## Artefactos Gerados

| Artefacto | Caminho |
|---|---|
| Distribuição de `price` e `log_price` | `reports/figures/05_price_distribution.png` |
| Top correlações Spearman | `reports/figures/05_top_spearman_correlations.png` |
| Correlação Spearman | `reports/figures/05_spearman_correlation_heatmap.png` |
| `log_price` por tipo de imóvel | `reports/figures/05_log_price_by_type.png` |
| Resumo de preço | `reports/statistical_outputs/05_price_summary.csv` |
| Correlações numéricas | `reports/statistical_outputs/05_numeric_correlations.csv` |
| Testes categóricos | `reports/statistical_outputs/05_categorical_tests.csv` |
| VIF | `reports/statistical_outputs/05_vif_summary.csv` |

## Recomendações Para Modelação

Antes de treinar modelos, recomenda-se:

1. Usar `log_price` como alvo candidato e comparar com modelação direta de `price`.
2. Excluir `price_m2`, `price_iqr_outlier` e `price_m2_iqr_outlier` como preditores diretos.
3. Fazer imputação, encoding e scaling dentro de pipelines ajustadas apenas no conjunto de treino.
4. Tratar categorias raras em `city`, `town`, `district_type` e `city_type`.
5. Usar validação com métricas interpretáveis, como MAE e RMSE em euros.
6. Comparar um baseline simples antes de modelos mais complexos.
7. Manter linguagem não causal nas conclusões.

## Conclusão

A validação estatística confirma que existe sinal útil nas variáveis físicas, amenidades, localização, tipologia, certificação energética e idade do imóvel. Também confirma que `price` é altamente assimétrico e que a modelação deve considerar `log_price`.

O próximo passo recomendado é criar `06_modeling_baseline.ipynb`, com separação treino/teste e pipelines locais de imputação, encoding e treino de modelos baseline.
