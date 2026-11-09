# aula2_passo1_selecao.ipynb



```python
import pandas as pd

# ── Caminhos dos arquivos ───────────────────────────────────────────────────
RESULTADOS = "RESULTADOS_2025_RN.csv"
CATALOGO   = "catalogo_escolas_rn.csv"

# ── 1.1  Carregamento dos dados brutos ─────────────────────────────────────
print("=" * 70)
print("PASSO 1 — SELEÇÃO")
print("=" * 70)
```
Saída:
```
======================================================================
PASSO 1 — SELEÇÃO
======================================================================

```

```python
df_raw = pd.read_csv(RESULTADOS, sep=";", encoding="latin1")
df_cat = pd.read_csv(CATALOGO,   sep=",", encoding="latin1")
```

```python
print(f"\n[RAW] Registros totais no arquivo de resultados   : {len(df_raw):,}")
print(f"[RAW] Colunas disponíveis                         : {df_raw.shape[1]}")
print(f"[CAT] Escolas no catálogo                         : {len(df_cat):,}")
```
Saída:
```

[RAW] Registros totais no arquivo de resultados   : 30,449
[RAW] Colunas disponíveis                         : 70
[CAT] Escolas no catálogo                         : 4,938

```

```python
presenca_completa = (
    (df_raw["TP_PRESENCA_CN"] == 1) &
    (df_raw["TP_PRESENCA_CH"] == 1) &
    (df_raw["TP_PRESENCA_LC"] == 1) &
    (df_raw["TP_PRESENCA_MT"] == 1)
)

presenca_completa
```
Saída:
```
0         True
1        False
2         True
3         True
4         True
         ...  
30444     True
30445     True
30446     True
30447     True
30448    False
Length: 30449, dtype: bool
```

```python
df_presentes = df_raw[presenca_completa].copy()

print(f"\n [SELEÇÃO] Candidatos com presença completa       : {len(df_presentes):,}")
print(f"[EXCLUSÃO] Descartados por ausência               : {len(df_raw) - len(df_presentes):,}")

```
Saída:
```

 [SELEÇÃO] Candidatos com presença completa       : 25,923
[EXCLUSÃO] Descartados por ausência               : 4,526

```

```python
COLUNAS = [
    "CO_ESCOLA",               # chave para join com catálogo
    "NO_MUNICIPIO_ESC",        # município da escola
    "TP_DEPENDENCIA_ADM_ESC",  # 1=Federal, 2=Estadual, 3=Municipal, 4=Privada
    "TP_LOCALIZACAO_ESC",      # 1=Urbana, 2=Rural
    "NU_NOTA_CN",              # Ciências da Natureza
    "NU_NOTA_CH",              # Ciências Humanas
    "NU_NOTA_LC",              # Linguagens e Códigos
    "NU_NOTA_MT",              # Matemática
    "NU_NOTA_REDACAO",      # Redação
]

df_sel = df_presentes[COLUNAS].copy()
```

```python
df_sel = df_sel.merge(df_cat, on="CO_ESCOLA", how="left")

print(f"\n[SELEÇÃO] Colunas selecionadas                   : {df_sel.shape[1]}")
print(f"[SELEÇÃO] Escolas identificadas pelo catálogo    : "
      f"{df_sel['NO_ESCOLA'].notna().sum():,} / {len(df_sel):,}")
```
Saída:
```

[SELEÇÃO] Colunas selecionadas                   : 10
[SELEÇÃO] Escolas identificadas pelo catálogo    : 25,738 / 25,923

```

```python
df_sel
```
Saída:
```
       CO_ESCOLA         NO_MUNICIPIO_ESC  TP_DEPENDENCIA_ADM_ESC  \
0       24077879                 Extremoz                       2   
1       24070297               São Miguel                       2   
2       24005908                 Caraúbas                       2   
3       24000647                  Baraúna                       2   
4       24083054  São Gonçalo do Amarante                       1   
...          ...                      ...                     ...   
25918   24039357                Barcelona                       2   
25919   24082147                Goianinha                       4   
25920   24061778                Goianinha                       2   
25921   24060798                     Arês                       2   
25922   24061778                Goianinha                       2   

       TP_LOCALIZACAO_ESC  NU_NOTA_CN  NU_NOTA_CH  NU_NOTA_LC  NU_NOTA_MT  \
0                       2       477.8       392.1       476.0       442.8   
1                       1       455.2       517.2       510.7       370.9   
2                       1       395.9       468.0       443.0       491.9   
3                       1       498.0       393.3       502.1       356.7   
4                       1       338.7       492.0       484.0       437.1   
...                   ...         ...         ...         ...         ...   
25918                   1       430.7       332.8       512.8       504.0   
25919                   1       563.9       432.0       547.9       601.8   
25920                   1       433.7       564.5       502.5       539.1   
25921                   1       400.4       432.8       400.4       412.6   
25922                   1       384.6       475.4       568.0       479.7   

       NU_NOTA_REDACAO                                          NO_ESCOLA  
0                400.0  CENTRO DE EDUCACAO PROFISSIONAL E AMBIENTAL ES...  
1                520.0                    ESCOLA ESTADUAL GILNEY DE SOUZA  
2                  0.0                   ESCOLA ESTADUAL SEBASTIAO GURGEL  
3                800.0                      ESCOLA ESTADUAL JOAO DE ABREU  
4                520.0              IFRN - CAMPUS SAO GONCALO DO AMARANTE  
...                ...                                                ...  
25918            540.0  ESCOLA ESTADUAL PROFESSOR TERTULIANO PINHEIRO ...  
25919            520.0            COLEGIO NOSSA SENHORA DOS PRAZERES LTDA  
25920            600.0                      ESCOLA ESTADUAL JOAO TIBURCIO  
25921            280.0                          ESCOLA ESTADUAL JACUMAUMA  
25922            580.0                      ESCOLA ESTADUAL JOAO TIBURCIO  

[25923 rows x 10 columns]
```

```python


print("\n[SELEÇÃO] Candidatos por tipo de escola:")
print(df_sel["TIPO_ESCOLA"].value_counts().to_string())
```
Saída:
```

[SELEÇÃO] Candidatos por tipo de escola:

```

```python
df_sel
```

```python
df_sel.to_csv("dados_selecionados.csv", index=False, encoding="utf-8")
print(f"\n[OK] Arquivo salvo: dados_selecionados.csv  ({len(df_sel):,} registros, "
      f"{df_sel.shape[1]} colunas)")
print("\nPronto! Execute o passo2_preprocessamento.py em seguida.")
```

