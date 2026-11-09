# Aula10_Pipeline_de_Limpeza.ipynb

# Aula 10 — Laboratório: Pipeline de Limpeza Completo

**Unidade 2 — Aquisição e Preparação de Dados** · Análise e Ciência de Dados (Especialização, IFRN)

Na Aula 09 aprendemos a **diagnosticar e corrigir** problemas de qualidade. Agora vamos juntar tudo num **pipeline**: uma sequência organizada e repetível de passos que leva os dados brutos até um dataset limpo, documentado e pronto para análise ou para um modelo de machine learning.

**O cenário (dados sintéticos).** Uma rede hospitalar fictícia do RN quer analisar suas internações. Os dados vêm de dois sistemas diferentes:

| Arquivo | Origem | Conteúdo |
|---|---|---|
| `dados/pacientes.csv` | sistema de cadastro | 200 pacientes: nascimento, sexo, município, escolaridade, plano de saúde |
| `dados/internacoes.json` | API do sistema hospitalar | 304 internações: datas, diagnóstico, gravidade, UTI, custo |

Nenhum registro é de paciente real: tudo foi sorteado por `gerar_dados.py` (semente fixa), com problemas inseridos de propósito.

**Roteiro (ETL):**

1. **E**xtract — ler as duas fontes;
2. **T**ransform — corrigir tipos, padronizar categorias, remover duplicatas, juntar as tabelas, criar atributos (idade, tempo de internação, faixas) e codificar categorias (one-hot, label/ordinal);
3. **L**oad — exportar o dataset limpo (CSV e Parquet) com um dicionário de dados;
4. Bônus — o mesmo pré-processamento com `Pipeline` e `ColumnTransformer` do scikit-learn.

> **Instalação:** `pip install pandas numpy scikit-learn pyarrow`

```python
import json
from pathlib import Path

import numpy as np
import pandas as pd

pd.set_option("display.width", 130)
pd.set_option("display.max_columns", 14)
DADOS = Path("dados")
SAIDA = Path("saida")
SAIDA.mkdir(exist_ok=True)
```

## Parte 1 — Extract: lendo as fontes

Cada fonte tem seu formato: o cadastro é um **CSV**; as internações chegam em **JSON** (uma lista de objetos, como as APIs da Aula 07). O Pandas lê os dois.

Um cuidado importante: na extração, leia tudo **como veio**. Correções ficam para a etapa de transformação — assim o arquivo original nunca é alterado e o pipeline pode ser executado de novo do zero.

```python
pacientes = pd.read_csv(DADOS / "pacientes.csv")
internacoes = pd.read_json(DADOS / "internacoes.json")

print("pacientes  :", pacientes.shape)
print("internacoes:", internacoes.shape)
print()
print(pacientes.head(4).to_string())
print()
print(internacoes.head(4).to_string())
```
Saída:
```
pacientes  : (200, 6)
internacoes: (304, 8)

  id_paciente data_nascimento sexo   municipio escolaridade plano_saude
0    PAC-0001      1993-10-22    F  Parnamirim  Fundamental         nao
1    PAC-0002      1943-01-26    M       Natal     Superior         Não
2    PAC-0003      1992-01-18    F       Caicó        Médio         Sim
3    PAC-0004      1980-07-06    F       Natal  Fundamental         Sim

  id_internacao id_paciente data_entrada   data_alta diagnostico_principal gravidade uti   custo_total
0     INT-00078    PAC-0129   2026-05-26  2026-06-03     Infecção urinária     Grave   S  R$ 15.764,91
1     INT-00098    PAC-0056   2026-05-23  2026-05-25     Infecção urinária      Leve   N   R$ 2.382,98
2     INT-00270    PAC-0024   2026-07-18  2026-07-28                   AVC  Moderada   N  R$ 12.493,78
3     INT-00139    PAC-0109   2026-08-21  2026-08-26     Infecção urinária     Grave   S  R$ 12.951,47

```

### Primeiro diagnóstico: os **tipos**

O comando `dtypes` mostra como o Pandas entendeu cada coluna. Repare: **todas** as colunas vieram como texto (`str`/`object`) — inclusive datas, custos e a coluna de UTI. Com texto não dá para calcular tempo de internação, somar custos nem treinar um modelo. Corrigir tipos é a primeira transformação.

```python
pd.DataFrame({"pacientes": pacientes.dtypes.astype(str)}).join(
    pd.DataFrame({"internacoes": internacoes.dtypes.astype(str)}), how="outer").fillna("—")
```
Saída:
```
                      pacientes internacoes
custo_total                   —         str
data_alta                     —         str
data_entrada                  —         str
data_nascimento             str           —
diagnostico_principal         —         str
escolaridade                str           —
gravidade                     —         str
id_internacao                 —         str
id_paciente                 str         str
municipio                   str           —
plano_saude                 str           —
sexo                        str           —
uti                           —         str
```

```python
for col in ["sexo", "plano_saude", "escolaridade"]:
    print(col, "→", pacientes[col].value_counts(dropna=False).to_dict())
print()
print("gravidade →", internacoes["gravidade"].value_counts().to_dict())
print("uti       →", internacoes["uti"].value_counts().to_dict())
print("custo     →", internacoes["custo_total"].head(3).tolist())
print("Duplicatas em internações:", internacoes.duplicated().sum())
```
Saída:
```
sexo → {'M': 100, 'F': 80, 'f': 7, 'Masculino': 6, 'm': 5, 'Feminino': 2}
plano_saude → {'Não': 128, 'Sim': 47, 'nao': 7, 'NÃO': 7, 'N': 6, 'sim': 3, 'S': 1, 'SIM': 1}
escolaridade → {'Médio': 74, 'Fundamental': 71, 'Superior': 37, nan: 6, 'SUPERIOR': 5, 'MÉDIO': 4, 'FUNDAMENTAL': 3}

gravidade → {'Leve': 119, 'Moderada': 111, 'Grave': 56, 'moderada': 7, 'leve': 6, 'grave': 5}
uti       → {'N': 256, 'S': 48}
custo     → ['R$ 15.764,91', 'R$ 2.382,98', 'R$ 12.493,78']
Duplicatas em internações: 4

```

Resumo do que precisa ser transformado:

| Coluna | Problema | Transformação |
|---|---|---|
| `data_nascimento` | dois formatos (`1993-10-22` e `22/10/1993`) | texto → `datetime` |
| `sexo` | `F`, `f`, `Feminino`, `M`, `m`, `Masculino` | padronizar para `F`/`M` |
| `plano_saude` | `Sim`, `sim`, `S`, `Não`, `nao`, `N`... | texto → booleano (`True`/`False`) |
| `escolaridade` | maiúsculas misturadas e 6 ausentes | padronizar + `"Não informado"` |
| `gravidade` | `Leve`/`leve`... | padronizar |
| `uti` | `S`/`N` | booleano |
| `custo_total` | texto `"R$ 15.764,91"` e 5 ausentes | texto → `float` |
| `data_entrada`, `data_alta` | texto | `datetime` |
| internações | 4 linhas duplicadas | remover |

## Parte 2 — Transform (1): tipos e padronização

### 2.1 Datas com formatos misturados

`pd.to_datetime` com um `format` explícito converte o que segue aquele formato e, com `errors="coerce"`, transforma o resto em `NaT` (ausente). Convertendo com cada formato e combinando com `fillna`, todas as datas são aproveitadas.

```python
p = pacientes.copy()          # trabalhamos sempre numa cópia
txt = p["data_nascimento"]
iso = pd.to_datetime(txt, format="%Y-%m-%d", errors="coerce")
br = pd.to_datetime(txt, format="%d/%m/%Y", errors="coerce")
p["data_nascimento"] = iso.fillna(br)

print("No formato ISO:", iso.notna().sum(), "| no formato dd/mm/aaaa:", br.notna().sum())
print("Datas que ficaram sem converter:", p["data_nascimento"].isna().sum())
print(p["data_nascimento"].dtype)
```
Saída:
```
No formato ISO: 185 | no formato dd/mm/aaaa: 15
Datas que ficaram sem converter: 0
datetime64[us]

```

### 2.2 Categorias de texto → valores padronizados

Para o `sexo`, basta olhar a **primeira letra** em maiúscula. Para o `plano_saude`, usamos um **dicionário de mapeamento** que transforma cada variação em `True`/`False` — um tipo booleano ocupa menos memória e deixa claro que só existem duas respostas.

> Dica: com `map`, qualquer valor que **não** esteja no dicionário vira `NaN`. Isso é bom: se aparecer uma grafia nova, você percebe na conferência em vez de ela passar despercebida.

```python
p["sexo"] = p["sexo"].str.strip().str[0].str.upper()

mapa_sim_nao = {"sim": True, "s": True, "não": False, "nao": False, "n": False}
p["plano_saude"] = p["plano_saude"].str.strip().str.lower().map(mapa_sim_nao).astype(bool)

p["escolaridade"] = p["escolaridade"].str.strip().str.capitalize().fillna("Não informado")

print(p["sexo"].value_counts().to_dict())
print(p["plano_saude"].value_counts().to_dict())
print(p["escolaridade"].value_counts().to_dict())
print(p.dtypes.astype(str).to_dict())
```
Saída:
```
{'M': 111, 'F': 89}
{False: 148, True: 52}
{'Médio': 78, 'Fundamental': 74, 'Superior': 42, 'Não informado': 6}
{'id_paciente': 'str', 'data_nascimento': 'datetime64[us]', 'sexo': 'str', 'municipio': 'str', 'escolaridade': 'str', 'plano_saude': 'bool'}

```

### 2.3 Internações: duplicatas, moeda, booleano e datas

O custo vem no formato brasileiro (`R$ 15.764,91`). Para virar número: tirar o `R$` e os espaços, tirar o **ponto de milhar** e trocar a **vírgula decimal** por ponto. Os 5 custos ausentes continuam `NaN` — vamos tratá-los depois da junção.

```python
i = internacoes.drop_duplicates().reset_index(drop=True)
print("Após remover duplicatas:", len(i), "| id_internacao único?", i["id_internacao"].is_unique)

def moeda_para_float(serie):
    """'R$ 1.234,56' -> 1234.56 (valores ausentes continuam NaN)."""
    return (serie.str.replace("R$", "", regex=False)
                 .str.strip()
                 .str.replace(".", "", regex=False)
                 .str.replace(",", ".", regex=False)
                 .astype(float))

i["custo_total"] = moeda_para_float(i["custo_total"])
i["uti"] = i["uti"].map({"S": True, "N": False})
i["gravidade"] = i["gravidade"].str.capitalize()
for col in ["data_entrada", "data_alta"]:
    i[col] = pd.to_datetime(i[col], format="%Y-%m-%d")

print(i.dtypes.astype(str).to_dict())
print(i[["custo_total"]].describe().round(2).T.to_string())
```
Saída:
```
Após remover duplicatas: 300 | id_internacao único? True
{'id_internacao': 'str', 'id_paciente': 'str', 'data_entrada': 'datetime64[us]', 'data_alta': 'datetime64[us]', 'diagnostico_principal': 'str', 'gravidade': 'str', 'uti': 'bool', 'custo_total': 'float64'}
             count     mean      std     min      25%      50%       75%       max
custo_total  295.0  8757.28  5970.08  776.87  4551.56  7274.02  10453.56  29393.77

```

### 2.4 Regras de validação

Depois de converter, verifique regras simples do domínio com `assert` — se alguma falhar, o pipeline **para** e avisa, em vez de gerar silenciosamente um dataset errado.

```python
assert (i["data_alta"] >= i["data_entrada"]).all(), "alta antes da entrada!"
assert i["gravidade"].isin(["Leve", "Moderada", "Grave"]).all()
assert p["sexo"].isin(["F", "M"]).all()
assert p["id_paciente"].is_unique
print("Todas as regras de validação passaram ✔")
```
Saída:
```
Todas as regras de validação passaram ✔

```

## Parte 3 — Transform (2): juntando as fontes

Cada internação tem um `id_paciente`. Com `merge` trazemos os dados do cadastro para a tabela de internações (relação **muitos-para-um**: um paciente pode ter várias internações).

- `how="left"` mantém **todas** as internações, mesmo as sem paciente correspondente;
- `validate="many_to_one"` faz o Pandas conferir que cada paciente aparece uma única vez no cadastro;
- `indicator=True` cria a coluna `_merge`, que mostra de onde veio cada linha.

```python
base = i.merge(p, on="id_paciente", how="left", validate="many_to_one", indicator=True)
print(base["_merge"].value_counts().to_string())
base[base["_merge"] == "left_only"][["id_internacao", "id_paciente", "diagnostico_principal"]]
```
Saída:
```
_merge
both          297
left_only       3
right_only      0

```
Saída:
```
    id_internacao id_paciente   diagnostico_principal
31      INT-00251    PAC-9003                     AVC
156     INT-00224    PAC-9001  Insuficiência cardíaca
269     INT-00198    PAC-9002        Fratura de fêmur
```

Três internações apontam para pacientes que **não existem** no cadastro (`PAC-9001` a `PAC-9003`) — um problema de **integridade referencial** entre sistemas. Sem nascimento e sexo, elas não servem para a análise; registramos o fato e as removemos.

```python
orfas = (base["_merge"] == "left_only").sum()
base = base[base["_merge"] == "both"].drop(columns="_merge").reset_index(drop=True)
base["plano_saude"] = base["plano_saude"].astype(bool)   # o left join deixou NaN nas órfãs → volta a ser booleano
print(f"Removidas {orfas} internações sem cadastro → {len(base)} linhas")
```
Saída:
```
Removidas 3 internações sem cadastro → 297 linhas

```

## Parte 4 — Engenharia de atributos

**Engenharia de atributos** (*feature engineering*) é criar novas colunas, mais úteis, a partir das existentes. Três exemplos clássicos:

1. **Atributos derivados** de datas: tempo de internação (dias) e idade na data da internação;
2. **Imputação** com informação de grupo (custo ausente → mediana do mesmo diagnóstico e gravidade);
3. **Discretização** (*binning*): transformar um número contínuo em faixas.

```python
base["tempo_internacao_dias"] = (base["data_alta"] - base["data_entrada"]).dt.days
base["idade"] = ((base["data_entrada"] - base["data_nascimento"]).dt.days // 365.25).astype(int)
base["mes_entrada"] = base["data_entrada"].dt.month

grupo = ["diagnostico_principal", "gravidade"]
base["custo_total"] = base["custo_total"].fillna(base.groupby(grupo)["custo_total"].transform("median"))
base["custo_por_dia"] = (base["custo_total"] / base["tempo_internacao_dias"]).round(2)

print("Ausentes restantes:", int(base.isna().sum().sum()))
base[["tempo_internacao_dias", "idade", "custo_total", "custo_por_dia"]].describe().round(1)
```
Saída:
```
Ausentes restantes: 0

```
Saída:
```
       tempo_internacao_dias  idade  custo_total  custo_por_dia
count                  297.0  297.0        297.0          297.0
mean                     6.7   49.0       8833.6         1337.0
std                      3.7   25.9       6033.4          799.4
min                      1.0    7.0        776.9          698.2
25%                      4.0   24.0       4565.0         1035.8
50%                      6.0   49.0       7286.6         1143.0
75%                      9.0   73.0      10687.7         1284.1
max                     20.0   91.0      29393.8         9902.4
```

### 4.1 Binning com `pd.cut` — faixas definidas por você

`pd.cut` corta a variável em intervalos com **limites escolhidos** (ex.: faixas etárias usadas pelo Ministério da Saúde). `right=False` faz cada intervalo incluir o limite inferior e excluir o superior: `[0, 18)`, `[18, 40)`...

```python
limites = [0, 18, 40, 60, 80, 120]
rotulos = ["0-17", "18-39", "40-59", "60-79", "80+"]
base["faixa_etaria"] = pd.cut(base["idade"], bins=limites, labels=rotulos, right=False)
base["faixa_etaria"].value_counts().sort_index()
```
Saída:
```
faixa_etaria
0-17     37
18-39    83
40-59    62
60-79    59
80+      56
Name: count, dtype: int64
```

### 4.2 Binning com `pd.qcut` — faixas com a mesma quantidade

`pd.qcut` usa **quantis**: cada faixa recebe (aproximadamente) o mesmo número de linhas. É útil quando não existe um limite "oficial" — aqui, dividimos o custo em quatro faixas (quartis).

```python
base["faixa_custo"] = pd.qcut(base["custo_total"], q=4, labels=["Baixo", "Médio", "Alto", "Muito alto"])
print(base["faixa_custo"].value_counts().sort_index().to_string())
print()
print(base.groupby("faixa_custo", observed=True)["custo_total"].agg(["min", "max"]).round(0).to_string())
```
Saída:
```
faixa_custo
Baixo         75
Médio         74
Alto          74
Muito alto    74

                 min      max
faixa_custo                  
Baixo          777.0   4565.0
Médio         4568.0   7287.0
Alto          7372.0  10688.0
Muito alto   10708.0  29394.0

```

Compare: com `cut` as faixas têm **larguras** definidas e quantidades diferentes; com `qcut` as faixas têm **quantidades** iguais e larguras diferentes.

Os atributos novos já contam uma história — veja o tempo médio de internação e a proporção de UTI por gravidade e por faixa etária:

```python
print(base.groupby("gravidade")[["tempo_internacao_dias", "custo_total", "uti"]].mean()
          .round(2).reindex(["Leve", "Moderada", "Grave"]).to_string())
print()
print(base.groupby("faixa_etaria", observed=True)["tempo_internacao_dias"].mean().round(1).to_string())
```
Saída:
```
           tempo_internacao_dias  custo_total   uti
gravidade                                          
Leve                        4.76      5523.36  0.02
Moderada                    6.64      8765.93  0.16
Grave                      10.87     15856.21  0.45

faixa_etaria
0-17     6.6
18-39    7.0
40-59    7.1
60-79    6.8
80+      5.7

```

## Parte 5 — Codificando variáveis categóricas

Algoritmos de machine learning trabalham com **números**. Precisamos transformar categorias (texto) em números — e o jeito certo depende do tipo de categoria:

| Tipo | Exemplo | Técnica |
|---|---|---|
| **Nominal** (sem ordem) | diagnóstico, município, sexo | **one-hot encoding** |
| **Ordinal** (com ordem) | gravidade: Leve < Moderada < Grave | **codificação ordinal** (0, 1, 2) |
| Rótulo / alvo | a variável a prever (ex.: UTI sim/não) | **label encoding** |

### 5.1 One-hot encoding com `pd.get_dummies`

Cria **uma coluna 0/1 para cada categoria**. Nenhuma categoria fica "maior" que a outra.

```python
onehot = pd.get_dummies(base["diagnostico_principal"], prefix="diag", dtype=int)
pd.concat([base[["id_internacao", "diagnostico_principal"]], onehot], axis=1).head(5)
```
Saída:
```
  id_internacao diagnostico_principal  diag_AVC  diag_Fratura de fêmur  diag_Infecção urinária  diag_Insuficiência cardíaca  \
0     INT-00078     Infecção urinária         0                      0                       1                            0   
1     INT-00098     Infecção urinária         0                      0                       1                            0   
2     INT-00270                   AVC         1                      0                       0                            0   
3     INT-00139     Infecção urinária         0                      0                       1                            0   
4     INT-00043     Infecção urinária         0                      0                       1                            0   

   diag_Pneumonia  
0               0  
1               0  
2               0  
3               0  
4               0  
```

**Armadilha da variável dummy:** as 5 colunas sempre somam 1 — qualquer uma delas pode ser deduzida das outras. Para modelos lineares (ex.: regressão), isso gera redundância; o comum é descartar uma coluna com `drop_first=True`. A categoria removida vira a **referência**.

```python
dummies_mun = pd.get_dummies(base["municipio"], prefix="mun", drop_first=True, dtype=int)
print("Categorias:", sorted(base["municipio"].unique()))
print("Colunas criadas:", list(dummies_mun.columns), "→ 'Caicó' é a referência (todas = 0)")
```
Saída:
```
Categorias: ['Caicó', 'Mossoró', 'Natal', 'Parnamirim']
Colunas criadas: ['mun_Mossoró', 'mun_Natal', 'mun_Parnamirim'] → 'Caicó' é a referência (todas = 0)

```

### 5.2 Por que **não** numerar categorias nominais?

Se trocarmos os diagnósticos por 0, 1, 2, 3, 4, um modelo pode "achar" que AVC (0) < Fratura (1) < Infecção (2)... e até que a média entre AVC e Infecção é Fratura! Essa ordem **não existe**. Por isso, para variáveis nominais, use one-hot.

### 5.3 Codificação ordinal — quando a ordem existe

Para a gravidade a ordem é real, então números crescentes fazem sentido. O jeito mais claro é um **dicionário explícito** (você controla a ordem):

```python
ordem_gravidade = {"Leve": 0, "Moderada": 1, "Grave": 2}
base["gravidade_cod"] = base["gravidade"].map(ordem_gravidade)

ordem_escolaridade = {"Não informado": -1, "Fundamental": 0, "Médio": 1, "Superior": 2}
base["escolaridade_cod"] = base["escolaridade"].map(ordem_escolaridade)

base[["gravidade", "gravidade_cod", "escolaridade", "escolaridade_cod"]].drop_duplicates("gravidade")
```
Saída:
```
  gravidade  gravidade_cod escolaridade  escolaridade_cod
0     Grave              2  Fundamental                 0
1      Leve              0        Médio                 1
2  Moderada              1  Fundamental                 0
```

### 5.4 Label encoding com o scikit-learn

O `LabelEncoder` numera as categorias em **ordem alfabética**. É feito para codificar o **alvo** (a variável que o modelo vai prever). Veja o que acontece se usado na gravidade: a ordem alfabética (Grave, Leve, Moderada) **não** é a ordem clínica!

```python
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder

le = LabelEncoder()
codigos = le.fit_transform(base["gravidade"])
print("Classes (ordem alfabética):", list(le.classes_), "→", list(range(len(le.classes_))))
print("Ou seja: Grave=0, Leve=1, Moderada=2  ✘ não respeita a gravidade")

oe = OrdinalEncoder(categories=[["Leve", "Moderada", "Grave"]])
base["gravidade_oe"] = oe.fit_transform(base[["gravidade"]]).astype(int).ravel()
print("OrdinalEncoder com a ordem informada:", dict(zip(oe.categories_[0], range(3))), " ✔")
print("Igual ao dicionário?", (base["gravidade_oe"] == base["gravidade_cod"]).all())
```
Saída:
```
Classes (ordem alfabética): ['Grave', 'Leve', 'Moderada'] → [0, 1, 2]
Ou seja: Grave=0, Leve=1, Moderada=2  ✘ não respeita a gravidade
OrdinalEncoder com a ordem informada: {'Leve': 0, 'Moderada': 1, 'Grave': 2}  ✔
Igual ao dicionário? True

```

**Resumo:** `LabelEncoder` → para o alvo; `OrdinalEncoder(categories=[...])` ou um dicionário → para atributos ordinais; `OneHotEncoder`/`get_dummies` → para atributos nominais.

## Parte 6 — Load: exportando o dataset limpo

Vamos montar o dataset final com colunas em uma ordem lógica, nomes claros e os tipos corretos, e exportá-lo em dois formatos:

- **CSV** — universal, abre em qualquer ferramenta, mas guarda **só texto**: na leitura o Pandas precisa adivinhar os tipos — datas e categorias voltam como texto e precisam ser reconvertidas;
- **Parquet** — formato colunar e compactado; **preserva os tipos** e é muito mais rápido em bases grandes.

```python
colunas = ["id_internacao", "id_paciente", "data_entrada", "data_alta", "mes_entrada",
           "tempo_internacao_dias", "diagnostico_principal", "gravidade", "gravidade_cod",
           "uti", "custo_total", "custo_por_dia", "faixa_custo",
           "sexo", "idade", "faixa_etaria", "municipio", "escolaridade", "escolaridade_cod", "plano_saude"]
limpo = base[colunas].sort_values("data_entrada").reset_index(drop=True)
limpo = pd.concat([limpo, pd.get_dummies(limpo["diagnostico_principal"], prefix="diag", dtype=int)], axis=1)

limpo.to_csv(SAIDA / "internacoes_limpo.csv", index=False, encoding="utf-8")
limpo.to_parquet(SAIDA / "internacoes_limpo.parquet", index=False)
print(limpo.shape)
print(limpo.head(3).T.to_string())
```
Saída:
```
(297, 25)
                                               0                    1                    2
id_internacao                          INT-00221            INT-00002            INT-00295
id_paciente                             PAC-0045             PAC-0070             PAC-0008
data_entrada                 2026-01-06 00:00:00  2026-01-09 00:00:00  2026-01-10 00:00:00
data_alta                    2026-01-15 00:00:00  2026-01-15 00:00:00  2026-01-22 00:00:00
mes_entrada                                    1                    1                    1
tempo_internacao_dias                          9                    6                   12
diagnostico_principal           Fratura de fêmur            Pneumonia            Pneumonia
gravidade                               Moderada             Moderada                Grave
gravidade_cod                                  1                    1                    2
uti                                        False                 True                False
custo_total                              8562.51             16948.09             13260.61
custo_por_dia                             951.39              2824.68              1105.05
faixa_custo                                 Alto           Muito alto           Muito alto
sexo                                           F                    F                    M
idade                                         63                   30                    7
faixa_etaria                               60-79                18-39                 0-17
municipio                                  Natal           Parnamirim              Mossoró
escolaridade                               Médio             Superior                Médio
escolaridade_cod                               1                    2                    1
plano_saude                                False                False                False
diag_AVC                                       0                    0                    0
diag_Fratura de fêmur                          1                    0                    0
diag_Infecção urinária                         0                    0                    0
diag_Insuficiência cardíaca                    0                    0                    0
diag_Pneumonia                                 0                    1                    1

```

```python
do_csv = pd.read_csv(SAIDA / "internacoes_limpo.csv")
do_parquet = pd.read_parquet(SAIDA / "internacoes_limpo.parquet")
cols = ["data_entrada", "uti", "faixa_etaria", "custo_total"]
pd.DataFrame({"memória": limpo[cols].dtypes.astype(str),
              "relido do CSV": do_csv[cols].dtypes.astype(str),
              "relido do Parquet": do_parquet[cols].dtypes.astype(str)})
```
Saída:
```
                     memória relido do CSV relido do Parquet
data_entrada  datetime64[us]           str    datetime64[us]
uti                     bool          bool              bool
faixa_etaria        category           str          category
custo_total          float64       float64           float64
```

```python
for f in ["internacoes_limpo.csv", "internacoes_limpo.parquet"]:
    print(f"{f:28s} {(SAIDA / f).stat().st_size / 1024:6.1f} KB")
```
Saída:
```
internacoes_limpo.csv          42.2 KB
internacoes_limpo.parquet      26.9 KB

```

### 6.1 Dicionário de dados

Um dataset limpo sem documentação é meio caminho andado. O **dicionário de dados** descreve cada coluna: tipo, significado e origem/transformação. Ele acompanha o arquivo exportado.

```python
descricao = {
    "id_internacao": "identificador único da internação",
    "id_paciente": "identificador do paciente (chave para o cadastro)",
    "data_entrada": "data de admissão",
    "data_alta": "data da alta",
    "mes_entrada": "mês da admissão (1-12) — derivado",
    "tempo_internacao_dias": "data_alta - data_entrada, em dias — derivado",
    "diagnostico_principal": "diagnóstico principal (nominal)",
    "gravidade": "Leve / Moderada / Grave (padronizado)",
    "gravidade_cod": "gravidade ordinal: 0=Leve, 1=Moderada, 2=Grave",
    "uti": "passou pela UTI (S/N → booleano)",
    "custo_total": "custo em R$ (texto → float; 5 ausentes imputados pela mediana do diagnóstico+gravidade)",
    "custo_por_dia": "custo_total / tempo_internacao_dias — derivado",
    "faixa_custo": "quartis do custo (pd.qcut)",
    "sexo": "F / M (padronizado)",
    "idade": "idade em anos na data de entrada — derivado",
    "faixa_etaria": "faixas 0-17, 18-39, 40-59, 60-79, 80+ (pd.cut)",
    "municipio": "município de residência",
    "escolaridade": "escolaridade (ausentes = 'Não informado')",
    "escolaridade_cod": "escolaridade ordinal: -1=Não informado, 0=Fundamental, 1=Médio, 2=Superior",
    "plano_saude": "possui plano de saúde (texto → booleano)",
}
dicionario = pd.DataFrame({"coluna": limpo.columns,
                           "tipo": limpo.dtypes.astype(str).values,
                           "descricao": [descricao.get(c, "one-hot do diagnóstico (0/1)") for c in limpo.columns]})
dicionario.to_csv(SAIDA / "dicionario_de_dados.csv", index=False, encoding="utf-8")
print(dicionario.to_string(index=False))
```
Saída:
```
                     coluna           tipo                                                                               descricao
              id_internacao            str                                                       identificador único da internação
                id_paciente            str                                       identificador do paciente (chave para o cadastro)
               data_entrada datetime64[us]                                                                        data de admissão
                  data_alta datetime64[us]                                                                            data da alta
                mes_entrada          int32                                                       mês da admissão (1-12) — derivado
      tempo_internacao_dias          int64                                            data_alta - data_entrada, em dias — derivado
      diagnostico_principal            str                                                         diagnóstico principal (nominal)
                  gravidade            str                                                   Leve / Moderada / Grave (padronizado)
              gravidade_cod          int64                                          gravidade ordinal: 0=Leve, 1=Moderada, 2=Grave
                        uti           bool                                                        passou pela UTI (S/N → booleano)
                custo_total        float64 custo em R$ (texto → float; 5 ausentes imputados pela mediana do diagnóstico+gravidade)
              custo_por_dia        float64                                          custo_total / tempo_internacao_dias — derivado
                faixa_custo       category                                                              quartis do custo (pd.qcut)
                       sexo            str                                                                     F / M (padronizado)
                      idade          int64                                             idade em anos na data de entrada — derivado
               faixa_etaria       category                                          faixas 0-17, 18-39, 40-59, 60-79, 80+ (pd.cut)
                  municipio            str                                                                 município de residência
               escolaridade            str                                               escolaridade (ausentes = 'Não informado')
           escolaridade_cod          int64              escolaridade ordinal: -1=Não informado, 0=Fundamental, 1=Médio, 2=Superior
                plano_saude           bool                                                possui plano de saúde (texto → booleano)
                   diag_AVC          int64                                                            one-hot do diagnóstico (0/1)
      diag_Fratura de fêmur          int64                                                            one-hot do diagnóstico (0/1)
     diag_Infecção urinária          int64                                                            one-hot do diagnóstico (0/1)
diag_Insuficiência cardíaca          int64                                                            one-hot do diagnóstico (0/1)
             diag_Pneumonia          int64                                                            one-hot do diagnóstico (0/1)

```

## Parte 7 — Organizando o ETL em funções

Um pipeline de verdade precisa ser **repetível**: no mês que vem chegam novos arquivos e tudo deve rodar de novo com um comando. Para isso, organizamos cada etapa em uma função. O resultado é idêntico ao que construímos passo a passo.

```python
def extrair(pasta):
    return pd.read_csv(pasta / "pacientes.csv"), pd.read_json(pasta / "internacoes.json")


def transformar_pacientes(p):
    p = p.copy()
    txt = p["data_nascimento"]
    p["data_nascimento"] = (pd.to_datetime(txt, format="%Y-%m-%d", errors="coerce")
                            .fillna(pd.to_datetime(txt, format="%d/%m/%Y", errors="coerce")))
    p["sexo"] = p["sexo"].str.strip().str[0].str.upper()
    p["plano_saude"] = p["plano_saude"].str.strip().str.lower().map(mapa_sim_nao).astype(bool)
    p["escolaridade"] = p["escolaridade"].str.strip().str.capitalize().fillna("Não informado")
    return p


def transformar_internacoes(i):
    i = i.drop_duplicates().reset_index(drop=True)
    i["custo_total"] = moeda_para_float(i["custo_total"])
    i["uti"] = i["uti"].map({"S": True, "N": False})
    i["gravidade"] = i["gravidade"].str.capitalize()
    for col in ["data_entrada", "data_alta"]:
        i[col] = pd.to_datetime(i[col], format="%Y-%m-%d")
    return i


def juntar_e_enriquecer(i, p):
    b = i.merge(p, on="id_paciente", how="inner", validate="many_to_one")
    b["tempo_internacao_dias"] = (b["data_alta"] - b["data_entrada"]).dt.days
    b["idade"] = ((b["data_entrada"] - b["data_nascimento"]).dt.days // 365.25).astype(int)
    b["custo_total"] = b["custo_total"].fillna(
        b.groupby(["diagnostico_principal", "gravidade"])["custo_total"].transform("median"))
    b["faixa_etaria"] = pd.cut(b["idade"], bins=limites, labels=rotulos, right=False)
    b["gravidade_cod"] = b["gravidade"].map(ordem_gravidade)
    return b


def validar(b):
    assert b["custo_total"].notna().all()
    assert (b["tempo_internacao_dias"] >= 0).all()
    assert b["id_internacao"].is_unique
    return b


pac_bruto, int_bruto = extrair(DADOS)
resultado = validar(juntar_e_enriquecer(transformar_internacoes(int_bruto), transformar_pacientes(pac_bruto)))
print(resultado.shape, "| mesmo custo total da versão passo a passo?",
      np.isclose(resultado["custo_total"].sum(), limpo["custo_total"].sum()))
```
Saída:
```
(297, 17) | mesmo custo total da versão passo a passo? True

```

## Parte 8 — Bônus: pré-processamento com scikit-learn

Quando o objetivo é treinar um modelo (Unidade 4), o scikit-learn oferece o mesmo pré-processamento em objetos reutilizáveis:

- `OneHotEncoder` — one-hot; com `handle_unknown="ignore"`, uma categoria nova (que não existia no treino) vira uma linha de zeros em vez de gerar erro;
- `OrdinalEncoder` — codificação ordinal com a ordem que você informar;
- `StandardScaler` / `MinMaxScaler` — padronização / normalização (Aula 09);
- `ColumnTransformer` — aplica uma transformação diferente a cada grupo de colunas;
- `Pipeline` — encadeia as etapas num único objeto com `fit` e `transform`.

**Regra de ouro (vazamento de dados / *data leakage*):** o pré-processamento **aprende** parâmetros (médias, desvios, lista de categorias). Esses parâmetros devem ser aprendidos (`fit`) **somente nos dados de treino** e depois aplicados (`transform`) ao teste. Se o `fit` usar o teste, informação do teste "vaza" para o modelo e a avaliação fica otimista demais.

```python
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler

nominais = ["diagnostico_principal", "sexo", "municipio"]
ordinais = ["gravidade"]
numericas = ["idade", "tempo_internacao_dias"]

preprocessador = ColumnTransformer([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False), nominais),
    ("ordinal", OrdinalEncoder(categories=[["Leve", "Moderada", "Grave"]]), ordinais),
    ("escala", StandardScaler(), numericas),
])
pipeline = Pipeline([("preprocessamento", preprocessador)])

X = limpo[nominais + ordinais + numericas]
X_treino, X_teste = train_test_split(X, test_size=0.25, random_state=42)

Xt_treino = pipeline.fit_transform(X_treino)   # fit SÓ no treino
Xt_teste = pipeline.transform(X_teste)         # teste: apenas transform
print("treino:", Xt_treino.shape, "| teste:", Xt_teste.shape)
print(list(pipeline.get_feature_names_out()))
```
Saída:
```
treino: (222, 14) | teste: (75, 14)
['onehot__diagnostico_principal_AVC', 'onehot__diagnostico_principal_Fratura de fêmur', 'onehot__diagnostico_principal_Infecção urinária', 'onehot__diagnostico_principal_Insuficiência cardíaca', 'onehot__diagnostico_principal_Pneumonia', 'onehot__sexo_F', 'onehot__sexo_M', 'onehot__municipio_Caicó', 'onehot__municipio_Mossoró', 'onehot__municipio_Natal', 'onehot__municipio_Parnamirim', 'ordinal__gravidade', 'escala__idade', 'escala__tempo_internacao_dias']

```

```python
escala = pipeline.named_steps["preprocessamento"].named_transformers_["escala"]
print("Médias aprendidas no TREINO (idade, dias):", escala.mean_.round(2))
nomes = pipeline.get_feature_names_out()
pos = [list(nomes).index("escala__idade"), list(nomes).index("escala__tempo_internacao_dias")]
print("Média após escalar — treino:", Xt_treino[:, pos].mean(axis=0).round(3) + 0.0,
      "| teste:", Xt_teste[:, pos].mean(axis=0).round(3))
```
Saída:
```
Médias aprendidas no TREINO (idade, dias): [49.49  6.59]
Média após escalar — treino: [0. 0.] | teste: [-0.073  0.124]

```

No treino a média padronizada é exatamente 0; no teste é **próxima** de 0, mas não igual — e é assim que deve ser: o teste foi transformado com a média e o desvio **do treino**.

Agora, uma internação de um município que **não existia** no treino (`Assu`). Com `handle_unknown="ignore"`, o pipeline não quebra: todas as colunas de município ficam 0.

```python
novo = pd.DataFrame([{"diagnostico_principal": "AVC", "sexo": "F", "municipio": "Assu",
                      "gravidade": "Grave", "idade": 70, "tempo_internacao_dias": 12}])
saida_nova = pd.DataFrame(pipeline.transform(novo), columns=nomes)
saida_nova.filter(like="municipio").join(saida_nova[["ordinal__gravidade"]])
```
Saída:
```
   onehot__municipio_Caicó  onehot__municipio_Mossoró  onehot__municipio_Natal  onehot__municipio_Parnamirim  ordinal__gravidade
0                      0.0                        0.0                      0.0                           0.0                 2.0
```

## Resumo do pipeline

```
Extract    read_csv / read_json  (fontes intocadas)
Transform  tipos: to_datetime, moeda → float, S/N → bool
           padronização: strip, capitalize, map
           duplicatas: drop_duplicates
           junção: merge(validate=..., indicator=True)
           atributos: tempo de internação, idade, cut, qcut
           codificação: get_dummies / OneHotEncoder · dicionário / OrdinalEncoder · LabelEncoder (alvo)
           validação: assert
Load       to_csv + to_parquet + dicionário de dados
```

**Próximo passo:** praticar com o exercício `Aula10_Exercicio_Pratico.ipynb` (consultas ambulatoriais) e depois fazer a **atividade de entrega** com `dados/exames_laboratoriais.csv`.

