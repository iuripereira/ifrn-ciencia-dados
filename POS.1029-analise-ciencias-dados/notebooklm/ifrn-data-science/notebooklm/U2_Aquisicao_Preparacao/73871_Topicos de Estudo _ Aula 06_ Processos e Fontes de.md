# Tópicos de Estudo — Aula 06: Processos e Fontes de

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 06: Processos e Fontes de Dados

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 06: Processos e Fontes de Dados  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:22  |

## Índice

- 1. Capítulo 1 — De onde vêm os dados: um panorama das fontes
- 2. Capítulo 2 — Arquivos: a fonte mais simples (e onde ela falha)
- 3. Capítulo 3 — Bancos de dados: quando o dado mora em tabelas relacionadas
- 4. Capítulo 4 — APIs REST: dados sob demanda, com regras do dono do serviço
- 5. Capítulo 5 — Web scraping: o último recurso, com responsabilidade
- 6. Capítulo 6 — Formatos de dados, licença e proveniência

## 1. Capítulo 1 — De onde vêm os dados: um panorama das fontes

Toda análise de dados começa antes da primeira linha de código: alguém precisa decidir onde os dados moram e como trazê-los para dentro do ambiente de trabalho. Esta aula cobre as quatro famílias de fontes mais comuns e os formatos que elas costumam falar.

#### As quatro famílias de fontes

- Arquivos — CSV, Excel, JSON, Parquet, XML, texto simples. A fonte mais previsível: o dado já está "parado", você só precisa lê-lo.
- Bancos de dados — sistemas como PostgreSQL, MySQL, SQL Server. O dado vive em tabelas relacionadas, e você conversa com ele por meio de SQL.
- APIs REST — um servidor remoto expõe endpoints HTTP que devolvem dados (normalmente em JSON) sob demanda, muitas vezes em tempo real.
- Web scraping — quando não existe arquivo, banco nem API, e a única forma de obter o dado é extraí-lo do HTML de uma página feita para humanos lerem, não para máquinas.

#### Por que a ordem acima não é aleatória

Ela reflete o quanto de trabalho e risco cada fonte exige. Um arquivo bem formado é a situação mais simples: leitura direta, sem rede, sem autenticação, sem terceiros. Um banco de dados exige uma conexão e permissões, mas ainda fala uma linguagem estruturada e estável (SQL). Uma API REST depende de um serviço de terceiros estar no ar, respeitar limites de uso e não mudar seu contrato sem aviso. Web scraping é o último recurso: você depende da estrutura visual de uma página, que pode mudar a qualquer redesign, e entra em território mais delicado do ponto de vista legal e ético (Capítulo 5).

#### Um exemplo real: o cadastro de estabelecimentos de saúde

Ao longo desta aula, o mesmo caso guia os quatro capítulos seguintes: o CNES (Cadastro Nacional de Estabelecimentos de Saúde), mantido pelo Ministério da Saúde. Os mesmos estabelecimentos de saúde do Rio Grande do Norte aparecem de quatro formas — como arquivo JSON salvo em disco, como tabela dentro de um banco SQLite, como resposta de uma API REST pública e ao lado de uma tabela raspada da Wikipédia — para que fique concreto o que muda (e o que não muda) de uma fonte para outra.

#### O ciclo de vida de um dado adquirido

Não basta "puxar" o dado uma vez. Um processo de aquisição saudável responde a quatro perguntas, sempre por escrito:

- De onde veio? (endpoint, URL, nome do arquivo, banco e tabela — a proveniência, tema do Capítulo 6)
- Quando foi coletado? (dados mudam; uma amostra de hoje pode não valer amanhã)
- Sob que licença posso usá-lo? (Capítulo 6 — nem todo dado público é dado livre)
- O que fazer se a fonte mudar ou cair? (arquivos de cache, versionamento, tratamento de erro)

As próximas aulas da Unidade 2 (limpeza, tratamento de dados ausentes, validação) partem do princípio de que os dados já chegaram até você de forma íntegra e rastreável — esta aula é o que garante essa base.

## 2. Capítulo 2 — Arquivos: a fonte mais simples (e onde ela falha)

Um arquivo bem-comportado é a fonte de dados mais fácil de usar: `pd.read_csv`, `pd.read_excel`, `pd.read_json` e pronto. Mas "bem-comportado" é a exceção, não a regra — a Aula 04 já mostrou isso com o CSV de matrículas do IFRN, cujo separador (`;`), decimal (`,`) e encoding (`utf-8`) precisaram ser declarados explicitamente.

#### As perguntas que todo arquivo exige

- Qual o encoding? `utf-8` é o padrão atual, mas arquivos exportados de sistemas legados brasileiros costumam vir em `latin-1` (também chamado `iso-8859-1`). Abrir com o encoding errado não gera erro imediato — gera acentos corrompidos ("informação" virando "informaÃ§Ã£o"), um bug silencioso e traiçoeiro.
- Qual o separador e o decimal? Planilhas brasileiras costumam usar `;` como separador de coluna (porque a vírgula já é o separador decimal) — o oposto do padrão americano.
- A primeira linha é cabeçalho? Nem sempre. Alguns exports incluem linhas de metadados ou títulos de relatório antes da tabela de fato (resolvido com `skiprows`).
- O arquivo cabe na memória? Um CSV de 50 GB não pode simplesmente virar um DataFrame inteiro — entram em cena leitura em blocos (`chunksize`) ou formatos colunares como Parquet.

#### Arquivo como cache de outra fonte

Uma prática comum — e usada no exemplo desta aula — é salvar em arquivo o resultado de uma chamada de API ou de uma consulta a banco:

```
import json
with open("dados/cnes_rn_amostra.json", "w", encoding="utf-8") as f:
    json.dump(resposta_da_api, f, ensure_ascii=False, indent=1)
```

Isso transforma uma fonte instável e dependente de rede (API) em uma fonte estável e reproduzível (arquivo). O preço é que o arquivo é uma fotografia: se o cadastro do CNES mudar amanhã, o arquivo salvo hoje não vai refletir isso — por isso é essencial registrar a data da coleta junto com os dados (Capítulo 6).

#### Arquivos não são só "tabelas"

Um DataFrame é a abstração mais usada em ciência de dados, mas nem todo arquivo é tabular por natureza: um JSON aninhado (Capítulo 4), um XML com hierarquias profundas, ou um GeoJSON com polígonos de fronteiras territoriais (usado no mapa desta aula) exigem uma etapa de "achatamento" (flattening) antes de virarem linhas e colunas — por exemplo, com `pd.json_normalize`.

## 3. Capítulo 3 — Bancos de dados: quando o dado mora em tabelas relacionadas

Um banco de dados relacional guarda os dados em tabelas conectadas por chaves, e a forma de "puxar" dados dele não é um método de leitura de arquivo — é uma consulta SQL. A diferença central para arquivos e APIs: o banco pode processar, filtrar e juntar os dados antes de entregá-los, o que muitas vezes é bem mais eficiente do que trazer tudo para o Python e filtrar depois.

#### Conectando o Python a um banco

Cada banco tem seu driver (`psycopg2`/`psycopg` para PostgreSQL, `pymysql` para MySQL, `pyodbc` para SQL Server, o módulo `sqlite3` — da biblioteca padrão — para SQLite). O Pandas abstrai boa parte disso com duas funções:

```
import sqlite3
import pandas as pd

conexao = sqlite3.connect("dados/exemplo.db")
df = pd.read_sql("SELECT * FROM estabelecimentos WHERE municipio = 'Natal'", conexao)

df.to_sql("estabelecimentos", conexao, index=False, if_exists="replace")
```

`read_sql` traz o resultado de uma consulta como DataFrame; `to_sql` faz o caminho inverso, gravando um DataFrame como tabela. É assim que o exemplo prático desta aula cria uma mini base SQLite em memória a partir dos dados do CNES e roda uma consulta agrupando estabelecimentos por município e tipo — o mesmo `GROUP BY` que a Aula 05 fez em Pandas, agora escrito em SQL.

#### SQL ou Pandas — quem faz o quê?

- Filtros, agregações e junções simples podem ser feitos em qualquer um dos dois — a régua é onde o dado já está e o volume envolvido.
- Se a tabela tem 200 milhões de linhas no banco, filtrar dentro do banco com `WHERE` antes de trazer o resultado para o Python evita transportar dados que serão descartados.
- Depois que o resultado já é pequeno e está em memória, Pandas costuma ser mais produtivo para exploração, limpeza e visualização.

#### Uma API também pode ser "um banco disfarçado"

Muitos serviços expõem, por trás de uma API REST, o mesmo tipo de filtro que um banco ofereceria (`WHERE codigo_municipio = ...` vira um parâmetro de URL). A diferença é que você não controla o schema, não pode fazer `JOIN` livremente entre tabelas do provedor, e está sujeito às regras de uso do serviço — o próximo capítulo detalha essa fonte.

## 4. Capítulo 4 — APIs REST: dados sob demanda, com regras do dono do serviço

Uma API REST é um contrato: o provedor define endereços (endpoints), parâmetros aceitos e o formato de resposta (quase sempre JSON); você faz requisições HTTP e recebe dados de volta. A biblioteca `requests` é o padrão em Python para isso.

#### Anatomia de uma requisição

```
import requests

url = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos"
parametros = {"codigo_municipio": 240810, "limit": 20}
resposta = requests.get(url, params=parametros, timeout=10)
resposta.raise_for_status()
dados = resposta.json()
```

`params` vira a query string da URL (`?codigo_municipio=240810&limit=20`); `resposta.json()` converte o corpo da resposta (texto) em listas e dicionários Python; `raise_for_status()` levanta uma exceção se o servidor devolveu um código de erro (4xx ou 5xx) em vez/de sucesso (2xx).

#### Duas armadilhas reais, descobertas testando a API do CNES

- Parâmetros aceitos silenciosamente, mas ignorados. Tentar filtrar por `uf=RN` ou `codigo_uf=24` não gera erro — a API simplesmente devolve dados de qualquer estado, como se o filtro não existisse. Só o parâmetro correto (`codigo_municipio`, com o código IBGE de 6 dígitos) filtra de verdade. A lição: sempre inspecionar o retorno, nunca supor que um parâmetro "razoável" funcionou só porque não deu erro.
- Limite de página fixo pelo servidor. Pedir `limit=1000` devolve no máximo 20 registros — o servidor ignora limites maiores que o seu teto interno. Para reunir mais dados é preciso paginar, repetindo a chamada com `offset=20`, `offset=40`, e assim por diante, até a resposta vir vazia.

#### Autenticação e limites de uso (rate limiting)

A API usada nesta aula é pública e não exige chave de acesso — mas a maioria das APIs comerciais exige uma API key ou token OAuth, enviado em um cabeçalho HTTP (`headers={"Authorization": "Bearer ..."}`). Praticamente toda API pública impõe algum limite de requisições por minuto/hora (rate limit); ultrapassá-lo costuma devolver o código HTTP `429 Too Many Requests`. Um bom cliente de API trata isso com espera (backoff) e nova tentativa, em vez de martelar o servidor.

#### JSON aninhado precisa de "achatamento"

A resposta de uma API raramente já é uma tabela: é comum vir como uma lista de dicionários, às vezes com dicionários dentro de dicionários. `pd.json_normalize(dados["estabelecimentos"])` resolve o caso simples; estruturas mais profundas (como a API de municípios do IBGE, que aninha microrregião dentro de mesorregião dentro de UF) exigem escolher manualmente quais níveis "puxar" para colunas.

## 5. Capítulo 5 — Web scraping: o último recurso, com responsabilidade

Web scraping é extrair dados do HTML de uma página feita para ser lida por humanos, não consumida por máquinas. É a fonte mais frágil (qualquer redesign visual quebra o código) e a mais delicada do ponto de vista legal — por isso vem por último na lista, e só deve ser considerada quando não existe arquivo, banco ou API disponíveis.

#### Antes de escrever uma linha de código

- Existe uma API para os mesmos dados? Muitos sites que parecem exigir scraping têm uma API não documentada (visível na aba "Network" do navegador) ou uma API oficial — sempre vale procurar antes.
- O que diz o `robots.txt`? Todo site pode publicar em `/robots.txt` quais partes permite ou proíbe que robôs acessem. Não é uma barreira técnica, mas ignorá-lo é uma falta ética e, em alguns contextos, uma evidência de má-fé.
- O que dizem os Termos de Uso? Muitos sites proíbem explicitamente coleta automatizada, mesmo de páginas tecnicamente acessíveis. Termos de uso são um contrato — violá-los pode ter consequências, independentemente do robots.txt.
- Sob que licença está o conteúdo? Dado acessível não é dado livre para reuso (Capítulo 6).

#### Extraindo uma tabela com BeautifulSoup

```
from bs4 import BeautifulSoup
import requests

html = requests.get("https://pt.wikipedia.org/wiki/...").text
sopa = BeautifulSoup(html, "html.parser")

tabela = sopa.find("table", {"class": "wikitable"})
linhas = []
for tr in tabela.find_all("tr")[1:]:
    colunas = [td.get_text(strip=True) for td in tr.find_all("td")]
    if colunas:
        linhas.append(colunas)
```

`find` localiza o primeiro elemento que casa com o seletor (aqui, uma tabela com a classe `wikitable`); `find_all` devolve todos os elementos que casam — aqui, todas as linhas (`tr`). `get_text(strip=True)` extrai o texto visível de cada célula, descartando as tags HTML.

#### Por que a Wikipédia é um bom laboratório para praticar

A Wikipédia publica seu conteúdo sob licença Creative Commons Atribuição-CompartilhaIgual (CC BY-SA), permite expressamente reuso — inclusive automatizado, dentro de limites razoáveis — e documenta isso claramente. É um dos poucos casos em que scraping educacional está sobre uma base legal e ética confortável. Ainda assim, boas práticas seguem valendo: identificar o seu programa no cabeçalho HTTP (User-Agent), espaçar as requisições no tempo e nunca sobrecarregar o servidor.

#### Fragilidade estrutural

Diferente de uma API, cujo contrato de dados é (em teoria) estável, uma página HTML pode ser redesenhada sem aviso — uma classe CSS renomeada quebra o scraper inteiro. Por isso scraping deve ser tratado como uma fonte de último recurso e, quando usado, isolado em um módulo próprio, fácil de consertar quando (não se) a página mudar.

## 6. Capítulo 6 — Formatos de dados, licença e proveniência

Depois de decidir a fonte, resta decidir (ou descobrir) o formato — e entender sob quais regras aquele dado pode ser usado. Os dois assuntos parecem distantes, mas aparecem juntos na prática: o formato afeta o quão fácil é registrar a proveniência de um dado, e a licença determina o que você tem permissão de fazer com ele depois de convertê-lo.

#### CSV — simples, universal, sem metadados

Texto puro, uma linha por registro, colunas separadas por um caractere (vírgula, ponto e vírgula, tabulação). Vantagem: qualquer ferramenta lê. Desvantagem: não guarda tipos (tudo é texto até alguém decidir o contrário), nem estrutura hierárquica, nem metadados sobre a fonte.

#### JSON — estrutura e aninhamento, sem tipagem de colunas

O formato padrão das APIs REST modernas: objetos (`{}`), listas (`[]`), pares chave-valor, aninhamento arbitrário. Permite representar estruturas que um CSV não representa bem (um estabelecimento com uma lista de serviços especializados, por exemplo) — mas exige "achatamento" para virar uma tabela (Capítulo 4). É comum — e recomendável — usar um JSON para guardar não só os dados, mas também metadados de proveniência (fonte, endpoint, data da coleta, licença), como neste exemplo:

```
{
  "fonte": "Ministério da Saúde — API de Dados Abertos (CNES)",
  "endpoint": "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos",
  "data_coleta": "2026-09-28",
  "licenca": "Dados abertos governamentais (Lei 12.527/2011)",
  "registros": [ ... ]
}
```

#### XML — a estrutura mais verbosa

Antecessor do JSON como formato de troca de dados na web, ainda comum em sistemas legados, notas fiscais eletrônicas e alguns webservices governamentais brasileiros. Usa tags abrindo e fechando (`<municipio>Natal</municipio>`), o que o torna bem mais verboso que JSON para representar o mesmo dado — no exemplo desta aula, os mesmos 3 registros em XML ocupam proporcionalmente mais espaço do que em JSON.

#### Parquet — formato colunar, feito para grandes volumes

Diferente de CSV e JSON (orientados a linha), o Parquet guarda os dados por coluna e de forma binária comprimida. Resultado: arquivos bem menores (no exemplo desta aula, o mesmo conjunto de 160 estabelecimentos ocupa menos espaço em Parquet do que em CSV, e uma fração do tamanho do JSON com metadados) e leitura seletiva de colunas sem precisar ler o arquivo inteiro. É o formato preferido para grandes volumes de dados tabulares no ecossistema de ciência de dados (Spark, pandas com PyArrow, data lakes).

#### GeoJSON — um caso especial de JSON para dados geográficos

Usado no mapa desta aula (contorno do Rio Grande do Norte, obtido da API de Malhas do IBGE): um JSON com uma estrutura padronizada para representar pontos, linhas e polígonos geográficos, com coordenadas de longitude e latitude. É o formato de troca padrão entre ferramentas de mapas (QGIS, Leaflet, geopandas).

#### Licença: o que você pode fazer com o dado

- Dados públicos governamentais brasileiros (como o CNES e o IBGE, usados nesta aula) são regidos pela Lei de Acesso à Informação (Lei 12.527/2011) e por políticas de dados abertos — via de regra, uso livre, inclusive comercial, com boa prática de citar a fonte.
- Creative Commons (CC) — família de licenças usada por Wikipédia (CC BY-SA, usada nesta aula), bancos de imagens e alguns datasets acadêmicos. As variações importam: `BY` exige atribuição, `SA` (share-alike) exige que derivados usem a mesma licença, `NC` proíbe uso comercial, `ND` proíbe modificações.
- Termos de uso proprietários — comuns em APIs comerciais e redes sociais: podem proibir redistribuição, uso comercial, ou exigir que os dados sejam apagados após um prazo.
- Ausência de licença explícita não significa domínio público — na dúvida, o dado deve ser tratado como protegido por padrão.

#### Proveniência: a rastreabilidade que sustenta a confiança

Um dado sem proveniência registrada é, na prática, inutilizável para qualquer decisão séria: ninguém pode auditar, reproduzir ou saber se ainda é válido. Registrar proveniência custa poucas linhas (como no JSON acima) e paga dividendo toda vez que alguém — inclusive você, seis meses depois — precisar responder "de onde veio esse número?".