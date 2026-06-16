# 03 - Compreensão Inicial dos Dados

## Objetivo

Este documento resume a primeira leitura do dataset usado no projeto de análise e previsão local de preços de imóveis em Portugal. O foco desta fase é compreender a estrutura dos dados, identificar as variáveis disponíveis e registar observações iniciais suportadas pelos dados.

## Fonte dos Dados

O ficheiro analisado encontra-se em:

```text
data/raw/portugal_listinigs.csv
```

O ficheiro foi tratado como fonte original. Nesta fase não foram feitas alterações ao ficheiro em `data/raw/`.

## Dimensão do Dataset

| Medida | Valor |
|---|---:|
| Linhas | 135 536 |
| Colunas | 25 |
| Unidade de observação | Anúncio imobiliário |

## Colunas originais

As colunas existentes no ficheiro original são:

```text
Price
District
City
Town
Type
EnergyCertificate
GrossArea
TotalArea
Parking
HasParking
Floor
ConstructionYear
EnergyEfficiencyLevel
PublishDate
Garage
Elevator
ElectricCarsCharging
TotalRooms
NumberOfBedrooms
NumberOfWC
ConservationStatus
LivingArea
LotSize
BuiltArea
NumberOfBathrooms
```

## Variável Alvo

A variável alvo prevista para a modelação é `Price`, que representa o preço anunciado do imóvel. O dataset contém 300 registos sem valor em `Price`, correspondendo a 0,22% das linhas.

Resumo inicial de `Price`:

| Estatística | Valor |
|---|---:|
| Registos não nulos | 135 236 |
| Mínimo | 1 |
| Percentil 25 | 84 000 |
| Mediana | 210 000 |
| Percentil 75 | 395 000 |
| Percentil 95 | 1 175 000 |
| Percentil 99 | 2 745 000 |
| Máximo | 1 380 000 000 |

O valor máximo é muito superior ao percentil 99 e deve ser analisado como potencial outlier ou caso especial antes da modelação.

## Grupos de Variáveis

As variáveis podem ser organizadas nos seguintes grupos:

| Grupo | Colunas |
|---|---|
| Localização | `District`, `City`, `Town` |
| Características do imóvel | `Type`, `GrossArea`, `TotalArea`, `LivingArea`, `LotSize`, `BuiltArea`, `Floor`, `ConstructionYear`, `ConservationStatus` |
| Preço | `Price` |
| Energia | `EnergyCertificate`, `EnergyEfficiencyLevel` |
| Estacionamento e equipamentos | `Parking`, `HasParking`, `Garage`, `Elevator`, `ElectricCarsCharging` |
| Divisões | `TotalRooms`, `NumberOfBedrooms`, `NumberOfWC`, `NumberOfBathrooms` |
| Publicação | `PublishDate` |

## Cobertura Geográfica Inicial

Existem 27 valores distintos em `District`, 275 em `City` e 2 263 em `Town`.

Os distritos com mais anúncios são:

| Distrito | Anuncios |
|---|---:|
| Lisboa | 31 351 |
| Porto | 22 681 |
| Setúbal | 11 579 |
| Braga | 11 445 |
| Faro | 8 943 |

As cidades com mais anúncios são:

| Cidade | Anuncios |
|---|---:|
| Lisboa | 8 396 |
| Sintra | 5 527 |
| Porto | 5 446 |
| Vila Nova de Gaia | 4 281 |
| Cascais | 3 236 |

## Tipos de Imóvel

Existem 21 valores distintos em `Type`. Os tipos mais frequentes são:

| Tipo | Anuncios |
|---|---:|
| Apartment | 47 378 |
| House | 36 736 |
| Land | 31 843 |
| Store | 5 333 |
| Farm | 3 889 |

Esta diversidade sugere que a distribuição de preço e área pode variar bastante por tipo de imóvel. A análise exploratória deve comparar os principais indicadores por `Type` antes de definir regras de tratamento.

## Datas de Publicação

A coluna `PublishDate` tem elevada falta de preenchimento. Foram identificados:

| Indicador | Valor |
|---|---:|
| Datas válidas após conversão | 28 779 |
| Valores não nulos mas não convertidos como data | 460 |
| Valores em falta | 106 297 |
| Data válida mínima | 2018-04-09 |
| Data válida máxima | 2025-01-28 |

A maioria das datas válidas situa-se em 2024. Como a cobertura temporal é incompleta, `PublishDate` deve ser usada com cautela.

## Observações Iniciais

- O dataset tem dimensão suficiente para análise exploratória e modelação, mas contém problemas relevantes de qualidade.
- As colunas de localização (`District`, `City`, `Town`) estão completas ou quase completas e devem ser importantes para previsão local de preços.
- Variáveis de área e características físicas apresentam valores extremos e alguns valores inválidos.
- Existem 8 913 linhas duplicadas exatas, equivalentes a 6,58% do dataset.
- Algumas variáveis parecem ser opcionais ou dependentes do tipo de imóvel, como `Floor`, `LotSize`, `GrossArea` e `ConservationStatus`.
- A coluna `Price` tem poucos valores em falta, mas apresenta valores extremos que exigem análise antes de qualquer remoção.

## Próximos Pontos de Análise

- Confirmar se os duplicados exatos representam anúncios repetidos ou artefactos de recolha.
- Avaliar distribuições de preço por distrito, cidade e tipo de imóvel.
- Distinguir valores em falta estruturais de valores em falta por erro de recolha.
- Definir regras justificadas para valores inválidos, valores extremos e transformações.
