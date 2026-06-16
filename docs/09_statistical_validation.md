# 09 - Validação Estatística

## Objetivo

Este documento valida a leitura estatística inicial do ficheiro `data/raw/portugal_listinigs.csv` e identifica cuidados necessários antes da análise inferencial, comparação entre grupos e modelação preditiva.

A validação foi feita diretamente sobre o ficheiro bruto, sem alterar `data/raw/`. Os resultados abaixo devem ser lidos como diagnóstico estatístico preliminar e não como conclusões causais sobre o mercado imobiliário.

## Base Validada

| Indicador | Valor |
|---|---:|
| Linhas | 135 536 |
| Colunas | 25 |
| Unidade de observação | Anúncio imobiliário |
| Duplicados exatos | 8 913 |
| Percentagem de duplicados exatos | 6,58% |
| Registos com `Price` preenchido | 135 236 |
| Registos sem `Price` | 300 |

As métricas documentadas em `03_data_understanding.md` e `05_data_quality.md` são coerentes com a validação direta do ficheiro bruto.

## Validação das Métricas Descritivas de `Price`

| Estatística | Valor |
|---|---:|
| Mínimo | 1 |
| Percentil 1 | 5 500 |
| Percentil 5 | 20 000 |
| Percentil 25 | 84 000 |
| Mediana | 210 000 |
| Média | 368 137,45 |
| Percentil 75 | 395 000 |
| Percentil 90 | 750 000 |
| Percentil 95 | 1 175 000 |
| Percentil 99 | 2 745 000 |
| Percentil 99,9 | 7 200 000 |
| Máximo | 1 380 000 000 |

A distribuição de `Price` é fortemente assimétrica à direita. A média é muito superior à mediana e o desvio-padrão é inflacionado por valores extremos. Para comunicação estatística e análise exploratória, a mediana, os quartis e percentis superiores são mais robustos do que a média.

O valor máximo de 1 380 000 000 euros não deve ser removido automaticamente apenas por ser extremo. Deve ser tratado como observação de alto risco estatístico: pode representar erro de recolha, erro de escala, anúncio excepcional ou registo não comparável com o resto da amostra.

## Efeito dos Duplicados nas Descritivas

| Base | Linhas | `Price` preenchido | Mediana | Média | P75 | P95 | P99 | Máximo |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Bruta | 135 536 | 135 236 | 210 000 | 368 137,45 | 395 000 | 1 175 000 | 2 745 000 | 1 380 000 000 |
| Sem duplicados exatos | 126 623 | 126 340 | 210 000 | 370 694,20 | 390 000 | 1 195 050 | 2 750 000 | 1 380 000 000 |

A remoção de duplicados exatos altera pouco a mediana e os percentis principais, mas deve ser aplicada no dataset processado para evitar repetição artificial de anúncios idênticos. Como o máximo se mantém, os valores extremos não são explicados apenas por duplicação.

## Interpretação de Outliers

Pela regra do intervalo interquartil aplicada a `Price`, o limite superior exploratório é 861 500 euros. Existem 10 589 registos acima desse limite, correspondendo a 7,81% do dataset bruto. Este critério é útil para sinalização, mas não deve ser usado como regra automática de remoção.

Em imobiliário, preços elevados podem ser legítimos quando associados a localizações premium, edifícios, hotéis, quintas, terrenos de grande dimensão ou propriedades comerciais. O tratamento de valores extremos deve ser contextual, pelo menos por `Type`, `District` e área disponível.

Exemplos de risco observados:

- `Price` máximo de 1 380 000 000 euros associado a uma moradia no distrito de Faro, muito acima do percentil 99,9.
- Registos de hotéis, edifícios e terrenos com preços entre 20 000 000 e 36 000 000 euros, que podem ser plausíveis mas não comparáveis com apartamentos ou moradias comuns.
- Áreas máximas extremamente elevadas, incluindo `TotalArea` de 61 420 070 000 e `LotSize` de 992 301 000, que sugerem possível erro de unidade, erro de digitação ou registos especiais.

Recomendação: criar indicadores de outlier e analisar os casos extremos antes de escolher entre exclusão, winsorization, transformação logarítmica ou modelos robustos.

## Valores em Falta

Os valores em falta não parecem ter o mesmo significado em todas as variáveis. Algumas ausências podem ser estruturais, por exemplo `LotSize` em apartamentos; outras podem refletir falhas de recolha ou anúncios incompletos.

| Variável | Valores em falta | Percentagem |
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
| `LivingArea` | 30 584 | 22,57% |
| `TotalArea` | 8 383 | 6,19% |
| `NumberOfBathrooms` | 6 836 | 5,04% |
| `Price` | 300 | 0,22% |

Antes da modelação, a imputação deve ser definida por tipo de variável e por contexto. Não é estatisticamente adequado aplicar uma imputação uniforme a todas as colunas.

Recomendações:

- Remover registos sem `Price` apenas na base de treino/análise, porque `Price` é a variável alvo.
- Criar indicadores de ausência de dados para variáveis com ausência potencialmente informativa.
- Avaliar ausência de dados por `Type`, `District` e `City` antes de imputar áreas, divisões ou datas.
- Evitar imputar variáveis com mais de 70% de ausência sem testar se acrescentam valor preditivo real.

## Valores Inválidos ou Suspeitos

Foram confirmados valores não positivos em variáveis de área:

| Variável | Registos não nulos | Valores `<= 0` | Percentagem nos não nulos |
|---|---:|---:|---:|
| `TotalArea` | 127 153 | 933 | 0,73% |
| `GrossArea` | 27 638 | 331 | 1,20% |
| `LivingArea` | 104 952 | 400 | 0,38% |
| `LotSize` | 39 583 | 626 | 1,58% |
| `BuiltArea` | 26 617 | 243 | 0,91% |

Áreas iguais ou inferiores a zero não são coerentes com a interpretação física destas variáveis. Devem ser convertidas para valores em falta ou removidas apenas numa versão processada, com regra documentada.

## Comparação Entre Grupos

As comparações entre grupos devem usar estatísticas robustas e considerar tamanhos amostrais desiguais. Os tipos de imóvel têm distribuições muito diferentes, pelo que comparar médias globais pode produzir conclusões enganadoras.

| `Type` | Registos com `Price` | Mediana de `Price` | Média de `Price` | P95 |
|---|---:|---:|---:|---:|
| Apartment | 47 236 | 280 000 | 371 592,05 | 914 859,75 |
| House | 36 652 | 259 250 | 453 562,55 | 1 300 000 |
| Land | 31 820 | 65 000 | 194 359,95 | 790 000 |
| Store | 5 325 | 130 000 | 239 697,78 | 750 000 |
| Farm | 3 883 | 265 000 | 596 948,85 | 2 200 000 |
| Building | 2 482 | 550 000 | 853 169,73 | 2 700 000 |

Também existem diferenças relevantes por distrito:

| `District` | Registos com `Price` | Mediana de `Price` | P95 |
|---|---:|---:|---:|
| Lisboa | 31 328 | 350 000 | 1 800 000 |
| Porto | 22 618 | 260 000 | 950 000 |
| Setúbal | 11 573 | 280 000 | 1 150 000 |
| Braga | 11 385 | 189 500 | 600 000 |
| Faro | 8 915 | 290 000 | 1 700 000 |

Estas diferenças são descritivas. Não provam que o tipo de imóvel ou o distrito causem determinado preço, porque há confundimento provável com área, localização específica, estado, data, segmento de mercado e qualidade do anúncio.

Para comparação formal entre grupos, recomenda-se:

- Usar mediana, IQR e percentis, não apenas média.
- Aplicar transformação `log(price)` quando fizer sentido.
- Usar testes não paramétricos ou modelos robustos se as distribuições continuarem assimétricas.
- Reportar tamanho do efeito e intervalos de confiança, não apenas valores-p.
- Fazer comparações dentro de grupos comparáveis, por exemplo apartamentos com apartamentos, e não todos os imóveis em conjunto.

## Correlações Futuras

As correlações preliminares calculadas diretamente sobre a base bruta mostram que Pearson é muito sensível aos valores extremos. Em várias variáveis, Pearson fica próximo de zero enquanto Spearman sugere associação monotónica mais clara.

| Variável | N pares válidos | Pearson com `Price` | Spearman com `Price` |
|---|---:|---:|---:|
| `NumberOfBathrooms` | 128 402 | 0,057 | 0,597 |
| `NumberOfBedrooms` | 46 908 | 0,344 | 0,435 |
| `TotalRooms` | 73 058 | 0,010 | 0,430 |
| `Parking` | 135 042 | 0,032 | 0,381 |
| `ConstructionYear` | 87 866 | 0,017 | 0,372 |
| `LivingArea` | 104 683 | 0,006 | 0,254 |
| `TotalArea` | 126 859 | -0,000 | 0,057 |
| `LotSize` | 39 499 | 0,028 | -0,032 |

Estas correlações são apenas exploratórias. Devem ser recalculadas depois da limpeza, remoção de duplicados, tratamento de valores inválidos e eventual transformação logarítmica. Também devem ser segmentadas por `Type`, porque uma área de terreno e uma área de apartamento não têm o mesmo significado económico.

Cuidados adicionais:

- Não usar `price_m2` como preditor direto de `Price`, porque contém a própria variável alvo.
- Verificar relações não lineares com gráficos e modelos flexíveis.
- Avaliar multicolinearidade entre áreas e contagens de divisões.
- Não interpretar correlação como causalidade.

## Preço por Metro Quadrado

Para registos com `Price > 0` e `TotalArea > 0`, existem 125 928 rácios válidos de `Price / TotalArea`.

| Estatística de `Price / TotalArea` | Valor |
|---|---:|
| Percentil 1 | 1,27 |
| Percentil 5 | 8,36 |
| Percentil 25 | 283,04 |
| Mediana | 1 483,52 |
| Percentil 75 | 2 954,55 |
| Percentil 95 | 6 117,84 |
| Percentil 99 | 9 832,92 |
| Percentil 99,9 | 23 823,43 |
| Máximo | 5 000 000 |

Foram observados 6 976 registos com menos de 10 euros por metro quadrado e 174 registos com mais de 20 000 euros por metro quadrado. Estes valores devem ser analisados antes de usar `price_m2` em relatórios exploratórios. Podem resultar de áreas incorretas, preços simbólicos, tipos de imóvel não comparáveis ou erros de unidade.

## Cuidados de Causalidade

Este dataset é observacional e baseado em anúncios. Por isso, a análise deve evitar linguagem causal.

Formulações adequadas:

- "Anúncios em Lisboa apresentam mediana de preço superior à mediana global."
- "Existe associação positiva entre número de casas de banho e preço anunciado."
- "A distribuição de preços difere entre tipos de imóvel."

Formulações a evitar:

- "Estar em Lisboa aumenta o preço."
- "Ter elevador causa preço mais alto."
- "Mais casas de banho fazem o imóvel valorizar."

Para sustentar afirmações causais seriam necessários desenho causal, variáveis de controlo adequadas, estratégia de identificação e discussão explícita de confundimento.

## Recomendações Antes da Modelação

Antes de treinar modelos, recomenda-se:

1. Criar uma versão processada em `data/processed/`, mantendo `data/raw/` intacto.
2. Remover duplicados exatos apenas na versão processada.
3. Remover ou isolar registos sem `Price` para treino supervisionado.
4. Converter valores não positivos em áreas para valores em falta.
5. Criar regras explícitas para valores extremos, preferencialmente por `Type` e localização.
6. Avaliar `log(price)` como variável alvo transformada ou métrica auxiliar.
7. Separar treino, validação e teste antes de imputações aprendidas nos dados.
8. Ajustar imputadores, scalers e encoders apenas no conjunto de treino.
9. Tratar categorias raras em `Type`, `City` e `Town` para reduzir instabilidade.
10. Excluir variáveis derivadas de `Price`, como `price_m2`, dos preditores diretos.
11. Documentar todas as decisões estatísticas no pipeline reprodutível.

## Conclusão

A base tem dimensão suficiente para análise estatística e modelação, mas apresenta assimetria extrema em `Price`, valores extremos em áreas, ausência de dados elevada em várias variáveis e duplicados exatos. As descritivas atuais estão globalmente corretas, mas devem ser comunicadas com foco em métricas robustas.

O próximo passo estatisticamente seguro é construir uma base processada com regras explícitas de limpeza, mantendo rastreabilidade das decisões e evitando interpretações causais sem suporte metodológico.
