# Auditoria ao Dataset Processado

## Objetivo

Auditar o ficheiro `data/processed/portugal_listings_initial_clean.csv` e compará-lo com `data/raw/portugal_listinigs.csv`, sem alterar os dados originais em `data/raw/`.

A auditoria incide sobre dimensões, duplicados, valores em falta, validade de `price`, validade de `total_area`, consistência de `price_m2`, valores extremos e riscos remanescentes.

## Ficheiros Auditados

| Ficheiro | Papel | Observação |
|---|---|---|
| `data/raw/portugal_listinigs.csv` | Dados originais | Usado apenas para leitura e comparação |
| `data/processed/portugal_listings_initial_clean.csv` | Dataset processado inicial | Dataset auditado |

## Comparação Geral

| Indicador | Raw | Processado | Diferença |
|---|---:|---:|---:|
| Linhas | 135 536 | 126 242 | -9 294 |
| Colunas | 25 | 29 | +4 |
| Duplicados exatos | 8 913 | 0 | -8 913 |
| Valores em falta em `price` | 300 | 0 | -300 |
| Valores não positivos em `total_area` | 933 | 0 | -933 |

O dataset processado tem menos 9 294 linhas do que o ficheiro original. Ao recomputar as etapas da preparação em memória, a diferença é explicada por 9 011 linhas duplicadas após normalização/preparação e 283 linhas sem `price` após a remoção desses duplicados.

O número de duplicados exatos no ficheiro raw é 8 913. Após renomeação, conversão de tipos, marcação de alguns valores inválidos e criação de variáveis derivadas, foram encontrados 9 011 duplicados antes da limpeza final. Esta diferença é compatível com transformações que tornam registos anteriormente distintos em linhas equivalentes na versão preparada.

## Colunas

O ficheiro raw contém 25 colunas originais. O ficheiro processado contém as mesmas variáveis em formato `snake_case` e acrescenta 4 variáveis derivadas:

| Variável derivada | Descrição |
|---|---|
| `price_m2` | Preço por metro quadrado, calculado a partir de `price` e `total_area` |
| `property_age` | Idade estimada do imóvel |
| `publish_year` | Ano extraído de `publish_date` |
| `publish_month` | Mês extraído de `publish_date` |

## Duplicados

| Verificação | Raw | Processado |
|---|---:|---:|
| Duplicados exatos | 8 913 | 0 |
| Percentagem de duplicados exatos | 6,58% | 0,00% |

Não foram encontrados duplicados exatos no dataset processado. A remoção de duplicados está alinhada com o objetivo de evitar contagens repetidas de anúncios idênticos na versão tratada.

## Variável Alvo: `price`

| Verificação | Raw | Processado |
|---|---:|---:|
| Valores em falta | 300 | 0 |
| Percentagem de valores em falta | 0,22% | 0,00% |
| Valores `<= 0` | 0 | 0 |
| Mínimo no processado | n/a | 1 |
| Percentil 99 no processado | n/a | 2 750 000 |
| Máximo no processado | n/a | 1 380 000 000 |

O dataset processado não contém valores nulos nem não positivos em `price`. Contudo, o máximo observado no processado é muito elevado face ao percentil 99, pelo que continua a existir risco de valores extremos relevantes na variável alvo.

## Área Total: `total_area`

| Verificação | Raw | Processado |
|---|---:|---:|
| Valores em falta | 8 383 | 8 671 |
| Percentagem de valores em falta | 6,19% | 6,87% |
| Valores `<= 0` | 933 | 0 |
| Mínimo válido no processado | n/a | 1 |
| Percentil 99 no processado | n/a | 51 520 |
| Máximo no processado | n/a | 61 420 071 105 |

Os valores não positivos de `total_area` foram removidos ou marcados como ausentes no dataset processado. O aumento de valores em falta face ao raw é esperado, porque áreas inválidas passam a não estar disponíveis para cálculo e análise.

Apesar disso, existem valores extremos muito elevados em `total_area`, incluindo um máximo de 61 420 071 105. Estes valores podem representar erros de unidade, erros de recolha ou casos muito específicos e devem ser avaliados antes de modelação.

## Preço por Metro Quadrado: `price_m2`

| Verificação | Valor no processado |
|---|---:|
| Valores em falta | 8 671 |
| Percentagem de valores em falta | 6,87% |
| Valores infinitos | 0 |
| Valores não finitos | 8 671 |
| Valores finitos `<= 0` | 0 |
| Valores finitos válidos | 117 571 |
| Mínimo finito | 0,000001 |
| Percentil 1 | 1,27 |
| Percentil 5 | 8,06 |
| Mediana | 1 474,29 |
| Percentil 95 | 6 134,45 |
| Percentil 99 | 9 876,77 |
| Percentil 99,9 | 24 413,55 |
| Máximo finito | 5 000 000 |

`price_m2` não contém valores infinitos nem valores não positivos finitos. Os valores em falta coincidem com os valores em falta de `total_area`, o que é consistente com o cálculo `price / total_area`.

Foram observados extremos inferiores e superiores. Exemplos de padrões detectados:

| Critério | Registos | Percentagem dos valores finitos |
|---|---:|---:|
| `price_m2 < 10` | 6 645 | 5,65% |
| `price_m2 < 50` | 15 205 | 12,93% |
| `price_m2 < 100` | 20 370 | 17,33% |
| `price_m2 > 50 000` | 53 | 0,05% |
| `price_m2 > 100 000` | 36 | 0,03% |
| `price_m2 > 500 000` | 12 | 0,01% |
| `price_m2 > 1 000 000` | 7 | 0,01% |

Pelo critério de Tukey aplicado a `price_m2`, com limite superior de 6 911,11, existem 4 226 valores acima desse limite, correspondendo a 3,59% dos valores finitos. Este critério deve ser usado apenas como sinalizador estatístico, não como regra automática de remoção.

Os extremos superiores estão associados, em vários casos, a áreas totais de 1 ou 2 metros quadrados ou a preços muito elevados. Os extremos inferiores estão associados, em vários casos, a áreas totais muito elevadas. Estes padrões sugerem risco de erros de área, unidades inconsistentes ou anúncios com características fora do padrão.

## Valores em Falta no Dataset Processado

| Coluna | Valores em falta | Percentagem |
|---|---:|---:|
| `conservation_status` | 108 263 | 85,76% |
| `built_area` | 101 711 | 80,57% |
| `gross_area` | 100 574 | 79,67% |
| `floor` | 100 224 | 79,39% |
| `publish_date` | 98 770 | 78,24% |
| `publish_year` | 98 770 | 78,24% |
| `publish_month` | 98 770 | 78,24% |
| `lot_size` | 90 113 | 71,38% |
| `number_of_bedrooms` | 82 586 | 65,42% |
| `number_of_wc` | 73 208 | 57,99% |
| `energy_efficiency_level` | 63 776 | 50,52% |
| `garage` | 63 776 | 50,52% |
| `electric_cars_charging` | 63 776 | 50,52% |
| `has_parking` | 62 496 | 49,50% |
| `total_rooms` | 57 637 | 45,66% |
| `construction_year` | 43 124 | 34,16% |
| `property_age` | 43 124 | 34,16% |
| `living_area` | 28 816 | 22,83% |
| `total_area` | 8 671 | 6,87% |
| `price_m2` | 8 671 | 6,87% |
| `number_of_bathrooms` | 6 499 | 5,15% |
| `parking` | 146 | 0,12% |
| `elevator` | 30 | 0,02% |
| `type` | 15 | 0,01% |
| `energy_certificate` | 13 | 0,01% |
| `town` | 2 | 0,00% |

As maiores taxas de valores em falta mantêm-se em variáveis estruturais ou descritivas, como `conservation_status`, áreas auxiliares, `floor`, data de publicação, `lot_size` e divisões. Estas colunas exigem uma estratégia explícita antes de análise estatística avançada ou modelação.

## Outras Validações Relevantes no Processado

Embora o pedido principal incida sobre `total_area`, foram também validadas áreas auxiliares e contagens sanitárias:

| Coluna | Valores em falta | Valores `<= 0` | Valores `< 0` |
|---|---:|---:|---:|
| `gross_area` | 100 574 | 0 | 0 |
| `living_area` | 28 816 | 0 | 0 |
| `lot_size` | 90 113 | 0 | 0 |
| `built_area` | 101 711 | 0 | 0 |
| `number_of_wc` | 73 208 | n/a | 0 |
| `number_of_bathrooms` | 6 499 | n/a | 0 |

Estes valores indicam que a limpeza aplicada ao dataset processado resolveu valores não positivos nas áreas auditadas e valores negativos nas contagens sanitárias principais.

## Riscos Remanescentes

- `price` não tem nulos nem valores não positivos, mas mantém valores extremos, incluindo um máximo de 1 380 000 000.
- `total_area` não tem valores não positivos, mas mantém máximos extremamente elevados, que afetam diretamente `price_m2`.
- `price_m2` não tem infinitos, mas apresenta extremos inferiores e superiores incompatíveis com uma interpretação direta sem validação adicional.
- Variáveis com percentagens muito elevadas de valores em falta podem ter utilidade limitada ou exigir imputação por tipo de imóvel, localização ou outro critério de domínio.
- `price_m2` deriva diretamente de `price`; por isso, pode ser útil para análise exploratória, mas representa risco de fuga de informação se for usado como variável explicativa em modelos para prever `price`.
- A ausência de uma chave única de anúncio limita a distinção entre duplicados reais, republicações e anúncios semelhantes.
- A remoção global de duplicados exatos pode ser adequada para análise inicial, mas deve continuar documentada para garantir reprodutibilidade.

## Conclusão

O dataset processado melhora a qualidade face ao raw nos pontos principais auditados: remove duplicados exatos, elimina linhas sem `price`, não contém áreas auditadas não positivas, remove contagens sanitárias negativas e não gera valores infinitos em `price_m2`.

Ainda assim, o ficheiro processado não deve ser considerado pronto para modelação final sem tratamento adicional de valores extremos, análise de valores em falta e exclusão controlada de variáveis derivadas da variável alvo quando houver risco de fuga de informação.
