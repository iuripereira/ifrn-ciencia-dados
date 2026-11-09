# aula2_passo3_transformacao.ipynb

```python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
```

```python
df = pd.read_csv("dados_preprocessados.csv", encoding="utf-8")

print("=" * 65)
print("PASSO 3 — TRANSFORMAÇÃO")
print("=" * 65)
print(f"\n[ENTRADA] {len(df):,} registros")

NOTAS_OBJ  = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT"]
NOTAS_TODAS= NOTAS_OBJ + ["NU_NOTA_REDACAO"]
```
Saída:
```
=================================================================
PASSO 3 — TRANSFORMAÇÃO
=================================================================

[ENTRADA] 24,330 registros

```

```python
# ── 3.1  Atributos derivados numéricos ──────────────────────────────────────
df["MEDIA_OBJETIVAS"] = df[NOTAS_OBJ].mean(axis=1).round(2)

# Média ponderada: 4 provas objetivas + redação (peso 1)
df["MEDIA_GERAL"] = (
    (df[NOTAS_OBJ].sum(axis=1) + df["NU_NOTA_REDACAO"]) / 5
).round(2)

df["DESVIO_NOTAS"] = df[NOTAS_TODAS].std(axis=1).round(2)

print("\n[FEATURE] MEDIA_OBJETIVAS, MEDIA_GERAL, DESVIO_NOTAS criados")
```
Saída:
```

[FEATURE] MEDIA_OBJETIVAS, MEDIA_GERAL, DESVIO_NOTAS criados

```

```python
df
```
Saída:
```
       CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0       24077879                 Extremoz                       2   
1       24070297               São Miguel                       2   
2       24000647                  Baraúna                       2   
3       24083054  São Gonçalo do Amarante                       1   
4       24087351                 Extremoz                       2   
...          ...                      ...                     ...   
24325   24039357                Barcelona                       2   
24326   24082147                Goianinha                       4   
24327   24061778                Goianinha                       2   
24328   24060798                     Arês                       2   
24329   24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
2                       1       498.0       393.3       502.1       356.7   
3                       1       338.7       492.0       484.0       437.1   
4                       1       414.5       470.5       506.9       385.6   
...                   ...         ...         ...         ...         ...   
24325                   1       430.7       332.8       512.8       504.0   
24326                   1       563.9       432.0       547.9       601.8   
24327                   1       433.7       564.5       502.5       539.1   
24328                   1       400.4       432.8       400.4       412.6   
24329                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  \
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...   
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA   
2                800.0                      ESCOLA ESTADUAL JOAO DE ABREU   
3                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE   
4                440.0  CEEP CENTRO DE EDUCACAO PROFISSIONAL PROFESSOR...   
...                ...                                                ...   
24325            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...   
24326            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA   
24327            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO   
24328            280.0                          ESCOLA ESTADUAL JACUMAUMA   
24329            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO   

      TIPO_ESCOLA  MEDIA_OBJETIVAS  MEDIA_GERAL  DESVIO_NOTAS  
0        Estadual           447.18       437.74         40.62  
1        Estadual           463.50       474.80         63.85  
2        Estadual           437.52       510.02        174.23  
3         Federal           437.95       454.36         71.20  
4        Estadual           444.38       443.50         47.31  
...           ...              ...          ...           ...  
24325    Estadual           445.08       464.06         83.79  
24326     Privada           536.40       533.12         63.80  
24327    Estadual           509.95       527.96         63.60  
24328    Estadual           411.55       385.24         60.30  
24329    Estadual           476.92       497.54         79.57  

[24330 rows x 14 columns]
```

```python
# ── 3.2  Atributos derivados categóricos ────────────────────────────────────
MAPA_AREA = {
    "NU_NOTA_CN": "Ciências Natureza",
    "NU_NOTA_CH": "Ciências Humanas",
    "NU_NOTA_LC": "Linguagens",
    "NU_NOTA_MT": "Matemática",
    "NU_NOTA_REDACAO": "Redação",
}

df["MELHOR_AREA"] = df[NOTAS_TODAS].idxmax(axis=1).map(MAPA_AREA)
df["PIOR_AREA"]   = df[NOTAS_TODAS].idxmin(axis=1).map(MAPA_AREA)

print("[FEATURE] MELHOR_AREA e PIOR_AREA criados")
print("\n  Melhor área mais comum:")
print(df["MELHOR_AREA"].value_counts().to_string())
print("\n  Pior área mais comum:")
print(df["PIOR_AREA"].value_counts().to_string())

```
Saída:
```
[FEATURE] MELHOR_AREA e PIOR_AREA criados

  Melhor área mais comum:
MELHOR_AREA
Redação              16852
Matemática            2597
Linguagens            2491
Ciências Humanas      1206
Ciências Natureza     1184

  Pior área mais comum:
PIOR_AREA
Matemática           7465
Ciências Natureza    7189
Ciências Humanas     5107
Linguagens           2497
Redação              2072

```

```python
df
```
Saída:
```
       CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0       24077879                 Extremoz                       2   
1       24070297               São Miguel                       2   
2       24000647                  Baraúna                       2   
3       24083054  São Gonçalo do Amarante                       1   
4       24087351                 Extremoz                       2   
...          ...                      ...                     ...   
24325   24039357                Barcelona                       2   
24326   24082147                Goianinha                       4   
24327   24061778                Goianinha                       2   
24328   24060798                     Arês                       2   
24329   24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
2                       1       498.0       393.3       502.1       356.7   
3                       1       338.7       492.0       484.0       437.1   
4                       1       414.5       470.5       506.9       385.6   
...                   ...         ...         ...         ...         ...   
24325                   1       430.7       332.8       512.8       504.0   
24326                   1       563.9       432.0       547.9       601.8   
24327                   1       433.7       564.5       502.5       539.1   
24328                   1       400.4       432.8       400.4       412.6   
24329                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  \
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...   
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA   
2                800.0                      ESCOLA ESTADUAL JOAO DE ABREU   
3                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE   
4                440.0  CEEP CENTRO DE EDUCACAO PROFISSIONAL PROFESSOR...   
...                ...                                                ...   
24325            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...   
24326            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA   
24327            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO   
24328            280.0                          ESCOLA ESTADUAL JACUMAUMA   
24329            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO   

      TIPO_ESCOLA  MEDIA_OBJETIVAS  MEDIA_GERAL  DESVIO_NOTAS  \
0        Estadual           447.18       437.74         40.62   
1        Estadual           463.50       474.80         63.85   
2        Estadual           437.52       510.02        174.23   
3         Federal           437.95       454.36         71.20   
4        Estadual           444.38       443.50         47.31   
...           ...              ...          ...           ...   
24325    Estadual           445.08       464.06         83.79   
24326     Privada           536.40       533.12         63.80   
24327    Estadual           509.95       527.96         63.60   
24328    Estadual           411.55       385.24         60.30   
24329    Estadual           476.92       497.54         79.57   

             MELHOR_AREA          PIOR_AREA  
0      Ciências Natureza   Ciências Humanas  
1                Redação         Matemática  
2                Redação         Matemática  
3                Redação  Ciências Natureza  
4             Linguagens         Matemática  
...                  ...                ...  
24325            Redação   Ciências Humanas  
24326         Matemática   Ciências Humanas  
24327            Redação  Ciências Natureza  
24328   Ciências Humanas            Redação  
24329            Redação  Ciências
```

```python
# ── 3.3  Codificação de variáveis categóricas ───────────────────────────────
# Localização: binária (simples e interpretável)
df["LOCALIZACAO_RURAL"] = (df["TP_LOCALIZACAO_ESC"] == 2).astype(int)

# Tipo de escola: One-Hot Encoding (para evitar ordenação implícita)
df["TIPO_ESCOLA"] = df["TIPO_ESCOLA"].fillna("Estadual")
dummies = pd.get_dummies(df["TIPO_ESCOLA"], prefix="ESCOLA", drop_first=False)
df = pd.concat([df, dummies], axis=1)

# Melhor área: Label Encoding (para algoritmos tree-based)
le = LabelEncoder()
df["MELHOR_AREA_COD"] = le.fit_transform(df["MELHOR_AREA"])
df["PIOR_AREA_COD"]   = le.fit_transform(df["PIOR_AREA"])

print("\n[ENCODING] LOCALIZACAO_RURAL, One-Hot TIPO_ESCOLA, Label MELHOR/PIOR_AREA")

```
Saída:
```

[ENCODING] LOCALIZACAO_RURAL, One-Hot TIPO_ESCOLA, Label MELHOR/PIOR_AREA

```

```python
df
```
Saída:
```
       CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0       24077879                 Extremoz                       2   
1       24070297               São Miguel                       2   
2       24000647                  Baraúna                       2   
3       24083054  São Gonçalo do Amarante                       1   
4       24087351                 Extremoz                       2   
...          ...                      ...                     ...   
24325   24039357                Barcelona                       2   
24326   24082147                Goianinha                       4   
24327   24061778                Goianinha                       2   
24328   24060798                     Arês                       2   
24329   24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
2                       1       498.0       393.3       502.1       356.7   
3                       1       338.7       492.0       484.0       437.1   
4                       1       414.5       470.5       506.9       385.6   
...                   ...         ...         ...         ...         ...   
24325                   1       430.7       332.8       512.8       504.0   
24326                   1       563.9       432.0       547.9       601.8   
24327                   1       433.7       564.5       502.5       539.1   
24328                   1       400.4       432.8       400.4       412.6   
24329                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  \
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...   
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA   
2                800.0                      ESCOLA ESTADUAL JOAO DE ABREU   
3                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE   
4                440.0  CEEP CENTRO DE EDUCACAO PROFISSIONAL PROFESSOR...   
...                ...                                                ...   
24325            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...   
24326            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA   
24327            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO   
24328            280.0                          ESCOLA ESTADUAL JACUMAUMA   
24329            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO   

       ... MEDIA_GERAL  DESVIO_NOTAS        MELHOR_AREA          PIOR_AREA  \
0      ...      437.74         40.62  Ciências Natureza   Ciências Humanas   
1      ...      474.80         63.85            Redação         Matemática   
2      ...      510.02        174.23            Redação         Matemática   
3      ...      454.36         71.20            Redação  Ciências Natureza   
4      ...      443.50         47.31         Linguagens         Matemática   
...    ...         ...           ...                ...                ...   
24325  ...      464.06         83.79            Redação   Ciências Humanas   
24326  ...      533.12         63.80         Matemática   Ciências Humanas   
24327  ...      527.96         63.60            Redação  Ciências Natureza   
24328  ...      385.24         60.30   Ciências Humanas            Redação   
24329  ...      497.54         79.57            Redação  Ciências Natureza   

      LOCALIZACAO_RURAL ESCOLA_Estadual  ESCOLA_Federal  ESCOLA_Privada  \
0                     1            True           False           False   
1                     0            True           False           False   
2                     0            True           False           False   
3                     0           False            True           False   
4        
```

```python
# ── 3.4  Variável-alvo: NIVEL_DESEMPENHO ────────────────────────────────────
LIMITES = [0, 400, 550, 700, 1001]
ROTULOS = ["Insuficiente", "Regular", "Bom", "Excelente"]

df["NIVEL_DESEMPENHO"] = pd.cut(
    df["MEDIA_GERAL"],
    bins=LIMITES,
    labels=ROTULOS,
    right=False
)

print("\n[TARGET] Distribuição de NIVEL_DESEMPENHO:")
contagem = df["NIVEL_DESEMPENHO"].value_counts().sort_index()
for nivel, n in contagem.items():
    print(f"   {nivel:<14}: {n:>5} ({n/len(df)*100:.1f}%)")
```
Saída:
```

[TARGET] Distribuição de NIVEL_DESEMPENHO:
   Insuficiente  :   686 (2.8%)
   Regular       : 13218 (54.3%)
   Bom           :  9376 (38.5%)
   Excelente     :  1050 (4.3%)

```

```python
# ── 3.5  Normalização Min-Max das notas brutas ──────────────────────────────
# (útil para algoritmos sensíveis à escala: KNN, SVM, Redes Neurais)
scaler = MinMaxScaler()
COLUNAS_NORM = NOTAS_TODAS + ["MEDIA_OBJETIVAS", "MEDIA_GERAL", "DESVIO_NOTAS"]
df_norm = df.copy()
df_norm[[c + "_NORM" for c in COLUNAS_NORM]] = scaler.fit_transform(df[COLUNAS_NORM])

print("\n[NORMALIZAÇÃO] Min-Max aplicada às notas e médias")
print(f"   Faixa original  MEDIA_GERAL: {df['MEDIA_GERAL'].min():.1f} – {df['MEDIA_GERAL'].max():.1f}")
print(f"   Faixa normalizd MEDIA_GERAL: "
      f"{df_norm['MEDIA_GERAL_NORM'].min():.3f} – {df_norm['MEDIA_GERAL_NORM'].max():.3f}")

```
Saída:
```

[NORMALIZAÇÃO] Min-Max aplicada às notas e médias
   Faixa original  MEDIA_GERAL: 306.8 – 843.5
   Faixa normalizd MEDIA_GERAL: 0.000 – 1.000

```

```python
df_norm
```
Saída:
```
       CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0       24077879                 Extremoz                       2   
1       24070297               São Miguel                       2   
2       24000647                  Baraúna                       2   
3       24083054  São Gonçalo do Amarante                       1   
4       24087351                 Extremoz                       2   
...          ...                      ...                     ...   
24325   24039357                Barcelona                       2   
24326   24082147                Goianinha                       4   
24327   24061778                Goianinha                       2   
24328   24060798                     Arês                       2   
24329   24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
2                       1       498.0       393.3       502.1       356.7   
3                       1       338.7       492.0       484.0       437.1   
4                       1       414.5       470.5       506.9       385.6   
...                   ...         ...         ...         ...         ...   
24325                   1       430.7       332.8       512.8       504.0   
24326                   1       563.9       432.0       547.9       601.8   
24327                   1       433.7       564.5       502.5       539.1   
24328                   1       400.4       432.8       400.4       412.6   
24329                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  \
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...   
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA   
2                800.0                      ESCOLA ESTADUAL JOAO DE ABREU   
3                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE   
4                440.0  CEEP CENTRO DE EDUCACAO PROFISSIONAL PROFESSOR...   
...                ...                                                ...   
24325            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...   
24326            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA   
24327            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO   
24328            280.0                          ESCOLA ESTADUAL JACUMAUMA   
24329            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO   

       ... PIOR_AREA_COD  NIVEL_DESEMPENHO  NU_NOTA_CN_NORM  NU_NOTA_CH_NORM  \
0      ...             0           Regular         0.286704         0.139941   
1      ...             3           Regular         0.244382         0.403199   
2      ...             3           Regular         0.324532         0.142466   
3      ...             1           Regular         0.026217         0.350168   
4      ...             3           Regular         0.168165         0.304924   
...    ...           ...               ...              ...              ...   
24325  ...             0           Regular         0.198502         0.015152   
24326  ...             0           Regular         0.447940         0.223906   
24327  ...             1           Regular         0.204120         0.502736   
24328  ...             4      Insuficiente         0.141760         0.225589   
24329  ...             1           Regular         0.112172         0.315236   

      NU_NOTA_LC_NORM NU_NOTA_MT_NORM  NU_NOTA_REDACAO_NORM  \
0            0.333682        0.196048              0.382979   
1            0.406276        0.085924              0.510638   
2            0.388285        0.064175              0.808511   
3            0.350418        0.187318              0.510638   
4            0.398326        0.108439        
```

```python
# ── 3.6  Visualização da distribuição de média geral ────────────────────────
CORES_NIVEL = {
    "Insuficiente": "#e15759",
    "Regular"     : "#f28e2b",
    "Bom"         : "#4e79a7",
    "Excelente"   : "#59a14f",
}

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Passo 3 — Transformação: Variável-Alvo e Distribuição", fontsize=13, fontweight="bold")

# Histograma da média geral com fronteiras dos níveis
ax = axes[0]
ax.hist(df["MEDIA_GERAL"], bins=60, color="#4e79a7", edgecolor="white", alpha=0.8)
for lim, rot in zip(LIMITES[1:-1], ROTULOS[:-1]):
    ax.axvline(lim, color="red", linestyle="--", linewidth=1.2)
    ax.text(lim + 5, ax.get_ylim()[1] * 0.95, rot, fontsize=8, color="red", rotation=90, va="top")
ax.set_title("Histograma da Média Geral")
ax.set_xlabel("Média Geral (pontos)")
ax.set_ylabel("Frequência")

# Pizza dos níveis
ax = axes[1]
sizes  = [contagem.get(r, 0) for r in ROTULOS]
colors = [CORES_NIVEL[r] for r in ROTULOS]
wedges, texts, autotexts = ax.pie(
    sizes, labels=ROTULOS, colors=colors,
    autopct="%1.1f%%", startangle=140, pctdistance=0.75
)
for at in autotexts:
    at.set_fontsize(9)
ax.set_title("Distribuição de Nível de Desempenho")

plt.tight_layout()
plt.savefig("passo3_transformacao.png", dpi=120, bbox_inches="tight")
plt.close()
print("\n[OK] Gráfico salvo: passo3_transformacao.png")
```
Saída:
```

[OK] Gráfico salvo: passo3_transformacao.png

```

```python
# ── 3.7  Definir conjunto de features para ML ───────────────────────────────
FEATURES = (
    ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO",
     "MEDIA_OBJETIVAS", "DESVIO_NOTAS", "LOCALIZACAO_RURAL",
     "MELHOR_AREA_COD", "PIOR_AREA_COD"]
    + [c for c in df.columns if c.startswith("ESCOLA_")]
)
TARGET = "NIVEL_DESEMPENHO"

print(f"\n[FEATURES FINAIS] ({len(FEATURES)} atributos):")
for f in FEATURES:
    print(f"   • {f}")

```
Saída:
```

[FEATURES FINAIS] (13 atributos):
   • NU_NOTA_CN
   • NU_NOTA_CH
   • NU_NOTA_LC
   • NU_NOTA_MT
   • NU_NOTA_REDACAO
   • MEDIA_OBJETIVAS
   • DESVIO_NOTAS
   • LOCALIZACAO_RURAL
   • MELHOR_AREA_COD
   • PIOR_AREA_COD
   • ESCOLA_Estadual
   • ESCOLA_Federal
   • ESCOLA_Privada

```

```python
# ── Salvar ───────────────────────────────────────────────────────────────────
df.to_csv("dados_transformados.csv", index=False, encoding="utf-8")
print(f"\n[OK] Arquivo salvo: dados_transformados.csv  ({len(df):,} registros)")
print("\nPronto! Execute o passo4_mineracao.py em seguida.")

```
Saída:
```

[OK] Arquivo salvo: dados_transformados.csv  (24,330 registros)

Pronto! Execute o passo4_mineracao.py em seguida.

```

