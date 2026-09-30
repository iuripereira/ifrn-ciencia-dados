# Aula 04 — Laboratório NumPy e Pandas I (Prática)

> Criação e manipulação de DataFrames; seleção e filtragem (loc/iloc); leitura de CSV/Excel; inspeção básica (head, info, describe); atribuição segura e tratamento de valores ausentes.
> Recursos: Jupyter Notebook, dados de exemplo (matrículas do IFRN — **dados sintéticos**).
> Avaliação: exercício prático entregue no Moodle + formulário avaliativo com 10 questões.
> Materiais: livro (6 capítulos, abaixo) · apostila PDF (31 p., link no README da Unidade) · pacote ZIP com notebook e dados · exemplo prático comentado · tarefa · formulário.

---

# Livro — Tópicos de Estudo

Leia com o Jupyter aberto: execute cada trecho, altere um parâmetro e observe o que muda. A apostila em PDF traz o mesmo conteúdo ampliado, com o laboratório guiado e o exercício.

## Capítulo 1 — Do array ao DataFrame

Na Aula 03 representamos uma pequena tabela como lista de dicionários. Funciona — mas tente responder, em Python puro, "qual a nota média dos estudantes do turno noturno, por campus, ignorando quem está sem nota?". São três laços aninhados, um dicionário acumulador e várias verificações de `None`. Em Pandas, cabe em uma linha.

### Três camadas empilhadas

- **Python puro (list, dict):** flexibilidade total, mas cada elemento é um objeto separado na memória e toda operação exige laço explícito.
- **NumPy (ndarray):** bloco contíguo de memória, um único tipo, operações vetorizadas em C. Em compensação: um só tipo por array, sem nomes de coluna, sem suporte nativo a ausentes em inteiros.
- **Pandas (Series, DataFrame):** colunas nomeadas e de tipos diferentes, índice rotulado, alinhamento automático, tratamento de ausentes e leitura de dezenas de formatos — ao custo de mais memória e alguma sobrecarga.

A frase que vale guardar: **Pandas é NumPy com rótulos, tipos mistos e tratamento de dados faltantes.** Quase tudo o que confunde em Pandas — o índice, o `NaN`, o dtype `object`, o `SettingWithCopyWarning` — aparece exatamente onde essas três adições encostam no NumPy de baixo.

### Vetorização

Vetorizar é aplicar uma operação a todos os elementos de uma vez. O laço continua existindo; apenas passou a rodar em código compilado.

```python
# Python puro: o laço está no seu código, interpretado
bonus = []
for n in lista_notas:
    bonus.append(n * 1.05)

# NumPy: o laço está dentro da biblioteca, compilado
bonus = notas * 1.05
```

Para arrays grandes, a segunda forma é tipicamente 10 a 100 vezes mais rápida. Regra prática: se você escreveu um `for` percorrendo linhas de um DataFrame, quase certamente existe uma forma vetorizada melhor.

### Indexação booleana: o mecanismo por trás de toda filtragem

```python
import numpy as np
notas = np.array([72.5, 68.0, 91.3, 55.4, 80.1])

notas >= 70            # array([ True, False,  True, False,  True])
notas[notas >= 70]     # array([72.5, 91.3, 80.1])
(notas >= 70).sum()    # 3   -> True vale 1, False vale 0
(notas >= 70).mean()   # 0.6 -> proporção de aprovados
```

Como `True == 1`, `mascara.sum()` conta os casos e `mascara.mean()` devolve a proporção. Você usará isso o tempo todo para calcular taxas.

### Ausentes em NumPy e em Pandas

Em NumPy, `np.mean` de um array com `NaN` devolve `NaN`; é preciso `np.nanmean`. Em Pandas, `.mean()` já ignora ausentes por padrão. É conveniente e perigoso: uma média calculada sobre 441 de 482 estudantes não é a média da turma, e o Pandas não avisa.

## Capítulo 2 — Series, DataFrame e o índice

### Series: um vetor com rótulos

```python
import pandas as pd

s = pd.Series([72.5, 68.0, 91.3],
              index=["20261000", "20261001", "20261002"],
              name="nota_final")

s.values   # array([72.5, 68. , 91.3])  -> o ndarray NumPy por baixo
s.index    # Index(['20261000', '20261001', '20261002'], dtype='object')
s.dtype    # dtype('float64')
```

### Alinhamento automático

O índice governa a combinação entre objetos: o Pandas casa os **rótulos**, não as posições.

```python
a = pd.Series([10, 20, 30], index=["x", "y", "z"])
b = pd.Series([ 1,  2,  3], index=["z", "y", "x"])   # ordem invertida

a + b
# x    13    <- 10 + 3, casado pelo rótulo "x"
# y    22
# z    31
```

Consequência: somar colunas vindas de DataFrames com índices diferentes pode produzir `NaN` — porque os rótulos não casaram. Ao concatenar ou reordenar, use `.reset_index(drop=True)`.

### DataFrame: um dicionário ordenado de Series

- `df.shape` — tupla (linhas, colunas)
- `df.columns` / `df.index` — rótulos de colunas e de linhas
- `df.dtypes` — tipo de cada coluna
- `df.to_numpy()` — conteúdo como array NumPy
- `len(df)` — número de linhas

### Os dtypes que você vai encontrar

- `int64` — inteiros. **Não aceita NaN**: um único ausente converte a coluna para `float64`.
- `float64` — decimais; padrão de coluna numérica com ausentes.
- `object` / `str` — texto e tipos mistos. Frequentemente sinaliza número lido como texto.
- `bool` — resultado de toda comparação.
- `datetime64[ns]` — datas; só com `parse_dates=` ou `pd.to_datetime()`.
- `category` — texto com poucos valores distintos; economiza memória (turno, campus).

Sintoma mais comum de leitura malfeita: coluna numérica aparece como `object`. Causas: vírgula decimal não declarada, separador de milhar, ou texto como `"N/D"` no meio dos números.

## Capítulo 3 — Criando DataFrames e lendo arquivos

### Cinco formas de criar um DataFrame

```python
# (a) dicionário de listas — as chaves viram colunas
df = pd.DataFrame({"campus": ["Natal-Central", "Mossoró"],
                   "alunos": [98, 70]})

# (b) lista de dicionários — um registro por linha; chave ausente vira NaN
df = pd.DataFrame([{"campus": "Natal-Central", "alunos": 98},
                   {"campus": "Mossoró"}])

# (c) lista de tuplas + columns
df = pd.DataFrame([("Natal-Central", 98), ("Mossoró", 70)],
                  columns=["campus", "alunos"])

# (d) array NumPy — quando tudo é numérico
df = pd.DataFrame(np.zeros((5, 3)), columns=["p1", "p2", "p3"])

# (e) com índice significativo
df = df.set_index("campus")    # promove coluna a índice
df = df.reset_index()          # desfaz
```

### read_csv: os parâmetros que importam

O CSV é texto sem esquema. Ler um CSV brasileiro com os padrões quase sempre dá errado, porque o padrão do Pandas é o formato norte-americano.

- `sep=";"` — separador de campos
- `decimal=","` — separador decimal
- `thousands="."` — separador de milhar
- `encoding="utf-8"` / `"latin-1"` / `"cp1252"`
- `dtype={"matricula": "string"}` — força o tipo de colunas específicas
- `usecols=[...]` e `nrows=1000` — lê só o necessário
- `na_values=["N/D", "-"]` — textos a tratar como ausente
- `parse_dates=["data"]` — converte para datetime64
- `index_col="matricula"`, `skiprows=3`

```python
df = pd.read_csv("dados/matriculas_ifrn_2026.csv",
                 sep=";", decimal=",", encoding="utf-8",
                 dtype={"matricula": "string"})
```

### Por que a matrícula não pode ser inteiro

Identificadores lidos como `int64` perdem zeros à esquerda (`"00123"` vira `123`), estouram a precisão em códigos longos e passam a aceitar operações sem sentido. Regra: **se não faz sentido calcular a média, não é número — é texto.** Vale para CPF, CEP, SIAPE e código de escola.

### Diagnóstico rápido

Antes de insistir em parâmetros, olhe o arquivo cru. Acentos corrompidos (`MossorÃ³`) indicam codificação errada; uma única coluna gigante indica `sep` errado.

```python
with open("dados/matriculas_ifrn_2026.csv", encoding="utf-8") as f:
    for _ in range(3):
        print(f.readline().rstrip())
```

### read_excel

Requer `openpyxl` para `.xlsx`. Diferença em relação ao CSV: existência de planilhas (abas).

```python
campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
todas  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name=None)   # dict
df     = pd.read_excel("relatorio.xlsx", skiprows=4)               # pula título decorativo
```

Planilhas costumam trazer células mescladas, títulos decorativos e totais no meio da tabela. Sempre confira `df.head()` e `df.dtypes` logo após ler um `.xlsx`.

### Gravando

`df.to_csv("saida.csv", index=False)` — sem `index=False`, o índice vira uma coluna anônima que reaparece como `Unnamed: 0` na próxima leitura.

## Capítulo 4 — Inspeção básica: as sete primeiras perguntas

1. `df.shape` — quantas linhas e colunas? Bate com o esperado?
2. `df.head()` / `df.sample(5)` — com o que os dados se parecem?
3. `df.info()` — tipo de cada coluna? Quantos não nulos?
4. `df.describe()` — as estatísticas fazem sentido?
5. `df.isna().sum()` — onde estão os buracos?
6. `df["col"].value_counts()` — que categorias existem?
7. `df.duplicated().sum()` — há linhas repetidas?

### Lendo o info()

- **Non-Null Count** — comparado ao total, revela quantos ausentes cada coluna tem. Se `RangeIndex` mostra 482 e a coluna 441, são 41 ausentes.
- **Dtype** — numérica aparecendo como `object` = leitura precisa ser corrigida.
- **memory usage** — `df.info(memory_usage="deep")` para o tamanho real de colunas de texto.

### Lendo o describe()

Por padrão resume colunas numéricas: count, mean, std, min, 25%, 50% (mediana), 75%, max.

- `count` menor que `len(df)` denuncia ausentes — e lembra que a média foi calculada só sobre os presentes.
- Média muito distante da mediana sugere assimetria ou valores extremos.
- `min`/`max` impossíveis (idade 0, nota 999) indicam erro de coleta ou código de ausência disfarçado.
- `df.describe(include="all")` inclui colunas de texto (unique, top, freq).

> Nota de versão: a partir do Pandas 3.0 as colunas de texto têm dtype próprio `str`, e `describe(include="object")` emite aviso. Prefira `include="all"`. Verifique com `pd.__version__`.

### value_counts(): o detector de sujeira

```python
df["turno"].value_counts()                  # contagem absoluta
df["turno"].value_counts(normalize=True)    # proporção
df["turno"].value_counts(dropna=False)      # inclui os NaN
df["campus"].nunique()                      # quantos distintos
```

`"Natal-Central"`, `"natal-central"` e `" Natal-Central "` aparecem como três valores diferentes. No conjunto desta aula, `nunique()` devolve **19 campi antes** da limpeza e **12 depois** de `str.strip()`.

## Capítulo 5 — Seleção com loc e iloc

- **`loc`** trabalha com **RÓTULOS** (o que está escrito no índice e nos nomes das colunas).
- **`iloc`** trabalha com **POSIÇÕES** (inteiros de 0 a n−1).

### Colchetes simples

```python
df["nota_final"]              # uma COLUNA -> Series
df[["nome", "nota_final"]]    # várias colunas -> DataFrame
df[0:5]                       # fatia de LINHAS por posição (ambíguo!)
df[df["nota_final"] > 90]     # filtragem booleana de LINHAS
```

Com texto, `[]` seleciona coluna; com fatia ou máscara, linhas. Para qualquer seleção que não seja "colunas inteiras", prefira `loc`/`iloc`.

### loc — por rótulo

```python
df.loc[0]                                   # linha de RÓTULO 0
df.loc[0, "nome"]                           # uma célula
df.loc[0:2]                                 # rótulos 0, 1 E 2 -> fim INCLUÍDO
df.loc[0:2, ["nome", "campus"]]             # linhas x colunas
df.loc[df["turno"] == "Noturno", "nota_final"]   # filtro + coluna
```

### iloc — por posição

```python
df.iloc[0]                    # PRIMEIRA linha, seja qual for o rótulo
df.iloc[0, 1]                 # 1ª linha, 2ª coluna
df.iloc[0:3]                  # posições 0, 1, 2 -> fim EXCLUÍDO
df.iloc[0:3, 0:4]             # 3 primeiras linhas, 4 primeiras colunas
df.iloc[-1]                   # última linha
df.iloc[[0, 5, 10], [1, 9]]   # listas de posições
```

### A pegadinha clássica

Com o índice padrão, `df.loc[0:2]` devolve **três** linhas e `df.iloc[0:2]` devolve **duas**. `loc` fatia rótulos (intervalo fechado), `iloc` fatia posições (semiaberto).

### Quando o índice deixa de ser 0, 1, 2…

```python
noturno = df[df["turno"] == "Noturno"]
noturno.index[:5]     # Index([0, 1, 5, 8, 10], ...) -> com buracos

noturno.loc[5]        # a linha cujo RÓTULO é 5
noturno.iloc[5]       # a 6ª linha deste subconjunto

noturno = noturno.reset_index(drop=True)   # renumera 0..n-1
```

Depois de `set_index("matricula")`, `dfm.loc["20261250"]` funciona e `dfm.iloc["20261250"]` falha: `iloc` exige inteiro de posição, nunca texto.

### at e iat

Acesso otimizado a um único escalar: `df.at[0, "nome"]` (rótulo) e `df.iat[0, 1]` (posição).

## Capítulo 6 — Filtragem, atribuição segura e valores ausentes

### Máscaras booleanas

```python
mascara = df["nota_final"] >= 70
df[mascara]
df.loc[mascara, ["nome", "nota_final"]]   # filtra E escolhe colunas
```

### Dois erros que todo iniciante comete

1. Usar `and`/`or` no lugar de `&`/`|` → `ValueError: The truth value of a Series is ambiguous`.
2. Esquecer os parênteses: `&` tem precedência maior que `>=`.

```python
# CERTO
df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)]    # E
df[(df["campus"] == "Mossoró") | (df["campus"] == "Apodi")]  # OU
df[~(df["situacao"] == "Aprovado")]                          # NÃO
```

### Atalhos legíveis

- `df["campus"].isin(lista)` — pertence a um conjunto
- `df["idade"].between(18, 24)` — intervalo fechado
- `df["curso"].str.contains("Sistemas|Redes", na=False)` — regex; `na=False` não é opcional
- `df.query("turno == 'Noturno' and nota_final >= 80")`
- `df.nlargest(10, "nota_final")`, `df.sort_values("nota_final", ascending=False)`

### Atribuição segura e o SettingWithCopyWarning

```python
# ERRADO — "indexação encadeada": dois colchetes em sequência
df[df["frequencia"].isna()]["frequencia"] = 85.0

# CERTO — uma única operação com loc: [linhas, coluna]
df.loc[df["frequencia"].isna(), "frequencia"] = 85.0
```

`df[mascara]` pode devolver cópia ou vista; se for cópia, a atribuição altera um objeto temporário descartado. Com `df.loc[linhas, coluna] = valor` o Pandas escreve no original. Ao derivar um subconjunto que será alterado, use `.copy()`.

### A armadilha do np.where com ausentes

`NaN >= 70` é `False`. Logo, `np.where(df["nota"] >= 70, "Bom", "A melhorar")` classifica silenciosamente os sem nota como "A melhorar". Correção:

```python
df["faixa"] = df["faixa"].mask(df["nota_final"].isna())
```

### NaN não é zero

- `df.isna().sum()` — ausentes por coluna
- `df.isna().mean()` — proporção
- `df.dropna(subset=["nota_final"])` — remove só quem falta naquela coluna
- `df["col"].fillna(df["col"].median())` — imputa pela mediana

A pergunta certa não é "como remover os NaN?", e sim "**por que eles estão ali?**". Os 41 estudantes sem `nota_final` estão em situação *Trancado* (27) ou *Em curso* (14): a nota **não existe ainda**. Preenchê-la com a média criaria desempenho fictício. Já a `frequencia` ausente em 9 registros é plausivelmente falha de registro, e imputar a mediana é defensável — desde que documentado.

### O que vem na Aula 05

Laboratório Pandas II — groupby, agg, pivot_table, merge/join, apply com lambda e method chaining.

---

# Exemplo Prático — Matrículas do IFRN (`exemplo_pandas.py`)

Roteiro guiado em oito passos, do arquivo bruto à primeira resposta. Usa o pacote **Laboratório — Notebook e conjuntos de dados (ZIP)**. Salve como `exemplo_pandas.py` ao lado da pasta `dados/`, ou copie bloco a bloco para um notebook.

> Os dados são sintéticos. Os números servem para conferir se o seu ambiente produz o mesmo resultado — não para tirar conclusões sobre o IFRN.

### Passo 1 — Ler corretamente

```python
import numpy as np
import pandas as pd

df = pd.read_csv("dados/matriculas_ifrn_2026.csv",
                 sep=";", decimal=",", encoding="utf-8",
                 dtype={"matricula": "string"})
print(df.shape)        # (482, 12)

campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")
```

Sem `sep=";"` o arquivo vira uma única coluna; sem `decimal=","` as notas viram texto. Vale executar o erro uma vez para reconhecê-lo depois.

### Passo 2 — Inspecionar

```python
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

Média (69,15) e mediana (69,70) praticamente coincidem: distribuição aproximadamente simétrica. Os 19 campi vêm de valores com espaços nas bordas.

### Passo 3 — Limpeza mínima

```python
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)
print(df.shape, df["campus"].nunique())   # (480, 12) 12
```

### Passo 4 — Selecionar

```python
df.iloc[0:3, 0:4]                              # 3 linhas, 4 colunas (por POSIÇÃO)
df.loc[0:2, ["nome", "campus", "nota_final"]]  # atenção: 0:2 INCLUI o 2

dfm = df.set_index("matricula")
dfm.loc["20261042", ["nome", "campus", "nota_final"]]
# nome          Ubiratan Rocha Barbosa
# campus                 Natal-Central
# nota_final                      76.4
```

### Passo 5 — Filtrar

```python
aprovados   = df[df["situacao"] == "Aprovado"]                                  # 281
noturno_bom = df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)]         #  35
metro       = df[df["campus"].isin(["Natal-Central","Natal-Zona Norte","Parnamirim"])]  # 174
jovens      = df[df["idade"].between(18, 24)]                                   # 189
ti          = df[df["curso"].str.contains("Sistemas|Redes", na=False)]          # 107
```

### Passo 6 — Atribuir com segurança

```python
df.loc[df["frequencia"].isna(), "frequencia"] = df["frequencia"].median()
print(df["frequencia"].isna().sum())   # 0
```

### Passo 7 — NumPy por baixo do Pandas

```python
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

A armadilha mais silenciosa da aula: `NaN >= 80` é `False`, então quem não tem nota cai no ramo `else` sem aviso.

### Passo 8 — Responder uma pergunta

```python
media_geral  = df["nota_final"].mean()                       # 69.20
media_campus = (df.groupby("campus")["nota_final"]
                  .mean().sort_values(ascending=False).round(2))
print(media_campus[media_campus > media_geral])
# Santa Cruz 74.55 | Currais Novos 72.28 | Apodi 71.69
# Mossoró 71.66 | Natal-Zona Norte 70.36 | Caicó 70.04
```

Leia com ceticismo: diferenças de 1 a 5 pontos, grupos de tamanhos muito distintos (Natal-Central 98; Caicó 23 — só 21 com nota), a média ignora curso, turno e ano de ingresso, e os dados são sintéticos. Reportar um ranking daqui seria um erro técnico grave.

---

# Exercício Prático — Aula 04 (entrega do notebook)

Aberto: sábado, 12/09/2026, 00:00 · 2 tentativas permitidas · 10 questões, 10,0 pontos. Detalhes em `atividade/README.md`.

# Formulário Avaliativo — Aula 04

10 questões objetivas sobre o livro, a apostila e o exemplo: leitura de CSV/Excel, `info` e `describe`, `loc` × `iloc`, máscaras booleanas, atribuição segura, `np.where` com ausentes e interpretação de resultados. Pode consultar o material durante a realização.
