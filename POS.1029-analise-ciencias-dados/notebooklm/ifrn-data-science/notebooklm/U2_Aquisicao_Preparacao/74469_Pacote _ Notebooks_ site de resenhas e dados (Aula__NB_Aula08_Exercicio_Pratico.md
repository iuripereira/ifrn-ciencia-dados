# Aula08_Exercicio_Pratico.ipynb

# Exercício Prático — Aula 08: Web Scraping com BeautifulSoup

**Análise e Ciência de Dados** (Especialização, IFRN) — Unidade 2, Aula 08

**Entrega:** este notebook **executado** (com as saídas visíveis) + os arquivos CSV/JSON gerados, compactados em um `.zip`, na tarefa *Exercício Prático — Aula 08* do Moodle. **Prazo: 24/10/2026 (23h59).**

Preencha os trechos marcados com `# TODO`. Use o notebook `Aula08_Web_Scraping_BeautifulSoup.ipynb` como referência — os padrões de código são os mesmos.
Coloque este notebook na mesma pasta da subpasta `site_resenhas/` (vem no pacote da aula).

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time, json, sys, subprocess
from io import StringIO
from urllib.parse import urljoin
from pathlib import Path

SAIDA = Path("dados_exercicio")
SAIDA.mkdir(exist_ok=True)
CABECALHOS = {"User-Agent": "SEU-NOME-AulaACD/1.0 (exercicio educacional)"}  # TODO: coloque seu nome

def baixar(url):
    resp = requests.get(url, headers=CABECALHOS, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")
```

## Parte A — Estante Potiguar (site local)

1. Coloque o site no ar (célula abaixo) e raspe **todas as resenhas**, seguindo o link "Próxima" (`li.proxima a`) e esperando 1 s entre as páginas.
2. Monte um DataFrame com: `livro`, `autor`, `nota`, `leitor`, `data`, `comentario`, `util` (use `None` quando o contador não existir).

```python
servidor = subprocess.Popen([sys.executable, "-m", "http.server", "8000", "--directory", "site_resenhas"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
BASE = "http://localhost:8000/"

resenhas = []
url = BASE
# TODO: laço de paginação — baixar a página, extrair cada article.resenha, seguir li.proxima a

df_res = pd.DataFrame(resenhas)
print(len(df_res), "resenhas")
```

3. Calcule, **por autor**, o número de resenhas e a nota média (ordenado da maior para a menor média).
4. Mostre a resenha **mais útil** (maior valor de `util`): livro, leitor e quantidade.
5. Leia a tabela `table#ranking` de `ranking.html` com `pd.read_html(..., decimal=",")` e confira se as médias por livro batem com as que você calcularia a partir das resenhas.

```python
# TODO: agrupamento por autor

# TODO: resenha mais útil

# TODO: tabela de ranking com pd.read_html e comparação

```

## Parte B — Books to Scrape (site real de treino)

6. Escolha **uma categoria com pelo menos 2 páginas** (lista no enunciado da tarefa; ex.: *Mystery*, *Romance*, *Fantasy*, *Food and Drink*). Os links das categorias estão em `div.side_categories ul li ul li a` na página inicial.
7. Raspe **todos os livros da categoria**, seguindo `li.next a` até o fim e esperando 1 s entre as páginas. Para cada livro guarde: `titulo` (atributo `title`), `preco` (float, sem o £), `nota` (1 a 5, a partir da classe `star-rating`) e `link` **absoluto** (use `urljoin` — nas categorias o `href` começa com `../../../`).

```python
CATEGORIA = "Mystery"   # TODO: escolha a sua
NOTAS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

inicio = baixar("https://books.toscrape.com/index.html")
# TODO: encontrar o link da CATEGORIA na barra lateral

livros = []
# TODO: laço de paginação na categoria (li.next a), com time.sleep(1)

df_livros = pd.DataFrame(livros)
print(len(df_livros), "livros na categoria", CATEGORIA)
```

8. Calcule: total de livros, preço médio, distribuição das notas e os **3 livros mais bem avaliados** (desempate pelo **menor** preço).
9. Abra a página de detalhe de **um** desses livros e extraia a tabela `table.table-striped` em um dicionário.

```python
# TODO: estatísticas da categoria

# TODO: tabela da página de detalhe de um livro

```

## Parte C — Salvar e refletir

10. Salve em `dados_exercicio/`: as resenhas (CSV) e os livros da categoria (CSV + JSON com **proveniência**: fonte, URL, data da coleta).
11. Responda na célula Markdown abaixo (3 a 5 linhas): que cuidados éticos e legais você tomou (robots.txt, identificação, intervalo entre requisições, dados pessoais/LGPD)? O que mudaria se o site **não** permitisse a coleta?

```python
# TODO: salvar CSV/JSON

servidor.terminate()
```

**Reflexão ética (escreva aqui):**

...

