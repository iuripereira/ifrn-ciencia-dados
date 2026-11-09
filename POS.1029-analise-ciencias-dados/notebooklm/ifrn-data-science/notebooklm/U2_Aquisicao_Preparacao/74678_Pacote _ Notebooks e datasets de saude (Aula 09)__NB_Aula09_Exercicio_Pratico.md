# Aula09_Exercicio_Pratico.ipynb

# Exercício Prático — Aula 09: limpando dados de triagem

**Análise e Ciência de Dados** (Especialização, IFRN) — Unidade 2, Aula 09

Este exercício é **para praticar** — não precisa ser entregue. A avaliação da aula é o **formulário avaliativo** no Moodle (prazo **30/10/2026**), e várias questões dele usam exatamente as situações deste exercício.

**Dados:** `dados/triagem_pa_sujo.csv` — 64 registros **sintéticos** de triagem em um pronto atendimento (nenhum paciente real): idade, temperatura, frequência cardíaca, saturação de O₂ e a classificação de risco (protocolo de cores Azul / Verde / Amarelo / Vermelho).

Em cada passo há um bloco **"Para conferir"** com o resultado esperado. Use o notebook `Aula09_Qualidade_e_Limpeza_de_Dados.ipynb` como referência.

## Passo 1 — Carregar e diagnosticar

Carregue o arquivo e responda: quantas linhas e colunas? Quantos ausentes por coluna? Quantas linhas duplicadas?

> **Para conferir:** 64 linhas × 7 colunas; 4 ausentes em `temperatura_c` e 2 em `saturacao_o2`; 4 linhas duplicadas.

```python
import pandas as pd
import numpy as np

t = pd.read_csv("dados/triagem_pa_sujo.csv")
# TODO: shape, isna().sum() e duplicated().sum()

```

## Passo 2 — Remover duplicatas

> **Para conferir:** restam 60 linhas.

```python
# TODO: drop_duplicates() e reset_index(drop=True)

```

## Passo 3 — Padronizar a classificação de risco

A coluna `classificacao_risco` tem `"verde"`, `"VERDE"`, `"Verde"`... Deixe tudo no formato `"Verde"` (primeira letra maiúscula).

> **Para conferir:** Verde 30, Amarelo 21, Azul 7, Vermelho 2.

```python
# TODO: str.strip() + str.capitalize() e depois value_counts()

```

## Passo 4 — Encontrar outliers com o IQR

Calcule Q1, Q3, IQR e os limites (Q1 − 1,5·IQR e Q3 + 1,5·IQR) para `freq_cardiaca`, `temperatura_c` e `saturacao_o2`, e liste os valores fora dos limites.

> **Para conferir:** frequência cardíaca → 300; temperatura → 375; saturação → 9, 90 e 92.
> Pense: quais são **erros** e quais são **valores reais** de pacientes graves?

```python
def outliers_iqr(serie):
    # TODO: devolver os valores abaixo de Q1 - 1.5*IQR ou acima de Q3 + 1.5*IQR
    pass

for col in ["freq_cardiaca", "temperatura_c", "saturacao_o2"]:
    print(col, outliers_iqr(t[col]))

```

## Passo 5 — Corrigir os erros (regras de domínio)

- Temperatura acima de 45 °C: a vírgula foi esquecida (375 → 37,5) → **divida por 10**.
- Frequência cardíaca fora de 30–220 bpm: impossível → **NaN**.
- Saturação abaixo de 50%: impossível → **NaN**. (90% e 92% são baixos, mas **reais** — ficam!)

> **Para conferir:** depois das correções, os ausentes passam a ser: temperatura 4, frequência cardíaca 1, saturação 3.

```python
# TODO: aplicar as três regras com df.loc[condição, coluna] = ...

```

## Passo 6 — Preencher os ausentes

- `temperatura_c` → mediana geral;
- `saturacao_o2` e `freq_cardiaca` → mediana **por classificação de risco** (`groupby(...).transform("median")`).

> **Para conferir:** mediana geral da temperatura = 36,8 °C; mediana da saturação no grupo Vermelho = 91%; nenhum ausente no final.

```python
# TODO: fillna com mediana geral e com mediana por grupo

```

## Passo 7 — Normalização e padronização

Crie `fc_minmax` (frequência cardíaca normalizada entre 0 e 1) e `temp_z` (temperatura padronizada pelo z-score).

> **Para conferir:** `fc_minmax` vai de 0 a 1 (média 0,43); `temp_z` tem média 0 e desvio-padrão 1.

```python
# TODO: fórmulas (x - min)/(max - min) e (x - média)/desvio

```

## Passo 8 — Conferir o resultado e salvar

Calcule as médias de temperatura, frequência cardíaca e saturação por classificação de risco e salve o arquivo limpo.

> **Para conferir:** o grupo **Vermelho** tem a maior temperatura média (38,2 °C), a maior frequência cardíaca (117 bpm) e a menor saturação (91%) — coerente com o protocolo de triagem. Se o seu resultado mostrar uma média de temperatura acima de 40 °C, algum erro ficou para trás!

```python
# TODO: groupby("classificacao_risco") + mean(); salvar em dados/triagem_pa_limpo.csv

```

