# Aula10_Exercicio_Pratico.ipynb

# Exercício Prático — Aula 10: mini-pipeline de consultas ambulatoriais

**Análise e Ciência de Dados** (Especialização, IFRN) — Unidade 2, Aula 10

Este exercício é **para praticar** — não precisa ser entregue. Ele treina, numa única tabela e em poucos passos, tudo o que a **atividade de entrega** (dataset de exames laboratoriais) vai pedir.

**Dados:** `dados/consultas_ambulatorio.csv` — 83 registros **sintéticos** de consultas em um ambulatório (nenhum paciente real): data, idade, especialidade, tempo de espera, valor e satisfação do paciente.

Em cada passo há um bloco **"Para conferir"** com o resultado esperado. Use o notebook `Aula10_Pipeline_de_Limpeza.ipynb` como referência.

## Passo 1 — Extract: carregar e olhar os tipos

Carregue o arquivo e veja `shape`, `dtypes` e as primeiras linhas. Quantas linhas duplicadas existem?

> **Para conferir:** 83 linhas × 7 colunas; só `id_consulta` é numérica — idade, espera e valor vieram como **texto** (`"62 anos"`, `"37 min"`, `"R$ 200,00"`); 3 linhas duplicadas.

```python
import pandas as pd
import numpy as np

c = pd.read_csv("dados/consultas_ambulatorio.csv")
# TODO: shape, dtypes, head() e duplicated().sum()

```

## Passo 2 — Remover duplicatas e padronizar o texto

Remova as duplicatas. Depois padronize `especialidade` (ex.: `"CARDIOLOGIA"` e `"cardiologia"` → `"Cardiologia"`) e `satisfacao` (`"boa"` → `"Boa"`).

> **Para conferir:** 80 linhas; especialidades: Clínica geral 25, Cardiologia 24, Pediatria 18, Ortopedia 13.

```python
# TODO: drop_duplicates() + reset_index(drop=True)
# TODO: str.strip().str.capitalize() nas duas colunas de texto

```

## Passo 3 — Transformação de tipos

Converta:
- `data_consulta` (`"11/08/2026"`) → `datetime`;
- `idade` (`"62 anos"`) e `tempo_espera` (`"37 min"`) → `int` (dica: `str.extract(r"(\d+)")` pega os dígitos);
- `valor_consulta` (`"R$ 200,00"`) → `float`.

> **Para conferir:** tempo médio de espera = 34,9 min; soma dos valores = R$ 13.100,00; primeira consulta em 03/08/2026.

```python
# TODO: pd.to_datetime(..., format="%d/%m/%Y")
# TODO: str.extract(r"(\d+)")[0].astype(int)
# TODO: moeda → float (tirar "R$", ponto de milhar e trocar vírgula por ponto)

```

## Passo 4 — Engenharia de atributos: binning

1. Crie `faixa_espera` com `pd.cut` nos limites `[0, 15, 30, 60, 999]` e rótulos `"até 15"`, `"16-30"`, `"31-60"`, `"mais de 60"` (use o padrão `right=True`: 15 min entra em "até 15").
2. Crie `dia_semana` com `c["data_consulta"].dt.day_name()`.

> **Para conferir:** faixas → até 15: 13 · 16-30: 24 · 31-60: 35 · mais de 60: 8.

```python
# TODO: pd.cut(c["tempo_espera"], bins=..., labels=...)
# TODO: dia_semana

```

## Passo 5 — Codificação: ordinal e one-hot

1. `satisfacao` tem ordem (Ruim < Regular < Boa < Ótima) → crie `satisfacao_cod` com um dicionário `{"Ruim": 0, "Regular": 1, "Boa": 2, "Ótima": 3}`.
2. `especialidade` **não** tem ordem → faça one-hot com `pd.get_dummies(..., prefix="esp", dtype=int)` e junte ao DataFrame.

> **Para conferir:** satisfação média (codificada) = 1,42; o DataFrame passa a ter 14 colunas.

```python
# TODO: map com o dicionário de ordem
# TODO: get_dummies + pd.concat([...], axis=1)

```

## Passo 6 — Uma pergunta com os atributos novos

Qual a satisfação média (codificada) em cada faixa de espera?

> **Para conferir:** a satisfação **cai** à medida que a espera aumenta: 2,85 (até 15) → 1,88 → 0,89 → 0,12 (mais de 60).

```python
# TODO: groupby("faixa_espera", observed=True)["satisfacao_cod"].mean()

```

## Passo 7 — Load: validar e exportar

Valide com `assert` (sem ausentes; `id_consulta` único; espera > 0) e exporte para `dados/consultas_limpo.csv`. Releia o arquivo e confira o `shape`.

> **Para conferir:** o arquivo relido tem 80 linhas × 14 colunas.

```python
# TODO: asserts
# TODO: to_csv(..., index=False) e read_csv para conferir

```

