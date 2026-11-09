"""Gera os dados SINTÉTICOS da Aula 10 — Pipeline de Limpeza Completo.

Nenhum registro é de paciente real: tudo é sorteado com semente fixa (reprodutível).
  dados/pacientes.csv              cadastro de pacientes (laboratório — fonte 1)
  dados/internacoes.json           internações hospitalares (laboratório — fonte 2)
  dados/consultas_ambulatorio.csv  consultas ambulatoriais (exercício prático)
  dados/exames_laboratoriais.csv   exames de laboratório (atividade de entrega)
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

RAIZ = Path(__file__).parent / "dados"
RAIZ.mkdir(exist_ok=True)
rng = np.random.default_rng(1010)


def reais(v):
    """1234.5 -> 'R$ 1.234,50' (formato brasileiro, como vem de muitos sistemas)."""
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"


# ============================================================================
# 1) Laboratório — fonte 1: cadastro de pacientes (CSV)
# ============================================================================
NP = 200
nasc = pd.to_datetime("1935-01-01") + pd.to_timedelta(rng.integers(0, 365 * 85, NP), unit="D")
pac = pd.DataFrame({
    "id_paciente": [f"PAC-{i:04d}" for i in range(1, NP + 1)],
    "data_nascimento": nasc.strftime("%Y-%m-%d"),
    "sexo": rng.choice(["F", "M"], NP, p=[0.52, 0.48]),
    "municipio": rng.choice(["Natal", "Mossoró", "Parnamirim", "Caicó"], NP, p=[0.45, 0.25, 0.2, 0.1]),
    "escolaridade": rng.choice(["Fundamental", "Médio", "Superior"], NP, p=[0.4, 0.4, 0.2]),
    "plano_saude": rng.choice(["Sim", "Não"], NP, p=[0.3, 0.7]),
}).astype(object)
for i in rng.choice(NP, 15, replace=False):
    pac.at[i, "data_nascimento"] = pd.to_datetime(pac.at[i, "data_nascimento"]).strftime("%d/%m/%Y")
for i in rng.choice(NP, 20, replace=False):
    pac.at[i, "sexo"] = {"F": rng.choice(["f", "Feminino"]), "M": rng.choice(["m", "Masculino"])}[pac.at[i, "sexo"]]
for i in rng.choice(NP, 25, replace=False):
    pac.at[i, "plano_saude"] = {"Sim": rng.choice(["S", "sim", "SIM"]), "Não": rng.choice(["N", "nao", "NÃO"])}[pac.at[i, "plano_saude"]]
for i in rng.choice(NP, 12, replace=False):
    pac.at[i, "escolaridade"] = pac.at[i, "escolaridade"].upper()
pac.loc[rng.choice(NP, 6, replace=False), "escolaridade"] = np.nan
pac.to_csv(RAIZ / "pacientes.csv", index=False, encoding="utf-8")

# ============================================================================
# 2) Laboratório — fonte 2: internações (JSON, como viria de uma API)
# ============================================================================
NI = 300
diags = ["Pneumonia", "Insuficiência cardíaca", "AVC", "Fratura de fêmur", "Infecção urinária"]
dia = rng.choice(diags, NI, p=[0.28, 0.2, 0.15, 0.12, 0.25])
grav = rng.choice(["Leve", "Moderada", "Grave"], NI, p=[0.45, 0.35, 0.20])
base_dias = {"Pneumonia": 6, "Insuficiência cardíaca": 8, "AVC": 10, "Fratura de fêmur": 7, "Infecção urinária": 4}
mult = {"Leve": 0.7, "Moderada": 1.0, "Grave": 1.8}
dias = np.array([max(1, round(rng.normal(base_dias[d] * mult[g], 2))) for d, g in zip(dia, grav)])
uti = np.array([rng.random() < {"Leve": 0.03, "Moderada": 0.15, "Grave": 0.6}[g] for g in grav])
custo = dias * rng.normal(1100, 150, NI) + uti * rng.normal(9000, 1500, NI)
entrada = pd.to_datetime("2026-01-05") + pd.to_timedelta(rng.integers(0, 240, NI), unit="D")
alta = entrada + pd.to_timedelta(dias, unit="D")
ids_pac = rng.choice(pac["id_paciente"], NI)
registros = []
for k in range(NI):
    registros.append({
        "id_internacao": f"INT-{k + 1:05d}",
        "id_paciente": ids_pac[k],
        "data_entrada": entrada[k].strftime("%Y-%m-%d"),
        "data_alta": alta[k].strftime("%Y-%m-%d"),
        "diagnostico_principal": dia[k],
        "gravidade": grav[k],
        "uti": "S" if uti[k] else "N",
        "custo_total": reais(custo[k]),
    })
for k in rng.choice(NI, 18, replace=False):
    registros[k]["gravidade"] = registros[k]["gravidade"].lower()
for k in rng.choice(NI, 5, replace=False):
    registros[k]["custo_total"] = None
for k, falso in zip(rng.choice(NI, 3, replace=False), ["PAC-9001", "PAC-9002", "PAC-9003"]):
    registros[k]["id_paciente"] = falso          # paciente que não existe no cadastro
registros += [dict(registros[k]) for k in rng.choice(NI, 4, replace=False)]   # duplicatas
rng.shuffle(registros)
(RAIZ / "internacoes.json").write_text(json.dumps(registros, ensure_ascii=False, indent=1), encoding="utf-8")

# ============================================================================
# 3) Exercício — consultas ambulatoriais (uma tabela, mais simples)
# ============================================================================
NC = 80
esp = rng.choice(["Cardiologia", "Pediatria", "Ortopedia", "Clínica geral"], NC, p=[0.25, 0.25, 0.2, 0.3])
idade_c = np.where(esp == "Pediatria", rng.integers(1, 15, NC), rng.integers(18, 90, NC))
espera = rng.gamma(2.2, 14, NC).round().astype(int) + 3
satis_por_espera = np.where(espera > 60, 0, np.where(espera > 30, 1, np.where(espera > 15, 2, 3)))
satis_idx = np.clip(satis_por_espera + rng.integers(-1, 2, NC), 0, 3)
satis = np.array(["Ruim", "Regular", "Boa", "Ótima"])[satis_idx]
valor = np.where(esp == "Clínica geral", 120.0, np.where(esp == "Pediatria", 150.0, 200.0))
datas_c = pd.to_datetime("2026-08-03") + pd.to_timedelta(rng.integers(0, 60, NC), unit="D")
cons = pd.DataFrame({
    "id_consulta": np.arange(501, 501 + NC),
    "data_consulta": datas_c.strftime("%d/%m/%Y"),
    "idade": [f"{v} anos" for v in idade_c],
    "especialidade": esp,
    "tempo_espera": [f"{v} min" for v in espera],
    "valor_consulta": [reais(v) for v in valor],
    "satisfacao": satis,
}).astype(object)
for i in rng.choice(NC, 12, replace=False):
    cons.at[i, "especialidade"] = rng.choice([cons.at[i, "especialidade"].lower(), cons.at[i, "especialidade"].upper()])
for i in rng.choice(NC, 10, replace=False):
    cons.at[i, "satisfacao"] = cons.at[i, "satisfacao"].lower()
cons = pd.concat([cons, cons.loc[rng.choice(NC, 3, replace=False)]], ignore_index=True)
cons = cons.sample(frac=1, random_state=10).reset_index(drop=True)
cons.to_csv(RAIZ / "consultas_ambulatorio.csv", index=False, encoding="utf-8")

# ============================================================================
# 4) Atividade de entrega — exames laboratoriais
# ============================================================================
NE = 150
tipos = {"Glicemia": ("mg/dL", 98, 15), "Colesterol total": ("mg/dL", 190, 35),
         "Creatinina": ("mg/dL", 0.95, 0.2), "Hemoglobina": ("g/dL", 13.5, 1.4)}
tp = rng.choice(list(tipos), NE)
res = np.array([max(0.1, rng.normal(tipos[t][1], tipos[t][2])) for t in tp])
datas_e = pd.to_datetime("2026-07-01") + pd.to_timedelta(rng.integers(0, 90, NE), unit="D")
ex = pd.DataFrame({
    "id_exame": [f"EX-{i:04d}" for i in range(1, NE + 1)],
    "id_paciente": rng.choice(pac["id_paciente"], NE),
    "data_coleta": datas_e.strftime("%Y-%m-%d"),
    "sexo": rng.choice(["F", "M"], NE),
    "idade": rng.integers(18, 92, NE).astype(float),
    "tipo_exame": tp,
    "resultado": [f"{v:.2f}".replace(".", ",") if t in ("Creatinina",) else f"{v:.1f}".replace(".", ",") for v, t in zip(res, tp)],
    "unidade": [tipos[t][0] for t in tp],
    "laboratorio": rng.choice(["LabNatal", "LabSaúde RN", "Laboratório Central"], NE),
    "prioridade": rng.choice(["Rotina", "Urgente", "Emergência"], NE, p=[0.7, 0.22, 0.08]),
}).astype(object)
for i in rng.choice(NE, 14, replace=False):
    ex.at[i, "data_coleta"] = pd.to_datetime(ex.at[i, "data_coleta"]).strftime("%d/%m/%Y")
for i in rng.choice(NE, 14, replace=False):
    ex.at[i, "sexo"] = {"F": "Feminino", "M": "masculino"}[ex.at[i, "sexo"]]
for i in rng.choice(NE, 12, replace=False):
    ex.at[i, "prioridade"] = ex.at[i, "prioridade"].upper()
for i in rng.choice(NE, 10, replace=False):
    ex.at[i, "laboratorio"] = " " + ex.at[i, "laboratorio"].lower() + " "
ex.loc[rng.choice(NE, 4, replace=False), "resultado"] = "999"
ex.loc[rng.choice(NE, 6, replace=False), "idade"] = np.nan
ex = pd.concat([ex, ex.loc[rng.choice(NE, 5, replace=False)]], ignore_index=True)
ex = ex.sample(frac=1, random_state=11).reset_index(drop=True)
ex.to_csv(RAIZ / "exames_laboratoriais.csv", index=False, encoding="utf-8")

print("pacientes", pac.shape, "| internacoes", len(registros), "| consultas", cons.shape, "| exames", ex.shape)
