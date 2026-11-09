"""
Aula 14 — scikit-learn: Fluxo de Trabalho em ML
Gera o dataset SINTÉTICO do exemplo guiado:

  dados/app_musica_churn.csv -> 1.500 usuários de um aplicativo de música
  fictício (o mesmo "app" da Aula 12), com a coluna-alvo `cancelou`
  (1 = cancelou a conta no mês seguinte).

O trabalho prático usa dados/delivery_hamburgueria.csv (o mesmo da Aula 12).
Nenhum registro corresponde a pessoa ou empresa real. Semente fixa.
"""
from pathlib import Path
import numpy as np
import pandas as pd

PASTA = Path(__file__).resolve().parent / "dados"
PASTA.mkdir(exist_ok=True)


def gerar_churn(seed: int = 14, n: int = 1500) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idade = rng.integers(16, 66, n)
    plano = np.where(rng.random(n) < (0.22 + 0.006 * (idade - 16)), "Premium", "Gratuito")
    premium = plano == "Premium"
    dispositivo = rng.choice(["Celular", "Computador", "Smart TV"], size=n, p=[0.66, 0.24, 0.10])
    meses_conta = np.clip(rng.gamma(2.0, 9.0, n).round().astype(int) + 1, 1, 72)
    horas = np.clip(18 - 0.2 * idade + 4 * premium + rng.gamma(2.0, 2.2, n) - 2, 0.5, None).round(1)
    playlists = rng.poisson(0.25 * horas + 2 * premium)
    anuncios = np.where(premium, 0, (horas * rng.normal(9, 1.5, n)).clip(0)).round().astype(int)
    dias_sem = np.clip(rng.exponential(6, n) + np.where(horas < 8, 6, 0), 0, 60).round().astype(int)
    chamados = rng.poisson(0.5 + 0.6 * (rng.random(n) < 0.2), n)
    satisf = np.clip(5.3 + 2 * premium - 0.01 * anuncios - 0.3 * chamados + rng.normal(0, 1.2, n), 0, 10).round(1)

    logit = (-0.9 + 0.17 * dias_sem - 0.13 * horas + 0.65 * chamados - 0.50 * (satisf - 5)
             - 0.035 * meses_conta + 0.5 * (~premium) + rng.normal(0, 0.3, n))
    prob = 1 / (1 + np.exp(-logit))
    cancelou = (rng.random(n) < prob).astype(int)

    df = pd.DataFrame({
        "usuario_id": np.arange(1, n + 1),
        "idade": idade,
        "plano": plano,
        "dispositivo": dispositivo,
        "meses_conta": meses_conta,
        "horas_semana": horas,
        "playlists_criadas": playlists,
        "anuncios_semana": anuncios,
        "dias_sem_acessar": dias_sem,
        "chamados_suporte": chamados,
        "satisfacao": satisf,
        "cancelou": cancelou,
    })
    # ~4% de satisfação não respondida (para praticar imputação no pipeline)
    faltantes = rng.choice(n, size=int(0.04 * n), replace=False)
    df.loc[faltantes, "satisfacao"] = np.nan
    return df


if __name__ == "__main__":
    df = gerar_churn()
    df.to_csv(PASTA / "app_musica_churn.csv", index=False)
    print(df.shape, "— taxa de cancelamento:", round(df["cancelou"].mean(), 3))
