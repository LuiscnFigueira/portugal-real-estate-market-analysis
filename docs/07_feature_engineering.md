# Feature Engineering

## Objetivo

Criar variáveis derivadas que possam apoiar a análise avançada e a futura modelação do preço anunciado dos imóveis, mantendo uma separação clara entre variáveis candidatas e variáveis com risco de fuga de informação.

Esta fase é implementada no notebook `notebooks/04_feature_engineering.ipynb` e no módulo reutilizável `src/features/build_features.py`.

## Fonte de Dados

| Elemento | Valor |
|---|---|
| Dataset de entrada | `data/processed/portugal_listings_prepared.csv.gz` |
| Dataset de saída | `data/processed/portugal_listings_features.csv` |
| Dataset de saída comprimido | `data/processed/portugal_listings_features.csv.gz` |
| Observações | 126 242 |
| Variáveis antes da fase 04 | 49 |
| Variáveis após a fase 04 | 71 |
| Features novas | 22 |

O ficheiro comprimido `.csv.gz` é o recomendado para upload no GitHub, porque o CSV sem compressão ultrapassa o limite prático do upload pelo browser.

## Features Criadas

| Grupo | Variáveis | Objetivo |
|---|---|---|
| Target transformado | `log_price` | Apoiar modelação futura com alvo menos assimétrico |
| Áreas em escala log | `log_total_area`, `log_living_area`, `log_gross_area`, `log_lot_size`, `log_built_area` | Reduzir impacto de assimetria e valores extremos |
| Rácios de área | `living_total_area_ratio`, `gross_total_area_ratio`, `built_total_area_ratio` | Comparar composição física do imóvel |
| Rácios de divisões | `bedrooms_per_room`, `bathrooms_per_bedroom`, `rooms_per_bathroom` | Representar organização interna do imóvel |
| Amenidades | `amenity_count`, `has_parking_or_garage` | Agregar sinais de estacionamento, garagem, elevador e carregamento elétrico |
| Missingness | `missing_core_feature_count` | Quantificar ausência de informação relevante |
| Idade | `construction_decade`, `property_age_group` | Capturar antiguidade de forma interpretável |
| Temporal | `publish_quarter`, `publish_month_sin`, `publish_month_cos` | Representar mês/trimestre de publicação |
| Localização combinada | `district_type`, `city_type` | Capturar interação entre localização e tipologia |

## Política de Leakage

As seguintes variáveis não devem ser usadas como preditores diretos num modelo cujo objetivo seja prever `price`:

| Variável | Motivo |
|---|---|
| `price` | Variável alvo |
| `log_price` | Transformação da variável alvo |
| `price_m2` | Calculada diretamente com `price` |
| `price_iqr_outlier` | Flag calculada a partir da distribuição de `price` |
| `price_m2_iqr_outlier` | Deriva de uma variável que usa `price` |

Além disso, as flags `*_iqr_outlier` devem ser tratadas com cautela, porque foram calculadas antes da separação treino/teste. Para modelação final, a deteção de outliers deve acontecer dentro de uma pipeline ajustada apenas no conjunto de treino.

## Variáveis Candidatas Para Modelação

A função `modeling_feature_columns()` devolve uma lista inicial de variáveis candidatas, excluindo alvo e leakage óbvio. Esta lista ainda não substitui uma pipeline de machine learning: antes do treino será necessário aplicar imputação, encoding, transformação de escala e separação treino/teste.

## Decisões Pendentes

- Definir estratégia de imputação por tipo de variável.
- Agregar categorias raras em variáveis de alta cardinalidade, como `city`, `town`, `city_type` e `district_type`.
- Escolher encoding adequado para variáveis categóricas.
- Decidir se `log_price` será usado como alvo transformado na modelação.
- Garantir que qualquer transformação estatística é ajustada apenas no conjunto de treino.

## Conclusão

A fase 04 cria uma base mais rica para modelação, mas ainda não treina modelos. O próximo passo deve ser a validação estatística e/ou criação de um baseline de machine learning com pipelines que controlem imputação, encoding, separação treino/teste e prevenção de leakage.
