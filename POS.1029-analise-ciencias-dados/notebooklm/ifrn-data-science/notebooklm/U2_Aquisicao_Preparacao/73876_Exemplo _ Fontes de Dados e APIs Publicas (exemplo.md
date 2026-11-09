# Exemplo — Fontes de Dados e APIs Públicas (exemplo

Este script percorre as quatro fontes de dados desta aula (arquivo, banco de dados, web scraping e — em comentário — API REST) e os principais formatos (JSON, CSV, Parquet, XML, GeoJSON), usando um caso real: estabelecimentos de saúde cadastrados no CNES (Cadastro Nacional de Estabelecimentos de Saúde, Ministério da Saúde) em oito municípios do Rio Grande do Norte, mais o contorno geográfico do estado (IBGE). Os dados foram coletados ao vivo em 2026-09-28 — não são sintéticos.

O pacote completo (script + dados + resultados) está disponível no recurso "Pacote — Exemplo de Fontes de Dados e APIs Públicas" desta seção. Baixe e rode com `python3 exemplo_fontes_dados.py` (dependências: pandas, beautifulsoup4, pyarrow, matplotlib).

#### Passo 1 — Arquivo: carregando o snapshot da API já salvo em disco

Os 160 registros (20 por município × 8 municípios — o teto do servidor, ver Capítulo 4) foram salvos em `dados/cnes_rn_amostra.json` junto com metadados de proveniência. O comentário no topo do script mostra exatamente a chamada `requests.get(...)` que gerou esse arquivo — incluindo as duas armadilhas reais da API descobertas testando (parâmetros ignorados silenciosamente e paginação via `offset`).

```
print("Passo 1 — Carregando o snapshot salvo da API (fonte: arquivo)")
with open(DADOS / "cnes_rn_amostra.json", encoding="utf-8") as f:
    payload = json.load(f)

df = pd.DataFrame(payload["registros"])
print(df.groupby("municipio").size().sort_values(ascending=False))
```

Saída real:

```
Passo 1 — Carregando o snapshot salvo da API (fonte: arquivo)
  fonte      : Ministério da Saúde — DEMAS API de Dados Abertos (CNES)
  endpoint   : https://apidadosabertos.saude.gov.br/cnes/estabelecimentos
  coletado em: 2026-09-28
  licença    : Dados abertos governamentais (Lei 12.527/2011) — uso livre com citação da fonte
  observação : Amostra: 20 primeiros estabelecimentos por município (limite fixo do servidor).

  160 estabelecimentos, 8 municípios
municipio
Acu             20
Caico           20
CearaMirim      20
CurraisNovos    20
Mossoro         20
Natal           20
Parnamirim      20
PauDosFerros    20
```

#### Passo 2 — Banco de dados: o mesmo DataFrame agora como tabela SQLite

`df.to_sql` grava o DataFrame como tabela; `pd.read_sql` traz de volta o resultado de uma consulta SQL — o mesmo tipo de `GROUP BY` que a Aula 05 fez em Pandas, agora escrito em SQL puro.

```
con = sqlite3.connect(":memory:")
df.to_sql("estabelecimentos", con, index=False, if_exists="replace")

consulta = """
    SELECT municipio, descricao_tipo_unidade, COUNT(*) AS n
    FROM estabelecimentos
    WHERE descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA')
    GROUP BY municipio, descricao_tipo_unidade
    ORDER BY n DESC
"""
resultado_sql = pd.read_sql(consulta, con)
```

Saída real:

```
   municipio         descricao_tipo_unidade  n
  CearaMirim CENTRO DE SAUDE/UNIDADE BASICA  6
  Parnamirim CENTRO DE SAUDE/UNIDADE BASICA  5
CurraisNovos CENTRO DE SAUDE/UNIDADE BASICA  2
         Acu CENTRO DE SAUDE/UNIDADE BASICA  1
     Mossoro CENTRO DE SAUDE/UNIDADE BASICA  1
PauDosFerros                 HOSPITAL GERAL  1
```

#### Passo 3 — Web scraping: extraindo uma tabela da Wikipédia com BeautifulSoup

Usamos um trecho HTML real, salvo de uma coleta feita em 2026-09-28 (para manter o exemplo reprodutível sem depender de rede). A Wikipédia publica seu conteúdo sob licença CC BY-SA 4.0, que permite reuso — inclusive automatizado — exigindo atribuição.

```
from bs4 import BeautifulSoup

with open(DADOS / "wikipedia_municipios_rn.html", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

tabela = soup.find("table")
for tr in tabela.find_all("tr")[1:]:
    cols = [td.get_text(strip=True) for td in tr.find_all("td")]
```

Saída real:

```
        municipio codigo_ibge
            Acari     2400109
   Afonso Bezerra     2400307
        Água Nova     2400406
       Alexandria     2400505
    Almino Afonso     2400604
Alto do Rodrigues     2400703
  Licença da fonte: CC BY-SA 4.0 (Wikipédia) — uso permitido, exige atribuição
  Antes de raspar um site: checar robots.txt e os termos de uso.
```

#### Passo 4 — O mesmo conjunto de dados, quatro formatos diferentes

O script grava os mesmos 160 registros em CSV (padrão brasileiro: separador `;`, decimal `,`), Parquet e um XML ilustrativo com 3 linhas, e compara o tamanho de cada arquivo.

```
df.to_csv(DADOS / "cnes_rn_amostra.csv", index=False, sep=";", decimal=",", encoding="utf-8")
df.to_parquet(DADOS / "cnes_rn_amostra.parquet", index=False)
# ... XML manual com xml.etree.ElementTree (ver script completo) ...
```

Saída real — comparação de tamanho dos mesmos 160 registros:

```
    Parquet                             7868 bytes
    CSV                                12451 bytes
    JSON (bruto, com metadados)        36809 bytes
```

O Parquet é o menor por ser colunar e binário; o JSON é o maior porque carrega, além dos dados, os metadados de proveniência (fonte, endpoint, data da coleta, licença) — um custo em espaço que se paga em rastreabilidade (Capítulo 6).

#### Passo 5 — Mapa: contorno real do RN (IBGE) + estabelecimentos (CNES)

O contorno do Rio Grande do Norte vem da API de Malhas do IBGE (formato GeoJSON, simplificado para fins didáticos); os pontos são as coordenadas reais de latitude/longitude dos 160 estabelecimentos do CNES, coloridos por município. O resultado (`mapa_estabelecimentos_rn.png`) está reproduzido na apostila em PDF desta aula e é gerado novamente sempre que o script roda.

```
with open(DADOS / "rn_contorno.json", encoding="utf-8") as f:
    contorno = json.load(f)
xs = [c[0] for c in contorno["coordinates"]]
ys = [c[1] for c in contorno["coordinates"]]

fig, ax = plt.subplots(figsize=(7, 6.5))
ax.plot(xs, ys, color="#00693e", linewidth=1.5)
for municipio, grupo in df.groupby("municipio"):
    ax.scatter(grupo["longitude"], grupo["latitude"], s=28, color=cores.get(municipio, "gray"),
               label=f"{municipio} ({len(grupo)})")
fig.savefig("mapa_estabelecimentos_rn.png", dpi=150)
```

Dois pontos da amostra de Mossoró ficam visivelmente fora do agrupamento principal no mapa gerado — um lembrete honesto de que dados reais têm ruído (coordenadas mal cadastradas, por exemplo), diferente dos dados sintéticos das Aulas 04 e 05, que não têm essas imperfeições porque foram gerados sem elas.

#### Para reproduzir

- Baixe o pacote "Pacote — Exemplo de Fontes de Dados e APIs Públicas" (ZIP) desta seção.
- Extraia mantendo a subpasta `dados/` junto do script (o script espera esse caminho relativo).
- Instale as dependências: `pip install pandas requests beautifulsoup4 pyarrow matplotlib`.
- Rode: `python3 exemplo_fontes_dados.py`. Ele recria os arquivos CSV/Parquet/XML e o mapa.

Última atualização: segunda-feira, 28 set. 2026, 09:05