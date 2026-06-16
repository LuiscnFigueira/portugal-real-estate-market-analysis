# Dicionário de Dados

Este documento descreve as variáveis utilizadas após a renomeação das colunas para formato `snake_case`.

## Variável Alvo

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `price` | Numérica | Preço anunciado do imóvel em euros. |

## Localização

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `district` | Categórica | Distrito onde o imóvel se localiza. |
| `city` | Categórica | Cidade ou concelho associado ao imóvel. |
| `town` | Categórica | Freguesia, localidade ou zona do imóvel. |

## Características do Imóvel

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `type` | Categórica | Tipo de imóvel, como apartamento, moradia, quinta ou terreno. |
| `gross_area` | Numérica | Área bruta do imóvel, quando disponível. |
| `total_area` | Numérica | Área total do imóvel. |
| `living_area` | Numérica | Área habitável do imóvel. |
| `lot_size` | Numérica | Área do lote ou terreno. |
| `built_area` | Numérica | Área construída. |
| `floor` | Categórica | Piso do imóvel. |
| `construction_year` | Inteira | Ano de construção do imóvel. |
| `conservation_status` | Categórica | Estado de conservação do imóvel. |

## Energia

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `energy_certificate` | Categórica | Certificação energética declarada no anúncio. |
| `energy_efficiency_level` | Categórica | Nível de eficiência energética, quando disponível. |

## Estacionamento e Equipamentos

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `parking` | Inteira | Número ou indicador numérico associado a estacionamento. |
| `has_parking` | Booleana | Indica se o imóvel tem estacionamento. |
| `garage` | Booleana | Indica se o imóvel tem garagem. |
| `elevator` | Booleana | Indica se o imóvel tem elevador. |
| `electric_cars_charging` | Booleana | Indica se existe carregamento para carros elétricos. |

## Divisões

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `total_rooms` | Inteira | Número total de divisões/quartos indicado no anúncio. |
| `number_of_bedrooms` | Inteira | Número de quartos. |
| `number_of_wc` | Inteira | Número de WC. |
| `number_of_bathrooms` | Inteira | Número de casas de banho. |

## Publicação

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `publish_date` | Data | Data de publicação do anúncio. |

## Variáveis Derivadas

| Variável | Tipo esperado | Descrição |
|---|---|---|
| `price_m2` | Numérica | Preço por metro quadrado, calculado como `price / total_area`. |
| `property_age` | Numérica | Idade estimada do imóvel, calculada como `2026 - construction_year`. |
| `publish_year` | Inteira | Ano extraído de `publish_date`. |
| `publish_month` | Inteira | Mês extraído de `publish_date`. |

## Nota Sobre Data Leakage

A variável `price_m2` inclui diretamente a variável alvo `price`. Por isso, pode ser usada na análise exploratória, mas não deve ser usada como variável explicativa num modelo cujo objetivo seja prever `price`.

