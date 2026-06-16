# Compreensão do Negócio

## Problema

O preço anunciado de um imóvel resulta da combinação de múltiplos fatores. Localização, área, tipologia, número de divisões, estacionamento, estado de conservação e certificação energética podem influenciar o valor, mas a relação entre estas variáveis tende a ser desigual entre regiões e tipos de imóvel.

O projeto procura estudar estas relações com base em anúncios imobiliários em Portugal e preparar uma solução local de previsão de preços. Nesta fase, o objetivo não é concluir sobre o mercado nem apresentar modelos finais, mas sim garantir que o problema está bem definido e que os dados são preparados de forma adequada.

## Objetivo de Negócio

Apoiar a interpretação do mercado imobiliário português através de análise de dados e criar uma base para estimar preços anunciados de imóveis de forma local e reprodutível.

## Questões de Investigação

- Que variáveis parecem ter maior relação com o preço anunciado?
- Como variam os preços entre distritos, cidades e tipologias?
- A área do imóvel explica diferenças relevantes de preço?
- A certificação energética e o estado de conservação têm associação observável com o preço?
- É possível construir um modelo local com erro suficientemente interpretável para apoio à decisão?
- Que limitações dos dados condicionam a qualidade da previsão?

## Público-Alvo

| Público | Necessidade principal |
|---|---|
| Compradores | Compreender valores anunciados por localização e características |
| Vendedores | Ter uma referência analítica para enquadrar preços |
| Profissionais imobiliários | Identificar padrões de mercado e fatores relevantes |
| Investidores | Comparar zonas, tipologias e potenciais oportunidades |
| Avaliadores do projeto | Verificar rigor metodológico, documentação e reprodutibilidade |

## Critérios de Sucesso

| Critério | Evidência esperada |
|---|---|
| Documentação clara | Ficheiros em `docs/` coerentes, objetivos e alinhados com CRISP-DM |
| Dados preparados | Dataset tratado guardado em `data/processed/` nas próximas etapas |
| Decisões justificadas | Regras de limpeza, exclusão e transformação documentadas |
| Controlo de fuga de informação | Variáveis derivadas da variável alvo excluídas da modelação preditiva |
| Modelação local | Modelos treinados sem dependência de APIs externas de IA |
| Avaliação interpretável | Métricas como MAE, RMSE e R2 explicadas no contexto do problema |

## Restrições e Cuidados

- O dataset representa anúncios e não necessariamente transações concluídas.
- O preço disponível deve ser interpretado como preço anunciado.
- A existência de valores em falta, duplicados e valores extremos deve ser tratada antes da modelação.
- Variáveis como `price_m2`, calculadas a partir de `price`, podem apoiar a análise exploratória, mas não devem ser usadas como input de modelos que preveem `price`.
- O projeto deve manter uma execução local, sem dependência de serviços externos de IA.

## Entregáveis Esperados

- Documentação técnica organizada por fase.
- Dataset processado e versionado em `data/processed/`.
- Gráficos exploratórios guardados em `reports/figures/`.
- Código reutilizável para preparação e modelação em `src/`.
- Modelos de referência e modelos comparativos avaliados com métricas consistentes.
