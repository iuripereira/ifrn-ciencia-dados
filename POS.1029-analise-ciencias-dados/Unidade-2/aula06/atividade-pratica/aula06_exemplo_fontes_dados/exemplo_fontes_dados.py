# -*- coding: utf-8 -*-
"""
Aula 06 — Processos e Fontes de Dados
Exemplo prático: estabelecimentos de saúde do Rio Grande do Norte (CNES)

Este script percorre as QUATRO fontes de dados da aula (arquivo, API REST,
banco de dados, web scraping) e os principais FORMATOS (JSON, CSV, Parquet,
XML, GeoJSON), usando um caso real: unidades de saúde cadastradas no CNES
(Cadastro Nacional de Estabelecimentos de Saúde), a mesma base que sustenta
o Cartão Nacional de Saúde e o financiamento do SUS.

Os dados de dados/cnes_rn_amostra.json foram coletados ao vivo em 2026-09-28
a partir da API pública do Ministério da Saúde (apidadosabertos.saude.gov.br)
e da API de Malhas do IBGE — são reais, não sintéticos. A chamada HTTP com
`requests` abaixo reproduz exatamente como foram obtidos; ela não é executada
neste ambiente de preparo de aula (sem acesso à internet), mas os arquivos em
dados/ já contêm o resultado real dessa chamada, pronto para uso pelos
estudantes.
"""

import json
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

DADOS = Path("dados")

# ---------------------------------------------------------------------------
# FONTE 1 — API REST (como seria obtido ao vivo)
# ---------------------------------------------------------------------------
# import requests
#
# url = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos"
# registros = []
# for codigo_municipio in [240810, 240800, 240325, 240200,
#                          240940, 240020, 240260, 240310]:
#     resp = requests.get(url, params={"codigo_municipio": codigo_municipio,
#                                       "limit": 20}, timeout=10)
#     resp.raise_for_status()
#     registros += resp.json()["estabelecimentos"]
#
# Duas armadilhas reais desta API (descobertas testando, não documentadas):
#   1) limit=20 é o TETO do servidor — pedir limit=1000 não muda nada;
#      para mais registros é preciso paginar com offset=20, offset=40, ...
#   2) o parâmetro de filtro por município é `codigo_municipio` (código IBGE
#      de 6 dígitos, sem o dígito verificador) — outros nomes plausíveis como
#      `uf`, `co_ibge` ou `codigo_uf` são aceitos sem erro, mas SILENCIOSAMENTE
#      ignorados, e a API devolve dados de qualquer município. Isso é comum em
#      APIs públicas: testar o retorno é obrigatório, não basta supor.

print("Passo 1 — Carregando o snapshot salvo da API (fonte: arquivo)")
with open(DADOS / "cnes_rn_amostra.json", encoding="utf-8") as f:
    payload = json.load(f)

print(f"  fonte      : {payload['fonte']}")
print(f"  endpoint   : {payload['endpoint']}")
print(f"  coletado em: {payload['data_coleta']}")
print(f"  licença    : {payload['licenca']}")
print(f"  observação : {payload['observacao']}")

df = pd.DataFrame(payload["registros"])
print(f"\n  {df.shape[0]} estabelecimentos, {df['municipio'].nunique()} municípios")
print(df.groupby("municipio").size().sort_values(ascending=False))

# ---------------------------------------------------------------------------
# FONTE 2 — Banco de dados (SQLite)
# ---------------------------------------------------------------------------
print("\nPasso 2 — Banco de dados: gravando em SQLite e consultando com SQL")
con = sqlite3.connect(":memory:")
df.to_sql("estabelecimentos", con, index=False, if_exists="replace")

consulta = """
    SELECT municipio,
           descricao_tipo_unidade,
           COUNT(*) AS n
    FROM estabelecimentos
    WHERE descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA')
    GROUP BY municipio, descricao_tipo_unidade
    ORDER BY n DESC
"""
resultado_sql = pd.read_sql(consulta, con)
print(resultado_sql.to_string(index=False))
con.close()

# ---------------------------------------------------------------------------
# FONTE 3 — Web scraping (HTML salvo de uma coleta real)
# ---------------------------------------------------------------------------
print("\nPasso 3 — Web scraping: extraindo uma tabela HTML com BeautifulSoup")
# Em uma coleta ao vivo:
#   import requests
#   html = requests.get("https://pt.wikipedia.org/wiki/Lista_de_municípios_do_Rio_Grande_do_Norte").text
# Aqui usamos o HTML já salvo (mesmo conteúdo, coletado em 2026-09-28) para
# manter o exemplo reprodutível sem depender de rede.
from bs4 import BeautifulSoup

with open(DADOS / "wikipedia_municipios_rn.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

linhas = []
tabela = soup.find("table")
for tr in tabela.find_all("tr")[1:]:
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
    if cols:
        linhas.append({"municipio": cols[1], "codigo_ibge": cols[2]})

df_scraping = pd.DataFrame(linhas)
print(df_scraping.to_string(index=False))
print("  Licença da fonte: CC BY-SA 4.0 (Wikipédia) — uso permitido, exige atribuição")
print("  Antes de raspar um site: checar robots.txt e os termos de uso.")

# ---------------------------------------------------------------------------
# FORMATOS — convertendo o mesmo DataFrame para CSV, Parquet, XML e GeoJSON
# ---------------------------------------------------------------------------
print("\nPasso 4 — Gravando o mesmo conjunto em diferentes formatos")

df.to_csv(DADOS / "cnes_rn_amostra.csv", index=False, sep=";", decimal=",", encoding="utf-8")
print(f"  CSV     : {(DADOS / 'cnes_rn_amostra.csv').stat().st_size} bytes")

df.to_parquet(DADOS / "cnes_rn_amostra.parquet", index=False)
print(f"  Parquet : {(DADOS / 'cnes_rn_amostra.parquet').stat().st_size} bytes")

# XML manual (mostra a estrutura verbosa e aninhada, típica de XML)
root = ET.Element("estabelecimentos")
for _, row in df.head(3).iterrows():
    el = ET.SubElement(root, "estabelecimento")
    for campo in ["municipio", "descricao_tipo_unidade", "latitude", "longitude"]:
        sub = ET.SubElement(el, campo)
        sub.text = str(row[campo])
ET.ElementTree(root).write(DADOS / "cnes_amostra_3linhas.xml", encoding="utf-8", xml_declaration=True)
print(f"  XML (3 linhas, ilustrativo): {(DADOS / 'cnes_amostra_3linhas.xml').stat().st_size} bytes")

tamanhos = {
    "JSON (bruto, com metadados)": (DADOS / "cnes_rn_amostra.json").stat().st_size,
    "CSV": (DADOS / "cnes_rn_amostra.csv").stat().st_size,
    "Parquet": (DADOS / "cnes_rn_amostra.parquet").stat().st_size,
}
print("\n  Comparação de tamanho (mesmos 160 registros, formatos diferentes):")
for nome, tam in sorted(tamanhos.items(), key=lambda x: x[1]):
    print(f"    {nome:<32} {tam:>7} bytes")

# ---------------------------------------------------------------------------
# MAPA — contorno real do RN (IBGE) + pontos reais dos estabelecimentos
# ---------------------------------------------------------------------------
print("\nPasso 5 — Mapa: contorno do RN (IBGE) + estabelecimentos (CNES)")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open(DADOS / "rn_contorno.json", encoding="utf-8") as f:
    contorno = json.load(f)

xs = [c[0] for c in contorno["coordinates"]]
ys = [c[1] for c in contorno["coordinates"]]

fig, ax = plt.subplots(figsize=(7, 6.5))
ax.plot(xs, ys, color="#00693e", linewidth=1.5)
ax.fill(xs, ys, color="#00693e", alpha=0.05)

cores = {
    "Natal": "#c0392b", "Mossoro": "#2980b9", "Parnamirim": "#8e44ad",
    "Caico": "#d68910", "PauDosFerros": "#16a085", "Acu": "#2c3e50",
    "CearaMirim": "#e91e8c", "CurraisNovos": "#7f8c8d",
}
for municipio, grupo in df.groupby("municipio"):
    ax.scatter(grupo["longitude"], grupo["latitude"], s=28, alpha=0.85,
               color=cores.get(municipio, "gray"), label=f"{municipio} ({len(grupo)})",
               edgecolors="white", linewidths=0.4)

ax.set_title("Estabelecimentos de saúde (CNES) em 8 municípios do RN — amostra real", fontsize=11)
ax.set_xlabel("longitude")
ax.set_ylabel("latitude")
ax.set_aspect("equal")
ax.legend(fontsize=7, loc="lower left", framealpha=0.9)
fig.tight_layout()
fig.savefig("mapa_estabelecimentos_rn.png", dpi=150)
print("  mapa salvo em mapa_estabelecimentos_rn.png")

print("\nConcluído.")
