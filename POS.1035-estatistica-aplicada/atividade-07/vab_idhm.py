"""
Relação entre o VAB absoluto e o IDHM nos 167 municípios do RN (2021 / 2010).

Reproduz, em código, a seção 2.1 do artigo_breve_v2.tex: a correlação de Pearson
é a média dos produtos dos valores padronizados (z-scores), ou seja, a inclinação
da reta Y = a + bX quando X e Y são medidos em desvios padrão.

Uso:  python3 vab_idhm.py
Saída: figuras/vab_idhm.html (gráfico interativo) + tabela de correlações no terminal.
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# 1. Carga do dataset (planilha montada a partir do IBGE/SIDRA, IBGE Cidades e Sebrae)
# ---------------------------------------------------------------------------
ARQ = ".data/RN_Valor_Adicionado_Municipios.xlsx"
VAB = "VAB total 2021 (mil R$)"
IDHM = "IDHM 2010"
SETORES = {
    "VAB total": VAB,
    "VAB Indústria": "VAB Indústria 2021 (mil R$)",
    "VAB Serviços": "VAB Serviços 2021 (mil R$)",
    "VAB Adm. pública": "VAB Adm. pública 2021 (mil R$)",
}

# A aba tem duas linhas de cabeçalho (grupo + nome da coluna); header=1 usa a segunda.
# As duas últimas linhas são de controle (sem município) e saem com o dropna.
df = (
    pd.read_excel(ARQ, sheet_name="Municipios_RN", header=1)
    .dropna(subset=["Município", IDHM])
    .reset_index(drop=True)
)
assert len(df) == 167, f"esperava 167 municípios, veio {len(df)}"


# ---------------------------------------------------------------------------
# 2. Correlação de Pearson "na mão", como no artigo (eq. 2):
#    z = (x - média) / desvio padrão   ->   r = soma(z_x * z_y) / (n - 1)
# ---------------------------------------------------------------------------
def pearson(x: pd.Series, y: pd.Series) -> float:
    zx = (x - x.mean()) / x.std(ddof=1)  # ddof=1: desvio padrão amostral (n-1)
    zy = (y - y.mean()) / y.std(ddof=1)
    return float((zx * zy).sum() / (len(x) - 1))


def classifica(r: float) -> str:
    """Escala usada na aba 'Correlacoes' da própria planilha."""
    r = abs(r)
    return "fraca" if r < 0.3 else "moderada" if r < 0.6 else "forte"


# Self-check: a fórmula manual tem de bater com numpy e pandas.
r_manual = pearson(df[VAB], df[IDHM])
assert np.isclose(r_manual, np.corrcoef(df[VAB], df[IDHM])[0, 1])
assert np.isclose(r_manual, df[VAB].corr(df[IDHM]))

# ---------------------------------------------------------------------------
# 3. Tabela: correlação de cada VAB absoluto com o IDHM
#    r² = fração da variação do IDHM "explicada" pela reta.
# ---------------------------------------------------------------------------
tabela = pd.DataFrame(
    [
        {
            "Variável": nome,
            "r (Pearson)": round(pearson(df[col], df[IDHM]), 3),
            "r²": round(pearson(df[col], df[IDHM]) ** 2, 3),
            "grau": classifica(pearson(df[col], df[IDHM])),
        }
        for nome, col in SETORES.items()
    ]
)
print("\nCorrelação linear entre VAB absoluto (2021) e IDHM (2010), 167 municípios:\n")
print(tabela.to_string(index=False))
print(
    f"\nLeitura: r = {r_manual:.2f} para o VAB total -> r² = {r_manual**2:.2f}. "
    f"A reta explica só {r_manual**2:.0%} da variação do IDHM; "
    f"{1 - r_manual**2:.0%} ficam fora dela. Correlação {classifica(r_manual)}, não alta."
)

# ---------------------------------------------------------------------------
# 4. Reta Y = a + bX (eq. 1 do artigo) ajustada por mínimos quadrados.
#    O VAB vai de R$ 12 mi (menor) a R$ 20,8 bi (Natal): sem escala log os 166
#    pontos restantes viram um borrão à esquerda. A reta é ajustada em log10(VAB),
#    e a correlação nessa escala fica praticamente igual (printada abaixo).
# ---------------------------------------------------------------------------
df["log_vab"] = np.log10(df[VAB])
b, a = np.polyfit(df["log_vab"], df[IDHM], deg=1)  # polyfit devolve [inclinação, intercepto]
r_log = pearson(df["log_vab"], df[IDHM])
print(f"Na escala log10 do VAB: r = {r_log:.2f} (reta IDHM = {a:.3f} + {b:.4f}·log10 VAB).")

# ---------------------------------------------------------------------------
# 5. Gráfico de dispersão (plotly) — um ponto por município, reta por cima,
#    rótulo direto só nos três casos do artigo.
# ---------------------------------------------------------------------------
CASOS = ["Natal", "Guamaré", "Ceará-Mirim"]
df["rótulo"] = df["Município"].where(df["Município"].isin(CASOS), "")

fig = px.scatter(
    df,
    x=VAB,
    y=IDHM,
    log_x=True,
    text="rótulo",
    hover_name="Município",
    hover_data={VAB: ":,.0f", IDHM: ":.3f", "rótulo": False},
    labels={VAB: "VAB total 2021 (mil R$, escala log)", IDHM: "IDHM 2010"},
    title=(
        f"VAB absoluto × IDHM nos 167 municípios do RN<br>"
        f"<sup>r = {r_manual:.2f} (VAB bruto) · r = {r_log:.2f} (log VAB) · "
        f"r² = {r_manual**2:.2f}: correlação {classifica(r_manual)}</sup>"
    ),
)
fig.update_traces(
    marker=dict(size=9, color="#2a78d6", opacity=0.75, line=dict(width=1, color="#fcfcfb")),
    textposition="top center",
)

# Reta de mínimos quadrados sobre a faixa observada do VAB.
xs = np.logspace(df["log_vab"].min(), df["log_vab"].max(), 100)
fig.add_trace(
    go.Scatter(
        x=xs,
        y=a + b * np.log10(xs),
        mode="lines",
        line=dict(color="#52514e", width=2, dash="dash"),
        name="reta Y = a + bX",
        hoverinfo="skip",
    )
)
fig.update_layout(
    template="plotly_white",
    showlegend=False,
    font=dict(family="Georgia, serif", size=13),
    margin=dict(l=60, r=30, t=90, b=60),
)
fig.update_xaxes(tickformat=",", showgrid=True, gridcolor="#e8e8e6")
fig.update_yaxes(showgrid=True, gridcolor="#e8e8e6")

SAIDA = "figuras/vab_idhm.html"
fig.write_html(SAIDA, include_plotlyjs="cdn")
print(f"\nGráfico salvo em {SAIDA}")
