# Aula09_Qualidade_e_Limpeza_de_Dados.ipynb

# Aula 09 — Qualidade de Dados e Limpeza

**Unidade 2 — Aquisição e Preparação de Dados** · Análise e Ciência de Dados (Especialização, IFRN)

Nas Aulas 06 a 08 aprendemos a **obter** dados (arquivos, APIs, web scraping). Dados obtidos quase nunca chegam prontos: têm valores faltando, registros repetidos, textos escritos de jeitos diferentes, unidades trocadas e erros de digitação. Esta aula mostra, passo a passo, como **diagnosticar** e **corrigir** esses problemas com Pandas.

**Dados da aula:** `dados/atendimentos_ubs_sujo.csv` — 250 registros **sintéticos** de atendimentos em Unidades Básicas de Saúde (UBS) de cinco municípios do RN. Nenhum dado é de paciente real: tudo foi sorteado por um script com semente fixa (`gerar_dados.py`) e os problemas foram inseridos de propósito.

Roteiro: diagnóstico → duplicatas → texto e categorias → datas → unidades → códigos sentinela → outliers (IQR e z-score) → valores ausentes → normalização e padronização → tidy data → salvar.

> **Instalação:** `pip install pandas numpy matplotlib`

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

pd.set_option("display.width", 130)
pd.set_option("display.max_columns", 12)
DADOS = Path("dados")

df = pd.read_csv(DADOS / "atendimentos_ubs_sujo.csv")
print(df.shape)
print(df.head(6).to_string())
```
Saída:
```
(250, 10)
   id_atendimento data_atendimento   municipio       sexo  idade  peso_kg  altura_cm  pressao_sistolica  glicemia_mg_dl         diagnostico
0            1149       2026-06-07       Natal  Masculino   86.0     85.2     171.00              133.0             NaN         Hipertensão
1            1220       2026-03-23  Parnamirim          M   41.0     90.5     171.00              131.0            89.0  Consulta de rotina
2            1095       08/05/2026  parnamirim          F   63.0     65.6     159.00              128.0           105.0         Hipertensão
3            1085       2026-06-08       Natal          M   23.0     80.8       1.59              124.0           105.0  Consulta de rotina
4            1004       2026-03-24       Natal          F   64.0     65.8     157.00              130.0           174.0            Diabetes
5            1122       2026-06-03       Natal          M   55.0     86.3     175.00              136.0           202.0            Diabetes

```

## Parte 1 — Diagnóstico: antes de limpar, meça

Nunca comece corrigindo: primeiro **meça** a qualidade. Quatro perguntas rápidas:

1. Quantos valores faltam em cada coluna? (`isna().sum()`)
2. Há linhas repetidas? (`duplicated().sum()`)
3. Os números fazem sentido? (`describe()` — olhe mínimo e máximo)
4. As categorias estão escritas de um único jeito? (`value_counts()`)

```python
ausentes = df.isna().sum()
pd.DataFrame({"ausentes": ausentes, "percentual": (ausentes / len(df) * 100).round(1)})
```
Saída:
```
                   ausentes  percentual
id_atendimento            0         0.0
data_atendimento          0         0.0
municipio                 0         0.0
sexo                      6         2.4
idade                     7         2.8
peso_kg                  12         4.8
altura_cm                 0         0.0
pressao_sistolica         6         2.4
glicemia_mg_dl           24         9.6
diagnostico               0         0.0
```

```python
print("Linhas duplicadas (idênticas):", df.duplicated().sum())
print()
print(df.describe().round(1).to_string())
```
Saída:
```
Linhas duplicadas (idênticas): 10

       id_atendimento  idade  peso_kg  altura_cm  pressao_sistolica  glicemia_mg_dl
count           250.0  243.0    238.0      250.0              244.0           226.0
mean           1120.2   54.0   1050.1      157.6              134.9           132.6
std              69.4   23.8   8805.0       31.4               79.1           146.2
min            1001.0   -3.0     35.3        1.6               12.0            62.0
25%            1060.2   37.0     60.2      156.2              119.0            91.0
50%            1120.5   53.0     72.1      162.5              128.0           101.0
75%            1179.8   70.0     84.5      170.0              141.0           115.0
max            1240.0  205.0  90900.0      185.0             1300.0           999.0

```

O `describe()` já denuncia vários problemas: idade **mínima de −3** e **máxima de 205** anos; peso **máximo de 90.900 kg**; altura **mínima de 1,6 cm**; pressão sistólica entre **12** e **1.300** mmHg; glicemia **máxima de 999**. Nenhum desses valores é possível num ser humano — são erros de digitação, de unidade ou códigos especiais.

```python
print(df["municipio"].value_counts().to_string())
print()
print(df["sexo"].value_counts(dropna=False).to_string())
```
Saída:
```
municipio
Natal             95
Mossoró           48
Parnamirim        36
Caicó             21
Pau dos Ferros    18
natal              7
parnamirim         5
pau dos ferros     4
Natal              4
Caico              3
mossoró            2
Mossoro            2
MOSSORÓ            1
PARNAMIRIM         1
caicó              1
Pau Dos Ferros     1
 NATAL             1

sexo
F            124
M             96
Masculino      7
FEMININO       6
NaN            6
Feminino       4
m              4
f              3

```

Para o computador, `"Natal"`, `"natal"`, `" NATAL"` e `"Natal "` (com espaço no fim) são **quatro municípios diferentes**. Se agruparmos sem limpar, Natal aparece fatiada em quatro linhas.

## Parte 2 — Duplicatas

`duplicated()` marca as linhas que repetem uma linha anterior (em **todas** as colunas, por padrão). Com `keep=False` ela marca todas as cópias, o que ajuda a inspecionar. Depois de remover, conferimos se o identificador do atendimento ficou único.

```python
copias = df[df.duplicated(keep=False)].sort_values("id_atendimento")
print(copias[["id_atendimento", "data_atendimento", "municipio", "idade", "diagnostico"]].head(6).to_string())

antes = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print(f"\nRemovidas {antes - len(df)} linhas duplicadas -> {len(df)} linhas")
print("id_atendimento é único?", df["id_atendimento"].is_unique)
```
Saída:
```
     id_atendimento data_atendimento municipio  idade         diagnostico
82             1016       2026-04-12     Natal   30.0  Consulta de rotina
246            1016       2026-04-12     Natal   30.0  Consulta de rotina
157            1037       2026-04-08     Natal   29.0         Hipertensão
87             1037       2026-04-08     Natal   29.0         Hipertensão
178            1041       2026-04-29   Mossoró   79.0         Hipertensão
71             1041       2026-04-29   Mossoró   79.0         Hipertensão

Removidas 10 linhas duplicadas -> 240 linhas
id_atendimento é único? True

```

## Parte 3 — Padronizando texto e categorias

A receita é: **tirar espaços** (`str.strip`), **uniformizar maiúsculas/minúsculas** (`str.title`, `str.upper`...) e, por fim, **mapear** as variações que sobraram para um valor oficial (`replace`/`map`).

```python
df["municipio"] = (df["municipio"].str.strip().str.title()
                   .replace({"Mossoro": "Mossoró", "Caico": "Caicó", "Pau Dos Ferros": "Pau dos Ferros"}))

df["sexo"] = (df["sexo"].str.strip().str.upper().str[0]      # 'Feminino' -> 'F', 'm' -> 'M'
              .fillna("Não informado"))

df["diagnostico"] = (df["diagnostico"].str.strip().str.lower()
                     .replace({"hipertensao": "hipertensão",
                               "infeccao respiratoria": "infecção respiratória"})
                     .str.capitalize())

print(df["municipio"].value_counts().to_string()); print()
print(df["sexo"].value_counts().to_string()); print()
print(df["diagnostico"].value_counts().to_string())
```
Saída:
```
municipio
Natal             101
Mossoró            51
Parnamirim         42
Caicó              25
Pau dos Ferros     21

sexo
F                133
M                101
Não informado      6

diagnostico
Consulta de rotina       88
Hipertensão              71
Infecção respiratória    42
Diabetes                 39

```

Repare que no `sexo` tratamos o ausente de um jeito **explícito** ("Não informado") em vez de inventar um valor: para uma variável categórica, chutar F ou M distorceria a análise.

## Parte 4 — Datas em formatos misturados

A coluna de data mistura `2026-03-14` (ISO) e `14/03/2026` (padrão brasileiro). Convertemos cada formato separadamente com `errors="coerce"` — o que não casar vira `NaT` (o "NaN" das datas) — e juntamos os dois resultados.

```python
iso = pd.to_datetime(df["data_atendimento"], format="%Y-%m-%d", errors="coerce")
br  = pd.to_datetime(df["data_atendimento"], format="%d/%m/%Y", errors="coerce")
df["data_atendimento"] = iso.fillna(br)

print("Datas não convertidas:", df["data_atendimento"].isna().sum())
print("Período:", df["data_atendimento"].min().date(), "a", df["data_atendimento"].max().date())
print("Tipo da coluna:", df["data_atendimento"].dtype)
```
Saída:
```
Datas não convertidas: 0
Período: 2026-03-02 a 2026-06-28
Tipo da coluna: datetime64[us]

```

## Parte 5 — Unidades trocadas

Algumas alturas foram digitadas em **metros** (1,59) e alguns pesos em **gramas** (90.900). Um adulto não tem 3 cm de altura nem 1.000 kg, então a regra de correção é simples e segura:

```python
em_metros = df["altura_cm"] < 3
em_gramas = df["peso_kg"] > 1000
print("Alturas em metros:", em_metros.sum(), "| Pesos em gramas:", em_gramas.sum())

df.loc[em_metros, "altura_cm"] = df.loc[em_metros, "altura_cm"] * 100
df.loc[em_gramas, "peso_kg"] = df.loc[em_gramas, "peso_kg"] / 1000

print(df[["altura_cm", "peso_kg"]].describe().round(1).loc[["min", "max"]].to_string())
```
Saída:
```
Alturas em metros: 9 | Pesos em gramas: 3
     altura_cm  peso_kg
min      144.0     35.3
max      185.0    108.6

```

## Parte 6 — Códigos sentinela

Muitos sistemas registram "não medido" com um número especial — `999`, `-1`, `0`. Esse número **não é um dado**: se ficar, ele puxa a média para cima. O certo é transformá-lo em ausente (`NaN`).

```python
print("Glicemia = 999:", (df["glicemia_mg_dl"] == 999).sum())
print("Média ANTES:", round(df["glicemia_mg_dl"].mean(), 1))
df["glicemia_mg_dl"] = df["glicemia_mg_dl"].replace(999, np.nan)
print("Média DEPOIS:", round(df["glicemia_mg_dl"].mean(), 1))
```
Saída:
```
Glicemia = 999: 5
Média ANTES: 129.5
Média DEPOIS: 109.1

```

## Parte 7 — Outliers: IQR e z-score

Um **outlier** é um valor muito distante dos demais. Ele pode ser um **erro** (pressão de 1.300 mmHg) ou um **caso raro real** (uma crise hipertensiva de 205 mmHg). Os métodos estatísticos apenas **apontam** candidatos; quem decide é o conhecimento do domínio.

### Método do IQR (intervalo interquartil)

$IQR = Q_3 - Q_1$; são suspeitos os valores abaixo de $Q_1 - 1{,}5 \cdot IQR$ ou acima de $Q_3 + 1{,}5 \cdot IQR$. Funciona bem mesmo com dados assimétricos, porque quartis não são afetados pelos próprios outliers.

```python
pas = df["pressao_sistolica"]
q1, q3 = pas.quantile([0.25, 0.75])
iqr = q3 - q1
lim_inf, lim_sup = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(f"Q1={q1:.0f}  Q3={q3:.0f}  IQR={iqr:.0f}  limites=[{lim_inf:.1f}, {lim_sup:.1f}]")

suspeitos = df[(pas < lim_inf) | (pas > lim_sup)]
print(suspeitos[["id_atendimento", "idade", "pressao_sistolica", "diagnostico"]].sort_values("pressao_sistolica").to_string())
```
Saída:
```
Q1=119  Q3=141  IQR=22  limites=[86.0, 174.0]
     id_atendimento  idade  pressao_sistolica            diagnostico
223            1137   68.0               12.0            Hipertensão
196            1039   28.0               83.0     Consulta de rotina
16             1023   70.0              179.0            Hipertensão
224            1219   86.0              205.0            Hipertensão
41             1133   43.0              410.0  Infecção respiratória
29             1003   19.0             1300.0     Consulta de rotina

```

Leitura caso a caso dos 6 suspeitos: **12**, **410** e **1.300 mmHg** são impossíveis → erro, viram ausentes. Já **205 mmHg** num paciente hipertenso é grave, mas **acontece** → fica; o mesmo vale para **179 mmHg** (hipertenso) e **83 mmHg** (pressão baixa, mas possível). **O IQR aponta, não condena.** Para decidir, usamos uma faixa fisiológica (60 a 260 mmHg).

```python
pas_antes = df["pressao_sistolica"].copy()
erro_pas = (df["pressao_sistolica"] < 60) | (df["pressao_sistolica"] > 260)
df.loc[erro_pas, "pressao_sistolica"] = np.nan
print("Pressões impossíveis transformadas em NaN:", erro_pas.sum())
```
Saída:
```
Pressões impossíveis transformadas em NaN: 3

```

```python
fig, axes = plt.subplots(1, 2, figsize=(9, 3.4), sharey=False)
for ax, serie, titulo in [(axes[0], pas_antes, "Antes"), (axes[1], df["pressao_sistolica"], "Depois")]:
    ax.boxplot(serie.dropna(), vert=False, widths=0.5,
               boxprops=dict(color="#00693e"), medianprops=dict(color="#00693e", linewidth=2),
               whiskerprops=dict(color="#00693e"), capprops=dict(color="#00693e"),
               flierprops=dict(marker="o", markersize=5, markerfacecolor="#c6580d", markeredgecolor="white"))
    ax.set_title(f"Pressão sistólica — {titulo}", fontsize=10)
    ax.set_xlabel("mmHg"); ax.set_yticks([])
    ax.grid(axis="x", color="#e5e7eb", linewidth=0.8); ax.set_axisbelow(True)
    for s in ["top", "right", "left"]: ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig("fig_boxplot_pressao.png", dpi=160)
print("Figura salva: fig_boxplot_pressao.png")
```
Saída:
```
Figura salva: fig_boxplot_pressao.png

```

### Método do z-score

$z = (x - \bar{x}) / s$ mede quantos desvios-padrão o valor está da média; costuma-se marcar $|z| > 3$. É simples, mas tem um ponto fraco: os próprios outliers inflam a média e o desvio-padrão, e um erro grande pode "esconder" outro menor. Veja na idade:

```python
idade = df["idade"]
z = (idade - idade.mean()) / idade.std()
print("Média:", round(idade.mean(), 1), "| desvio-padrão:", round(idade.std(), 1))
print(pd.DataFrame({"idade": idade, "z": z.round(2)})[z.abs() > 3].to_string())
print("\nIdade -3 tem z =", round(z[idade == -3].iloc[0], 2), "-> NÃO foi marcada pelo z-score")
```
Saída:
```
Média: 54.0 | desvio-padrão: 23.8
     idade     z
82   205.0  6.34
109  150.0  4.03

Idade -3 tem z = -2.39 -> NÃO foi marcada pelo z-score

```

O z-score pegou 150 e 205 anos, mas deixou passar **−3 anos** (z ≈ −2,4), que é tão impossível quanto. Mais uma vez, a **regra de domínio** (idade entre 0 e 110) é mais confiável:

```python
erro_idade = (df["idade"] < 0) | (df["idade"] > 110)
df.loc[erro_idade, "idade"] = np.nan
print("Idades impossíveis transformadas em NaN:", erro_idade.sum())
print("Nova faixa de idade:", df["idade"].min(), "a", df["idade"].max())
```
Saída:
```
Idades impossíveis transformadas em NaN: 3
Nova faixa de idade: 18.0 a 89.0

```

## Parte 8 — Valores ausentes: remover ou preencher?

Depois das correções, os erros viraram `NaN` e se somaram aos ausentes originais. Duas saídas:

- **`dropna()`** — remove linhas (ou colunas) com ausentes. Simples, mas pode jogar fora muita informação boa.
- **`fillna()`** — preenche (imputa). A **mediana** é mais resistente a valores extremos que a média; preencher **por grupo** (ex.: mediana da glicemia por diagnóstico) respeita diferenças reais entre grupos.

```python
print(df.isna().sum()[lambda s: s > 0].to_string())
print("\nLinhas com pelo menos um ausente:", df.isna().any(axis=1).sum(), "de", len(df))
print("Se usássemos dropna(): restariam", len(df.dropna()), "linhas")
```
Saída:
```
idade                10
peso_kg              11
pressao_sistolica     9
glicemia_mg_dl       27

Linhas com pelo menos um ausente: 50 de 240
Se usássemos dropna(): restariam 190 linhas

```

```python
df_limpo = df.copy()
df_limpo["idade"] = df_limpo["idade"].fillna(df_limpo["idade"].median())
df_limpo["peso_kg"] = df_limpo["peso_kg"].fillna(df_limpo.groupby("sexo")["peso_kg"].transform("median"))
for col in ["glicemia_mg_dl", "pressao_sistolica"]:
    df_limpo[col] = df_limpo[col].fillna(df_limpo.groupby("diagnostico")[col].transform("median"))

print("Ausentes restantes:", int(df_limpo.isna().sum().sum()))
print(df_limpo.groupby("diagnostico")["glicemia_mg_dl"].median().to_string())
```
Saída:
```
Ausentes restantes: 0
diagnostico
Consulta de rotina        98.0
Diabetes                 169.0
Hipertensão               96.0
Infecção respiratória     99.0

```

Por que **por grupo**? A glicemia mediana dos pacientes com diabetes (~170 mg/dL) é bem diferente da dos demais (~100). Preencher todos com a mediana geral "rebaixaria" os diabéticos e "elevaria" os outros.

> **Boa prática:** guarde um indicador de que o valor foi imputado (ex.: `df["glicemia_imputada"] = df["glicemia_mg_dl"].isna()` **antes** do `fillna`). Isso mantém a transparência para análises futuras.

## Parte 9 — Normalização e padronização

Variáveis em escalas muito diferentes (idade em anos, glicemia em mg/dL) atrapalham algoritmos que usam distâncias (k-NN, k-means) ou gradiente — tema da Unidade 4. Duas transformações clássicas:

| Técnica | Fórmula | Resultado |
|---|---|---|
| **Normalização (min-max)** | $(x - \min) / (\max - \min)$ | valores entre 0 e 1 |
| **Padronização (z-score)** | $(x - \bar{x}) / s$ | média 0 e desvio-padrão 1 |

```python
for col in ["idade", "glicemia_mg_dl"]:
    x = df_limpo[col]
    df_limpo[col + "_minmax"] = (x - x.min()) / (x.max() - x.min())
    df_limpo[col + "_z"] = (x - x.mean()) / x.std()

cols = ["idade", "idade_minmax", "idade_z", "glicemia_mg_dl", "glicemia_mg_dl_minmax", "glicemia_mg_dl_z"]
print(df_limpo[cols].describe().loc[["mean", "std", "min", "max"]].round(2).to_string())
```
Saída:
```
      idade  idade_minmax  idade_z  glicemia_mg_dl  glicemia_mg_dl_minmax  glicemia_mg_dl_z
mean  53.17          0.50     0.00          108.98                   0.34             -0.00
std   20.05          0.28     1.00           28.72                   0.21              1.00
min   18.00          0.00    -1.75           62.00                   0.00             -1.64
max   89.00          1.00     1.79          202.00                   1.00              3.24

```

A forma da distribuição **não muda** — só a escala. Normalize/padronize **depois** de tratar outliers: um único 1.300 mmHg esmagaria todos os outros valores perto de zero na normalização min-max. (Na Aula 10 faremos o mesmo com `MinMaxScaler` e `StandardScaler` do scikit-learn.)

## Parte 10 — Tidy data (dados organizados)

Segundo Hadley Wickham, um conjunto de dados é **tidy** quando:

1. cada **variável** é uma coluna;
2. cada **observação** é uma linha;
3. cada **tipo de unidade observacional** é uma tabela.

A planilha de doses de vacina contra influenza abaixo está no formato **largo**: o **mês** (uma variável) está espalhado pelos nomes das colunas.

```python
larga = pd.read_csv(DADOS / "vacinacao_influenza_larga.csv")
print(larga.to_string(index=False))
```
Saída:
```
     municipio  mar  abr  mai  jun
         Natal  397 1187 1131  499
       Mossoró  243  628  866  283
    Parnamirim  170  456  587  224
         Caicó   87  278  305  106
Pau dos Ferros   70  183  211   81

```

```python
longa = larga.melt(id_vars="municipio", var_name="mes", value_name="doses")
print(longa.head(7).to_string(index=False))
print("...", longa.shape)
```
Saída:
```
     municipio mes  doses
         Natal mar    397
       Mossoró mar    243
    Parnamirim mar    170
         Caicó mar     87
Pau dos Ferros mar     70
         Natal abr   1187
       Mossoró abr    628
... (20, 3)

```

No formato **longo** (tidy), perguntas viram uma linha de código — e qualquer ferramenta de gráfico entende a tabela:

```python
ordem = ["mar", "abr", "mai", "jun"]
print(longa.groupby("mes")["doses"].sum().reindex(ordem).to_string())
print()
print("Mês de pico em cada município:")
print(longa.loc[longa.groupby("municipio")["doses"].idxmax()].to_string(index=False))
```
Saída:
```
mes
mar     967
abr    2732
mai    3100
jun    1193

Mês de pico em cada município:
     municipio mes  doses
         Caicó mai    305
       Mossoró mai    866
         Natal abr   1187
    Parnamirim mai    587
Pau dos Ferros mai    211

```

```python
# e o caminho inverso, quando um relatório pede o formato largo:
de_volta = longa.pivot(index="municipio", columns="mes", values="doses")[ordem]
print(de_volta.to_string())
```
Saída:
```
mes             mar   abr   mai  jun
municipio                           
Caicó            87   278   305  106
Mossoró         243   628   866  283
Natal           397  1187  1131  499
Parnamirim      170   456   587  224
Pau dos Ferros   70   183   211   81

```

## Parte 11 — Salvando o dataset limpo e o relatório de limpeza

```python
final = df_limpo.drop(columns=[c for c in df_limpo.columns if c.endswith(("_minmax", "_z"))])
final.to_csv(DADOS / "atendimentos_ubs_limpo.csv", index=False, encoding="utf-8")

relatorio = {
    "linhas_originais": 250,
    "duplicatas_removidas": 10,
    "pressoes_impossiveis": int(erro_pas.sum()),
    "idades_impossiveis": int(erro_idade.sum()),
    "linhas_finais": len(final),
    "ausentes_finais": int(final.isna().sum().sum()),
}
for k, v in relatorio.items():
    print(f"{k:22s} {v}")
```
Saída:
```
linhas_originais       250
duplicatas_removidas   10
pressoes_impossiveis   3
idades_impossiveis     3
linhas_finais          240
ausentes_finais        0

```

## Resumo

| Problema | Diagnóstico | Correção |
|---|---|---|
| Valores ausentes | `isna().sum()` | `dropna()` ou `fillna()` (mediana, por grupo) |
| Duplicatas | `duplicated()` | `drop_duplicates()` |
| Texto inconsistente | `value_counts()` | `str.strip()`, `str.title()`, `replace()` |
| Datas misturadas | `dtype` = texto | `pd.to_datetime(..., format=..., errors="coerce")` |
| Unidades trocadas | `describe()` (min/max) | regra de conversão com `loc` |
| Códigos sentinela | valores repetidos estranhos (999) | `replace(999, np.nan)` |
| Outliers | IQR, z-score, boxplot | regra de domínio; erro → `NaN` |
| Escalas diferentes | `describe()` | normalização min-max / padronização z |
| Formato largo | variáveis nos nomes das colunas | `melt()` / `pivot()` |

**Próximos passos:** faça o **exercício prático** (`Aula09_Exercicio_Pratico.ipynb`, com dados de triagem de pronto atendimento) e responda ao **formulário avaliativo** no Moodle até **30/10/2026**.

