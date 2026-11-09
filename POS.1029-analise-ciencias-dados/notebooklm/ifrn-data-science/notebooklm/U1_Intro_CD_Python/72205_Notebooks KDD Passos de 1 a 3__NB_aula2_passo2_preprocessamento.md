# aula2_passo2_preprocessamento.ipynb

```python

%matplotlib inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


```

```python
# ── Entrada ─────────────────────────────────────────────────────────────────
df = pd.read_csv("dados_selecionados.csv", encoding="utf-8")

print("=" * 65)
print("PASSO 2 — PRÉ-PROCESSAMENTO")
print("=" * 65)
print(f"\n[ENTRADA] {len(df):,} registros, {df.shape[1]} colunas")

```
Saída:
```
=================================================================
PASSO 2 — PRÉ-PROCESSAMENTO
=================================================================

[ENTRADA] 25,923 registros, 11 colunas

```

```python
NOTAS = ["NU_NOTA_CN", "NU_NOTA_CH", "NU_NOTA_LC", "NU_NOTA_MT", "NU_NOTA_REDACAO"]

print("\n[DIAGNÓSTICO] Valores ausentes (NaN) por coluna:")
for col in NOTAS:
    n = df[col].isna().sum()
    print(f"   {col} : {n} ({n/len(df)*100:.1f}%)")

print("\n[DIAGNÓSTICO] Notas zero (suspeitas) por coluna:")
for col in NOTAS:
    n = (df[col] == 0).sum()
    print(f"   {col}: {n} ({n/len(df)*100:.1f}%)")
```
Saída:
```

[DIAGNÓSTICO] Valores ausentes (NaN) por coluna:
   NU_NOTA_CN : 0 (0.0%)
   NU_NOTA_CH : 0 (0.0%)
   NU_NOTA_LC : 0 (0.0%)
   NU_NOTA_MT : 0 (0.0%)
   NU_NOTA_REDACAO : 0 (0.0%)

[DIAGNÓSTICO] Notas zero (suspeitas) por coluna:
   NU_NOTA_CN: 1 (0.0%)
   NU_NOTA_CH: 39 (0.2%)
   NU_NOTA_LC: 3 (0.0%)
   NU_NOTA_MT: 2 (0.0%)
   NU_NOTA_REDACAO: 1555 (6.0%)

```

```python
antes = len(df)
for col in NOTAS:
    df[col] = df[col].replace(0, np.nan)
```

```python
print(f"\n[TRATAMENTO] Notas zero convertidas para NaN em: {NOTAS}")

```
Saída:
```

[TRATAMENTO] Notas zero convertidas para NaN em: ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']

```

```python
df_clean = df.dropna(subset=NOTAS).copy()
removidos = antes - len(df_clean)
print(f"[TRATAMENTO] Registros removidos por nota NaN    : {removidos:,}")
print(f"[RESULTADO]  Registros restantes                 : {len(df_clean):,}")
```
Saída:
```
[TRATAMENTO] Registros removidos por nota NaN    : 1,593
[RESULTADO]  Registros restantes                 : 24,330

```

```python
dupl = df_clean.duplicated().sum()
print(f"\n[DIAGNÓSTICO] Registros duplicados               : {dupl}")
if dupl:
    df_clean = df_clean.drop_duplicates()
    print(f"[TRATAMENTO]  Duplicatas removidas.")
```
Saída:
```

[DIAGNÓSTICO] Registros duplicados               : 0

```

```python
# ── 2.5  Checar e corrigir tipos de dados ───────────────────────────────────
df_clean["CO_ESCOLA"] = df_clean["CO_ESCOLA"].astype(str)
df_clean["TP_LOCALIZACAO_ESC"] = df_clean["TP_LOCALIZACAO_ESC"].astype("Int64")
df_clean["TP_DEPENDENCIA_ADM_ESC"] = df_clean["TP_DEPENDENCIA_ADM_ESC"].astype("Int64")

```

```python
df_clean
```
Saída:
```
      CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0      24077879                 Extremoz                       2   
1      24070297               São Miguel                       2   
3      24000647                  Baraúna                       2   
4      24083054  São Gonçalo do Amarante                       1   
5      24087351                 Extremoz                       2   
...         ...                      ...                     ...   
25918  24039357                Barcelona                       2   
25919  24082147                Goianinha                       4   
25920  24061778                Goianinha                       2   
25921  24060798                     Arês                       2   
25922  24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
3                       1       498.0       393.3       502.1       356.7   
4                       1       338.7       492.0       484.0       437.1   
5                       1       414.5       470.5       506.9       385.6   
...                   ...         ...         ...         ...         ...   
25918                   1       430.7       332.8       512.8       504.0   
25919                   1       563.9       432.0       547.9       601.8   
25920                   1       433.7       564.5       502.5       539.1   
25921                   1       400.4       432.8       400.4       412.6   
25922                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  \
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...   
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA   
3                800.0                      ESCOLA ESTADUAL JOAO DE ABREU   
4                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE   
5                440.0  CEEP CENTRO DE EDUCACAO PROFISSIONAL PROFESSOR...   
...                ...                                                ...   
25918            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...   
25919            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA   
25920            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO   
25921            280.0                          ESCOLA ESTADUAL JACUMAUMA   
25922            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO   

      TIPO_ESCOLA  
0        Estadual  
1        Estadual  
3        Estadual  
4         Federal  
5        Estadual  
...           ...  
25918    Estadual  
25919     Privada  
25920    Estadual  
25921    Estadual  
25922    Estadual  

[24330 rows x 11 columns]
```

```python
# ── 2.6  Padronizar tipo de escola faltante (sem match no catálogo) ──────────
sem_nome = df_clean["NO_ESCOLA"].isna().sum()
if sem_nome:
    df_clean["NO_ESCOLA"] = df_clean["NO_ESCOLA"].fillna("Escola não identificada")
    print(f"\n[TRATAMENTO] Escolas sem match no catálogo       : {sem_nome} → preenchidas")
```
Saída:
```

[TRATAMENTO] Escolas sem match no catálogo       : 175 → preenchidas

```

```python
# ── 2.7  Boxplots antes/depois da limpeza para cada nota ────────────────────
fig, axes = plt.subplots(1, 5, figsize=(18, 5))
fig.suptitle("Distribuição das Notas após Pré-processamento\n(candidatos com presença completa e notas válidas)",
             fontsize=12, fontweight="bold")

```
Saída:
```
Text(0.5, 0.98, 'Distribuição das Notas após Pré-processamento\n(candidatos com presença completa e notas válidas)')
```
Saída:
```
<Figure size 1800x500 with 5 Axes>
```

```python
LABELS = ["Ciências\nNatureza", "Ciências\nHumanas", "Linguagens", "Matemática", "Redação"]
CORES  = ["#4e79a7", "#f28e2b", "#59a14f", "#e15759", "#76b7b2"]
```

```python
fig, axes = plt.subplots(1, 5, figsize=(18, 5))
fig.suptitle("Distribuição das Notas após Pré-processamento\n(candidatos com presença completa e notas válidas)",
             fontsize=12, fontweight="bold")

# Assuming NOTAS, LABELS, CORES, df_clean are still defined from previous cells
for ax, col, label, cor in zip(axes, NOTAS, LABELS, CORES):
    ax.boxplot(df_clean[col].dropna(), patch_artist=True,
               boxprops=dict(facecolor=cor, alpha=0.7),
               medianprops=dict(color="black", linewidth=2))
    ax.set_title(label, fontsize=10)
    ax.set_ylabel("Nota (0–1000)")
    ax.set_xticks([])
    media = df_clean[col].mean()
    mediana = df_clean[col].median()
    ax.axhline(media, color="navy", linestyle="--", linewidth=1,
               label=f"Média: {media:.0f} ")
    ax.axhline(mediana, color="black", linestyle="-", linewidth=1,
               label=f"Mediana: {mediana:.0f} ")
    ax.legend(fontsize=8)

plt.tight_layout()
plt.show()

plt.savefig("passo2_boxplots.png", dpi=120, bbox_inches="tight")
print("\n[OK] Gráfico salvo: passo2_boxplots.png")
```
Saída:
```
<Figure size 1800x500 with 5 Axes>
```
Saída:
```

[OK] Gráfico salvo: passo2_boxplots.png

```
Saída:
```
<Figure size 640x480 with 0 Axes>
```

```python
# ── 2.8  Relatório final ─────────────────────────────────────────────────────
print("\n[RESUMO PRÉ-PROCESSAMENTO]")
print(f"   Registros de entrada  : {antes:,}")
print(f"   Registros de saída    : {len(df_clean):,}")
print(f"   Perda total           : {antes - len(df_clean):,} ({(antes-len(df_clean))/antes*100:.1f}%)")
print("\n[ESTATÍSTICAS FINAIS DAS NOTAS]")
print(df_clean[NOTAS].describe().round(2).to_string())
```
Saída:
```

[RESUMO PRÉ-PROCESSAMENTO]
   Registros de entrada  : 25,923
   Registros de saída    : 24,330
   Perda total           : 1,593 (6.1%)

[ESTATÍSTICAS FINAIS DAS NOTAS]
       NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  NU_NOTA_REDACAO
count    24330.00    24330.00    24330.00    24330.00         24330.00
mean       503.88      510.46      532.86      520.11           638.38
std         75.35       81.77       68.25      126.67           160.20
min        324.70      325.60      316.50      314.80            40.00
25%        449.80      447.20      491.70      416.80           520.00
50%        502.60      509.85      537.40      499.80           640.00
75%        553.00      570.40      579.70      608.40           760.00
max        858.70      800.80      794.50      967.70           980.00

```

```python
df_clean.to_csv("dados_preprocessados.csv", index=False, encoding="utf-8")
print(f"\n[OK] Arquivo salvo: dados_preprocessados.csv  ({len(df_clean):,} registros)")
print("\nPronto! Execute o passo3_transformacao.py em seguida.")
```
Saída:
```

[OK] Arquivo salvo: dados_preprocessados.csv  (24,330 registros)

Pronto! Execute o passo3_transformacao.py em seguida.

```

