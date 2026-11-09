# Tópicos de Estudo — Aula 08: Web Scraping com Beau

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 08: Web Scraping com BeautifulSoup

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 08: Web Scraping com BeautifulSoup  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:23  |

## Descrição

Roteiro de leitura da Aula 08 em 5 capítulos curtos: o que é web scraping, anatomia do HTML e BeautifulSoup, seletores CSS, tabelas e paginação, uso ético e limitações legais.

## Índice

- 1. Web scraping: o que é e quando usar
- 2. Anatomia do HTML e o BeautifulSoup
- 3. Seletores CSS na prática
- 4. Tabelas e paginação
- 5. Uso ético e limitações legais

## 1. Web scraping: o que é e quando usar

Web scraping é baixar páginas web com um programa e extrair delas, automaticamente, as informações de interesse. É a quarta família de fontes de dados vista na Aula 06 — e a mais frágil: a página foi feita para pessoas lerem, não para programas consumirem, e qualquer mudança no visual do site pode quebrar o código.

#### Ordem de preferência

- Arquivo pronto (CSV, Excel, portal de dados abertos);
- API (Aula 07) — canal oficial, estruturado e estável;
- Web scraping — quando o dado só existe na página HTML.

#### O fluxo de uma coleta

```
requests.get(url) → resp.text (HTML) → BeautifulSoup → select(...) → lista de dicionários → DataFrame → CSV/JSON
```

#### Nossas fontes nesta aula

- Estante Potiguar — mini-site de resenhas de clássicos brasileiros, criado para a aula (leitores e comentários fictícios). Roda no seu computador com `python -m http.server 8000 --directory site_resenhas`.
- Books to Scrape (`books.toscrape.com`) — site real mantido para treino de scraping: 1.000 livros, preço e avaliação em estrelas, 50 páginas.

Grandes sites de resenhas reais (de livros ou restaurantes) costumam proibir a coleta automatizada nos Termos de Uso e publicam comentários de pessoas reais — por isso usamos fontes onde a coleta é permitida.

## 2. Anatomia do HTML e o BeautifulSoup

Uma página HTML é uma árvore de tags. Cada tag pode ter atributos; para scraping, os mais úteis são `class` e `id`. Uma resenha da Estante Potiguar:

```
<article class="resenha" data-id="1">
  <h2 class="livro">Dom Casmurro</h2>
  <p class="autor">Machado de Assis</p>
  <div class="nota" data-nota="5">★★★★★</div>
  <p class="leitor">Por <span class="nome">Ana P.</span> em <time datetime="2026-09-02">02/09/2026</time></p>
  <p class="comentario">Releio a cada cinco anos...</p>
</article>
```

A mesma informação pode aparecer como texto (★★★★★, 02/09/2026) e como atributo (`data-nota="5"`, `datetime="2026-09-02"`). Prefira a versão mais limpa — normalmente o atributo.

#### BeautifulSoup em quatro linhas

```
soup = BeautifulSoup(html, "html.parser")
soup.find("h2").get_text()                    # 'Dom Casmurro'
soup.find("div", class_="nota")["data-nota"]  # '5'
soup.find_all("article")                      # lista de tags
```

- `get_text(strip=True)` — texto visível, sem espaços nas pontas;
- `tag["atr"]` (erro se não existir) e `tag.get("atr")` (devolve `None`);
- `tag["class"]` devolve uma lista: `class="star-rating Three"` → `["star-rating", "Three"]`.

Atenção à codificação: se o servidor responde só `text/html`, sem charset, o `requests` assume ISO-8859-1 e "página" vira "pÃ¡gina", "£51.77" vira "Â£51.77". Corrija com `resp.encoding = "utf-8"` antes de usar `resp.text`.

Dica: use o botão direito → Inspecionar do navegador para descobrir tags, classes e atributos.

## 3. Seletores CSS na prática

Com `select()` e `select_one()` o BeautifulSoup aceita seletores CSS, a mesma linguagem usada nas folhas de estilo.

   Seletor |  Encontra |
  `.comentario` |  elementos com a classe comentario |
  `#ranking` |  o elemento com id ranking |
  `article.resenha` |  <article> com a classe resenha |
  `article.resenha span.nome` |  span.nome em qualquer nível dentro da resenha |
  `ul.paginacao > li` |  <li> filho direto da lista |
  `div[data-nota]` |  <div> que tem o atributo data-nota |

`select()` devolve uma lista (talvez vazia); `select_one()` devolve o primeiro elemento ou `None`.

#### Extraindo uma lista de resenhas

```
for art in soup.select("article.resenha"):
    util = art.select_one(".util")          # pode não existir!
    registro = {
        "livro": art.select_one("h2.livro").get_text(strip=True),
        "nota": int(art.select_one("div.nota")["data-nota"]),
        "data": art.select_one("time")["datetime"],
        "util": int(util.get_text().split()[0]) if util else None,
    }
```

No Books to Scrape, a avaliação fica no nome da classe: `<p class="star-rating Three">` → `pod.select_one("p.star-rating")["class"][1]` devolve `"Three"`, que um dicionário converte em 3.

## 4. Tabelas e paginação

#### Tabelas HTML

Duas formas de transformar uma `<table>` em dados:

```
# Manual (controle total)
tabela = soup.select_one("table#ranking")
linhas = [[td.get_text(strip=True) for td in tr.select("td")] for tr in tabela.select("tbody tr")]

# Pandas (rápido) — StringIO vem do módulo io
ranking = pd.read_html(StringIO(resp.text), attrs={"id": "ranking"}, decimal=",", thousands=".")[0]
```

`read_html` devolve uma lista de DataFrames. Com `decimal=","`, a nota "4,50" vira o número 4.5 — sem isso, a coluna fica como texto.

#### Paginação

A estratégia mais robusta é seguir o link "próxima página" até ele não existir. O `href` costuma ser relativo; `urljoin` monta o endereço completo.

```
url = BASE      # endereço do site local (ver notebook)
while url:
    soup = BeautifulSoup(baixar(url).text, "html.parser")
    todas.extend(extrair_resenhas(soup))
    link = soup.select_one("li.proxima a")
    url = urljoin(url, link["href"]) if link else None
    time.sleep(PAUSA)   # PAUSA = 1 segundo
```

Resultado na Estante Potiguar: 3 páginas, 24 resenhas. No Books to Scrape, o link é `li.next a`; as 5 primeiras páginas trazem 100 livros (preço médio £34,56 em 09/10/2026).

## 5. Uso ético e limitações legais

Conseguir baixar uma página não significa poder coletá-la em massa. Antes de raspar:

- Termos de Uso — muitos sites proíbem a coleta automatizada.
- robots.txt — na raiz do site; lista caminhos proibidos (`Disallow`) e o intervalo entre requisições (`Crawl-delay`). Em Python: `urllib.robotparser.RobotFileParser`. A ausência do arquivo não é um "vale tudo".
- Existe API? Se existir, prefira-a.
- Dados pessoais — nomes, fotos e perfis são protegidos pela LGPD (Lei 13.709/2018) mesmo quando públicos. Colete só o necessário; anonimize quando possível.
- Direitos autorais — resenhas têm autoria: analisar estatisticamente é diferente de republicar.

#### Boas maneiras de um robô

- Identifique-se no `User-Agent`;
- espere entre requisições (`time.sleep`) e baixe só o necessário;
- guarde os dados localmente e registre a proveniência (fonte, URL, data).

#### Limitações técnicas

O `requests` só recebe o HTML enviado pelo servidor; páginas montadas por JavaScript aparecem vazias para o BeautifulSoup (seria preciso Selenium/Playwright). CAPTCHAs e bloqueios são sinais de que o site não quer ser raspado.