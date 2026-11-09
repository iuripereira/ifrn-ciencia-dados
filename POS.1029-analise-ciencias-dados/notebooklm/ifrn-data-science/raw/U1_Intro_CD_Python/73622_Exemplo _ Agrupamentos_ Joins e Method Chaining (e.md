# Exemplo — Agrupamentos, Joins e Method Chaining (e

Este é o roteiro guiado da Aula 05. Ele usa os mesmos dados da Aula 04 (reaproveitados de propósito) e o pacote 🗂️ Laboratório — Notebook e conjuntos de dados (ZIP). Salve o código como `exemplo_pandas2.py` ao lado da pasta `dados/`, ou copie bloco a bloco para um notebook.

Lembrete: os dados são sintéticos. Os números abaixo servem para você conferir se o seu ambiente está produzindo o mesmo resultado — não para tirar conclusões sobre o IFRN.

#### Passo 0 — Recapitulando a leitura e limpeza da Aula 04

```
df = pd.read_csv("dados/matriculas_ifrn_2026.csv", sep=";", decimal=",",
                 encoding="utf-8", dtype={"matricula": "string"})
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)

campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")

print(f"matrículas: {df.shape} | campi: {campi.shape} | cursos: {cursos.shape}")
# matrículas: (480, 12) | campi: (12, 5) | cursos: (10, 4)
```

#### Passo 1 — groupby

```
media_por_campus = df.groupby("campus")["nota_final"].mean().round(2)
media_por_campus.sort_values(ascending=False)
# Santa Cruz        74.55
# Currais Novos     72.28
# Apodi             71.69
# ...
# João Câmara       63.78
```

`groupby(["campus", "turno"])["nota_final"].mean()` produz um MultiIndex. E a armadilha do capítulo:

```
tamanho   = df.groupby("campus").size()
contagem  = df.groupby("campus")["nota_final"].count()
ausentes  = tamanho - contagem
#                   linhas  notas_presentes  ausentes
# Natal-Central         98               87        11
# Mossoró               70               62         8
```

#### Passo 2 — agg

```
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

#### Passo 3 — pivot_table

```
df.pivot_table(values="nota_final", index="campus", columns="turno", aggfunc="mean").round(1)
#                Matutino  Noturno  Vespertino
# Apodi              69.9     72.0        73.7
# Caicó              68.0     72.4        67.9

via_groupby = df.groupby(["campus","turno"])["nota_final"].mean().unstack("turno").round(1)
print("Equivalente ao pivot_table?", via_groupby.equals(tabela))  # True
```

```
df.pivot_table(values="matricula", index="campus", columns="situacao",
               aggfunc="count", fill_value=0, margins=True, margins_name="Total")
#             Aprovado  Em curso  Reprovado por falta  Reprovado por nota  Trancado  Total
# Total            281        14                    72                  86        27    480
```

#### Passo 4 — merge / join

```
df_campi    = df.merge(campi, on="campus", how="left", validate="m:1")
df_completo = df_campi.merge(cursos, on="curso", how="left", validate="m:1")
print(df_completo[["regiao","eixo_tecnologico"]].isna().sum())
# regiao              0
# eixo_tecnologico    0   -> nenhum merge "furou"
```

```
cursos_sem_ti = cursos[cursos["eixo_tecnologico"] != "Informação e Comunicação"]
inner = df.merge(cursos_sem_ti, on="curso", how="inner")
left  = df.merge(cursos_sem_ti, on="curso", how="left")
# inner: 271 linhas (só cursos que casaram)
# left : 480 linhas (todas as linhas de df, com NaN onde não casou)
# NaN em "eixo_tecnologico" no left: 209
```

```
checagem = df.merge(cursos, on="curso", how="left", indicator=True)
checagem["_merge"].value_counts()
# both          480
# left_only       0
# right_only      0   -> confirma que todo curso de df tem correspondência
```

#### Passo 5 — apply, lambda e method chaining

```
condicoes = [df_completo["nota_final"].isna(),
             (df_completo["nota_final"] >= 85) & (df_completo["frequencia"] >= 90),
             df_completo["nota_final"] >= 60]
valores = ["Sem nota", "Destaque", "Regular"]
df_completo["perfil_vetorizado"] = np.select(condicoes, valores, default="Atenção")
print((df_completo["perfil"] == df_completo["perfil_vetorizado"]).all())  # True
# apply(axis=1) e a versão vetorizada concordam em 100% das linhas
```

```
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
#                                          n_estudantes  taxa_aprovacao  nota_media
# Metropolitana  Produção Industrial                 12           0.917      75.508
# Oeste          Recursos Naturais                   14           0.857      78.162
# Oeste          Gestão e Negócios                   19           0.842      69.232
```

#### Passo 6 — Respondendo uma pergunta mais rica

```
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

Leia o resultado com o mesmo ceticismo da Aula 04: os tamanhos de grupo variam bastante (de 8 a dezenas de estudantes), os dados são sintéticos, e uma taxa de aprovação de 84,6% sobre 13 estudantes tem uma margem de incerteza grande. O valor do `groupby` aqui não é produzir um ranking definitivo — é organizar a pergunta de forma que a resposta possa ser auditada linha por linha.

Última atualização automática ao publicar esta página.

Última atualização: segunda-feira, 21 set. 2026, 09:09