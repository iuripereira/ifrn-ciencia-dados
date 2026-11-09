# Exemplo — Laboratório Pandas com as matrículas do 

Este é o roteiro guiado da Aula 04. Ele usa os arquivos do pacote Laboratório — Notebook e conjuntos de dados (ZIP). Salve o código como `exemplo_pandas.py` ao lado da pasta `dados/`, ou copie bloco a bloco para um notebook.

Lembrete: os dados são sintéticos. Os números abaixo servem para você conferir se o seu ambiente está produzindo o mesmo resultado — não para tirar conclusões sobre o IFRN.

#### Passo 1 — Ler corretamente

```
import numpy as np
import pandas as pd

df = pd.read_csv("dados/matriculas_ifrn_2026.csv",
                 sep=";", decimal=",", encoding="utf-8",
                 dtype={"matricula": "string"})
print(df.shape)        # (482, 12)
```

Sem `sep=";"` o arquivo inteiro vira uma única coluna; sem `decimal=","` as notas viram texto. Vale executar o erro uma vez para reconhecê-lo depois.

```
campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")
```

#### Passo 2 — Inspecionar

```
df.info()
print(df.describe().round(2))
print(df.isna().sum())
print("duplicadas:", df.duplicated().sum())
print("campi distintos:", df["campus"].nunique())
```

```
nota_final  -> 441 non-null de 482  (41 ausentes)
frequencia  -> 473 non-null de 482  ( 9 ausentes)
duplicadas: 2
campi distintos: 19   <- o IFRN não tem 19 campi neste conjunto!
```

Média (69,15) e mediana (69,70) das notas praticamente coincidem: distribuição aproximadamente simétrica. Os 19 campi vêm de valores com espaços nas bordas: `" Mossoró "` é, para o Pandas, diferente de `"Mossoró"`.

#### Passo 3 — Limpeza mínima

```
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)
print(df.shape, df["campus"].nunique())   # (480, 12) 12
```

#### Passo 4 — Selecionar

```
df.iloc[0:3, 0:4]                              # 3 linhas, 4 colunas (por POSIÇÃO)
df.loc[0:2, ["nome", "campus", "nota_final"]]  # atenção: 0:2 INCLUI o 2

dfm = df.set_index("matricula")
dfm.loc["20261042", ["nome", "campus", "nota_final"]]
# nome          Ubiratan Rocha Barbosa
# campus                 Natal-Central
# nota_final                      76.4
```

#### Passo 5 — Filtrar

```
aprovados   = df[df["situacao"] == "Aprovado"]                                  # 281
noturno_bom = df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)]         #  35
metro       = df[df["campus"].isin(["Natal-Central","Natal-Zona Norte","Parnamirim"])]  # 174
jovens      = df[df["idade"].between(18, 24)]                                   # 189
ti          = df[df["curso"].str.contains("Sistemas|Redes", na=False)]          # 107
```

Parênteses em cada condição e `&` no lugar de `and` — as duas regras que evitam o `ValueError: The truth value of a Series is ambiguous`.

#### Passo 6 — Atribuir com segurança

```
df.loc[df["frequencia"].isna(), "frequencia"] = df["frequencia"].median()
print(df["frequencia"].isna().sum())   # 0
```

Uma única operação `loc[linhas, coluna]`. A forma encadeada `df[mascara]["frequencia"] = ...` dispara `SettingWithCopyWarning` e pode não alterar nada.

#### Passo 7 — NumPy por baixo do Pandas

```
mask = (df["nota_final"] >= 60).to_numpy()
print(type(mask), mask.dtype, mask.sum(), "de", mask.size)
# <class 'numpy.ndarray'> bool 337 de 480

df["faixa"] = np.where(df["nota_final"] >= 80, "Alta",
                np.where(df["nota_final"] >= 60, "Média", "Baixa"))
print(df["faixa"].value_counts(dropna=False))
# Média 244 | Baixa 143 | Alta 93   <- "Baixa" inclui, indevidamente, os 41 sem nota

df["faixa"] = df["faixa"].mask(df["nota_final"].isna())
print(df["faixa"].value_counts(dropna=False))
# Média 244 | Baixa 102 | Alta 93 | NaN 41   <- correto
```

Esta é a armadilha mais silenciosa da aula: `NaN >= 80` é `False`, então quem não tem nota cai no ramo `else` sem que nada avise.

#### Passo 8 — Responder uma pergunta

```
media_geral  = df["nota_final"].mean()                      # 69.20
media_campus = (df.groupby("campus")["nota_final"]
                  .mean().sort_values(ascending=False).round(2))
print(media_campus[media_campus > media_geral])
# Santa Cruz 74.55 | Currais Novos 72.28 | Apodi 71.69
# Mossoró 71.66 | Natal-Zona Norte 70.36 | Caicó 70.04
```

Leia o resultado com ceticismo. As diferenças são de 1 a 5 pontos, os grupos têm tamanhos muito distintos (Natal-Central tem 98 estudantes; Caicó, 23 — e apenas 21 com nota), a média ignora curso, turno e ano de ingresso, e os dados são sintéticos. Reportar um ranking a partir daqui seria um erro técnico grave. O `groupby` usado aqui é o tema da Aula 05.

Última atualização: sábado, 12 set. 2026, 14:12