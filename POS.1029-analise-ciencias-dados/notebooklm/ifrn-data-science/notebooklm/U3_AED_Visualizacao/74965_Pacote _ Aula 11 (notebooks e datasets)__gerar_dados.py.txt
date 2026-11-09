"""Gera os dados SINTÉTICOS da Aula 11 — Fundamentos de AED e Estatística Descritiva.

Tudo é sorteado com semente fixa (reprodutível); nenhum registro é de pessoa ou empresa real.
  dados/desempenho_estudantes.csv  300 estudantes de um curso fictício (laboratório)
  dados/sorveteria.csv             90 dias de vendas de uma sorveteria fictícia (exercício)
"""
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).parent / "dados"
RAIZ.mkdir(exist_ok=True)
rng = np.random.default_rng(1111)

# ============================================================================
# 1) Laboratório — desempenho de estudantes
# ============================================================================
N = 300
turno = rng.choice(["Manhã", "Tarde", "Noite"], N, p=[0.40, 0.30, 0.30])
p_trab = np.where(turno == "Noite", 0.75, 0.20)
trabalha = np.where(rng.random(N) < p_trab, "Sim", "Não")
trab = trabalha == "Sim"

horas_estudo = np.round(rng.gamma(3.0, 2.6, N) * np.where(trab, 0.7, 1.0), 1)         # assimétrica à direita
horas_sono = np.round(np.clip(rng.normal(7.3, 0.8, N) - 0.7 * trab, 4.0, 9.5), 1)
tempo_celular = np.round(np.clip(rng.normal(4.2, 1.4, N) - 0.25 * (horas_sono - 7), 0.5, 10), 1)
faltas = rng.poisson(np.where(trab, 6, 3.5))
deslocamento = np.round(rng.lognormal(3.1, 0.55, N)).astype(int)                     # minutos, muito assimétrica
mes_nasc = rng.integers(1, 13, N)                                                       # sem relação com nada

nota = (3.2
        + 1.55 * np.log1p(horas_estudo)          # relação crescente, mas que "satura" (não linear)
        + 0.35 * (horas_sono - 7)
        - 0.17 * (tempo_celular - 4)
        - 0.14 * faltas
        + rng.normal(0, 0.75, N))
nota = np.round(np.clip(nota, 0, 10), 1)

est = pd.DataFrame({
    "id_estudante": [f"E{i:03d}" for i in range(1, N + 1)],
    "turno": turno,
    "trabalha": trabalha,
    "horas_estudo_semana": horas_estudo,
    "horas_sono": horas_sono,
    "tempo_celular_h": tempo_celular,
    "faltas": faltas,
    "deslocamento_min": deslocamento,
    "mes_nascimento": mes_nasc,
    "nota_final": nota,
})
est.to_csv(RAIZ / "desempenho_estudantes.csv", index=False, encoding="utf-8")

# ============================================================================
# 2) Exercício — sorveteria (90 dias de verão)
# ============================================================================
D = 90
datas = pd.date_range("2026-01-05", periods=D, freq="D")
temp = np.round(26 + 4.5 * np.sin(np.linspace(0, 3 * np.pi, D)) + rng.normal(0, 1.6, D), 1)
fim_semana = datas.dayofweek >= 5
chuva = np.round(np.where(rng.random(D) < 0.25, rng.gamma(1.5, 9, D), 0.0), 1)        # muitos zeros
sorvetes = np.round(18 * temp - 330 + 60 * fim_semana - 2.2 * chuva + rng.normal(0, 22, D)).astype(int)
sorvetes = np.clip(sorvetes, 20, None)
cafes = np.round(260 - 6 * temp + 25 * (chuva > 0) + rng.normal(0, 12, D)).astype(int)
festival = 40                                                       # dia de festival na praça: vendas atípicas
sorvetes[festival] = 1150
sorv = pd.DataFrame({
    "data": datas.strftime("%Y-%m-%d"),
    "dia_semana": datas.dayofweek.map(dict(enumerate(["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]))),
    "fim_de_semana": np.where(fim_semana, "Sim", "Não"),
    "temperatura_max": temp,
    "chuva_mm": chuva,
    "sorvetes_vendidos": sorvetes,
    "cafes_vendidos": cafes,
})
sorv.to_csv(RAIZ / "sorveteria.csv", index=False, encoding="utf-8")

print("estudantes", est.shape, "| sorveteria", sorv.shape)
