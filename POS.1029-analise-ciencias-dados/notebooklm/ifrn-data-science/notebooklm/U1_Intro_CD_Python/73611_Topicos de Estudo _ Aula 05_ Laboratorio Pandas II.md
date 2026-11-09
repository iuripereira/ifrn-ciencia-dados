# Tópicos de Estudo — Aula 05: Laboratório Pandas II

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 05: Laboratório Pandas II

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 05: Laboratório Pandas II  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:22  |

## Índice

- 1. Capítulo 1 — groupby: dividir, aplicar, combinar
- 2. Capítulo 2 — agg: várias estatísticas de uma vez
- 3. Capítulo 3 — pivot_table: o groupby de duas dimensões
- 4. Capítulo 4 — merge e join: combinando tabelas
- 5. Capítulo 5 — apply, lambda e por que vetorizar continua vencendo
- 6. Capítulo 6 — method chaining e pipe

## 1. Capítulo 1 — groupby: dividir, aplicar, combinar

Na Aula 04 respondemos "qual a nota média por campus?" com um único `groupby`. Esta aula aprofunda essa ferramenta e acrescenta as que faltavam para transformar uma tabela bruta em respostas: `agg`, `pivot_table`, `merge`, `apply` e o estilo de method chaining.

#### O padrão split-apply-combine

Todo `groupby` segue três passos, sempre na mesma ordem:

- Dividir (split) — o DataFrame é particionado em grupos, um por valor distinto da coluna (ou colunas) de agrupamento.
- Aplicar (apply) — uma função (média, contagem, soma, uma função personalizada) roda separadamente em cada grupo.
- Combinar (combine) — os resultados de cada grupo são reunidos de volta em uma única Series ou DataFrame.

Nada disso é mágico: `df.groupby("campus")["nota_final"].mean()` é conceitualmente equivalente a fazer um laço sobre cada campus, calcular a média do subconjunto e depois montar uma tabela com os resultados — só que o Pandas faz isso de forma vetorizada e muito mais rápida.

#### Agrupando por uma coluna

```
media_por_campus = df.groupby("campus")["nota_final"].mean().round(2)
media_por_campus.sort_values(ascending=False)
```

`df.groupby("campus")` sozinho não calcula nada: devolve um objeto `DataFrameGroupBy`, uma promessa de agrupamento. O cálculo só acontece quando se aplica uma função — `.mean()`, `.sum()`, `.count()` etc.

#### Agrupando por várias colunas

```
df.groupby(["campus", "turno"])["nota_final"].mean()
```

O resultado tem um `MultiIndex`: um índice hierárquico, com um nível para cada coluna de agrupamento. Para "achatar" esse índice em uma tabela larga, com o segundo nível virando colunas, usa-se `.unstack()` — o assunto do Capítulo 3.

#### size() não é count()

Esta é a armadilha mais comum do capítulo:

- `df.groupby("campus").size()` — conta linhas do grupo, ausentes incluídos.
- `df.groupby("campus")["nota_final"].count()` — conta apenas os valores não ausentes daquela coluna específica.

```
tamanho   = df.groupby("campus").size()
contagem  = df.groupby("campus")["nota_final"].count()
ausentes  = tamanho - contagem   # quantos "sumiram" na coluna
```

No conjunto desta disciplina, Natal-Central tem 98 linhas mas apenas 87 notas presentes — a diferença (11) são os estudantes sem `nota_final`, e só aparece quando as duas contagens são comparadas lado a lado.

#### Iterando grupos (bastidores, raramente necessário)

```
for campus, grupo in df.groupby("campus"):
    print(campus, len(grupo), grupo["nota_final"].mean())
```

Serve para entender o mecanismo por dentro; no dia a dia, quase sempre há uma forma vetorizada (agg, pivot_table, apply) que resolve sem laço explícito.

## 2. Capítulo 2 — agg: várias estatísticas de uma vez

`.mean()` sozinho devolve um único número por grupo. Quando é preciso mais de uma estatística ao mesmo tempo, entra o `agg` (abreviação de aggregate).

#### Uma lista de funções

```
df.groupby("campus")["nota_final"].agg(["mean", "median", "std", "count"])
```

Cada string da lista é o nome de uma função conhecida do Pandas (`"mean"`, `"sum"`, `"min"`, `"max"`, `"std"`, `"count"`, `"nunique"` …). O resultado é uma tabela com uma coluna por estatística.

#### Várias colunas, cada uma com suas próprias funções

```
df.groupby("turno").agg({
    "nota_final": ["mean", "count"],
    "frequencia": "mean",
    "idade": "median",
})
```

Aqui o resultado tem colunas em MultiIndex: `("nota_final", "mean")`, `("nota_final", "count")` etc. Funciona, mas essas colunas de dois níveis são incômodas de referenciar depois (`resultado[("nota_final", "mean")]`).

#### Named aggregation — a forma recomendada

Desde o Pandas 0.25, é possível nomear cada coluna resultante diretamente:

```
df.groupby("turno").agg(
    nota_media=("nota_final", "mean"),
    nota_desvio=("nota_final", "std"),
    n_estudantes=("matricula", "count"),
    taxa_aprovacao=("situacao", lambda s: (s == "Aprovado").mean() * 100),
).round(2)
```

Cada argumento nomeado tem a forma `nome_da_coluna_de_saida=(coluna_de_origem, função)`. O resultado sai com colunas planas — `nota_media`, `n_estudantes` — prontas para usar em `sort_values`, gráficos ou um novo `merge`. Sempre que uma tabela de resumo precisar de nomes de coluna claros, esta é a forma preferida.

#### Uma lambda dentro do agg

`taxa_aprovacao=("situacao", lambda s: (s == "Aprovado").mean() * 100)` merece atenção: dentro do `agg`, `s` é a coluna daquele grupo — uma Series só com os valores de `situacao` daquele campus, por exemplo. `s == "Aprovado"` produz uma máscara booleana; `.mean()` dessa máscara é a proporção de `True`; multiplicar por 100 converte para percentual. É a mesma lógica de "máscara booleana + `.mean()`" da Aula 04, agora aplicada dentro de cada grupo.

## 3. Capítulo 3 — pivot_table: o groupby de duas dimensões

Quando o resultado que se quer é uma tabela "larga" — uma categoria nas linhas, outra nas colunas, um valor resumido em cada célula — `pivot_table` é o caminho mais direto.

#### A forma básica

```
df.pivot_table(values="nota_final", index="campus",
              columns="turno", aggfunc="mean")
```

Os quatro parâmetros centrais:

- `values` — a coluna que será resumida dentro de cada célula.
- `index` — a(s) coluna(s) que viram as linhas da tabela.
- `columns` — a(s) coluna(s) que viram as colunas da tabela.
- `aggfunc` — a função de resumo (`"mean"` por padrão, mas pode ser `"sum"`, `"count"`, uma lista, ou uma função personalizada).

#### É exatamente um groupby + unstack

```
df.groupby(["campus", "turno"])["nota_final"].mean().unstack("turno")
```

Este código produz o mesmo resultado do `pivot_table` acima. `pivot_table` é um atalho para esse padrão frequente: agrupar por duas colunas e "desempilhar" uma delas em colunas. Saber os dois caminhos ajuda a reconhecer a mesma operação escrita de formas diferentes.

#### fill_value e margins

```
df.pivot_table(values="matricula", index="campus", columns="situacao",
              aggfunc="count", fill_value=0,
              margins=True, margins_name="Total")
```

`fill_value=0` substitui por zero as combinações campus×situação que não ocorreram (em vez de `NaN`) — faz sentido aqui porque "zero estudantes nessa situação" é um valor válido, não um dado ausente. `margins=True` acrescenta uma linha e uma coluna de totais, o que serve como conferência: a soma das partes deve bater com o total geral.

#### Múltiplas funções de agregação

```
df.pivot_table(values="nota_final", index="turno", columns="modalidade",
              aggfunc=["mean", "count"])
```

Passar uma lista em `aggfunc` produz colunas em dois níveis (a função e depois a categoria) — útil para ver média e tamanho da amostra lado a lado, e lembrar que uma média sobre poucos casos merece menos confiança.

#### crosstab: quando só interessa contar

`pd.crosstab(df["turno"], df["situacao"])` é uma versão simplificada, dedicada a tabelas de contagem cruzando duas colunas categóricas — equivalente a um `pivot_table` com `aggfunc="count"`, mas com uma assinatura mais direta quando não se precisa de nenhum outro parâmetro.

## 4. Capítulo 4 — merge e join: combinando tabelas

Até aqui, cada tabela foi analisada isoladamente. Mas `matriculas_ifrn_2026.csv` só tem o nome do campus e do curso — os detalhes (região, número de docentes, eixo tecnológico, carga horária) estão em `campi_ifrn.xlsx`. `merge` é a operação que junta essas tabelas pela coluna em comum.

#### Merge muitos-para-um

```
df_campi = df.merge(campi, on="campus", how="left", validate="m:1")
df_completo = df_campi.merge(cursos, on="curso", how="left", validate="m:1")
```

Cada estudante (muitos) pertence a exatamente um campus (um) — por isso a relação é "muitos-para-um" (`m:1`). `on="campus"` diz qual coluna serve de chave de junção; ela precisa existir, com o mesmo nome e os mesmos valores, nas duas tabelas (é por isso que o `str.strip()` da Aula 04 é indispensável antes do merge — `" Mossoró "` não casaria com `"Mossoró"`).

#### validate: verificação, não correção

`validate="m:1"` não conserta nada — ele verifica que a tabela à direita (`campi`) tem no máximo uma linha por valor de chave. Se por engano `campi` tivesse duas linhas para "Mossoró", um merge sem `validate` duplicaria silenciosamente todas as linhas de estudantes daquele campus; com `validate="m:1"`, o Pandas levanta `MergeError` imediatamente. É uma rede de segurança barata que vale usar sempre que a cardinalidade da relação for conhecida.

#### how: o que fazer com quem não casa

   how |  Mantém |
  `"inner"` |  só as linhas cuja chave existe nas DUAS tabelas |
  `"left"` |  TODAS as linhas da tabela da esquerda; sem casamento, entra `NaN` |
  `"right"` |  todas as linhas da tabela da direita (o espelho de `"left"`) |
  `"outer"` |  todas as linhas de ambas, com `NaN` onde faltar |

```
cursos_parcial = cursos[cursos["eixo_tecnologico"] != "Informação e Comunicação"]

inner = df.merge(cursos_parcial, on="curso", how="inner")   # perde quem faz TI
left  = df.merge(cursos_parcial, on="curso", how="left")    # mantém todos, com NaN
```

`how="left"` é o padrão mais seguro quando o objetivo é enriquecer uma tabela principal sem perder nenhuma de suas linhas — é o que se quer ao juntar matrículas com campi ou cursos.

#### Auditando o resultado com indicator=True

```
checagem = df.merge(cursos, on="curso", how="left", indicator=True)
checagem["_merge"].value_counts()
```

A coluna `_merge` (valores `"both"`, `"left_only"`, `"right_only"`) é a forma mais direta de confirmar que um merge se comportou como esperado — especialmente útil quando as chaves vêm de fontes diferentes e podem ter pequenas divergências de grafia.

#### join(): atalho quando a chave é o índice

```
campi_idx = campi.set_index("campus")
df.join(campi_idx[["regiao", "num_docentes"]], on="campus")
```

`join` é essencialmente um `merge` especializado para o caso em que a tabela da direita já está indexada pela chave de junção. O parâmetro `on` diz qual coluna de `df` deve ser comparada com o índice de `campi_idx`.

## 5. Capítulo 5 — apply, lambda e por que vetorizar continua vencendo

#### apply em uma única coluna

```
df["situacao_curta"] = df["situacao"].apply(
    lambda s: "OK" if s == "Aprovado" else "Não-OK")
```

`Series.apply(funcao)` chama `funcao` uma vez para cada valor da coluna e monta uma nova Series com os retornos. É flexível — a função pode ter qualquer lógica — mas paga o preço de rodar em Python puro, elemento a elemento.

#### apply(axis=1): uma linha inteira por vez

```
def classificar(linha):
    if pd.isna(linha["nota_final"]):
        return "Sem nota"
    if linha["nota_final"] >= 85 and linha["frequencia"] >= 90:
        return "Destaque"
    if linha["nota_final"] >= 60:
        return "Regular"
    return "Atenção"

df["perfil"] = df.apply(classificar, axis=1)
```

Com `axis=1`, cada chamada de `classificar` recebe uma linha inteira (uma Series com todas as colunas), o que permite combinar várias colunas numa mesma regra. É a ferramenta certa quando a lógica é condicional demais para caber em uma única expressão vetorizada — mas é também a forma mais lenta de operar em um DataFrame, porque o Pandas monta uma Series por linha antes de cada chamada.

#### A mesma regra, vetorizada

```
condicoes = [
    df["nota_final"].isna(),
    (df["nota_final"] >= 85) & (df["frequencia"] >= 90),
    df["nota_final"] >= 60,
]
valores = ["Sem nota", "Destaque", "Regular"]
df["perfil_v2"] = np.select(condicoes, valores, default="Atenção")
```

`np.select` testa uma lista de condições, na ordem, e devolve o valor correspondente à primeira verdadeira — exatamente a lógica do `if/elif/else` de `classificar`, mas avaliada sobre a coluna inteira de uma vez. Em uma base de alguns milhares de linhas a diferença é imperceptível; em milhões de linhas, pode ser a diferença entre segundos e minutos.

#### Quando usar cada um

- Existe uma expressão vetorizada direta (comparação, `np.where`, `np.select`, operação aritmética)? Use-a.
- A lógica depende de várias colunas de forma difícil de expressar sem `if`, ou chama uma função externa complexa (uma API, um modelo)? `apply` é aceitável — comece por ele, otimize depois se o desempenho importar.
- Um laço `for` explícito percorrendo `df.iterrows()` quase nunca é a resposta certa: é ainda mais lento que `apply` e existe quase sempre um caminho vetorizado ou um `apply` mais direto.

#### lambda não é exclusivo do apply

As mesmas funções anônimas aparecem dentro de `agg` (Capítulo 2), de `assign` e de `sort_values(key=...)`. O padrão é sempre o mesmo: `lambda argumento: expressão`, uma forma compacta de escrever uma função de uma linha sem precisar de `def` em outro lugar do código.

## 6. Capítulo 6 — method chaining e pipe

#### O problema das variáveis intermediárias

Uma análise de vários passos, escrita "passo a passo", costuma acumular nomes de variáveis que só servem de ponte:

```
tmp1 = df_completo[df_completo["situacao"] != "Trancado"]
tmp2 = tmp1.copy()
tmp2["aprovado"] = tmp2["situacao"] == "Aprovado"
tmp3 = tmp2.groupby(["regiao", "eixo_tecnologico"])
tmp4 = tmp3.agg(n=("matricula", "count"), taxa_aprovacao=("aprovado", "mean"))
tmp5 = tmp4[tmp4["n"] >= 10]
resultado = tmp5.sort_values("taxa_aprovacao", ascending=False)
```

Funciona, mas cada `tmpN` é uma oportunidade de erro: usar `tmp2` onde deveria ser `tmp3`, esquecer de atualizar uma referência depois de editar o código no meio.

#### A mesma sequência, encadeada

```
resultado = (
    df_completo
    .query("situacao != 'Trancado'")
    .assign(aprovado=lambda d: d["situacao"] == "Aprovado")
    .groupby(["regiao", "eixo_tecnologico"])
    .agg(n=("matricula", "count"), taxa_aprovacao=("aprovado", "mean"))
    .query("n >= 10")
    .sort_values("taxa_aprovacao", ascending=False)
)
```

Os parênteses externos permitem quebrar a expressão em várias linhas sem usar `\`. Cada método devolve um novo objeto, sobre o qual o próximo método é chamado — uma leitura de cima para baixo que corresponde exatamente à ordem das transformações: filtrar, criar coluna, agrupar, agregar, filtrar de novo, ordenar.

#### Duas peças que tornam o encadeamento possível

- `query("expressão")` — filtra linhas usando uma condição escrita como texto, sem precisar repetir o nome do DataFrame nem usar `&`/`|` com parênteses (compare com `df[(df["nota"] > 5) & (df["turno"] == "Noturno")]` contra `df.query("nota > 5 and turno == 'Noturno'")`).
- `assign(coluna=lambda d: expressão)` — cria (ou substitui) uma coluna sem precisar de uma atribuição `df["coluna"] = ...` separada. O `lambda d: ...` recebe o DataFrame naquele ponto da cadeia — não o `df_completo` original — o que é essencial quando uma etapa anterior já filtrou ou transformou os dados.

#### .pipe(): encaixando sua própria função na cadeia

```
def com_faixa_carga(d):
    d = d.copy()
    d["carga_faixa"] = pd.cut(d["carga_horaria"],
                              bins=[0, 1200, 1800, 3000],
                              labels=["Até 1200h", "1201–1800h", "Acima de 1800h"])
    return d

resultado2 = (
    df_completo
    .pipe(com_faixa_carga)
    .groupby("carga_faixa", observed=True)["nota_final"]
    .mean()
)
```

Quando uma etapa é complexa demais para uma `lambda` de uma linha, `.pipe(funcao)` deixa continuar a cadeia chamando uma função nomeada — a função recebe o DataFrame corrente e devolve o próximo, exatamente como qualquer outro método da cadeia. É a forma recomendada de misturar lógica personalizada com method chaining, em vez de "sair" da cadeia com uma variável intermediária.

#### Quando NÃO encadear

Method chaining melhora a leitura quando os passos são poucos e formam uma narrativa clara. Uma cadeia de dez ou mais métodos, ou que precisa ser depurada com frequência (inspecionar o resultado no meio do caminho), costuma ficar mais clara quebrada em duas ou três variáveis com nomes que dizem o que cada etapa representa. A regra não é "sempre encadear" — é "encadear quando isso deixa a intenção mais legível, não menos".