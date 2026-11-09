UNIDADE 2 — AQUISIÇÃO E PREPARAÇÃO DE DADOS

Aula 06

Processos e Fontes de Dados

Arquivos • Bancos de Dados • APIs REST • Web Scraping

Especialização em Ciência de Dados — IFRN  


Prof. Plácido Antônio de Souza Neto

ROTEIRO DA AULA

Agenda e objetivos

- Reconhecer as quatro famílias de fontes de dados e o custo/risco de cada uma
- Ler arquivos evitando armadilhas reais de encoding e separador decimal
- Conectar Python a bancos relacionais via SQL (sqlite3, pandas)
- Consumir APIs REST com requests e reconhecer armadilhas reais de filtro e paginação
- Fazer web scraping com responsabilidade (robots.txt, Termos de Uso)
- Comparar formatos de dados e registrar licença e proveniência

NESTA AULA

1

Panorama das 4 fontes

2

Arquivos

3

Bancos de dados

4

APIs REST

5

Web scraping

6

Formatos, licença e proveniência

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

2

PANORAMA

As quatro famílias de fontes de dados

1

2

3

4

Arquivos

Bancos de dados

APIs REST

Web scraping

CSV, Excel, JSON, Parquet, XML.

Dado "parado" — leitura direta,

sem rede, sem autenticação.

→

PostgreSQL, MySQL, SQLite…

Conexão + permissões, mas

fala SQL — estável e estruturado.

→

Endpoints HTTP sob demanda.

Depende de um serviço de

terceiros no ar, com limites.

→

Extrai HTML feito para humanos.

Último recurso: estrutura muda

e território legal é delicado.

Esforço/risco: baixo

Esforço/risco: moderado

Esforço/risco: alto

Esforço/risco: mais alto

A ordem não é aleatória: reflete o quanto de trabalho e risco cada fonte exige.

Estudo de caso desta aula — CNES: os mesmos estabelecimentos de saúde do Rio Grande do Norte aparecem nas quatro formas: arquivo JSON em disco, tabela em banco SQLite, resposta de API REST pública e tabela raspada da Wikipédia — para deixar concreto o que muda (e o que não muda) de uma fonte para outra.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

3

FONTE 1 DE 4

Arquivos: a fonte mais simples (e onde ela falha)

pd.read\_csv, pd.read\_excel, pd.read\_json… mas "bem-comportado" é a exceção, não a regra.

Arquivo como cache de outra fonte

Qual o encoding?

Salvar em arquivo o resultado de uma chamada de API transforma uma fonte instável (rede) em reproduzível — mas é uma fotografia: se a fonte mudar amanhã, o arquivo de hoje não reflete isso.

utf-8 é o padrão atual; sistemas legados brasileiros costumam salvar em latin-1 (iso-8859-1). Erro silencioso: "informação" vira "informaÃ§Ã£o".

Separador e decimal?

Planilhas brasileiras usam ; como separador de coluna, porque a vírgula já é o separador decimal — o oposto do padrão americano.

import json

with open("dados/cnes\_rn\_amostra.json",

          "w", encoding="utf-8") as f:

    json.dump(resposta\_da\_api, f,

              ensure\_ascii=False, indent=1)

A 1ª linha é cabeçalho?

Nem sempre — alguns exports trazem metadados antes da tabela (resolvido com skiprows).

Registre sempre a data da coleta junto com o arquivo salvo.

Cabe na memória?

Um CSV de 50 GB não vira DataFrame inteiro: leitura em blocos (chunksize) ou formato colunar (Parquet).

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

4

FONTE 2 DE 4

Bancos de dados: quando o dado mora em tabelas

- O dado vive em tabelas relacionadas; a forma de acessá-lo é uma consulta SQL, não um método de leitura de arquivo
- O banco filtra, agrega e junta os dados antes de entregá-los — muitas vezes mais eficiente que trazer tudo para o Python
- Cada banco tem seu driver: psycopg2 (PostgreSQL), pymysql (MySQL), pyodbc (SQL Server), sqlite3 (biblioteca padrão)

Python + SQLite (o exemplo desta aula)

import sqlite3

import pandas as pd

conexao = sqlite3.connect("dados/exemplo.db")

df = pd.read\_sql(

    "SELECT * FROM estabelecimentos "

    "WHERE municipio = 'Natal'", conexao)

df.to\_sql("estabelecimentos", conexao,

          index=False, if\_exists="replace")

SQL ou Pandas — quem faz o quê?

- Tabela com 200 milhões de linhas? Filtrar com WHERE dentro do banco evita transportar dados que serão descartados
- Resultado já pequeno e em memória? Pandas é mais produtivo para exploração, limpeza e visualização

read\_sql traz o resultado como DataFrame; to\_sql grava um DataFrame como tabela — o mesmo GROUP BY por município e tipo que a Aula 05 fez em Pandas, agora em SQL.

Uma API também pode ser "um banco disfarçado" — mas sem schema livre, sem JOIN, e sujeita às regras do provedor.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

5

FONTE 3 DE 4

APIs REST: dados sob demanda, com regras do dono

Um contrato: o provedor define endpoints, parâmetros aceitos e o formato de resposta (quase sempre JSON).

Anatomia de uma requisição

params  vira a query string da URL (?codigo\_municipio=...&amp;limit=20)

import requests

url = "https://apidadosabertos.saude.gov.br/"

      "cnes/estabelecimentos"

parametros = {"codigo\_municipio": 240810,

              "limit": 20}

resposta = requests.get(url,

               params=parametros, timeout=10)

resposta.raise\_for\_status()

dados = resposta.json()

.json()  converte o corpo da resposta em listas e dicionários Python

raise\_for\_status()  levanta exceção se o servidor devolveu erro 4xx/5xx

Autenticação e rate limiting

Esta API é pública e sem chave — a maioria exige API key/token OAuth (header Authorization: Bearer). Exceder o limite de requisições costuma devolver HTTP 429; um bom cliente espera e tenta de novo (backoff).

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

6

DESCOBERTA TESTANDO A API DO CNES

APIs REST: duas armadilhas reais

Nenhuma delas gera um erro — as duas exigem inspecionar o retorno com atenção.

1

Parâmetros aceitos, mas ignorados

2

Limite de página fixo pelo servidor

O que acontece  


Filtrar por uf=RN ou codigo\_uf=24 não gera erro — a API devolve dados de qualquer estado, como se o filtro não existisse.



Como resolver  


Só codigo\_municipio (código IBGE de 6 dígitos) filtra de verdade. Lição: sempre inspecionar o retorno, nunca supor que um parâmetro "razoável" funcionou só porque não deu erro.

O que acontece  


Pedir limit=1000 devolve no máximo 20 registros — o servidor ignora limites maiores que o seu teto interno.



Como resolver  


Solução: paginar repetindo a chamada com offset=20, offset=40… até a resposta vir vazia.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

7

FONTE 4 DE 4 — ÚLTIMO RECURSO

Web scraping: quando usar, com responsabilidade

Extrair dados do HTML de uma página feita para humanos lerem, não para máquinas.

BeautifulSoup: extraindo uma tabela

Antes de escrever uma linha de código

- Existe uma API para os mesmos dados? (aba Network do navegador, ou API oficial)
- O que diz o robots.txt do site?
- O que dizem os Termos de Uso? (violá-los tem consequências, mesmo sem violar o robots.txt)
- Sob que licença está o conteúdo? Acessível não é sinônimo de livre para reuso

from bs4 import BeautifulSoup

import requests

html = requests.get(url).text

sopa = BeautifulSoup(html, "html.parser")

tabela = sopa.find("table",

                    {"class": "wikitable"})

linhas = [

  [td.get\_text(strip=True)

   for td in tr.find\_all("td")]

  for tr in tabela.find\_all("tr")[1:]

]

Ética em campo: identifique seu programa no cabeçalho HTTP (User-Agent), espace as requisições no tempo e nunca sobrecarregue o servidor. A Wikipédia (usada nesta aula) publica sob CC BY-SA e permite reuso automatizado dentro de limites razoáveis — um dos poucos casos com base legal e ética confortável. Diferente de uma API, o HTML pode mudar sem aviso: isole o scraper em módulo próprio.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

8

DEPOIS DA FONTE, O FORMATO

Formatos de dados comparados

Mesmo conjunto de dados do CNES, gravado em formatos diferentes — tamanhos reais medidos nesta aula.

| Formato                  | Estrutura                                  | Base                      | Tamanho real         |
|--------------------------|--------------------------------------------|---------------------------|----------------------|
| Parquet                  | Colunar, binário, comprimido               | 160 registros             | 7.868 bytes  (menor) |
| CSV                      | Linhas, sem tipos nem metadados            | 160 registros             | 12.451 bytes         |
| JSON (bruto + metadados) | Objetos aninhados, chave-valor             | 160 registros             | 36.809 bytes         |
| XML                      | Tags de abertura/fechamento — mais verboso | 3 registros (ilustrativo) | 694 bytes            |

- Parquet vence por ser colunar e comprimido: menor arquivo e leitura seletiva de colunas, sem abrir o arquivo inteiro — por isso é o preferido para grandes volumes (Spark, PyArrow, data lakes).
- XML: 694 bytes para só 3 linhas (~231 bytes/registro) já é mais verboso que os 160 registros inteiros em CSV (~78 bytes/registro) — o custo das tags de abertura/fechamento.
- GeoJSON é um caso especial de JSON para dados geográficos (próximo slide).

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

9

UM CASO ESPECIAL DE JSON

GeoJSON e mapas

- JSON com estrutura padronizada para representar pontos, linhas e polígonos geográficos, com coordenadas de longitude e latitude
- Formato de troca padrão entre ferramentas de mapas: QGIS, Leaflet, geopandas
- Usado nesta aula: o contorno do Rio Grande do Norte, obtido da API de Malhas do IBGE
- Combinado com os pontos dos estabelecimentos do CNES, gera o mapa real da próxima página

polígono (contorno RN)

+ pontos (estabelecimentos)

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

10

ENTREGÁVEL DA AULA

O mapa real desta aula

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula06_Slides_Fontes_de_Dados_artifacts/image_000000_1a418c154bf4f50d226ecbf34aeb289eb32462ec5ad814e68e7a2680cbd6bcc6.png)

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula06_Slides_Fontes_de_Dados_artifacts/image_000001_1a418c154bf4f50d226ecbf34aeb289eb32462ec5ad814e68e7a2680cbd6bcc6.png)

Dados reais desta aula

- 160 estabelecimentos de saúde, 8 municípios
- 20 registros por município (limite fixo do servidor da API)
- Açu, Caicó, Ceará-Mirim, Currais Novos, Mossoró, Natal, Parnamirim, Pau dos Ferros

Fontes

Ministério da Saúde — API de Dados Abertos (CNES)  


apidadosabertos.saude.gov.br/cnes/estabelecimentos



IBGE — API de Malhas (contorno territorial do RN)



Coletado em 2026-09-28 · Licença: dados abertos governamentais (Lei 12.527/2011)

Estabelecimentos de saúde (CNES) em 8 municípios do RN, sobre o contorno territorial (IBGE)

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

11

SOB QUE REGRAS POSSO USAR O DADO?

Licença: o que você pode fazer com o dado

Lei de Acesso à Informação

Creative Commons (CC)

Termos proprietários

Dados públicos governamentais

Wikipédia usa CC BY-SA nesta aula

APIs comerciais, redes sociais

CNES e IBGE, usados nesta aula. Lei 12.527/2011 — via de regra, uso livre, inclusive comercial, com boa prática de citar a fonte.

BY exige atribuição · SA (share-alike) exige mesma licença nos derivados · NC proíbe uso comercial · ND proíbe modificações.

Podem proibir redistribuição e uso comercial, ou exigir que os dados sejam apagados após um prazo.

Ausência de licença explícita não significa domínio público — na dúvida, trate o dado como protegido por padrão.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

12

A RASTREABILIDADE QUE SUSTENTA A CONFIANÇA

Proveniência: registrar de onde veio o dado

- Um dado sem proveniência registrada é, na prática, inutilizável para qualquer decisão séria: ninguém pode auditar, reproduzir ou saber se ainda é válido
- Registrar proveniência custa poucas linhas e paga dividendos toda vez que alguém — inclusive você, seis meses depois — precisar responder "de onde veio esse número?"

Exemplo real desta aula: metadados junto dos dados

{

  "fonte": "Ministério da Saúde —

            API de Dados Abertos (CNES)",

  "endpoint": "apidadosabertos.saude.gov.br/

               cnes/estabelecimentos",

  "data\_coleta": "2026-09-28",

  "licenca": "Dados abertos governamentais

              (Lei 12.527/2011)",

  "registros": [ ... ]

}

As quatro perguntas de todo processo de aquisição

- De onde veio? (endpoint, URL, arquivo, banco e tabela)
- Quando foi coletado? (dados mudam; a amostra de hoje pode não valer amanhã)
- Sob que licença posso usá-lo?
- O que fazer se a fonte mudar ou cair? (cache, versionamento, tratamento de erro)

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

13

FECHANDO O RACIOCÍNIO

Checklist: qual fonte usar, quando?

1

Existe um arquivo pronto?

Use-o direto — CSV, Excel, JSON, Parquet. Confira encoding e separador antes de tudo.

↓

2

Não, mas há um banco acessível?

Conecte com o driver certo e filtre com SQL (WHERE) antes de trazer para o Python.

↓

3

Não, mas existe uma API?

Use requests + params. Teste se os filtros realmente funcionam e cuide da paginação.

↓

4

Nada disso?

Web scraping como último recurso: robots.txt, Termos de Uso, módulo isolado.

Sempre, em qualquer caso: registre fonte, data da coleta e licença.

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

14

DEPOIS DA AULA

Próximos passos

Exercício prático

Formulário avaliativo

- Aplique o pipeline de aquisição de dados a um caso à sua escolha
- Identifique a família de fonte mais adequada (arquivo, banco, API ou scraping)
- Leia os dados tratando encoding/separador (se arquivo) ou testando parâmetros e paginação (se API)
- Registre fonte, data da coleta e licença junto dos dados obtidos — entregue até 13/10/2026

10

questões objetivas

- Cobrem: encoding, paginação, parâmetros ignorados, checagens antes de scraping, formatos (CSV/JSON/XML/Parquet/GeoJSON), licenças CC e proveniência
- Prazo de envio: até 13/10/2026 (15 dias após esta aula)

Aula 06 — Processos e Fontes de Dados  |  Análise e Ciência de Dados — IFRN

15

Dúvidas?

Obrigado pela atenção — Aula 06: Processos e Fontes de Dados

Próxima aula

Unidade 2 continua com limpeza e tratamento de dados ausentes, partindo do princípio de que os dados já chegaram de forma íntegra e rastreável.

Prof. Plácido Antônio de Souza Neto  


placido.neto@ifrn.edu.br  


Especialização em Ciência de Dados — IFRN