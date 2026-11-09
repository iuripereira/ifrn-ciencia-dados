"""
Figuras do artigo_breve_v2.tex: Guamaré (indústria), Natal (serviços) e
Ceará-Mirim (administração pública) comparados aos 167 municípios do RN.
Variáveis de comparação do ano de 2021 (VAB, PIB per capita, população,
emprego formal do CEMPRE 2021); o IDHM é o de 2010, único disponível por município.

Uso:   python3 graficos_artigo.py          (cwd = atividade-07)
       Requer plotly >= 5 e kaleido >= 1 (pip install kaleido); o kaleido usa um
       Chrome/Chromium instalado — sem ele, `python3 -m kaleido_get_chrome`.
Saída: figuras/fig1_boxplot.png        boxplot da participação por setor, município em destaque
       figuras/fig2_separatrizes.png   PIB per capita ordenado, linhas em P10 e P90
       figuras/fig3_setor_dominante.png nº de municípios por setor de maior VAB, 2002-2021
       figuras/fig4_setores_idhm.png   participação de cada setor x IDHM, reta e município
       figuras/fig5_adm_inversa.png    IDHM e emprego formal por setor dominante (boxplot)
Fonte: .data/RN_Valor_Adicionado_Municipios.xlsx (IBGE/SIDRA 5938, IBGE Cidades)
       .data/cempre_2021_rn.json (IBGE/SIDRA 6449, CEMPRE 2021, total da CNAE)
"""

import json

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ARQ = ".data/RN_Valor_Adicionado_Municipios.xlsx"
CASOS = {"Guamaré": "Indústria", "Natal": "Serviços", "Ceará-Mirim": "Adm. pública"}
SETORES = [
    "Indústria",
    "Serviços",
    "Adm. pública",
    "Agropecuária",
]  # só para achar o maior VAB
ALVO = SETORES[:3]  # setores do artigo; a agropecuária não entra em nenhuma figura
# Paleta categórica validada (dataviz), ordem fixa por setor; cinza para reta/referência.
COR = {
    "Indústria": "#2a78d6",
    "Serviços": "#eb6834",
    "Adm. pública": "#1baf7a",
    "Agropecuária": "#eda100",
    "ref": "#52514e",
    "caso": "#0b0b0b",
}
# Layout comum: fonte serifada, vírgula decimal (separators), grade recessiva, sem eixos superior/direito.
LAYOUT = {
    "template": "plotly_white",
    "font": {"family": "serif", "size": 11, "color": "#0b0b0b"},
    "separators": ",.",
    "paper_bgcolor": "white",
    "plot_bgcolor": "white",
    "margin": {"l": 55, "r": 10, "t": 10, "b": 45},
    "showlegend": False,
}
EIXO = {
    "gridcolor": "#e8e8e6",
    "gridwidth": 1,
    "zeroline": False,
    "showline": True,
    "linecolor": "#333",
    "ticks": "outside",
    "tickcolor": "#333",
    "ticklen": 3,
    "title_font_size": 11,
}
PX = 100  # 1 polegada da figura antiga = 100 px; scale=3 no export dá ~300 dpi


def rgba(hex_, a):
    r, g, b = (int(hex_[i : i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{a})"


def figura(larg, alt, **layout):
    return go.Figure(layout=dict(LAYOUT, width=larg * PX, height=alt * PX, **layout))


def caixa(fig, x, dados, cor, larg=0.5, **kw):
    """Boxplot de um grupo em posição numérica x (permite deslocar outros marcadores ao lado)."""
    fig.add_trace(
        go.Box(
            x=[x] * len(dados),
            y=dados,
            width=larg,
            fillcolor=rgba(cor, 0.35),
            line={"color": cor, "width": 1.2},
            boxpoints="outliers",
            marker={"color": COR["ref"], "size": 3, "opacity": 0.5},
            showlegend=False,
        ),
        **kw,
    )


def ponto_caso(fig, x, y, legenda=False, **kw):
    fig.add_trace(
        go.Scatter(
            x=[x],
            y=[y],
            mode="markers",
            marker={"color": COR["caso"], "size": 10},
            name="município escolhido",
            showlegend=legenda,
        ),
        **kw,
    )


def rotulo(fig, x, y, texto, dx=0, dy=0, ha="center", va="middle", tam=10, **kw):
    fig.add_annotation(
        x=x,
        y=y,
        text=texto,
        showarrow=False,
        xshift=dx,
        yshift=dy,
        xanchor=ha,
        yanchor=va,
        font=dict(size=tam),
        **kw,
    )


def salvar(fig, nome):
    fig.update_xaxes(**EIXO)
    fig.update_yaxes(**EIXO)
    fig.write_image(f"figuras/{nome}.png", scale=3)
    print("ok", nome)


# ---------------------------------------------------------------------------
# Carga e variáveis derivadas (tudo de 2021, exceto IDHM 2010)
# ---------------------------------------------------------------------------
mun = (
    pd.read_excel(ARQ, sheet_name="Municipios_RN", header=1)
    .dropna(subset=["Município", "IDHM 2010"])
    .reset_index(drop=True)
)
assert len(mun) == 167
PART = {
    "Indústria": "Part. Indústria no VAB (%)",
    "Serviços": "Part. Serviços no VAB (%)",
    "Adm. pública": "Part. Adm. pública no VAB (%)",
}
for s in SETORES:
    mun[s] = mun[PART[s]] * 100
mun["PIB pc"] = mun["PIB per capita 2021 (R$) – IBGE"] / 1e3  # R$ mil
mun["Dominante"] = mun[SETORES].idxmax(axis=1)  # setor de maior VAB em 2021

# Emprego formal 2021: pessoal ocupado assalariado (CEMPRE 2021) / população estimada 2021
cempre = pd.DataFrame(json.load(open(".data/cempre_2021_rn.json"))[1:])
cempre = cempre[cempre["D2N"] == "Pessoal ocupado assalariado"]
cempre = cempre.assign(
    cod=cempre["D1C"].astype(int), assal=pd.to_numeric(cempre["V"], errors="coerce")
)
mun["cod"] = mun["Código IBGE"].astype(int)
mun = mun.merge(cempre[["cod", "assal"]], on="cod", how="left")
mun["Emprego formal"] = mun["assal"] / mun["População estimada 2021"] * 100
assert mun["Emprego formal"].notna().all(), "CEMPRE 2021 com sigilo em algum município"

idx = {m: mun.index[mun["Município"] == m][0] for m in CASOS}
print("Setor dominante em 2021:", mun["Dominante"].value_counts().to_dict())

# ---------------------------------------------------------------------------
# Fig. 1 - Boxplot da participação de cada setor no VAB (167 municípios),
#          média ± desvio padrão e município escolhido
# ---------------------------------------------------------------------------
fig = figura(
    6.4,
    2.8,
    showlegend=True,
    margin={"l": 55, "r": 10, "t": 10, "b": 60},
    legend={
        "orientation": "h",
        "x": 0.5,
        "y": -0.18,
        "xanchor": "center",
        "yanchor": "top",
        "font_size": 10,
    },
)
alvo = list(CASOS.values())
for i, s in enumerate(alvo):
    x = mun[s]
    caixa(fig, i, x, COR[s])
    fig.add_trace(
        go.Scatter(
            x=[i + 0.33],
            y=[x.mean()],
            mode="markers",
            name="média ± desvio padrão",
            marker=dict(symbol="diamond", size=7, color=COR["ref"]),
            showlegend=i == 0,
            error_y={
                "type": "data",
                "array": [x.std(ddof=1)],
                "color": COR["ref"],
                "thickness": 1,
                "width": 3,
            },
        )
    )
    m = next(k for k, v in CASOS.items() if v == s)
    ponto_caso(fig, i, mun.loc[idx[m], s], legenda=i == 0)
    rotulo(
        fig,
        i,
        mun.loc[idx[m], s],
        f"{m}<br>{mun.loc[idx[m], s]:.0f}%",
        dx=-10,
        ha="right",
    )
    print(
        f"  {s}: mediana={x.median():.1f} média={x.mean():.1f} dp={x.std(ddof=1):.1f} "
        f"Q1={x.quantile(0.25):.1f} Q3={x.quantile(0.75):.1f} {m}={mun.loc[idx[m], s]:.1f}"
    )
fig.update_xaxes(
    tickvals=list(range(3)), ticktext=alvo, showgrid=False, range=[-0.5, 2.6]
)
fig.update_yaxes(title_text="Participação no VAB, 2021 (%)", range=[0, 100])
salvar(fig, "fig1_boxplot")

# ---------------------------------------------------------------------------
# Fig. 2 - Separatrizes: PIB per capita 2021 em ordem crescente, linhas em P10 e P90,
#          pontos coloridos pelo setor dominante, municípios escolhidos rotulados
# ---------------------------------------------------------------------------
ordem = mun.sort_values("PIB pc").reset_index()
p10, p90 = mun["PIB pc"].quantile([0.10, 0.90])
fig = figura(
    6.4,
    2.9,
    showlegend=True,
    legend={
        "x": 0.01,
        "y": 0.99,
        "xanchor": "left",
        "yanchor": "top",
        "font_size": 10,
        "bgcolor": "rgba(0,0,0,0)",
        "title": dict(text="Setor de maior VAB (nº de municípios)", font_size=10),
    },
)
for s in ALVO:  # os 3 municípios em que nenhum setor-alvo é o maior ficam de fora
    sel = ordem["Dominante"] == s
    fig.add_trace(
        go.Scatter(
            x=ordem.index[sel],
            y=ordem.loc[sel, "PIB pc"],
            mode="markers",
            marker={"color": COR[s], "size": 5},
            name=f"{s} ({sel.sum()})",
        )
    )
for p, nome in [(p10, "P10"), (p90, "P90")]:
    fig.add_hline(
        y=np.log10(p),
        line={"color": COR["ref"], "dash": "dash", "width": 1},
        annotation_position="top left",  # eixo log: shape em log10
        annotation_text=f"{nome} = R$ {p * 1e3:,.0f}".replace(",", "."),
        annotation_font={"size": 10, "color": COR["ref"]},
    )
for m in CASOS:
    i = ordem.index[ordem["Município"] == m][0]
    fig.add_trace(
        go.Scatter(
            x=[i],
            y=[ordem.loc[i, "PIB pc"]],
            mode="markers",
            showlegend=False,
            marker={
                "symbol": "circle-open",
                "size": 9,
                "color": COR["caso"],
                "line": {"width": 1.2},
            },
        )
    )
    rotulo(
        fig,
        i,
        np.log10(ordem.loc[i, "PIB pc"]),
        m,
        dx=-6,
        dy=8,
        ha="right",
        va="bottom",
    )
fig.update_yaxes(
    type="log",
    range=[np.log10(4), np.log10(260)],
    tickvals=[5, 10, 20, 50, 100, 200],
    title_text="PIB per capita 2021 (R$ mil, log)",
)
fig.update_xaxes(title_text="167 municípios em ordem crescente de PIB per capita")
print(
    f"  P10={p10 * 1e3:.0f} P90={p90 * 1e3:.0f}; acima do P90 por setor:",
    ordem.loc[ordem["PIB pc"] >= p90, "Dominante"].value_counts().to_dict(),
)
salvar(fig, "fig2_separatrizes")

# ---------------------------------------------------------------------------
# Fig. 3 - Nº de municípios por setor de maior VAB, 2002-2021 (linha)
#          Agropecuária a preços correntes = VAB total - (indústria + serviços + adm.)
# ---------------------------------------------------------------------------
hist = pd.read_excel(ARQ, sheet_name="Serie_Historica")
hist.columns = [
    int(float(c)) if str(c).replace(".0", "").isdigit() else c for c in hist.columns
]
ANOS = list(range(2002, 2022))
hist = hist[
    (hist["Preços"] == "Correntes")
    & (hist["Município"] != "RIO GRANDE DO NORTE (total)")
]
serie = {
    s: hist[hist["Série"].str.startswith("VAB " + s)]
    .set_index("Município")[ANOS]
    .astype(float)
    for s in ["Indústria", "Serviços", "Adm. pública", "total"]
}
serie["Agropecuária"] = (
    serie["total"] - serie["Indústria"] - serie["Serviços"] - serie["Adm. pública"]
)
dom_ano = (
    pd.DataFrame(
        {
            ano: pd.concat([serie[s][ano].rename(s) for s in SETORES], axis=1)
            .idxmax(axis=1)
            .value_counts()
            for ano in ANOS
        }
    )
    .fillna(0)
    .astype(int)
    .reindex(SETORES)
)
assert dom_ano.loc["Adm. pública", 2021] == 122, dom_ano[2021]
fig = figura(
    6.4,
    2.5,
    showlegend=True,
    legend={
        "x": 0.98,
        "y": 0.5,
        "xanchor": "right",
        "yanchor": "middle",
        "font_size": 10,
        "bgcolor": "rgba(0,0,0,0)",
    },
)
for s in ALVO:
    fig.add_trace(
        go.Scatter(
            x=ANOS,
            y=dom_ano.loc[s],
            mode="lines",
            line=dict(color=COR[s], width=2),
            name=f"{s} ({dom_ano.loc[s, 2021]} em 2021)",
        )
    )
rotulo(fig, 2021, 122, "<b>122</b>", dx=4, ha="left", tam=11)
fig.update_xaxes(tickvals=list(range(2002, 2022, 3)), range=[2002, 2022.5])
fig.update_yaxes(title_text="Nº de municípios", range=[0, 167])
print("  dominante por ano:\n", dom_ano.loc[:, [2002, 2010, 2021]].to_string())
salvar(fig, "fig3_setor_dominante")

# ---------------------------------------------------------------------------
# Fig. 4 - Participação de cada setor (X) x IDHM (Y): reta Y = a + bX ajustada aos 167,
#          média do RN e município escolhido do setor em destaque
# ---------------------------------------------------------------------------
fig = make_subplots(
    rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.04, subplot_titles=[" "] * 3
)
fig.update_layout(
    LAYOUT, width=6.4 * PX, height=2.3 * PX, margin=dict(l=55, r=10, t=25, b=70)
)
for j, (m, s) in enumerate(CASOS.items(), start=1):
    x, y = mun[s], mun["IDHM 2010"]
    b, a = np.polyfit(x, y, 1)
    xs = np.linspace(x.min(), x.max(), 50)
    fig.add_trace(
        go.Scatter(
            x=x, y=y, mode="markers", marker={"color": COR[s], "size": 5, "opacity": 0.5}
        ),
        row=1,
        col=j,
    )
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=a + b * xs,
            mode="lines",
            line={"color": COR["ref"], "width": 1.5, "dash": "dash"},
        ),
        row=1,
        col=j,
    )
    fig.add_trace(
        go.Scatter(
            x=[x.mean()],
            y=[y.mean()],
            mode="markers",
            marker={
                "symbol": "cross-thin",
                "size": 11,
                "line": {
                    "color": COR["caso"],
                    "width": 1.5
                },
            },
        ),
        row=1,
        col=j,
    )
    ponto_caso(fig, x[idx[m]], y[idx[m]], row=1, col=j)
    dx, dy, ha, va = {
        "Guamaré": (0, 8, "center", "bottom"),
        "Natal": (-8, -4, "right", "top"),
        "Ceará-Mirim": (-8, -10, "right", "top"),
    }[m]
    rotulo(fig, x[idx[m]], y[idx[m]], m, dx, dy, ha, va, row=1, col=j)
    fig["layout"]["annotations"][j - 1].update(
        text=f"{s}: b = " + f"{b * 100:+.3f}".replace(".", ","),
        font_size=11,
        x=fig["layout"][f"xaxis{j if j > 1 else ''}"]["domain"][0],
        xanchor="left",
    )
    print(
        f"  {s} x IDHM: b={b:.3g} (por 100 p.p.: {b * 100:+.3f}) r={np.corrcoef(x, y)[0, 1]:.2f}"
    )
fig.update_yaxes(title_text="IDHM 2010", row=1, col=1)
fig.update_xaxes(
    title_text="Participação do setor no VAB municipal, 2021 (%)", row=1, col=2
)
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.42,
    showarrow=False,
    font={"size": 9, "color": COR["ref"]},
    text="b = variação do IDHM por 100 pontos percentuais · ponto preto = município escolhido · + = média do RN · tracejado = reta Y = a + bX",
)
salvar(fig, "fig4_setores_idhm")

# ---------------------------------------------------------------------------
# Fig. 5 - Relação inversa: municípios cuja maior atividade é a administração pública
#          têm IDHM menor e menos emprego formal (boxplots por setor dominante)
# ---------------------------------------------------------------------------
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12)
fig.update_layout(
    LAYOUT, width=6.4 * PX, height=2.6 * PX, margin=dict(l=55, r=10, t=20, b=60)
)
grupos = ALVO
for j, (col, lab) in enumerate(
    [("IDHM 2010", "IDHM 2010"), ("Emprego formal", "Emprego formal, 2021 (%)")],
    start=1,
):
    dados = [mun.loc[mun["Dominante"] == s, col] for s in grupos]
    for i, (s, d) in enumerate(zip(grupos, dados)):
        caixa(fig, i, d, COR[s], larg=0.55, row=1, col=j)
        fig.add_annotation(
            x=i,
            y=1,
            yref="y domain",
            text=f"n = {len(d)}",
            showarrow=False,
            yanchor="bottom",
            font={"size": 9, "color": COR["ref"]},
            row=1,
            col=j,
        )
        m = [k for k, v in CASOS.items() if v == s]
        if m:
            ponto_caso(fig, i, mun.loc[idx[m[0]], col], row=1, col=j)
    fig.update_xaxes(
        tickvals=list(range(len(grupos))),
        ticktext=grupos,
        showgrid=False,
        tickfont_size=10,
        row=1,
        col=j,
    )
    fig.update_yaxes(title_text=lab, row=1, col=j)
    print(
        f"  mediana de {col} por setor dominante:",
        {s: round(d.median(), 3) for s, d in zip(grupos, dados)},
    )
fig.add_annotation(
    xref="paper",
    yref="paper",
    x=0.5,
    y=-0.3,
    showarrow=False,
    font={"size": 11},
    text="Setor de maior VAB em 2021 (ponto preto = município escolhido)",
)
salvar(fig, "fig5_adm_inversa")

# Linha da Tabela 1 (emprego formal 2021 por grupo de PIB per capita) para o artigo
g = pd.cut(
    mun["PIB pc"],
    [0, p10, p90, np.inf],
    labels=["até P10", "P10-P90", "a partir de P90"],
    right=False,
)
print(
    "  % pop. em emprego formal 2021, mediana por grupo:",
    mun.groupby(g, observed=True)["Emprego formal"].median().round(1).to_dict(),
)
