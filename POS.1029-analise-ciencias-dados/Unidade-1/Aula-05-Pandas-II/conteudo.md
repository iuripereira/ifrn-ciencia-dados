# Aula 05 — Laboratório Pandas II — Agrupamentos e Joins (Prática)

> groupby, agg (named aggregation), pivot_table, merge/join, apply e lambda, introdução ao method chaining.
> Recursos: Jupyter Notebook, mesmo conjunto de dados da Aula 04 (matrículas do IFRN — **dados sintéticos**).
> Avaliação: exercício prático entregue no Moodle + formulário avaliativo com 10 questões (pode ser refeito; vale a maior nota).
> Materiais: livro (6 capítulos, abaixo) · apostila PDF (26 p., link no README da Unidade) · pacote ZIP com notebook e dados · exemplo prático comentado · tarefa · formulário.

---

# Livro — Tópicos de Estudo

## Capítulo 1 — groupby: dividir, aplicar, combinar

Na Aula 04 respondemos "qual a nota média por campus?" com um único `groupby`. Esta aula aprofunda essa ferramenta e acrescenta `agg`, `pivot_table`, `merge`, `apply` e o estilo de method chaining.

### O padrão split-apply-combine

1. **Dividir (split)** — o DataFrame é particionado em grupos, um por valor distinto da(s) coluna(s) de agrupamento.
2. **Aplicar (apply)** — uma função (média, contagem, soma, personalizada) roda em cada grupo.
3. **Combinar (combine)** — os resultados são reunidos em uma única Series ou DataFrame.

`df.groupby("campus")["nota_final"].mean()` equivale a um laço sobre cada campus calculando a média do subconjunto — só que vetorizado e muito mais rápido.

### Agrupando por uma coluna

```python
media_por_campus = df.groupby("campus")["nota_final"].mean().round(2)
media_por_campus.sort_values(ascending=False)
```

`df.groupby("campus")` sozinho não calcula nada: devolve um `DataFrameGroupBy`, uma promessa de agrupamento. O cálculo só acontece ao aplicar `.mean()`, `.sum()`, `.count()` etc.

### Agrupando por várias colunas

```python
df.groupby(["campus", "turno"])["nota_final"].mean()
```

O resultado tem um **MultiIndex** (um nível por coluna de agrupamento). Para achatá-lo em tabela larga, `.unstack()` — Capítulo 3.

### size() não é count()

- `df.groupby("campus").size()` — conta **linhas** do grupo, ausentes incluídos.
- `df.groupby("campus")["nota_final"].count()` — conta apenas valores **não ausentes** daquela coluna.

```python
tamanho   = df.groupby("campus").size()
contagem  = df.groupby("campus")["nota_final"].count()
ausentes  = tamanho - contagem   # quantos "sumiram" na coluna
```

Natal-Central tem 98 linhas mas apenas 87 notas presentes — a diferença (11) só aparece comparando as duas contagens.

### Iterando grupos (bastidores, raramente necessário)

```python
for campus, grupo in df.groupby("campus"):
    print(campus, len(grupo), grupo["nota_final"].mean())
```

## Capítulo 2 — agg: várias estatísticas de uma vez

### Uma lista de funções

```python
df.groupby("campus")["nota_final"].agg(["mean", "median", "std", "count"])
```

### Várias colunas, cada uma com suas funções

```python
df.groupby("turno").agg({
    "nota_final": ["mean", "count"],
    "frequencia": "mean",
    "idade": "median",
})
```

Resultado com colunas em MultiIndex — `("nota_final", "mean")` — incômodas de referenciar depois.

### Named aggregation — a forma recomendada

```python
df.groupby("turno").agg(
    nota_media=("nota_final", "mean"),
    nota_desvio=("nota_final", "std"),
    n_estudantes=("matricula", "count"),
    taxa_aprovacao=("situacao", lambda s: (s == "Aprovado").mean() * 100),
).round(2)
```

Forma `nome_da_coluna_de_saida=(coluna_de_origem, função)`. Colunas planas, prontas para `sort_values`, gráficos ou novo `merge`.

### Uma lambda dentro do agg

Em `taxa_aprovacao=("situacao", lambda s: (s == "Aprovado").mean() * 100)`, `s` é a coluna **daquele grupo**. `s == "Aprovado"` produz máscara booleana; `.mean()` é a proporção de `True`; `* 100` vira percentual — a lógica "máscara + mean" da Aula 04, aplicada por grupo.

## Capítulo 3 — pivot_table: o groupby de duas dimensões

```python
df.pivot_table(values="nota_final", index="campus",
               columns="turno", aggfunc="mean")
```

- `values` — coluna resumida em cada célula.
- `index` — vira as linhas.
- `columns` — vira as colunas.
- `aggfunc` — função de resumo (`"mean"` padrão; `"sum"`, `"count"`, lista ou função).

### É exatamente um groupby + unstack

```python
df.groupby(["campus", "turno"])["nota_final"].mean().unstack("turno")
```

### fill_value e margins

```python
df.pivot_table(values="matricula", index="campus", columns="situacao",
               aggfunc="count", fill_value=0,
               margins=True, margins_name="Total")
```

`fill_value=0` troca `NaN` por zero nas combinações inexistentes — válido porque "zero estudantes" é valor real, não ausente. `margins=True` acrescenta totais — conferência: a soma das partes deve bater com o total.

### Múltiplas funções

```python
df.pivot_table(values="nota_final", index="turno", columns="modalidade",
               aggfunc=["mean", "count"])
```

Útil para ver média e tamanho da amostra lado a lado: média sobre poucos casos merece menos confiança.

### crosstab

`pd.crosstab(df["turno"], df["situacao"])` — tabela de contagem cruzada, equivalente a `pivot_table(aggfunc="count")` com assinatura mais direta.

## Capítulo 4 — merge e join: combinando tabelas

`matriculas_ifrn_2026.csv` só tem nome do campus e do curso; região, docentes, eixo e carga horária estão em `campi_ifrn.xlsx`.

### Merge muitos-para-um

```python
df_campi = df.merge(campi, on="campus", how="left", validate="m:1")
df_completo = df_campi.merge(cursos, on="curso", how="left", validate="m:1")
```

Cada estudante (muitos) pertence a um campus (um): relação `m:1`. A chave `on` precisa existir com o mesmo nome e os mesmos valores nas duas tabelas — por isso o `str.strip()` da Aula 04 é indispensável (`" Mossoró "` não casa com `"Mossoró"`).

### validate: verificação, não correção

`validate="m:1"` verifica que `campi` tem no máximo uma linha por chave. Se houvesse duas linhas para "Mossoró", um merge sem `validate` **duplicaria silenciosamente** os estudantes daquele campus; com `validate`, o Pandas levanta `MergeError`. Rede de segurança barata.

### how: o que fazer com quem não casa

| how | Mantém |
|---|---|
| `"inner"` | só linhas cuja chave existe nas DUAS tabelas |
| `"left"` | TODAS as linhas da esquerda; sem casamento, `NaN` |
| `"right"` | todas as da direita |
| `"outer"` | todas de ambas, `NaN` onde faltar |

```python
cursos_parcial = cursos[cursos["eixo_tecnologico"] != "Informação e Comunicação"]

inner = df.merge(cursos_parcial, on="curso", how="inner")   # perde quem faz TI
left  = df.merge(cursos_parcial, on="curso", how="left")    # mantém todos, com NaN
```

`how="left"` é o padrão mais seguro para **enriquecer** uma tabela principal sem perder linhas.

### Auditando com indicator=True

```python
checagem = df.merge(cursos, on="curso", how="left", indicator=True)
checagem["_merge"].value_counts()
```

Coluna `_merge` (`both`, `left_only`, `right_only`) confirma o comportamento do merge.

### join(): atalho quando a chave é o índice

```python
campi_idx = campi.set_index("campus")
df.join(campi_idx[["regiao", "num_docentes"]], on="campus")
```

## Capítulo 5 — apply, lambda e por que vetorizar continua vencendo

### apply em uma coluna

```python
df["situacao_curta"] = df["situacao"].apply(
    lambda s: "OK" if s == "Aprovado" else "Não-OK")
```

Chama a função uma vez por valor — flexível, mas em Python puro, elemento a elemento.

### apply(axis=1): uma linha inteira por vez

```python
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

Permite combinar várias colunas numa regra — mas é a forma mais lenta: o Pandas monta uma Series por linha.

### A mesma regra, vetorizada

```python
condicoes = [
    df["nota_final"].isna(),
    (df["nota_final"] >= 85) & (df["frequencia"] >= 90),
    df["nota_final"] >= 60,
]
valores = ["Sem nota", "Destaque", "Regular"]
df["perfil_v2"] = np.select(condicoes, valores, default="Atenção")
```

`np.select` testa as condições em ordem e devolve o valor da primeira verdadeira — o `if/elif/else` sobre a coluna inteira. Em milhões de linhas, é a diferença entre segundos e minutos.

### Quando usar cada um

- Existe expressão vetorizada direta (comparação, `np.where`, `np.select`, aritmética)? **Use-a.**
- Lógica difícil sem `if` ou chamada externa complexa (API, modelo)? `apply` é aceitável — otimize depois se necessário.
- `for` sobre `df.iterrows()` quase nunca é a resposta: mais lento que `apply`.

### lambda não é exclusivo do apply

Aparece em `agg`, `assign` e `sort_values(key=...)`: `lambda argumento: expressão`.

## Capítulo 6 — method chaining e pipe

### O problema das variáveis intermediárias

```python
tmp1 = df_completo[df_completo["situacao"] != "Trancado"]
tmp2 = tmp1.copy()
tmp2["aprovado"] = tmp2["situacao"] == "Aprovado"
tmp3 = tmp2.groupby(["regiao", "eixo_tecnologico"])
tmp4 = tmp3.agg(n=("matricula", "count"), taxa_aprovacao=("aprovado", "mean"))
tmp5 = tmp4[tmp4["n"] >= 10]
resultado = tmp5.sort_values("taxa_aprovacao", ascending=False)
```

Cada `tmpN` é oportunidade de erro.

### A mesma sequência, encadeada

```python
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

Parênteses externos permitem quebrar linhas sem `\`. Leitura de cima para baixo = ordem das transformações.

### Duas peças que tornam o encadeamento possível

- **`query("expressão")`** — filtra por condição em texto, sem repetir o nome do DataFrame nem `&`/`|` com parênteses.
- **`assign(coluna=lambda d: expressão)`** — cria coluna sem atribuição separada. O `d` é o DataFrame **naquele ponto da cadeia**, não o original.

### .pipe(): encaixando sua própria função

```python
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

### Quando NÃO encadear

Cadeias de dez ou mais métodos, ou que precisam ser depuradas com frequência, ficam mais claras quebradas em duas ou três variáveis com nomes significativos. Regra: encadear quando deixa a intenção **mais** legível.

---

# Exemplo Prático — Agrupamentos, Joins e Method Chaining (`exemplo_pandas2.py`)

Usa os mesmos dados da Aula 04 e o pacote Laboratório (ZIP). Salve ao lado da pasta `dados/` ou copie bloco a bloco para um notebook.

> Dados sintéticos. Os números servem para conferir o seu ambiente, não para concluir sobre o IFRN.

### Passo 0 — Recapitulando leitura e limpeza

```python
df = pd.read_csv("dados/matriculas_ifrn_2026.csv", sep=";", decimal=",",
                 encoding="utf-8", dtype={"matricula": "string"})
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)

campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")

print(f"matrículas: {df.shape} | campi: {campi.shape} | cursos: {cursos.shape}")
# matrículas: (480, 12) | campi: (12, 5) | cursos: (10, 4)
```

### Passo 1 — groupby

```python
media_por_campus = df.groupby("campus")["nota_final"].mean().round(2)
media_por_campus.sort_values(ascending=False)
# Santa Cruz        74.55
# Currais Novos     72.28
# Apodi             71.69
# ...
# João Câmara       63.78

tamanho   = df.groupby("campus").size()
contagem  = df.groupby("campus")["nota_final"].count()
ausentes  = tamanho - contagem
#                   linhas  notas_presentes  ausentes
# Natal-Central         98               87        11
# Mossoró               70               62         8
```

### Passo 2 — agg

```python
df.groupby("turno").agg(
    nota_media=("nota_final", "mean"),
    nota_desvio=("nota_final", "std"),
    n_estudantes=("matricula", "count"),
    taxa_aprovacao=("situacao", lambda s: (s == "Aprovado").mean() * 100),
).round(2)
#             nota_media  nota_desvio  n_estudantes  taxa_aprovacao
# Matutino         70.90        12.05           150           65.33
# Noturno          66.76        12.47           214           55.14
# Vespertino       71.62        12.12           116           56.03
```

### Passo 3 — pivot_table

```python
tabela = df.pivot_table(values="nota_final", index="campus", columns="turno", aggfunc="mean").round(1)
#                Matutino  Noturno  Vespertino
# Apodi              69.9     72.0        73.7
# Caicó              68.0     72.4        67.9

via_groupby = df.groupby(["campus","turno"])["nota_final"].mean().unstack("turno").round(1)
print("Equivalente ao pivot_table?", via_groupby.equals(tabela))   # True

df.pivot_table(values="matricula", index="campus", columns="situacao",
               aggfunc="count", fill_value=0, margins=True, margins_name="Total")
#             Aprovado  Em curso  Reprovado por falta  Reprovado por nota  Trancado  Total
# Total            281        14                   72                  86        27    480
```

### Passo 4 — merge / join

```python
df_campi    = df.merge(campi, on="campus", how="left", validate="m:1")
df_completo = df_campi.merge(cursos, on="curso", how="left", validate="m:1")
print(df_completo[["regiao","eixo_tecnologico"]].isna().sum())
# regiao              0
# eixo_tecnologico    0   -> nenhum merge "furou"

cursos_sem_ti = cursos[cursos["eixo_tecnologico"] != "Informação e Comunicação"]
inner = df.merge(cursos_sem_ti, on="curso", how="inner")
left  = df.merge(cursos_sem_ti, on="curso", how="left")
# inner: 271 linhas (só cursos que casaram)
# left : 480 linhas (todas as linhas de df, com NaN onde não casou)
# NaN em "eixo_tecnologico" no left: 209

checagem = df.merge(cursos, on="curso", how="left", indicator=True)
checagem["_merge"].value_counts()
# both          480
# left_only       0
# right_only      0   -> todo curso de df tem correspondência
```

### Passo 5 — apply, lambda e method chaining

```python
condicoes = [df_completo["nota_final"].isna(),
             (df_completo["nota_final"] >= 85) & (df_completo["frequencia"] >= 90),
             df_completo["nota_final"] >= 60]
valores = ["Sem nota", "Destaque", "Regular"]
df_completo["perfil_vetorizado"] = np.select(condicoes, valores, default="Atenção")
print((df_completo["perfil"] == df_completo["perfil_vetorizado"]).all())   # True
# apply(axis=1) e a versão vetorizada concordam em 100% das linhas

resultado = (
    df_completo
    .query("situacao != 'Trancado'")
    .assign(aprovado=lambda d: d["situacao"] == "Aprovado")
    .groupby(["regiao", "eixo_tecnologico"])
    .agg(n_estudantes=("matricula","count"), taxa_aprovacao=("aprovado","mean"),
         nota_media=("nota_final","mean"))
    .round(3)
    .query("n_estudantes >= 10")
    .sort_values("taxa_aprovacao", ascending=False)
)
#                                           n_estudantes  taxa_aprovacao  nota_media
# Metropolitana  Produção Industrial                  12           0.917      75.508
# Oeste          Recursos Naturais                    14           0.857      78.162
# Oeste          Gestão e Negócios                    19           0.842      69.232
```

> A coluna `perfil` (via `apply(classificar, axis=1)`, Cap. 5) precisa ter sido criada em `df_completo` antes da comparação.

### Passo 6 — Respondendo uma pergunta mais rica

```python
resposta = (
    df_completo
    .assign(aprovado=lambda d: (d["situacao"] == "Aprovado").astype(int))
    .groupby(["campus", "eixo_tecnologico"])
    .agg(n=("matricula","count"), taxa_aprovacao=("aprovado","mean"))
    .query("n >= 8")
    .assign(taxa_aprovacao=lambda d: (d["taxa_aprovacao"]*100).round(1))
    .sort_values("taxa_aprovacao", ascending=False)
)
#                                          n  taxa_aprovacao
# Mossoró        Gestão e Negócios        13            84.6
# Apodi          Informação e Comunicação 16            75.0
# Parnamirim     Controle e Processos     11            72.7
```

Mesmo ceticismo da Aula 04: tamanhos de grupo variam (8 a dezenas), dados sintéticos, e 84,6% sobre 13 estudantes tem margem de incerteza grande. O valor do `groupby` aqui é organizar a pergunta de forma que a resposta possa ser **auditada linha por linha**.

---

# Exercício Prático — Aula 05 (entrega do notebook)

Aberto: segunda-feira, 21/09/2026, 00:00 · 10 questões, 10,0 pontos. Detalhes em `atividade/README.md`.

# Formulário Avaliativo — Aula 05

10 questões objetivas sobre groupby, agg, pivot_table, merge/join, apply/lambda e method chaining. Pode ser refeito; considera-se a maior nota. Link: https://presencial.ava.ifrn.edu.br/mod/quiz/view.php?id=73625
