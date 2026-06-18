# Visão Geral do Projeto

## Título

Análise e Previsão Local de Preços de Imóveis em Portugal

## Enquadramento

O mercado imobiliário português apresenta diferenças relevantes entre distritos, cidades, tipologias e características físicas dos imóveis. O preço anunciado de um imóvel pode depender de fatores como localização, área, número de divisões, estado de conservação, certificação energética, estacionamento e antiguidade.

Este projeto organiza uma análise de anúncios imobiliários em Portugal e prepara os dados para uma futura etapa de modelação local. A abordagem segue a metodologia CRISP-DM e mantém uma separação clara entre dados originais, dados tratados, documentação e código reutilizável.

## Objetivo Principal

Construir uma base analítica fiável para estudar o mercado imobiliário português e, numa fase posterior, desenvolver modelos locais de machine learning capazes de estimar o preço anunciado de imóveis.

## Objetivos Específicos

- Documentar o problema, os dados disponíveis e as decisões tomadas.
- Carregar o dataset original sem alterar a fonte em `data/raw/`.
- Uniformizar nomes de variáveis para `snake_case`.
- Converter datas, categorias, booleanos e inteiros para tipos adequados.
- Criar variáveis derivadas úteis para análise exploratória e modelação futura.
- Identificar riscos de qualidade de dados e de fuga de informação.
- Preparar o caminho para pipelines reprodutíveis de preparação e modelação.

## Âmbito Atual

| Área | Incluído nesta fase | Fora desta fase |
|---|---|---|
| Organização | Estrutura documental, notebooks numerados e código reutilizável | Aplicação final ou dashboard |
| Dados | Leitura, renomeação, tipos, preparação estruturada e datasets processados | Alteração manual de `data/raw/` |
| Feature engineering | Features de área, divisões, amenidades, tempo, localização e missingness | Encoding final e imputação dentro de pipeline |
| Análise | Diagnóstico de qualidade e preparação para validação estatística | Conclusões causais |
| Modelação | Definição dos cuidados e variáveis candidatas | Treino e comparação final de modelos |
| Entrega | Documentação profissional e coerente | Aplicação final ou deployment |

## Dataset

| Campo | Descrição |
|---|---|
| Nome | Portugal Real Estate 2024 |
| Fonte | Kaggle |
| Ficheiro original | `data/raw/portugal_listinigs.csv` |
| Observações iniciais | 135 536 anúncios |
| Variáveis originais | 25 |
| Variável alvo | `price` |

## Princípios de Trabalho

- Não alterar manualmente os dados originais.
- Guardar versões tratadas em `data/processed/`.
- Guardar gráficos em `reports/figures/`.
- Explicar decisões metodológicas relevantes na documentação.
- Evitar resultados não verificados ou conclusões antes da modelação.
- Executar a análise e a previsão de forma local, sem APIs externas de IA.

## Metodologia CRISP-DM

| Fase CRISP-DM | Aplicação neste projeto |
|---|---|
| Business Understanding | Definir problema, objetivos, público-alvo e critérios de sucesso |
| Data Understanding | Caracterizar variáveis, estrutura, cobertura e limitações dos dados |
| Data Preparation | Preparar tipos, valores válidos, variáveis derivadas e datasets processados |
| Modeling | Treinar modelos locais de regressão numa fase posterior |
| Evaluation | Avaliar desempenho e utilidade dos modelos com métricas interpretáveis |
| Deployment | Organizar resultados para consulta local, relatório ou apresentação |

## Estado Atual

O trabalho realizado até ao momento cobre as fases de inicialização, compreensão dos dados, preparação estruturada e feature engineering. Já existem datasets processados em `data/processed/`, código reutilizável em `src/`, testes automatizados e documentação técnica. Ainda não existem modelos treinados nem métricas finais de desempenho.
