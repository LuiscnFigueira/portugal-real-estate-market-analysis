# Preparação dos Dados

## Objetivo

Preparar o dataset para análise exploratória e modelação futura, garantindo nomes consistentes, tipos adequados e regras explícitas para valores inválidos. Esta preparação é preliminar e deve evoluir para um pipeline reutilizável nas próximas fases.

## Fonte de Dados

| Elemento | Valor |
|---|---|
| Ficheiro original | `data/raw/portugal_listinigs.csv` |
| Ficheiro processado inicial | `data/processed/portugal_listings_initial_clean.csv` |
| Ficheiro preparado | `data/processed/portugal_listings_prepared.csv` |
| Ficheiro preparado comprimido para GitHub | `data/processed/portugal_listings_prepared.csv.gz` |
| Observações iniciais | 135 536 |
| Variáveis originais | 25 |
| Observações processadas | 126 242 |
| Variáveis processadas | 29 |
| Observações preparadas | 126 242 |
| Variáveis preparadas | 49 |
| Variável alvo | `price` |

O ficheiro original em `data/raw/` não deve ser alterado. Qualquer versão tratada deve ser gravada em `data/processed/`.

## Decisões de Preparação

| Decisão | Justificação |
|---|---|
| Renomear colunas para `snake_case` | Facilita leitura, consistência e utilização em Python |
| Converter `publish_date` para data | Permite análise temporal e extração de ano/mês |
| Converter booleanos para tipo `boolean` | Preserva valores em falta e evita misturar texto com lógica |
| Converter categorias para `category` | Reduz ambiguidade sem impor encoding prematuro |
| Converter inteiros para `Int64` | Permite representar inteiros com valores nulos |
| Remover duplicados exatos na versão processada | Evita contagens repetidas de anúncios idênticos sem alterar `data/raw/` |
| Marcar preços e áreas não positivas como nulos | Valores iguais ou inferiores a zero não são válidos para análise de preço |
| Criar indicadores de valores em falta | Preserva informação sobre ausência sem imputação prematura |
| Criar flags de outliers por IQR | Sinaliza valores extremos sem remover casos potencialmente legítimos |

## Renomeação de Colunas

As variáveis originais foram renomeadas para nomes mais consistentes. Exemplos principais:

| Nome original | Nome normalizado |
|---|---|
| `Price` | `price` |
| `District` | `district` |
| `EnergyCertificate` | `energy_certificate` |
| `GrossArea` | `gross_area` |
| `TotalArea` | `total_area` |
| `ConstructionYear` | `construction_year` |
| `PublishDate` | `publish_date` |
| `NumberOfBedrooms` | `number_of_bedrooms` |
| `NumberOfBathrooms` | `number_of_bathrooms` |

## Conversão de Tipos

| Grupo | Variáveis |
|---|---|
| Data | `publish_date` |
| Booleanas | `has_parking`, `garage`, `elevator`, `electric_cars_charging` |
| Categóricas | `district`, `city`, `town`, `type`, `energy_certificate`, `floor`, `energy_efficiency_level`, `conservation_status` |
| Inteiras com nulos | `parking`, `construction_year`, `total_rooms`, `number_of_bedrooms`, `number_of_wc`, `number_of_bathrooms` |
| Numéricas contínuas | `price`, `gross_area`, `total_area`, `living_area`, `lot_size`, `built_area` |

Na conversão de booleanos foram considerados valores textuais como `true`, `false`, `yes`, `no`, `sim`, `não` e `nao`, preservando valores ausentes quando não existia informação válida.

## Regras de Validação Inicial

| Regra | Ação |
|---|---|
| `price <= 0` | Converter para valor em falta |
| `total_area <= 0` | Converter para valor em falta |
| `price_m2 <= 0` | Converter para valor em falta |
| `property_age < 0` | Converter para valor em falta |
| Duplicados exatos | Remover apenas na versão em memória ou no dataset processado |
| `price` em falta | Remover da versão usada para análise/modelação |

Estas regras são conservadoras: removem apenas casos incompatíveis com o objetivo imediato, como ausência da variável alvo, e mantêm para análise posterior observações que possam exigir interpretação contextual.

## Duplicados

Foram identificados 8 913 duplicados exatos. No notebook de inicialização, a remoção foi aplicada na versão em memória para preparar a análise preliminar. O ficheiro original em `data/raw/` não foi alterado.

Na próxima fase, esta regra deve ser reproduzida num pipeline e guardada apenas numa versão processada em `data/processed/`.

## Preço Ausente

Foram identificados 300 registos sem valor em `price`. Como `price` é a variável alvo do projeto, estes registos foram removidos na versão em memória usada para análise preliminar.

Esta remoção não altera o ficheiro original e deve ser repetida de forma explícita no pipeline que vier a gerar o dataset processado.

## Estado da Preparação

A preparação atual cria uma base mais coerente para análise e já existe código reutilizável em `src/` para gerar o dataset processado inicial e a versão preparada.

O comando principal para gerar a versão processada inicial é:

```bash
python3 -m src.data.make_dataset
```

A versão preparada foi criada no notebook:

```text
notebooks/03_data_preparation.ipynb
```

Para upload no GitHub via interface web, deve ser usado o ficheiro comprimido
`data/processed/portugal_listings_prepared.csv.gz`, porque o CSV sem compressão
ultrapassa o limite de 25 MB do upload no browser.

Validações observadas no dataset processado:

| Validação | Resultado |
|---|---:|
| Linhas | 126 242 |
| Colunas na versão inicial | 29 |
| Colunas na versão preparada | 49 |
| Valores em falta em `price` | 0 |
| Duplicados exatos | 0 |
| Valores infinitos em `price_m2` | 0 |
| Valores não positivos em `total_area` | 0 |

Validações adicionais da versão preparada:

| Validação | Resultado |
|---|---:|
| Indicadores de valores em falta criados | 11 |
| Flags de outliers por IQR criadas | 9 |
| Outliers sinalizados em `price` | 10 582 |

Os outliers foram sinalizados, mas não removidos. Esta decisão é intencional, porque imóveis extremos podem ser legítimos dependendo do tipo de imóvel, localização e área.

Antes do treino de modelos será necessário definir:

- Estratégia final para valores em falta.
- Critérios de tratamento ou retenção de valores extremos.
- Colunas a excluir por baixa utilidade, excesso de valores em falta ou risco de fuga de informação.
- Encoding de variáveis categóricas.
- Separação entre treino, validação e teste.
- Confirmar se o dataset processado inicial é suficiente ou se deve ser criada uma versão final para modelação.

## Riscos a Controlar

| Risco | Mitigação proposta |
|---|---|
| Misturar dados originais e tratados | Manter `data/raw/` intacto e gravar outputs em `data/processed/` |
| Introduzir fuga de informação | Excluir variáveis derivadas da variável alvo durante a modelação |
| Remover valores extremos legítimos | Analisar extremos por localização, área e tipo antes de eliminar |
| Perder reprodutibilidade | Migrar transformações do notebook para funções em `src/` |
