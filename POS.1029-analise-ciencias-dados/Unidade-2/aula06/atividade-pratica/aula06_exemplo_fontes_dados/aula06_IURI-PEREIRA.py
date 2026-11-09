# -*- coding: utf-8 -*-
"""
Aula 06 — Processos e Fontes de Dados — Atividade prática
Aluno: Iuri Pereira

Base: dados/cnes_rn_amostra.json — amostra real de estabelecimentos de saúde
do CNES em 8 municípios do RN, coletada da API de Dados Abertos do Ministério
da Saúde (DEMAS) em 2026-09-28.

Tarefas (README da aula):
  1. Carregar o JSON e registrar a proveniência (fonte, endpoint, data, licença).
  2. Gravar em SQLite e rodar uma consulta SQL própria com GROUP BY.
  3. Exportar em CSV, Parquet e JSON Lines e comparar os tamanhos.
  4. Checklist ética e legal antes de raspar um site.
  5. (Extra) Gráfico com os dados.

Pode rodar de qualquer pasta: os caminhos partem da pasta do script.
"""

import json
import sqlite3
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent  # independe do diretório de onde o script é chamado
DADOS = BASE / "dados"
SAIDA = BASE / "saida"  # pasta própria, para não sobrescrever os arquivos do exemplo
SAIDA.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# PASSO 1 — Carga do arquivo e registro da proveniência
# ---------------------------------------------------------------------------
print("Passo 1 — Carregando dados/cnes_rn_amostra.json")
with open(DADOS / "cnes_rn_amostra.json", encoding="utf-8") as f:
    payload = json.load(f)

# A proveniência fica num dicionário: é impressa aqui e gravada junto das
# exportações, para que o dado nunca circule separado da sua origem.
proveniencia = {
    "fonte": payload["fonte"],
    "endpoint": payload["endpoint"],
    "parametros": payload["parametros_exemplo"],
    "data_coleta": payload["data_coleta"],
    "licenca": payload["licenca"],
    "observacao": payload["observacao"],
}
for chave, valor in proveniencia.items():
    print(f"  {chave:<12}: {valor}")

df = pd.DataFrame(payload["registros"])
print(f"\n  {df.shape[0]} registros x {df.shape[1]} colunas")
print(df.dtypes.to_string())

# Checagens mínimas de qualidade antes de usar o dado
print("\n  Nulos por coluna:", df.isna().sum().to_dict())
print("  Linhas duplicadas (mesmo tipo e mesma coordenada):", df.duplicated().sum())
# Coordenadas "redondas" como (-5.795, -35.209) repetidas sugerem geocodificação
# pelo centro do município, não pelo endereço — vale anotar como limitação.

# ---------------------------------------------------------------------------
# PASSO 2 — Banco de dados: SQLite + consulta própria com GROUP BY
# ---------------------------------------------------------------------------
print("\nPasso 2 — SQLite: diversidade de tipos de unidade por município")
con = sqlite3.connect(SAIDA / "cnes_rn.sqlite")
df.to_sql("estabelecimentos", con, index=False, if_exists="replace")

# Pergunta: em cada município, quantos tipos diferentes de unidade aparecem
# na amostra, e qual a fatia de consultórios isolados e de atenção básica?
# Município com poucos tipos e muito consultório = oferta pouco diversificada.
consulta = """
    SELECT municipio,
           COUNT(*)                                   AS total,
           COUNT(DISTINCT descricao_tipo_unidade)     AS tipos_distintos,
           SUM(descricao_tipo_unidade = 'CONSULTORIO ISOLADO')            AS consultorios,
           SUM(descricao_tipo_unidade = 'CENTRO DE SAUDE/UNIDADE BASICA') AS ubs,
           ROUND(100.0 * SUM(descricao_tipo_unidade = 'CONSULTORIO ISOLADO')
                 / COUNT(*), 1)                       AS pct_consultorio
    FROM estabelecimentos
    GROUP BY municipio
    HAVING COUNT(*) >= 10
    ORDER BY tipos_distintos DESC, pct_consultorio ASC
"""
resultado_sql = pd.read_sql(consulta, con)
print(resultado_sql.to_string(index=False))
con.close()

# ---------------------------------------------------------------------------
# PASSO 3 — Formatos: CSV, Parquet e JSON Lines; comparação de tamanho
# ---------------------------------------------------------------------------
print("\nPasso 3 — Exportando o mesmo conjunto em formatos diferentes")
arquivos = {
    "CSV": SAIDA / "cnes_rn.csv",
    "Parquet": SAIDA / "cnes_rn.parquet",
    "JSON Lines": SAIDA / "cnes_rn.jsonl",
}
df.to_csv(arquivos["CSV"], index=False, sep=";", decimal=",", encoding="utf-8")
df.to_parquet(arquivos["Parquet"], index=False)
df.to_json(arquivos["JSON Lines"], orient="records", lines=True, force_ascii=False)

# Proveniência viaja junto, num arquivo ao lado
with open(SAIDA / "PROVENIENCIA.json", "w", encoding="utf-8") as f:
    json.dump(proveniencia, f, ensure_ascii=False, indent=1)

tamanhos = {nome: p.stat().st_size for nome, p in arquivos.items()}
tamanhos["JSON original (com metadados)"] = (DADOS / "cnes_rn_amostra.json").stat().st_size
menor = min(tamanhos.values())
print(f"  {'formato':<32} {'bytes':>8} {'x menor':>8}")
for nome, tam in sorted(tamanhos.items(), key=lambda x: x[1]):
    print(f"  {nome:<32} {tam:>8} {tam / menor:>8.1f}")

# Leitura de volta: o Parquet preserva os tipos; o CSV volta tudo que não for
# número como texto e depende de acertar sep/decimal na leitura.
df_parquet = pd.read_parquet(arquivos["Parquet"])
assert df_parquet.equals(df), "Parquet deveria voltar idêntico ao DataFrame original"
print("  Parquet relido: idêntico ao original (tipos preservados).")
print("  Parquet é o menor mesmo com 160 linhas: armazena por coluna e comprime")
print("  valores repetidos (município, tipo de unidade). JSON repete o nome de cada")
print("  campo em toda linha, por isso é o maior.")

# ---------------------------------------------------------------------------
# PASSO 4 — Checklist ética e legal antes de fazer scraping
# ---------------------------------------------------------------------------
# Site escolhido: Portal da Transparência do RN (transparencia.rn.gov.br)
CHECKLIST = """
Passo 4 — Checklist antes de raspar o Portal da Transparência do RN

[ ] 1. Existe API ou download oficial (CSV/dados abertos)? Se sim, usar e NÃO raspar.
[ ] 2. robots.txt (https://<site>/robots.txt): o caminho desejado está em Disallow?
       Há Crawl-delay? Respeitar ambos — robots.txt é a vontade explícita do dono.
[ ] 3. Termos de uso: proíbem coleta automatizada, reprodução ou uso comercial?
[ ] 4. Licença do conteúdo: dados abertos (LAI 12.527/2011), CC BY, CC BY-SA...?
       Anotar a exigência de atribuição e citar a fonte no trabalho.
[ ] 5. Dados pessoais (LGPD 13.709/2018): nomes, CPFs, salários de servidores?
       Coletar só o necessário, anonimizar/agregar, não republicar dado pessoal.
[ ] 6. Login, captcha ou paywall? Contornar isso NÃO é aceitável — parar aqui.
[ ] 7. Carga no servidor: 1 requisição por vez, pausa entre elas (>= 1 s),
       horário de menor uso, cache local para não repetir downloads.
[ ] 8. Identificação: User-Agent com nome e contato (e-mail) do coletor.
[ ] 9. Registrar a proveniência: URL, data/hora da coleta, versão da página.
[ ] 10. Na dúvida sobre qualquer item, pedir autorização ao responsável pelo site.
"""
print(CHECKLIST)

# ---------------------------------------------------------------------------
# PASSO 5 (extra) — Gráfico: tipos de unidade por município
# ---------------------------------------------------------------------------
print("Passo 5 — Gráfico: composição dos tipos de unidade por município")
import matplotlib
import plotly.express as px

matplotlib.use("Agg")  # gera o PNG sem precisar de janela
import matplotlib.pyplot as plt

# Os 5 tipos mais frequentes ficam com nome; o resto vira "OUTROS"
top5 = df["descricao_tipo_unidade"].value_counts().head(5).index
tipo = df["descricao_tipo_unidade"].where(df["descricao_tipo_unidade"].isin(top5), "OUTROS")
tabela = pd.crosstab(df["municipio"], tipo)
tabela = tabela[list(top5) + ["OUTROS"]]

fig, ax = plt.subplots(figsize=(10, 5.5))
tabela.plot(kind="barh", stacked=True, ax=ax, colormap="tab20", width=0.75)
ax.set_title("Tipos de estabelecimento de saúde (CNES) — amostra de 20 por município do RN", fontsize=11)
ax.set_xlabel("estabelecimentos na amostra")
ax.set_ylabel("")
ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)
fig.text(0.01, 0.01, f"Fonte: {proveniencia['fonte']}, coleta {proveniencia['data_coleta']}", fontsize=7, color="gray")
fig.tight_layout()
fig.savefig(SAIDA / "tipos_por_municipio.png", dpi=150)
print(f"  gráfico salvo em {SAIDA / 'tipos_por_municipio.png'}")

# Os mesmos dados, interativos com Plotly (o Plotly não converte figura do
# matplotlib: a figura é montada de novo a partir da mesma tabela)
fig_plotly = px.bar(
    tabela, orientation="h",
    title="Tipos de estabelecimento de saúde (CNES) — amostra de 20 por município do RN",
    labels={"value": "estabelecimentos na amostra", "municipio": "", "descricao_tipo_unidade": "tipo"},
)
fig_plotly.write_html(SAIDA / "tipos_por_municipio.html")
print(f"  gráfico interativo salvo em {SAIDA / 'tipos_por_municipio.html'}")

print("\nConcluído.")
