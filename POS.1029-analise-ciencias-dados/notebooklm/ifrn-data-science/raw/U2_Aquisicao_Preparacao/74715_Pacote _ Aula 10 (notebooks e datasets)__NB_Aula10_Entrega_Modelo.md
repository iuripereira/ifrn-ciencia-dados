# Aula10_Entrega_Modelo.ipynb

# Atividade de Entrega — Aula 10: pipeline de limpeza de exames laboratoriais

**Análise e Ciência de Dados** (Especialização, IFRN) — Unidade 2, Aula 10

**Nome:** _____________________________________________

**O que entregar (Tarefa no Moodle, prazo 30/10/2026):**
1. este notebook **executado e comentado** (`.ipynb`), com o seu nome no arquivo;
2. o dataset limpo `exames_laboratoriais_limpo.csv`;
3. (opcional) o dicionário de dados em CSV, se você não o deixou no próprio notebook.

**Dados:** `dados/exames_laboratoriais.csv` — 155 registros **sintéticos** de exames laboratoriais (nenhum paciente real).

**Regras de documentação:** antes de cada bloco de código, escreva uma célula de texto explicando **o que** será feito e **por quê**; depois, comente o resultado (o que mudou? quantas linhas/valores foram afetados?). Use os notebooks da aula como referência.

## Requisitos

| # | Etapa | O que fazer |
|---|---|---|
| 1 | Extract e diagnóstico | carregar, `shape`, `dtypes`, ausentes, duplicatas e `value_counts` das categorias |
| 2 | Duplicatas | remover as linhas repetidas e conferir que `id_exame` ficou único |
| 3 | Tipos | `data_coleta` (dois formatos) → `datetime`; `resultado` (`"84,2"`) → `float` |
| 4 | Padronização | `sexo` → `F`/`M`; `prioridade` → `Rotina`/`Urgente`/`Emergência`; `laboratorio` → nomes oficiais sem espaços extras |
| 5 | Valores inválidos e ausentes | o código **999** em `resultado` significa "amostra não processada" → ausente; imputar `resultado` pela mediana **do mesmo tipo de exame** e `idade` pela mediana |
| 6 | Engenharia de atributos | `faixa_etaria` com `pd.cut` (18-39, 40-59, 60-79, 80+); `mes_coleta`; `alterado` (True/False) usando a tabela de referência abaixo |
| 7 | Codificação | `prioridade_cod` ordinal (Rotina=0, Urgente=1, Emergência=2); one-hot de `tipo_exame` |
| 8 | Validação | pelo menos 3 `assert` (ex.: sem ausentes, `id_exame` único, resultados positivos) |
| 9 | Load | exportar `exames_laboratoriais_limpo.csv` (sem índice) e mostrar o **dicionário de dados** (coluna, tipo, descrição) |
| 10 | Conclusão | 3 a 5 linhas: problemas encontrados, decisões tomadas e um achado com os dados limpos |

**Valores de referência (simplificados, apenas para fins didáticos):**

| Exame | Unidade | Faixa considerada normal |
|---|---|---|
| Glicemia | mg/dL | 70 a 99 |
| Colesterol total | mg/dL | abaixo de 190 |
| Creatinina | mg/dL | 0,6 a 1,2 |
| Hemoglobina | g/dL | 12,0 a 17,5 |

Nomes oficiais dos laboratórios: `LabNatal`, `LabSaúde RN`, `Laboratório Central`.

**Pontos de controle (para você conferir):** 150 linhas após remover duplicatas · 4 resultados com código 999 e 6 idades ausentes (após remover duplicatas) · nenhum ausente no dataset final · seguindo exatamente os requisitos, o arquivo final tem 150 linhas e 18 colunas.

**Critérios de avaliação (10 pontos):** limpeza e tipos corretos (3,0) · engenharia de atributos e codificação (2,5) · validação e exportação do dataset (1,5) · documentação — células de texto, comentários e dicionário de dados (2,0) · conclusão (1,0).

## 1. Extract e diagnóstico

_Explique aqui o que vai verificar._

```python
import pandas as pd
import numpy as np

ex = pd.read_csv("dados/exames_laboratoriais.csv")
# seu código aqui

```

## 2. Duplicatas

_Explique e comente o resultado._

```python
# seu código aqui

```

## 3. Transformação de tipos

_Explique e comente o resultado._

```python
# seu código aqui

```

## 4. Padronização das categorias

_Explique e comente o resultado._

```python
# seu código aqui

```

## 5. Valores inválidos e ausentes

_Explique e comente o resultado._

```python
# seu código aqui

```

## 6. Engenharia de atributos

_Explique e comente o resultado._

```python
# seu código aqui

```

## 7. Codificação das categorias

_Explique e comente o resultado._

```python
# seu código aqui

```

## 8. Validação

_Explique as regras escolhidas._

```python
# seu código aqui

```

## 9. Load e dicionário de dados

_Explique e comente o resultado._

```python
# seu código aqui

```

## 10. Conclusão

_Escreva aqui de 3 a 5 linhas._

