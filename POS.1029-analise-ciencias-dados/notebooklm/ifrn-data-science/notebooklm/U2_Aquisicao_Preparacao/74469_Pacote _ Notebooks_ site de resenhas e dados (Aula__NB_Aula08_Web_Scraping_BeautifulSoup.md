# Aula08_Web_Scraping_BeautifulSoup.ipynb

# Aula 08 — Laboratório: Web Scraping com BeautifulSoup

**Unidade 2 — Aquisição e Preparação de Dados** · Análise e Ciência de Dados (Especialização, IFRN)

Na Aula 07 os dados chegaram prontos, em JSON, por uma API. Hoje o cenário é outro: o dado existe, mas só está publicado **numa página feita para humanos lerem**. *Web scraping* é a técnica de baixar essa página e extrair dela, de forma automática, as informações que nos interessam.

Vamos trabalhar com **avaliações e comentários de livros** em duas fontes:

1. **Estante Potiguar** — um mini-site de resenhas de leitores criado para esta aula (pasta `site_resenhas/` do pacote). Os livros são clássicos brasileiros; os leitores e comentários são **fictícios**. Ele roda no seu próprio computador, então você pode raspar à vontade sem incomodar ninguém.
2. **Books to Scrape** (`books.toscrape.com`) — um site **real**, mantido publicamente justamente para quem quer treinar web scraping: 1.000 livros, com preço, avaliação em estrelas e 50 páginas de catálogo.

O que você vai praticar: análise da estrutura HTML · seletores CSS · extração de tabelas · paginação · uso ético (robots.txt, identificação, intervalo entre requisições).

> **Instalação:** `pip install requests beautifulsoup4 pandas lxml`
> **Importante:** abra este notebook na mesma pasta onde está a subpasta `site_resenhas/` (é assim que o pacote ZIP vem organizado).

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time, json, sys, subprocess
from io import StringIO
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from pathlib import Path

DADOS = Path("dados")
DADOS.mkdir(exist_ok=True)

# Sempre se identifique: diga quem é o robô e para que serve
CABECALHOS = {"User-Agent": "AulaACD-IFRN/1.0 (atividade educacional de web scraping)"}
pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)
print("requests", requests.__version__, "| bs4 ok | pandas", pd.__version__)
```
Saída:
```
requests 2.33.1 | bs4 ok | pandas 3.0.2

```

## Parte 1 — O HTML é uma árvore

Uma página HTML é uma árvore de **tags** (`<article>`, `<h2>`, `<p>`...). Cada tag pode ter **atributos** — os mais úteis para scraping são `class` e `id`, porque é por eles que os desenvolvedores organizam (e estilizam) a página. O BeautifulSoup lê esse texto e devolve um objeto que você navega com Python.

Vamos começar com um trecho de HTML pequeno, igual ao formato de uma resenha da Estante Potiguar:

```python
html_exemplo = """
<article class="resenha" data-id="1">
  <h2 class="livro">Dom Casmurro</h2>
  <p class="autor">Machado de Assis</p>
  <div class="nota" data-nota="5">★★★★★</div>
  <p class="leitor">Por <span class="nome">Ana P.</span> em <time datetime="2026-09-02">02/09/2026</time></p>
  <p class="comentario">Releio a cada cinco anos e sempre mudo de opinião sobre Capitu.</p>
</article>
"""
soup = BeautifulSoup(html_exemplo, "html.parser")

print(soup.find("h2").get_text())                 # primeira tag <h2>
print(soup.find("p", class_="autor").get_text())  # <p> com class="autor"
print(soup.find("div", class_="nota")["data-nota"])  # valor de um atributo
print(soup.find("time")["datetime"])
```
Saída:
```
Dom Casmurro
Machado de Assis
5
2026-09-02

```

### Seletores CSS: `select()` e `select_one()`

Além de `find`/`find_all`, o BeautifulSoup aceita **seletores CSS** — a mesma linguagem usada nas folhas de estilo. Eles são mais curtos e funcionam igual em outras ferramentas (navegador, Selenium, Scrapy).

| Seletor | Encontra |
|---|---|
| `h2` | toda tag `<h2>` |
| `.nota` | qualquer tag com `class="nota"` |
| `#ranking` | a tag com `id="ranking"` |
| `p.autor` | `<p>` com classe `autor` |
| `article .nome` | `.nome` em qualquer nível **dentro** de `<article>` |
| `ul > li` | `<li>` filho **direto** de `<ul>` |
| `div[data-nota]` | `<div>` que tenha o atributo `data-nota` |
| `li.proxima a` | o link dentro do item "próxima" |

`select()` devolve uma **lista** (pode ser vazia); `select_one()` devolve **o primeiro** elemento ou `None`.

```python
print(soup.select_one("article .nome").get_text())
print(soup.select_one("div[data-nota]")["data-nota"])
print([tag.name for tag in soup.select("article > *")])
```
Saída:
```
Ana P.
5
['h2', 'p', 'div', 'p', 'p']

```

> **Dica de ouro:** no navegador, clique com o botão direito sobre o dado que você quer e escolha **Inspecionar**. A ferramenta do desenvolvedor mostra a tag, as classes e os atributos — é daí que saem os seletores.

## Parte 2 — Antes de raspar: as regras do site

Antes da primeira requisição, responda três perguntas:

1. **O site permite?** Leia os *Termos de Uso* e o arquivo `robots.txt` (sempre na raiz: `https://site/robots.txt`). Ele diz quais caminhos os robôs não devem visitar (`Disallow`) e, às vezes, o intervalo mínimo entre requisições (`Crawl-delay`).
2. **Existe uma API?** Se existir (Aula 07), prefira a API: é mais estável e é o canal oficial.
3. **Os dados são pessoais?** Nomes, e-mails e perfis de pessoas são dados pessoais protegidos pela **LGPD** (Lei 13.709/2018), mesmo quando estão visíveis na página.

Vamos colocar a Estante Potiguar no ar no seu computador. A célula abaixo inicia um servidor web simples do próprio Python, servindo a pasta `site_resenhas/` em `http://localhost:8000/`.

```python
servidor = subprocess.Popen(
    [sys.executable, "-m", "http.server", "8000", "--directory", "site_resenhas"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
)
time.sleep(1.5)
BASE = "http://localhost:8000/"
print("Site no ar em", BASE)
```
Saída:
```
Site no ar em http://localhost:8000/

```

```python
robo = RobotFileParser(urljoin(BASE, "robots.txt"))
robo.read()

for caminho in ["index.html", "ranking.html", "privado/rascunhos.html"]:
    print(f"{caminho:25s} permitido? {robo.can_fetch(CABECALHOS['User-Agent'], urljoin(BASE, caminho))}")
print("Intervalo pedido entre requisições (Crawl-delay):", robo.crawl_delay("*"), "s")
```
Saída:
```
index.html                permitido? True
ranking.html              permitido? True
privado/rascunhos.html    permitido? False
Intervalo pedido entre requisições (Crawl-delay): 1 s

```

```python
resposta = requests.get(BASE, headers=CABECALHOS, timeout=10)
print("Status:", resposta.status_code)
print("Content-Type:", resposta.headers.get("Content-Type"))
print("Encoding adivinhado pelo requests:", resposta.encoding)
print("Título lido sem corrigir:", BeautifulSoup(resposta.text, "html.parser").title.get_text())
```
Saída:
```
Status: 200
Content-Type: text/html
Encoding adivinhado pelo requests: ISO-8859-1
Título lido sem corrigir: Resenhas â pÃ¡gina 1 | Estante Potiguar

```

Os acentos saíram embaralhados! O servidor respondeu apenas `text/html`, **sem** informar o *charset*. Nesse caso o `requests` segue a regra antiga do HTTP e assume **ISO-8859-1** — mas a página foi gravada em **UTF-8**, então "Resenhas — página" vira "Resenhas â pÃ¡gina". Isso acontece com muitos sites reais (inclusive o Books to Scrape, na Parte 6). A correção é dizer ao `requests` qual é a codificação certa antes de ler `resposta.text`:

```python
resposta.encoding = "utf-8"
pagina = BeautifulSoup(resposta.text, "html.parser")
print("Título corrigido:", pagina.title.get_text())
print("Resenhas nesta página:", len(pagina.select("article.resenha")))

# Daqui em diante, usamos uma função que já baixa, confere o status e corrige a codificação
def baixar(url):
    resp = requests.get(url, headers=CABECALHOS, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp
```
Saída:
```
Título corrigido: Resenhas — página 1 | Estante Potiguar
Resenhas nesta página: 8

```

## Parte 3 — Extraindo as resenhas da página 1

Agora transformamos cada `<article class="resenha">` em um dicionário. Repare em dois cuidados que fazem diferença em dados reais:

- a nota vem do **atributo** `data-nota` (um número limpo), e não das estrelas `★★★★☆` (que precisariam ser contadas);
- nem toda resenha tem o contador "pessoas acharam útil" — quando o elemento não existe, `select_one` devolve `None`, e o código precisa tratar isso em vez de quebrar.

```python
def extrair_resenhas(soup):
    registros = []
    for art in soup.select("article.resenha"):
        util = art.select_one(".util")
        registros.append({
            "id": int(art["data-id"]),
            "livro": art.select_one("h2.livro").get_text(strip=True),
            "autor": art.select_one("p.autor").get_text(strip=True),
            "nota": int(art.select_one("div.nota")["data-nota"]),
            "leitor": art.select_one("span.nome").get_text(strip=True),
            "data": art.select_one("time")["datetime"],
            "comentario": art.select_one("p.comentario").get_text(strip=True),
            "util": int(util.get_text().split()[0]) if util else None,
        })
    return registros

pagina1 = extrair_resenhas(pagina)
print(len(pagina1), "resenhas extraídas")
print(json.dumps(pagina1[0], ensure_ascii=False, indent=2))
```
Saída:
```
8 resenhas extraídas
{
  "id": 1,
  "livro": "Dom Casmurro",
  "autor": "Machado de Assis",
  "nota": 5,
  "leitor": "Ana P.",
  "data": "2026-09-02",
  "comentario": "Releio a cada cinco anos e sempre mudo de opinião sobre Capitu. Narrador mais suspeito da literatura brasileira.",
  "util": 31
}

```

## Parte 4 — Paginação: seguindo o link "Próxima"

Sites dividem listas longas em páginas. A estratégia mais robusta é **seguir o link "próxima página"** até ele não existir mais — assim o código não precisa saber de antemão quantas páginas há. Dois detalhes:

- o `href` costuma ser **relativo** (`pagina-2.html`); `urljoin` monta o endereço completo;
- respeite o `Crawl-delay` com `time.sleep()` entre uma página e outra.

```python
todas = []
url = BASE
pausa = robo.crawl_delay("*") or 1

while url:
    soup_pag = BeautifulSoup(baixar(url).text, "html.parser")
    novas = extrair_resenhas(soup_pag)
    todas.extend(novas)
    print(f"{url:40s} -> {len(novas)} resenhas (acumulado: {len(todas)})")

    link = soup_pag.select_one("li.proxima a")
    url = urljoin(url, link["href"]) if link else None
    if url:
        time.sleep(pausa)

df_resenhas = pd.DataFrame(todas)
print("\nTotal:", len(df_resenhas), "resenhas")
```
Saída:
```
http://localhost:8000/                   -> 8 resenhas (acumulado: 8)
http://localhost:8000/pagina-2.html      -> 8 resenhas (acumulado: 16)
http://localhost:8000/pagina-3.html      -> 8 resenhas (acumulado: 24)

Total: 24 resenhas

```

```python
resumo = (df_resenhas.groupby("livro")["nota"]
          .agg(resenhas="count", media="mean")
          .sort_values("media", ascending=False))
print(resumo.round(2))
print("\nResenhas sem o contador 'útil':", df_resenhas["util"].isna().sum())
```
Saída:
```
                                  resenhas  media
livro                                            
O Alienista                              4   4.50
Dom Casmurro                             4   4.25
Memórias Póstumas de Brás Cubas          4   4.25
O Cortiço                                4   4.00
Triste Fim de Policarpo Quaresma         4   4.00
Iracema                                  4   3.50

Resenhas sem o contador 'útil': 2

```

## Parte 5 — Extraindo tabelas

Tabelas HTML (`<table>`, `<tr>`, `<th>`, `<td>`) são o formato mais "amigável" para scraping. Há dois caminhos:

1. **Manual, com BeautifulSoup** — você percorre as linhas e células (controle total);
2. **`pd.read_html`** — o Pandas encontra as tabelas da página e já devolve DataFrames (rápido, ótimo quando a tabela é bem formada).

A página `ranking.html` da Estante Potiguar tem uma tabela com `id="ranking"`. Atenção a um detalhe brasileiro: a nota média usa **vírgula decimal** (`4,50`).

```python
resp = baixar(urljoin(BASE, "ranking.html"))
soup_rank = BeautifulSoup(resp.text, "html.parser")
tabela = soup_rank.select_one("table#ranking")

cabecalho = [th.get_text(strip=True) for th in tabela.select("thead th")]
linhas = [[td.get_text(strip=True) for td in tr.select("td")] for tr in tabela.select("tbody tr")]
print(cabecalho)
for linha in linhas[:3]:
    print(linha)
```
Saída:
```
['Posição', 'Livro', 'Autor', 'Ano', 'Resenhas', 'Nota média']
['1', 'O Alienista', 'Machado de Assis', '1882', '4', '4,50']
['2', 'Dom Casmurro', 'Machado de Assis', '1899', '4', '4,25']
['3', 'Memórias Póstumas de Brás Cubas', 'Machado de Assis', '1881', '4', '4,25']

```

```python
ranking = pd.read_html(StringIO(resp.text), attrs={"id": "ranking"}, decimal=",", thousands=".")[0]
print(ranking)
print()
print(ranking.dtypes)
```
Saída:
```
   Posição                             Livro             Autor   Ano  Resenhas  Nota média
0        1                       O Alienista  Machado de Assis  1882         4        4.50
1        2                      Dom Casmurro  Machado de Assis  1899         4        4.25
2        3   Memórias Póstumas de Brás Cubas  Machado de Assis  1881         4        4.25
3        4                         O Cortiço   Aluísio Azevedo  1890         4        4.00
4        5  Triste Fim de Policarpo Quaresma      Lima Barreto  1915         4        4.00
5        6                           Iracema   José de Alencar  1865         4        3.50

Posição         int64
Livro             str
Autor             str
Ano             int64
Resenhas        int64
Nota média    float64
dtype: object

```

Com `decimal=","` o Pandas já converteu `4,50` em `4.5` (número). Sem esse parâmetro, a coluna viria como texto — e qualquer média ou ordenação sairia errada.

## Parte 6 — Um site real de treino: Books to Scrape

`books.toscrape.com` é mantido publicamente **para que estudantes pratiquem scraping**. Ele não tem `robots.txt` (o endereço devolve 404) — o que **não** significa "vale tudo": continuamos nos identificando e esperando entre as requisições.

As saídas abaixo foram obtidas ao vivo em **09/10/2026**. Rode as células para ver o estado atual do site.

Estrutura de cada livro no catálogo (descoberta com *Inspecionar*):

```html
<article class="product_pod">
  <p class="star-rating Three"></p>
  <h3><a href="catalogue/a-light-in-the-attic_1000/index.html" title="A Light in the Attic">A Light in ...</a></h3>
  <p class="price_color">£51.77</p>
</article>
```

Repare: a **avaliação está escondida no nome da classe** (`star-rating Three`) e o título completo está no atributo `title` (o texto visível vem cortado com "...").

```python
URL_LIVROS = "https://books.toscrape.com/catalogue/page-1.html"
resp = requests.get(URL_LIVROS, headers=CABECALHOS, timeout=10)
print("Content-Type:", resp.headers.get("Content-Type"))
print("Encoding adivinhado pelo requests:", resp.encoding)
print("Preço lido sem corrigir:", BeautifulSoup(resp.text, "html.parser").select_one("p.price_color").get_text())

resp.encoding = "utf-8"   # o site não declara o charset; corrigimos à mão
soup_livros = BeautifulSoup(resp.text, "html.parser")
print("Preço lido corrigido:  ", soup_livros.select_one("p.price_color").get_text())
```
Saída:
```
Content-Type: text/html
Encoding adivinhado pelo requests: ISO-8859-1
Preço lido sem corrigir: Â£51.77
Preço lido corrigido:   £51.77

```

O mesmo problema da Parte 2, agora num site real: o servidor responde só `text/html`, sem charset, e o símbolo `£` (gravado em UTF-8) vira `Â£`. Por isso a função `baixar()` já corrige a codificação.

```python
NOTAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def extrair_livros(soup):
    livros = []
    for pod in soup.select("article.product_pod"):
        classe_nota = pod.select_one("p.star-rating")["class"][1]      # ex.: "Three"
        livros.append({
            "titulo": pod.select_one("h3 a")["title"],
            "preco_libras": float(pod.select_one("p.price_color").get_text().replace("£", "")),
            "nota": NOTAS[classe_nota],
        })
    return livros

pagina1_livros = extrair_livros(soup_livros)
print(len(pagina1_livros), "livros na página 1")
for livro in pagina1_livros[:5]:
    print(livro)
```
Saída:
```
20 livros na página 1
{'titulo': 'A Light in the Attic', 'preco_libras': 51.77, 'nota': 3}
{'titulo': 'Tipping the Velvet', 'preco_libras': 53.74, 'nota': 1}
{'titulo': 'Soumission', 'preco_libras': 50.1, 'nota': 1}
{'titulo': 'Sharp Objects', 'preco_libras': 47.82, 'nota': 4}
{'titulo': 'Sapiens: A Brief History of Humankind', 'preco_libras': 54.23, 'nota': 5}

```

### Paginação no site real

O catálogo tem **50 páginas**. Para não sobrecarregar o site na aula, vamos coletar só as **5 primeiras** (100 livros), seguindo o link `li.next a` e esperando 1 segundo entre as páginas. Para coletar o catálogo inteiro, basta remover o limite — leva cerca de 1 minuto.

```python
livros = []
url = "https://books.toscrape.com/catalogue/page-1.html"
paginas_lidas = 0

while url and paginas_lidas < 5:
    soup_pag = BeautifulSoup(baixar(url).text, "html.parser")
    livros.extend(extrair_livros(soup_pag))
    paginas_lidas += 1
    print(soup_pag.select_one("li.current").get_text(strip=True), "->", len(livros), "livros")

    proxima = soup_pag.select_one("li.next a")
    url = urljoin(url, proxima["href"]) if proxima else None
    time.sleep(1)

df_livros = pd.DataFrame(livros)
print("\nPreço médio: £", round(df_livros["preco_libras"].mean(), 2))
print(df_livros["nota"].value_counts().sort_index())
```
Saída:
```
Page 1 of 50 -> 20 livros
Page 2 of 50 -> 40 livros
Page 3 of 50 -> 60 livros
Page 4 of 50 -> 80 livros
Page 5 of 50 -> 100 livros

Preço médio: £ 34.56
nota
1    22
2    19
3    22
4    18
5    19
Name: count, dtype: int64

```

```python
print(df_livros.groupby("nota")["preco_libras"].agg(["count", "mean"]).round(2))
```
Saída:
```
      count   mean
nota              
1        22  35.52
2        19  35.91
3        22  36.84
4        18  33.98
5        19  30.01

```

Curiosidade dos dados: nesta amostra, livros com **5 estrelas** têm o **menor** preço médio. Como o site é de treino, preços e notas são gerados sem relação entre si — numa análise real, esse tipo de achado seria o ponto de partida para investigar, nunca uma conclusão.

### A tabela da página de um livro

Cada livro tem uma página de detalhe com uma tabela de informações do produto (`table.table-striped`), com pares `<th>`/`<td>`:

```python
url_livro = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
soup_livro = BeautifulSoup(baixar(url_livro).text, "html.parser")

print("Título:", soup_livro.select_one("div.product_main h1").get_text())
print("Categoria:", soup_livro.select("ul.breadcrumb li")[2].get_text(strip=True))
info = {tr.th.get_text(strip=True): tr.td.get_text(strip=True)
        for tr in soup_livro.select("table.table-striped tr")}
for chave, valor in info.items():
    print(f"  {chave:20s} {valor}")
```
Saída:
```
Título: A Light in the Attic
Categoria: Poetry
  UPC                  a897fe39b1053632
  Product Type         Books
  Price (excl. tax)    £51.77
  Price (incl. tax)    £51.77
  Tax                  £0.00
  Availability         In stock (22 available)
  Number of reviews    0

```

## Parte 7 — Salvando o resultado (com proveniência)

Assim como na Aula 07, salvamos os dados **junto com a informação de onde e quando vieram**.

```python
df_resenhas.to_csv(DADOS / "resenhas_estante_potiguar.csv", index=False, encoding="utf-8")
df_livros.to_csv(DADOS / "books_toscrape_5paginas.csv", index=False, encoding="utf-8")

with open(DADOS / "resenhas_estante_potiguar.json", "w", encoding="utf-8") as f:
    json.dump({
        "fonte": "Estante Potiguar (site fictício da Aula 08, servido localmente)",
        "url": BASE,
        "coletado_em": "2026-10-09",
        "observacao": "leitores e comentários fictícios; nomes abreviados",
        "resenhas": todas,
    }, f, ensure_ascii=False, indent=2)

for arq in sorted(DADOS.glob("*")):
    if not arq.name.startswith("_"):
        print(arq.name)
```
Saída:
```
books_toscrape_5paginas.csv
resenhas_estante_potiguar.csv
resenhas_estante_potiguar.json

```

```python
servidor.terminate()   # desliga o servidor local da Estante Potiguar
print("Servidor encerrado.")
```
Saída:
```
Servidor encerrado.

```

## Resumo e checklist ético

| Etapa | Ferramenta |
|---|---|
| Baixar a página | `requests.get(url, headers=..., timeout=...)` |
| Corrigir acentos/símbolos | `resp.encoding = "utf-8"` (quando o servidor não informa o charset) |
| Ler o HTML | `BeautifulSoup(resp.text, "html.parser")` |
| Encontrar elementos | `select()` / `select_one()` com seletores CSS |
| Ler texto e atributos | `.get_text(strip=True)`, `tag["atributo"]` |
| Paginar | seguir `li.next a` / `li.proxima a` com `urljoin` |
| Tabelas | `pd.read_html(StringIO(html), decimal=",")` |

**Antes de raspar qualquer site:** ☐ existe API? ☐ li os Termos de Uso? ☐ conferi o `robots.txt`? ☐ me identifiquei no `User-Agent`? ☐ uso `time.sleep()` entre requisições? ☐ coleto só o necessário e evito dados pessoais (LGPD)? ☐ guardo a proveniência?

**Próximos passos:** faça o **exercício prático** (entrega no Moodle) e o **formulário avaliativo** — ambos com prazo até **24/10/2026**.

