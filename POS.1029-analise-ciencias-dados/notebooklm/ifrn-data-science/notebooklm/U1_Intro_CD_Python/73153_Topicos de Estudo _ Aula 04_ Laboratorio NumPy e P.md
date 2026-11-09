# Tópicos de Estudo — Aula 04: Laboratório NumPy e P

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 04: Laboratório NumPy e Pandas I

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 04: Laboratório NumPy e Pandas I  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:22  |

## Descrição

Conteúdo teórico da Aula 04 em formato de livro, em 6 capítulos: da lista Python ao DataFrame; anatomia de `Series` e `DataFrame`; criação de DataFrames e leitura de CSV/Excel; inspeção básica (`head`, `info`, `describe`); seleção com `loc` e `iloc`; filtragem booleana, atribuição segura e valores ausentes.

Leia com o Jupyter aberto: execute cada trecho, altere um parâmetro e observe o que muda. A apostila em PDF traz o mesmo conteúdo ampliado, com o laboratório guiado e o exercício.

## Índice

- 1. Capítulo 1 — Do array ao DataFrame
- 2. Capítulo 2 — Series, DataFrame e o índice
- 3. Capítulo 3 — Criando DataFrames e lendo arquivos
- 4. Capítulo 4 — Inspeção básica: as sete primeiras perguntas
- 5. Capítulo 5 — Seleção com loc e iloc
- 6. Capítulo 6 — Filtragem, atribuição segura e valores ausentes

## 1. Capítulo 1 — Do array ao DataFrame

Na Aula 03 representamos uma pequena tabela como uma lista de dicionários. Funciona — mas tente responder, em Python puro, a pergunta "qual a nota média dos estudantes do turno noturno, por campus, ignorando quem está sem nota?". O código tem três laços aninhados, um dicionário acumulador e várias verificações de `None`. Em Pandas, a mesma pergunta cabe em uma linha.

#### Três camadas empilhadas

- Python puro (`list`, `dict`): flexibilidade total, mas cada elemento é um objeto separado na memória e toda operação exige laço explícito.
- NumPy (`ndarray`): bloco contíguo de memória, um único tipo, operações vetorizadas executadas em C. Em compensação: um só tipo por array, sem nomes de coluna, sem suporte nativo a ausentes em inteiros.
- Pandas (`Series`, `DataFrame`): colunas nomeadas e de tipos diferentes, índice rotulado, alinhamento automático, tratamento de ausentes e leitura de dezenas de formatos — ao custo de mais memória e alguma sobrecarga.

A frase que vale guardar: Pandas é NumPy com rótulos, tipos mistos e tratamento de dados faltantes. Quase tudo o que confunde em Pandas — o índice, o `NaN`, o `dtype object`, o `SettingWithCopyWarning` — aparece exatamente onde essas três adições encostam no NumPy de baixo.

#### Vetorização

Vetorizar é aplicar uma operação a todos os elementos de uma vez. O laço continua existindo; apenas passou a rodar em código compilado.

```
# Python puro: o laço está no seu código, interpretado
bonus = []
for n in lista_notas:
    bonus.append(n * 1.05)

# NumPy: o laço está dentro da biblioteca, compilado
bonus = notas * 1.05
```

Para arrays grandes, a segunda forma é tipicamente 10 a 100 vezes mais rápida. Regra prática: se você escreveu um `for` percorrendo linhas de um DataFrame, quase certamente existe uma forma vetorizada melhor.

#### Indexação booleana: o mecanismo por trás de toda filtragem

```
import numpy as np
notas = np.array([72.5, 68.0, 91.3, 55.4, 80.1])

notas >= 70            # array([ True, False,  True, False,  True])
notas[notas >= 70]     # array([72.5, 91.3, 80.1])
(notas >= 70).sum()    # 3   -> True vale 1, False vale 0
(notas >= 70).mean()   # 0.6 -> proporção de aprovados
```

Como `True == 1`, `mascara.sum()` conta os casos e `mascara.mean()` devolve a proporção. Você usará isso o tempo todo para calcular taxas.

#### Ausentes em NumPy e em Pandas

Em NumPy, `np.mean` de um array com `NaN` devolve `NaN`; é preciso usar `np.nanmean`. Em Pandas, `.mean()` já ignora ausentes por padrão. É conveniente e perigoso: uma média calculada sobre 441 de 482 estudantes não é a média da turma, e o Pandas não avisa.

## 2. Capítulo 2 — Series, DataFrame e o índice

#### Series: um vetor com rótulos

Uma `Series` é um array unidimensional acompanhado de um índice (os rótulos das posições) e de um nome.

```
import pandas as pd

s = pd.Series([72.5, 68.0, 91.3],
              index=["20261000", "20261001", "20261002"],
              name="nota_final")

s.values   # array([72.5, 68. , 91.3])  -> o ndarray NumPy por baixo
s.index    # Index(['20261000', '20261001', '20261002'], dtype='object')
s.dtype    # dtype('float64')
```

#### Alinhamento automático

O índice não é decoração: ele governa a combinação entre objetos. Ao operar duas Series, o Pandas casa os rótulos, não as posições.

```
a = pd.Series([10, 20, 30], index=["x", "y", "z"])
b = pd.Series([ 1,  2,  3], index=["z", "y", "x"])   # ordem invertida

a + b
# x    13    <- 10 + 3, casado pelo rótulo "x"
# y    22
# z    31
```

Consequência prática: somar colunas vindas de DataFrames com índices diferentes pode produzir `NaN` — não porque os dados estejam errados, mas porque os rótulos não casaram. Ao concatenar ou reordenar, use `.reset_index(drop=True)`.

#### DataFrame: um dicionário ordenado de Series

Um `DataFrame` é uma tabela bidimensional: várias Series que compartilham o mesmo índice.

- `df.shape` — tupla (linhas, colunas)
- `df.columns` / `df.index` — rótulos de colunas e de linhas
- `df.dtypes` — tipo de cada coluna
- `df.to_numpy()` — o conteúdo como array NumPy
- `len(df)` — número de linhas

#### Os dtypes que você vai encontrar

- `int64` — inteiros. Não aceita `NaN`: um único ausente converte a coluna inteira para `float64`.
- `float64` — decimais; tipo padrão de coluna numérica com ausentes.
- `object` / `str` — texto e tipos mistos. Frequentemente sinaliza número lido como texto.
- `bool` — resultado de toda comparação.
- `datetime64[ns]` — datas; só aparece com `parse_dates=` ou `pd.to_datetime()`.
- `category` — texto com poucos valores distintos; economiza muita memória em colunas como `turno` ou `campus`.

Sintoma mais comum de leitura malfeita: uma coluna que deveria ser numérica aparece como `object`. Causas quase sempre: vírgula decimal não declarada, separador de milhar, ou um texto como `"N/D"` no meio dos números.

## 3. Capítulo 3 — Criando DataFrames e lendo arquivos

#### Cinco formas de criar um DataFrame

```
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
df = df.set_index("campus")     # promove coluna a índice
df = df.reset_index()           # desfaz
```

#### read_csv: os parâmetros que importam

O CSV é apenas texto, sem esquema, e cada sistema o gera à sua maneira. Ler um CSV brasileiro com os parâmetros padrão quase sempre dá errado, porque o padrão do Pandas é o formato norte-americano.

- `sep=";"` — separador de campos
- `decimal=","` — separador decimal
- `thousands="."` — separador de milhar
- `encoding="utf-8"` / `"latin-1"` / `"cp1252"`
- `dtype={"matricula": "string"}` — força o tipo de colunas específicas
- `usecols=[...]` e `nrows=1000` — lê só o necessário
- `na_values=["N/D", "-"]` — textos a tratar como ausente
- `parse_dates=["data"]` — converte para `datetime64`
- `index_col="matricula"`, `skiprows=3`

```
df = pd.read_csv("dados/matriculas_ifrn_2026.csv",
                 sep=";", decimal=",", encoding="utf-8",
                 dtype={"matricula": "string"})
```

#### Por que a matrícula não pode ser inteiro

Identificadores lidos como `int64` perdem zeros à esquerda (`"00123"` vira `123`), estouram a precisão em códigos longos e passam a aceitar operações sem sentido, como somar duas matrículas. Regra: se não faz sentido calcular a média, não é número — é texto. Vale para CPF, CEP, SIAPE e código de escola.

#### Diagnóstico rápido

Antes de insistir em parâmetros, olhe o arquivo cru — as três primeiras linhas revelam quase tudo. Acentos corrompidos (`MossorÃ³`) indicam codificação errada; uma única coluna gigante indica `sep` errado.

```
with open("dados/matriculas_ifrn_2026.csv", encoding="utf-8") as f:
    for _ in range(3):
        print(f.readline().rstrip())
```

#### read_excel

Requer `openpyxl` para arquivos `.xlsx`. A diferença em relação ao CSV é a existência de planilhas (abas).

```
campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
todas  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name=None)  # dict
df     = pd.read_excel("relatorio.xlsx", skiprows=4)  # pula título decorativo
```

Planilhas costumam trazer células mescladas, títulos decorativos e totais no meio da tabela. Sempre confira `df.head()` e `df.dtypes` logo após ler um `.xlsx`.

#### Gravando

`df.to_csv("saida.csv", index=False)` — sem `index=False`, o índice vira uma coluna anônima que reaparece como `Unnamed: 0` na próxima leitura.

## 4. Capítulo 4 — Inspeção básica: as sete primeiras perguntas

Diante de um arquivo desconhecido, esta sequência deve ser automática. Leva menos de um minuto e evita horas de análise sobre dados quebrados.

- `df.shape` — quantas linhas e colunas? O número bate com o esperado?
- `df.head()` / `df.sample(5)` — com o que esses dados se parecem?
- `df.info()` — que tipo tem cada coluna? Quantos não nulos?
- `df.describe()` — as estatísticas fazem sentido?
- `df.isna().sum()` — onde estão os buracos?
- `df["col"].value_counts()` — que categorias existem?
- `df.duplicated().sum()` — há linhas repetidas?

#### Lendo o info()

É a saída mais informativa do Pandas. Três colunas importam:

- Non-Null Count — comparado ao total de linhas, revela imediatamente quantos ausentes cada coluna tem. Se `RangeIndex` mostra 482 e a coluna mostra 441, são 41 ausentes.
- Dtype — coluna que deveria ser numérica aparecendo como `object` significa que a leitura precisa ser corrigida antes de qualquer análise.
- memory usage — use `df.info(memory_usage="deep")` para o tamanho real das colunas de texto.

#### Lendo o describe()

Por padrão resume apenas colunas numéricas: `count`, `mean`, `std`, `min`, `25%`, `50%` (mediana), `75%`, `max`.

- `count` menor que `len(df)` denuncia ausentes naquela coluna — e lembra que a média exibida foi calculada só sobre os presentes.
- Média muito distante da mediana sugere assimetria ou valores extremos.
- `min` ou `max` impossíveis (idade 0, nota 999) indicam erro de coleta ou código de ausência disfarçado de número.
- `df.describe(include="all")` inclui as colunas de texto, com `unique`, `top` e `freq`.

Nota de versão: a partir do Pandas 3.0 as colunas de texto têm dtype próprio `str`, e `describe(include="object")` emite aviso de compatibilidade. Prefira `include="all"`. Verifique sua versão com `pd.__version__`.

#### value_counts(): o detector de sujeira

```
df["turno"].value_counts()                  # contagem absoluta
df["turno"].value_counts(normalize=True)    # proporção
df["turno"].value_counts(dropna=False)      # inclui os NaN
df["campus"].nunique()                      # quantos distintos
```

É a ferramenta número um para detectar categorias sujas: `"Natal-Central"`, `"natal-central"` e `" Natal-Central "` aparecem como três valores diferentes. No conjunto desta aula, `nunique()` devolve 19 campi antes da limpeza e 12 depois de `str.strip()`.

## 5. Capítulo 5 — Seleção com loc e iloc

Este é o ponto em que a maioria dos iniciantes escorrega. A confusão desaparece com uma única distinção:

`loc` trabalha com RÓTULOS (o que está escrito no índice e nos nomes das colunas).
`iloc` trabalha com POSIÇÕES (inteiros de 0 a n−1, como em listas Python).

#### Colchetes simples

```
df["nota_final"]              # uma COLUNA -> Series
df[["nome", "nota_final"]]    # várias colunas -> DataFrame
df[0:5]                       # fatia de LINHAS por posição (ambíguo!)
df[df["nota_final"] > 90]     # filtragem booleana de LINHAS
```

Note a ambiguidade: com um texto, `[]` seleciona coluna; com fatia ou máscara, seleciona linhas. Por isso, para qualquer seleção que não seja "uma ou mais colunas inteiras", prefira `loc` ou `iloc`.

#### loc — por rótulo

```
df.loc[0]                                 # linha de RÓTULO 0
df.loc[0, "nome"]                         # uma célula
df.loc[0:2]                               # rótulos 0, 1 E 2 -> fim INCLUÍDO
df.loc[0:2, ["nome", "campus"]]           # linhas x colunas
df.loc[df["turno"] == "Noturno", "nota_final"]   # filtro + coluna
```

#### iloc — por posição

```
df.iloc[0]                    # PRIMEIRA linha, seja qual for o rótulo
df.iloc[0, 1]                 # 1ª linha, 2ª coluna
df.iloc[0:3]                  # posições 0, 1, 2 -> fim EXCLUÍDO
df.iloc[0:3, 0:4]             # 3 primeiras linhas, 4 primeiras colunas
df.iloc[-1]                   # última linha
df.iloc[[0, 5, 10], [1, 9]]   # listas de posições
```

#### A pegadinha clássica

Com o índice padrão, `df.loc[0:2]` devolve três linhas e `df.iloc[0:2]` devolve duas. Não é bug: `loc` fatia rótulos (intervalo fechado), `iloc` fatia posições (intervalo semiaberto, como toda fatia Python).

#### Quando o índice deixa de ser 0, 1, 2…

```
noturno = df[df["turno"] == "Noturno"]
noturno.index[:5]     # Index([0, 1, 5, 8, 10], ...) -> com buracos

noturno.loc[5]        # a linha cujo RÓTULO é 5
noturno.iloc[5]       # a 6ª linha deste subconjunto

noturno = noturno.reset_index(drop=True)   # renumera 0..n-1
```

Depois de `set_index("matricula")`, `dfm.loc["20261250"]` funciona e `dfm.iloc["20261250"]` falha: `iloc` exige um inteiro de posição, nunca um texto.

#### at e iat

Versões otimizadas para acessar um único valor escalar: `df.at[0, "nome"]` (rótulo) e `df.iat[0, 1]` (posição). Mais rápidas, porém mais restritas.

## 6. Capítulo 6 — Filtragem, atribuição segura e valores ausentes

#### Máscaras booleanas

Filtrar é selecionar linhas por uma condição. A condição produz uma Series de `True`/`False` do tamanho do DataFrame, usada como índice.

```
mascara = df["nota_final"] >= 70
df[mascara]
df.loc[mascara, ["nome", "nota_final"]]   # filtra E escolhe colunas
```

#### Dois erros que todo iniciante comete

- Usar `and`/`or` no lugar de `&`/`|`. Os operadores do Python esperam um único booleano e disparam `ValueError: The truth value of a Series is ambiguous`.
- Esquecer os parênteses. `&` tem precedência maior que `>=`, então `df["a"] > 1 & df["b"] < 2` é avaliado na ordem errada.

```
# CERTO
df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)]   # E
df[(df["campus"] == "Mossoró") | (df["campus"] == "Apodi")]  # OU
df[~(df["situacao"] == "Aprovado")]                          # NÃO
```

#### Atalhos que deixam o código legível

- `df["campus"].isin(lista)` — pertence a um conjunto; substitui uma cadeia de `|`
- `df["idade"].between(18, 24)` — intervalo fechado
- `df["curso"].str.contains("Sistemas|Redes", na=False)` — texto contém; aceita regex. `na=False` não é opcional: um ausente produziria `NaN` na máscara e levantaria erro.
- `df.query("turno == 'Noturno' and nota_final >= 80")` — filtro em string
- `df.nlargest(10, "nota_final")`, `df.sort_values("nota_final", ascending=False)`

#### Atribuição segura e o SettingWithCopyWarning

```
# ERRADO — "indexação encadeada": dois colchetes em sequência
df[df["frequencia"].isna()]["frequencia"] = 85.0

# CERTO — uma única operação com loc: [linhas, coluna]
df.loc[df["frequencia"].isna(), "frequencia"] = 85.0
```

Por quê? `df[mascara]` pode devolver uma cópia ou uma vista — o Pandas não garante qual. Se for cópia, a atribuição altera um objeto temporário que será descartado. Com `df.loc[linhas, coluna] = valor` o Pandas sabe que a intenção é escrever no original. Ao derivar um subconjunto que será alterado, use `.copy()` explicitamente.

#### A armadilha do np.where com ausentes

`NaN >= 70` é `False`. Logo, `np.where(df["nota"] >= 70, "Bom", "A melhorar")` classifica silenciosamente todos os estudantes sem nota como "A melhorar". A correção é reinserir o ausente depois:

```
df["faixa"] = df["faixa"].mask(df["nota_final"].isna())
```

#### NaN não é zero

Ausente significa "não sei", e isso é diferente de "zero" e de "vazio".

- `df.isna().sum()` — quantos ausentes por coluna
- `df.isna().mean()` — proporção de ausentes
- `df.dropna(subset=["nota_final"])` — remove só quem falta naquela coluna
- `df["col"].fillna(df["col"].median())` — imputa pela mediana

A pergunta certa não é "como remover os `NaN`?", e sim "por que eles estão ali?". No conjunto desta aula, os 41 estudantes sem `nota_final` estão em situação Trancado (27) ou Em curso (14): a nota não existe ainda — não foi perdida. Preenchê-la com a média criaria desempenho fictício. Já a `frequencia` ausente em 9 registros é plausivelmente falha de registro, e imputar a mediana é defensável — desde que a decisão seja documentada.

#### O que vem na Aula 05

Laboratório Pandas II — Agrupamentos e Joins: `groupby`, `agg`, `pivot_table`, `merge`/`join`, `apply` com `lambda` e method chaining.