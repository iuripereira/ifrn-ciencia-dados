"""Gera os datasets SINTÉTICOS ("sujos") da Aula 09 — Qualidade de Dados e Limpeza.

Nenhum dado é de paciente real: tudo é sorteado com semente fixa (reprodutível).
Os problemas de qualidade são inseridos de propósito e documentados abaixo.
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).parent / "dados"
RAIZ.mkdir(exist_ok=True)
rng = np.random.default_rng(2026)

# ----------------------------------------------------------------------------
# 1) Laboratório: atendimentos em Unidades Básicas de Saúde (UBS) do RN
# ----------------------------------------------------------------------------
N = 240
municipios = ["Natal", "Mossoró", "Parnamirim", "Caicó", "Pau dos Ferros"]
pesos_mun = [0.40, 0.25, 0.18, 0.10, 0.07]
diagnosticos = ["Hipertensão", "Diabetes", "Consulta de rotina", "Infecção respiratória"]

idade = rng.integers(18, 90, N).astype(float)
sexo = rng.choice(["F", "M"], N, p=[0.56, 0.44])
altura = np.where(sexo == "F", rng.normal(158, 6, N), rng.normal(171, 7, N)).round(0)
imc = rng.normal(27, 4.5, N).clip(17, 42)
peso = (imc * (altura / 100) ** 2).round(1)
diag = rng.choice(diagnosticos, N, p=[0.32, 0.18, 0.35, 0.15])
pas = rng.normal(125, 14, N) + np.where(diag == "Hipertensão", 18, 0) + (idade - 50) * 0.25
pas = pas.round(0)
glic = rng.normal(98, 12, N) + np.where(diag == "Diabetes", 70, 0)
glic = glic.round(0)
datas = pd.to_datetime("2026-03-02") + pd.to_timedelta(rng.integers(0, 120, N), unit="D")

df = pd.DataFrame({
    "id_atendimento": np.arange(1001, 1001 + N),
    "data_atendimento": datas.strftime("%Y-%m-%d"),
    "municipio": rng.choice(municipios, N, p=pesos_mun),
    "sexo": sexo,
    "idade": idade,
    "peso_kg": peso,
    "altura_cm": altura,
    "pressao_sistolica": pas,
    "glicemia_mg_dl": glic,
    "diagnostico": diag,
}).astype({"municipio": object, "sexo": object, "diagnostico": object, "data_atendimento": object})


def escolher(n, excluir=()):
    pool = np.setdiff1d(np.arange(N), np.array(list(excluir), dtype=int))
    return rng.choice(pool, n, replace=False)


usados = set()


def marca(idx):
    usados.update(int(i) for i in idx)
    return idx


# Texto inconsistente
for i in marca(escolher(30)):
    m = df.at[i, "municipio"]
    variantes = {"Natal": ["natal", " NATAL", "Natal "], "Mossoró": ["Mossoro", "MOSSORÓ", "mossoró"],
                 "Parnamirim": ["parnamirim", "PARNAMIRIM"], "Caicó": ["Caico", "caicó"],
                 "Pau dos Ferros": ["Pau Dos Ferros", "pau dos ferros"]}[m]
    df.at[i, "municipio"] = rng.choice(variantes)
for i in escolher(25):
    df.at[i, "sexo"] = {"F": rng.choice(["f", "Feminino", "FEMININO"]), "M": rng.choice(["m", "Masculino"])}[df.at[i, "sexo"]]
for i in escolher(20):
    df.at[i, "diagnostico"] = {"Hipertensão": "hipertensao", "Diabetes": "DIABETES",
                               "Consulta de rotina": "consulta de rotina",
                               "Infecção respiratória": "Infeccao respiratoria"}[df.at[i, "diagnostico"]]

# Datas em formato brasileiro misturado
for i in escolher(18):
    d = pd.to_datetime(df.at[i, "data_atendimento"])
    df.at[i, "data_atendimento"] = d.strftime("%d/%m/%Y")

# Unidades erradas: altura em metros, peso em gramas
for i in marca(escolher(9, usados)):
    df.at[i, "altura_cm"] = round(df.at[i, "altura_cm"] / 100, 2)
for i in marca(escolher(3, usados)):
    df.at[i, "peso_kg"] = round(df.at[i, "peso_kg"] * 1000, 0)

# Erros de digitação que viram outliers
erros_idade = marca(escolher(3, usados))
for i, v in zip(erros_idade, [150, 205, -3]):
    df.at[i, "idade"] = v
erros_pas = marca(escolher(3, usados))
for i, v in zip(erros_pas, [12, 1300, 410]):          # 12 → 120?  1300 → 130?
    df.at[i, "pressao_sistolica"] = v
# um valor extremo PLAUSÍVEL (crise hipertensiva) — não é erro
plaus = marca(escolher(1, usados))
df.loc[plaus, "pressao_sistolica"] = 205
df.loc[plaus, "diagnostico"] = "Hipertensão"

# Ausentes (NaN) e um código sentinela 999 = "não medido"
for col, n in [("idade", 7), ("peso_kg", 11), ("glicemia_mg_dl", 22), ("pressao_sistolica", 6)]:
    df.loc[escolher(n, usados), col] = np.nan
df.loc[escolher(6, usados), "sexo"] = np.nan
df.loc[marca(escolher(5, usados)), "glicemia_mg_dl"] = 999

# Duplicatas exatas (registro lançado duas vezes)
dup = df.loc[rng.choice(np.arange(N), 10, replace=False)]
df_lab = pd.concat([df, dup], ignore_index=True)
df_lab = df_lab.sample(frac=1, random_state=7).reset_index(drop=True)
df_lab.to_csv(RAIZ / "atendimentos_ubs_sujo.csv", index=False, encoding="utf-8")

# ----------------------------------------------------------------------------
# 2) Tidy data: doses de vacina contra influenza por município e mês (formato LARGO)
# ----------------------------------------------------------------------------
larga = pd.DataFrame({"municipio": municipios})
for mes, base in [("mar", 900), ("abr", 2600), ("mai", 3100), ("jun", 1200)]:
    larga[mes] = (base * np.array(pesos_mun) * rng.uniform(0.85, 1.15, len(municipios))).round(0).astype(int)
larga.to_csv(RAIZ / "vacinacao_influenza_larga.csv", index=False, encoding="utf-8")

# ----------------------------------------------------------------------------
# 3) Exercício: triagem de pronto atendimento (menor e mais simples)
# ----------------------------------------------------------------------------
M = 60
risco = rng.choice(["Azul", "Verde", "Amarelo", "Vermelho"], M, p=[0.15, 0.45, 0.30, 0.10])
tri = pd.DataFrame({
    "id_paciente": [f"P{n:03d}" for n in range(1, M + 1)],
    "sexo": rng.choice(["F", "M"], M),
    "idade": rng.integers(1, 95, M).astype(float),
    "temperatura_c": (rng.normal(37.0, 0.6, M) + np.where(risco == "Vermelho", 1.2, 0)).round(1),
    "freq_cardiaca": (rng.normal(84, 10, M) + np.where(risco == "Vermelho", 25, 0)).round(0),
    "saturacao_o2": (rng.normal(97, 1.4, M) - np.where(risco == "Vermelho", 5, 0)).round(0).clip(80, 100),
    "classificacao_risco": risco,
}).astype({"classificacao_risco": object, "sexo": object})
for i in rng.choice(M, 12, replace=False):
    tri.at[i, "classificacao_risco"] = {"Azul": "azul", "Verde": rng.choice(["verde", "VERDE"]),
                                        "Amarelo": rng.choice(["amarelo", "AMARELO"]),
                                        "Vermelho": "vermelho"}[tri.at[i, "classificacao_risco"]]
alvo = rng.choice(M, 9, replace=False)
tri.loc[alvo[0], "temperatura_c"] = 375.0       # vírgula esquecida: 37,5
tri.loc[alvo[1], "freq_cardiaca"] = 300.0       # erro de digitação
tri.loc[alvo[2], "saturacao_o2"] = 9.0          # 9 em vez de 96?
tri.loc[alvo[3:7], "temperatura_c"] = np.nan
tri.loc[alvo[7:9], "saturacao_o2"] = np.nan
dup_t = tri.loc[rng.choice(np.setdiff1d(np.arange(M), alvo), 4, replace=False)]
tri = pd.concat([tri, dup_t], ignore_index=True).sample(frac=1, random_state=3).reset_index(drop=True)
tri.to_csv(RAIZ / "triagem_pa_sujo.csv", index=False, encoding="utf-8")

print("lab:", df_lab.shape, "| larga:", larga.shape, "| exercicio:", tri.shape)
