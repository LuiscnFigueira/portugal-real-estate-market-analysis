# Feature Engineering

## Objetivo

Criar variáveis derivadas que facilitem a análise exploratória e ajudem a preparar a futura modelação. Nesta fase, as variáveis criadas têm sobretudo valor analítico; a sua utilização em modelos deve ser decidida com cuidado para evitar fuga de informação.

## Variáveis Derivadas

| Variável | Fórmula curta | Utilização prevista |
|---|---|---|
| `price_m2` | `price / total_area` | Comparar valores entre imóveis com áreas diferentes |
| `property_age` | `2026 - construction_year` | Estimar idade do imóvel |
| `publish_year` | Ano de `publish_date` | Analisar distribuição temporal por ano |
| `publish_month` | Mês de `publish_date` | Analisar sazonalidade ou concentração mensal |

## Preço por Metro Quadrado

A variável `price_m2` permite comparar anúncios com áreas diferentes e pode ser útil para:

- Comparar preços médios por metro quadrado entre distritos.
- Identificar zonas com valores anunciados mais elevados.
- Detetar anúncios com preços ou áreas potencialmente anómalos.

Como `price_m2` é calculado diretamente a partir de `price`, não deve ser usada como variável explicativa num modelo cujo objetivo seja prever `price`.

## Idade do Imóvel

A variável `property_age` estima a idade do imóvel com base no ano de construção. Valores negativos foram considerados impossíveis e marcados como valores em falta.

Esta variável pode ajudar a observar diferenças entre imóveis recentes e antigos, mas deve ser interpretada com cautela quando `construction_year` estiver ausente ou tiver qualidade incerta.

## Variáveis Temporais

As variáveis `publish_year` e `publish_month` derivam de `publish_date`. Podem apoiar a análise temporal dos anúncios, desde que a cobertura e fiabilidade da data de publicação sejam suficientes.

## Decisões Para Modelação

| Variável | Pode entrar no modelo de previsão de `price`? | Justificação |
|---|---|---|
| `price_m2` | Não | É calculada com a variável alvo e causaria fuga de informação |
| `property_age` | Sim, após validação | Deriva de `construction_year`, não de `price` |
| `publish_year` | A avaliar | Pode capturar efeito temporal, mas depende da qualidade da data |
| `publish_month` | A avaliar | Pode captar sazonalidade, mas pode ter baixo poder explicativo |

## Próximas Melhorias Possíveis

- Criar agrupamentos geográficos apenas se forem úteis e bem documentados.
- Avaliar rácios de área quando as colunas forem suficientemente completas.
- Normalizar categorias raras antes do encoding.
- Separar claramente variáveis usadas para análise exploratória e variáveis permitidas no treino.

## Nota Sobre Leakage

Qualquer variável que use diretamente `price` ou informação posterior ao momento da previsão deve ser excluída dos inputs de modelação. Esta regra é essencial para que as métricas futuras representem desempenho realista.
