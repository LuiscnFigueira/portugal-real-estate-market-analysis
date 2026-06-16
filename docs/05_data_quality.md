# 05 - Qualidade dos Dados

## Objetivo

Este documento regista o diagnóstico inicial de qualidade do ficheiro `data/raw/portugal_listinigs.csv`. A análise cobre valores em falta, duplicados, tipos de dados, valores inválidos e valores extremos. Nesta fase foram calculados indicadores, mas não foram aplicadas transformações ao ficheiro original.

## Resumo Geral

| Indicador | Valor |
|---|---:|
| Linhas | 135 536 |
| Colunas | 25 |
| Duplicados exatos | 8 913 |
| Percentagem de duplicados exatos | 6,58% |
| Valores em falta em `Price` | 300 |
| Percentagem de valores em falta em `Price` | 0,22% |

## Tipos de Dados

Na leitura inicial, as colunas numéricas principais foram interpretadas como `float64`, incluindo `Price`, áreas, ano de construção e contagens de divisões. As restantes colunas foram lidas como texto ou valores booleanos mistos.

Foi observado um aviso de tipos mistos em algumas colunas durante a leitura com `pandas`. Isto sugere que algumas variáveis podem conter combinações de texto, booleanos, números ou valores em falta. Antes da modelação, será necessário normalizar tipos de dados, especialmente em colunas como `HasParking`, `Floor`, `Garage`, `Elevator`, `ElectricCarsCharging` e `PublishDate`.

## Valores em Falta

As colunas com maior percentagem de valores em falta são:

| Coluna | Valores em falta | Percentagem |
|---|---:|---:|
| `ConservationStatus` | 116 244 | 85,77% |
| `BuiltArea` | 108 919 | 80,36% |
| `GrossArea` | 107 898 | 79,61% |
| `Floor` | 107 607 | 79,39% |
| `PublishDate` | 106 297 | 78,43% |
| `LotSize` | 95 953 | 70,80% |
| `NumberOfBedrooms` | 88 495 | 65,29% |
| `NumberOfWC` | 78 280 | 57,76% |
| `EnergyEfficiencyLevel` | 68 247 | 50,35% |
| `ElectricCarsCharging` | 68 247 | 50,35% |
| `Garage` | 68 247 | 50,35% |

Outras colunas relevantes:

| Coluna | Valores em falta | Percentagem |
|---|---:|---:|
| `HasParking` | 67 321 | 49,67% |
| `TotalRooms` | 62 292 | 45,96% |
| `ConstructionYear` | 47 515 | 35,06% |
| `LivingArea` | 30 584 | 22,57% |
| `TotalArea` | 8 383 | 6,19% |
| `NumberOfBathrooms` | 6 836 | 5,04% |
| `Price` | 300 | 0,22% |

Os valores em falta não devem ser tratados de forma uniforme. Por exemplo, a ausência de `LotSize` pode ser normal em apartamentos, enquanto a ausência de `Price` afeta diretamente a variável alvo.

## Duplicados

Foram identificadas 8 913 linhas duplicadas exatas, correspondendo a 6,58% do dataset.

Estes registos devem ser removidos ou sinalizados apenas numa versão processada dos dados, mantendo o ficheiro original em `data/raw/` intacto. A decisão deve ficar documentada no pipeline de preparação.

## Valores Inválidos ou Suspeitos

Foram identificados os seguintes casos objetivos:

| Regra analisada | Registos |
|---|---:|
| `Price <= 0` | 0 |
| `Price` em falta | 300 |
| `TotalArea <= 0` | 933 |
| `GrossArea <= 0` | 331 |
| `LivingArea <= 0` | 400 |
| `LotSize <= 0` | 626 |
| `BuiltArea <= 0` | 243 |
| `ConstructionYear < 1900` | 0 |
| `ConstructionYear > 2026` | 0 |
| `TotalRooms < 0` | 0 |
| `NumberOfBedrooms < 0` | 0 |
| `NumberOfWC < 0` | 1 |
| `NumberOfBathrooms < 0` | 3 |

Valores negativos em áreas, WC ou casas de banho não são coerentes com o domínio e devem ser tratados como inválidos numa fase posterior. Valores iguais a zero podem ser válidos em algumas contagens, mas são suspeitos em áreas físicas.

## Valores Extremos

Algumas variáveis apresentam máximos muito distantes dos percentis superiores:

| Coluna | Mediana | Percentil 99 | Máximo |
|---|---:|---:|---:|
| `Price` | 210 000 | 2 745 000 | 1 380 000 000 |
| `TotalArea` | 159 | 50 022,68 | 61 420 070 000 |
| `GrossArea` | 164 | 18 711,80 | 12 750 000 |
| `LivingArea` | 118 | 18 787,18 | 5 429 000 |
| `LotSize` | 679 | 129 590 | 992 301 000 |
| `BuiltArea` | 168 | 19 997,60 | 12 750 000 |
| `TotalRooms` | 3 | 12 | 2 751 |
| `NumberOfBathrooms` | 1 | 7 | 131 |

Estes valores podem representar erros, unidades inconsistentes ou propriedades muito específicas. A decisão de remover, limitar ou transformar valores extremos deve depender de análise por tipo de imóvel e localização.

## Datas

A coluna `PublishDate` apresenta problemas de completude e conversão:

| Indicador | Valor |
|---|---:|
| Valores em falta | 106 297 |
| Valores não nulos mas não convertidos como data | 460 |
| Datas válidas após conversão | 28 779 |
| Data válida mínima | 2018-04-09 |
| Data válida máxima | 2025-01-28 |

Antes de usar variáveis temporais, deve ser confirmada a consistência de `PublishDate` e a relevância temporal face ao objetivo do modelo.

## Riscos Para a Modelação

- Valores extremos em `Price` e áreas podem distorcer métricas, escalas e modelos sensíveis a valores extremos.
- A elevada falta de preenchimento em várias colunas pode reduzir o valor preditivo dessas variáveis ou exigir imputação cuidadosa.
- Duplicados exatos podem enviesar a distribuição se representarem repetição artificial de anúncios.
- Mistura de tipos de dados pode causar erros em pipelines de preparação e modelação.
- Alguns campos podem ter significado diferente por tipo de imóvel, especialmente terrenos, apartamentos, lojas, quintas e moradias.

## Decisões Recomendadas Para a Próxima Fase

- Preservar `data/raw/` sem alterações.
- Criar um dataset tratado em `data/processed/` apenas na fase de preparação.
- Remover ou sinalizar duplicados exatos com critério documentado.
- Converter nomes de colunas para `snake_case` apenas no dataset tratado ou no pipeline.
- Converter `PublishDate` para data e tratar valores não convertíveis como ausentes.
- Tratar valores negativos em áreas e contagens como inválidos.
- Analisar valores extremos por `Type`, `District` e `City` antes de aplicar limites globais.
- Evitar usar variáveis derivadas de `Price`, como preço por metro quadrado, como preditores diretos do próprio `Price`.

