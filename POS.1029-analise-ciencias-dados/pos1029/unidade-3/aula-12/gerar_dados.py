"""
Aula 12 — Laboratório de Visualização (Matplotlib, Seaborn e Plotly)
Gera os DOIS conjuntos de dados SINTÉTICOS usados na aula.

1) dados/delivery_hamburgueria.csv  -> exemplo guiado (600 pedidos de uma
   hamburgueria fictícia, em 8 semanas)
2) dados/app_musica_usuarios.csv     -> exercício prático (240 usuários de um
   aplicativo de música fictício)

Nenhum registro corresponde a pessoa ou empresa real. A semente é fixa:
rodar este script de novo gera exatamente os mesmos arquivos.
"""
from pathlib import Path
import numpy as np
import pandas as pd

PASTA = Path(__file__).resolve().parent / "dados"
PASTA.mkdir(exist_ok=True)


def gerar_delivery(seed: int = 12) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 600
    dias = pd.date_range("2026-08-03", periods=56, freq="D")  # 8 semanas
    # fim de semana tem mais pedidos
    peso = np.where(dias.dayofweek >= 4, 1.6, 1.0)
    data = rng.choice(dias, size=n, p=peso / peso.sum())
    data = pd.to_datetime(np.sort(data))
    nomes_dia = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    dia_semana = [nomes_dia[d] for d in data.dayofweek]
    fds = data.dayofweek >= 4  # sex, sáb, dom

    turno = np.where(rng.random(n) < 0.35, "Almoço", "Jantar")
    bairros = ["Centro", "Jardim", "Lagoa", "Praia", "Serra"]
    dist_media = {"Centro": 1.8, "Jardim": 3.2, "Lagoa": 4.5, "Praia": 5.5, "Serra": 7.5}
    bairro = rng.choice(bairros, size=n, p=[0.28, 0.24, 0.18, 0.18, 0.12])
    distancia = np.array([rng.gamma(6, dist_media[b] / 6) for b in bairro])
    distancia = np.clip(distancia, 0.4, 14).round(1)

    # bicicleta só em entregas curtas
    veiculo = np.where((distancia <= 3.0) & (rng.random(n) < 0.45), "Bicicleta", "Moto")

    # chuva por dia (cerca de 25% dos dias)
    dias_chuva = set(rng.choice(dias, size=14, replace=False))
    chuva = np.array(["Sim" if d in dias_chuva else "Não" for d in data])

    # tempo de entrega (min): base + distância + efeitos + ruído assimétrico
    tempo = (
        14
        + 3.1 * distancia
        + np.where(chuva == "Sim", 7, 0)
        + np.where((turno == "Jantar") & fds, 5, 0)
        + np.where(veiculo == "Bicicleta", 2.5 * distancia, 0)
        + rng.gamma(2.0, 3.0, n)  # cauda à direita
    )
    # alguns atrasos excepcionais (pedido trocado, endereço errado)
    idx_atraso = rng.choice(n, size=8, replace=False)
    tempo[idx_atraso] += rng.uniform(25, 45, size=8)
    tempo = tempo.round(0).astype(int)

    itens = rng.poisson(np.where(fds, 3.2, 2.4)) + 1
    valor = (itens * rng.normal(27, 4, n) + rng.normal(0, 6, n)).clip(18).round(2)
    taxa = (4 + 0.9 * distancia + rng.normal(0, 0.4, n)).clip(4).round(2)

    # avaliação 1–5 cai com o tempo de entrega
    nota_lat = 5.6 - 0.045 * tempo + rng.normal(0, 0.55, n)
    avaliacao = np.clip(np.round(nota_lat), 1, 5).astype(int)

    df = pd.DataFrame({
        "pedido_id": np.arange(1, n + 1),
        "data": data.date,
        "dia_semana": dia_semana,
        "turno": turno,
        "bairro": bairro,
        "distancia_km": distancia,
        "veiculo": veiculo,
        "chuva": chuva,
        "itens": itens,
        "valor_pedido": valor,
        "taxa_entrega": taxa,
        "tempo_entrega_min": tempo,
        "avaliacao": avaliacao,
    })
    return df


def gerar_musica(seed: int = 2026) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n = 240
    idade = rng.integers(16, 66, n)
    plano = np.where(rng.random(n) < (0.25 + 0.006 * (idade - 16)), "Premium", "Gratuito")
    generos = ["Pop", "Rock", "Sertanejo", "Forró", "MPB", "Eletrônica"]
    genero = rng.choice(generos, size=n, p=[0.24, 0.16, 0.20, 0.14, 0.14, 0.12])
    bonus_gen = {"Pop": 1.5, "Rock": 0.5, "Sertanejo": 1.0, "Forró": 0.0, "MPB": -1.0, "Eletrônica": 3.5}
    dispositivo = rng.choice(["Celular", "Computador", "Smart TV"], size=n, p=[0.68, 0.22, 0.10])

    horas = (
        19
        - 0.22 * idade
        + np.where(plano == "Premium", 4.0, 0)
        + np.array([bonus_gen[g] for g in genero])
        + rng.gamma(2.0, 2.0, n)
    ).clip(0.5).round(1)
    playlists = rng.poisson(0.25 * horas + np.where(plano == "Premium", 2, 0))
    anuncios = np.where(plano == "Gratuito", (horas * rng.normal(9, 1.5, n)).clip(0), 0).round(0).astype(int)
    satisfacao = (
        5.2 + np.where(plano == "Premium", 2.0, 0) - 0.012 * anuncios + rng.normal(0, 1.1, n)
    ).clip(0, 10).round(1)

    return pd.DataFrame({
        "usuario_id": np.arange(1, n + 1),
        "idade": idade,
        "plano": plano,
        "genero_favorito": genero,
        "dispositivo": dispositivo,
        "horas_semana": horas,
        "playlists_criadas": playlists,
        "anuncios_semana": anuncios,
        "satisfacao": satisfacao,
    })


if __name__ == "__main__":
    d = gerar_delivery()
    m = gerar_musica()
    d.to_csv(PASTA / "delivery_hamburgueria.csv", index=False)
    m.to_csv(PASTA / "app_musica_usuarios.csv", index=False)
    print(f"delivery_hamburgueria.csv: {d.shape}")
    print(f"app_musica_usuarios.csv:   {m.shape}")
