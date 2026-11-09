# Aula11_Exercicio_Pratico.ipynb

# Exercício Prático — Aula 11: o verão da sorveteria

**Análise e Ciência de Dados** (Especialização, IFRN) — Unidade 3, Aula 11

Este exercício é **para praticar** — não precisa ser entregue. A avaliação da aula é o **formulário avaliativo** no Moodle (prazo **10/11/2026**), e várias questões usam exatamente as situações deste exercício.

**Dados:** `dados/sorveteria.csv` — 90 dias de verão de uma sorveteria **fictícia** (dados sintéticos): data, dia da semana, se é fim de semana, temperatura máxima (°C), chuva (mm), sorvetes vendidos e cafés vendidos.

Em cada passo há um bloco **"Para conferir"** com o resultado esperado. Use o notebook `Aula11_AED_Estatistica_Descritiva.ipynb` como referência.

## Passo 1 — Carregar e classificar as variáveis

Carregue o arquivo, veja `shape` e `head()` e classifique cada coluna: qualitativa (nominal/ordinal) ou quantitativa (discreta/contínua).

> **Para conferir:** 90 linhas × 7 colunas. `dia_semana` e `fim_de_semana` são qualitativas nominais; `sorvetes_vendidos` e `cafes_vendidos` são quantitativas discretas (contagens); `temperatura_max` e `chuva_mm` são quantitativas contínuas.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

s = pd.read_csv("dados/sorveteria.csv")
# TODO: shape e head()

```

## Passo 2 — Tendência central

Calcule média e mediana de `sorvetes_vendidos` e `temperatura_max`. Depois descubra o dia de **maior** venda: o que aconteceu?

> **Para conferir:** sorvetes → média 177,6 e mediana 174,5; temperatura → média 26,9 °C e mediana 27,2 °C. O maior valor é **1.150 sorvetes** em 14/02/2026 — muito acima de todos os outros dias (o segundo maior é 317). Foi um sábado de festival na praça — e um dia relativamente fresco (21,8 °C).

```python
# TODO: mean() e median(); idxmax() ou sort_values() para achar o dia de maior venda

```

## Passo 3 — Sem o dia atípico

Crie `s2` sem o dia do festival e recalcule média e mediana dos sorvetes. Qual medida mudou mais?

> **Para conferir:** sem o festival → média 166,7 e mediana 174,0. A **média** caiu cerca de 11 sorvetes; a mediana, só 0,5.

```python
# TODO: s2 = s[s["sorvetes_vendidos"] < 1000]

```

## Passo 4 — Dispersão

Para `temperatura_max` e `sorvetes_vendidos` (use `s2`), calcule desvio-padrão, coeficiente de variação (CV) e IQR.

> **Para conferir:** temperatura → desvio 3,2 °C, CV 12%, IQR 4,6 °C; sorvetes → desvio 68,5, CV 41%, IQR 102,0. As vendas variam muito mais (em termos relativos) que a temperatura.

```python
# TODO: std(), std()/mean()*100 e quantile(0.75) - quantile(0.25)

```

## Passo 5 — Forma da distribuição

Faça o histograma de `chuva_mm` e calcule a assimetria (`skew`) de `chuva_mm` e `temperatura_max`. Quantos dias **não** choveu?

> **Para conferir:** 67 dos 90 dias sem chuva; a chuva é fortemente assimétrica à direita (skew ≈ 2,3) — por isso média (3,3 mm) é muito maior que a mediana (0 mm). A temperatura é quase simétrica (skew ≈ −0,1).

```python
# TODO: plt.hist(...), skew(), (s["chuva_mm"] == 0).sum()

```

## Passo 6 — Fim de semana vende mais?

Compare média e mediana de sorvetes entre fins de semana e dias úteis (use `s2`).

> **Para conferir:** fim de semana (24 dias) → média 204,6 e mediana 202,0; dias úteis (65 dias) → média 152,7 e mediana 160,0. Nos fins de semana vendem-se cerca de 50 sorvetes a mais.

```python
# TODO: groupby("fim_de_semana")["sorvetes_vendidos"].agg(["count", "mean", "median"])

```

## Passo 7 — Correlação: temperatura × sorvetes

1. Calcule Pearson e Spearman entre `temperatura_max` e `sorvetes_vendidos` **com todos os dias** (`s`).
2. Repita **sem o festival** (`s2`).
3. Faça o gráfico de dispersão de `s`. Por que os dois coeficientes discordam tanto?

> **Para conferir:** com todos os dias → Pearson 0,32 e Spearman 0,80; sem o festival → Pearson 0,85 e Spearman 0,86. Um único ponto extremo derrubou o Pearson; o Spearman, baseado em postos, quase não foi afetado.

```python
# TODO: corr() e corr(method="spearman") em s e em s2; plt.scatter(...)

```

## Passo 8 — Matriz de correlação

Calcule a matriz de Spearman de `temperatura_max`, `chuva_mm`, `sorvetes_vendidos` e `cafes_vendidos` (use `s2`). Qual a correlação mais negativa?

> **Para conferir:** as mais negativas são temperatura × cafés e sorvetes × cafés (ambas ≈ −0,76): em dias quentes vendem-se mais sorvetes e menos cafés. Chuva × cafés é positiva (≈ 0,49).

```python
# TODO: s2[[...]].corr(method="spearman").round(2)

```

## Passo 9 — Hipóteses exploratórias

Escreva **duas** hipóteses exploratórias específicas e testáveis sugeridas pelos passos anteriores e diga que evidência descritiva apoia cada uma.

> **Para conferir (exemplos):** H1 — "A cada grau a mais de temperatura máxima, as vendas de sorvete aumentam" (ρ ≈ 0,86 sem o festival). H2 — "Nos fins de semana vendem-se mais sorvetes que nos dias úteis, mesmo com temperaturas semelhantes" (≈50 a mais; entre 26 e 30 °C, mediana de 226 contra 173). Lembre: correlação não prova causa — a temperatura e o fim de semana podem agir juntos.

```python
# TODO: escreva suas hipóteses numa célula de texto (Markdown)

```

