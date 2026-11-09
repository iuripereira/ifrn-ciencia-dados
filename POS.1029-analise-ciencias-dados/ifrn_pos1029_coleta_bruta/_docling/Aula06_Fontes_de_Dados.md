INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE ESPECIALIZAÇÃO EM CIÊNCIA DE DADOS  ·  DISCIPLINA: ANÁLISE E CIÊNCIA DE DADOS

## Aula 06 - Processos e Fontes de Dados

Arquivos, bancos de dados, APIs REST e web scraping; formatos CSV/JSON/XML/Parquet/GeoJSON; licença e proveniência de dados

Unidade

Natureza Unidade 2 - Aquisição e Preparação de Dados (Aula 06, primeira aula)

Aula teórico-prática

Carga horária

4 h/a - 2 h de exposição guiada + 2 h de laboratório

Pré-

requisitos

Recursos

Avaliação Aulas 04-05 - DataFrames, leitura de CSV/Excel, groupby/agg/merge em Pandas Jupyter  Notebook/Lab, pandas , requests , beautifulsoup4 , sqlite3 (biblioteca padrão), pyarrow Exercício prático entregue no Moodle + formulário avaliativo (10 questões)

Professor Plácido Antônio de Souza Neto

## Objetivos de aprendizagem

Ao final desta aula, espera-se que o estudante seja capaz de:

1. Identificar e diferenciar as  quatro famílias de fontes de dados (arquivos, bancos de dados,  APIs  REST  e  web  scraping),  escolhendo  entre  elas  a  partir  do  que  está disponível e do risco envolvido em cada uma.
2. Ler  e  escrever dados  nos  formatos  CSV,  JSON,  XML  e  Parquet  com  Pandas, reconhecendo as vantagens e limitações de cada um.
3. Reconhecer o GeoJSON como um formato de dados geográficos e interpretar seu uso na construção de um mapa simples.
4. Consumir uma  API  REST  real  com  a  biblioteca requests ,  incluindo  o  envio  de parâmetros, a checagem de erros com raise\_for\_status() e  a  leitura  da  resposta  em JSON.
5. Implementar paginação de uma API que limita o tamanho de cada resposta, usando um parâmetro de deslocamento ( offset ).
6. Gravar  e  consultar dados  em  um  banco  SQLite  a  partir  do  Pandas,  com to\_sql , read\_sql e uma consulta SQL com GROUP BY .
7. Realizar web scraping responsável com BeautifulSoup, incluindo a verificação prévia de robots.txt e termos de uso.
8. Explicar a diferença entre licença e proveniência de um conjunto de dados, e registrar essas informações junto aos dados coletados.

## Sumário

## Parte I - Fundamentos teóricos

- 1.1 De onde vêm os dados: um panorama das fontes
- 1.2 Arquivos: a fonte mais simples (e onde ela falha)
- 1.3 Bancos de dados: quando o dado mora em tabelas relacionadas
- 1.4 APIs REST: dados sob demanda, com regras do dono do serviço
- 1.5 Web scraping: o último recurso, com responsabilidade
- 1.6 Formatos de dados, licença e proveniência

## Parte II - Tópicos de estudo dirigido (roteiro de leitura)

- Parte III - Laboratório guiado: estabelecimentos de saúde do RN (CNES)

Parte IV - Exercício prático avaliativo (entrega no Moodle)

Parte V - Formulário avaliativo (10 questões)

Apêndice A - Colinha de comandos

Apêndice B - Referências e leituras recomendadas

## SOBRE OS DADOS USADOS NESTA AULA

Diferente das Aulas 04 e 05, que usaram um conjunto sintético de  matrículas  do  IFRN gerado com semente fixa, esta aula usa dados reais de  fontes  públicas  do  governo  brasileiro:  o CNES (Cadastro  Nacional  de  Estabelecimentos  de  Saúde,  API  do  Ministério  da  Saúde),  o  contorno geográfico do Rio Grande do Norte (API de Malhas do IBGE) e uma pequena tabela raspada da Wikipédia.  Os  três  foram  coletados  ao  vivo  em 28/09/2026 e  salvos  em  disco  com  metadados completos de proveniência (fonte, endpoint, data da coleta, licença) ao lado dos dados. O contraste é  proposital:  depois  de  duas  aulas  manipulando  um  conjunto  artificial  e  controlado,  esta  aula mostra como os mesmos conceitos e ferramentas se comportam diante de dados de verdade - com suas imprecisões, limites de servidor e regras de uso que nenhum gerador sintético reproduz.

## Parte I - Fundamentos teóricos

Fontes de dados, formatos, licença e proveniência - a base de toda a Unidade 2

A Unidade 1 tratou os dados como algo que já estava pronto para uso - um CSV e um Excel entregues junto com o enunciado. A Unidade 2 começa um passo antes: de onde vêm os dados que chegam até esse CSV, como trazê-los de forma confiável e sob que condições eles podem ser usados. Esta aula cobre as quatro famílias de fontes mais comuns, os principais formatos  que  elas  falam  e  os  dois  temas  que  sustentam  qualquer  trabalho  sério  de aquisição de dados: licença e proveniência.

## 1.1 De onde vêm os dados: um panorama das fontes

Toda análise de dados começa antes da primeira linha de código: alguém precisa decidir onde os dados moram e como trazê-los para dentro do ambiente de trabalho.

## As quatro famílias de fontes

- Arquivos - CSV, Excel, JSON, Parquet, XML, texto simples. A fonte mais previsível: o dado já está "parado", você só precisa lê-lo.
- Bancos de dados - sistemas como PostgreSQL, MySQL, SQL Server. O dado vive em tabelas relacionadas, e você conversa com ele por meio de SQL.
- APIs  REST -  um  servidor  remoto  expõe  endpoints  HTTP  que  devolvem  dados (normalmente em JSON) sob demanda, muitas vezes em tempo real.
- Web scraping - quando não existe arquivo, banco nem API, e a única forma de obter o dado é extraí-lo do HTML de uma página feita para humanos lerem, não para máquinas.

## Por que a ordem acima não é aleatória

Ela reflete o quanto de trabalho e risco cada fonte exige. Um arquivo bem formado é a situação mais simples: leitura direta, sem rede, sem autenticação, sem terceiros. Um banco de dados exige uma conexão e permissões, mas ainda fala uma linguagem estruturada e estável  (SQL).  Uma  API  REST  depende  de  um  serviço  de  terceiros  estar  no  ar,  respeitar limites de uso e não mudar seu contrato sem aviso. Web scraping é o último recurso: você depende da estrutura visual de uma página, que pode mudar a qualquer redesign, e entra em território mais delicado do ponto de vista legal e ético (Capítulo 5).

## Um exemplo real: o cadastro de estabelecimentos de saúde

Ao longo desta aula, o mesmo caso guia os quatro capítulos seguintes: o CNES (Cadastro Nacional  de  Estabelecimentos  de  Saúde),  mantido  pelo  Ministério  da  Saúde.  Os  mesmos estabelecimentos de saúde do Rio Grande do Norte aparecem de quatro formas - como arquivo JSON salvo em disco, como tabela dentro de um banco SQLite, como resposta de uma API REST pública e ao lado de uma tabela raspada da Wikipédia - para que fique concreto o que muda (e o que não muda) de uma fonte para outra.

## O ciclo de vida de um dado adquirido

Não basta "puxar" o dado uma vez. Um processo de aquisição saudável responde a quatro perguntas, sempre por escrito:

- De onde veio? (endpoint, URL, nome do arquivo, banco e tabela - a proveniência , tema do Capítulo 6)
- Quando foi coletado? (dados mudam; uma amostra de hoje pode não valer amanhã)
- Sob que licença posso usá-lo? (Capítulo 6 - nem todo dado público é dado livre)
- O que fazer se a fonte mudar ou cair? (arquivos de cache, versionamento, tratamento de erro)

As próximas aulas da Unidade 2 (limpeza, tratamento de dados ausentes, validação) partem do princípio de que os dados já chegaram até você de forma íntegra e rastreável - esta aula é o que garante essa base.

## 1.2 Arquivos: a fonte mais simples (e onde ela falha)

Um  arquivo  bem-comportado  é  a  fonte  de  dados  mais  fácil  de  usar: pd.read\_csv , pd.read\_excel , pd.read\_json e pronto. Mas "bem-comportado" é a exceção, não a regra - a Aula 04 já mostrou isso com o CSV de matrículas do IFRN, cujo separador ( ; ), decimal ( , ) e encoding ( utf-8 ) precisaram ser declarados explicitamente.

## As perguntas que todo arquivo exige

- Qual  o  encoding? utf-8 é  o  padrão  atual,  mas  arquivos  exportados  de  sistemas legados brasileiros costumam vir em latin-1 (também chamado iso-8859-1 ). Abrir com o  encoding  errado  não  gera  erro  imediato  -  gera  acentos  corrompidos  ("informação" virando "informaÃ§Ã£o"), um bug silencioso e traiçoeiro.
- Qual o separador e o decimal? Planilhas brasileiras costumam usar ; como separador de coluna (porque a vírgula já é o separador decimal) - o oposto do padrão americano.
- A  primeira  linha  é  cabeçalho? Nem  sempre.  Alguns  exports  incluem  linhas  de metadados ou títulos de relatório antes da tabela de fato (resolvido com skiprows ).
- O  arquivo  cabe  na  memória? Um  CSV  de  50  GB  não  pode  simplesmente  virar  um DataFrame  inteiro  -  entram  em  cena  leitura  em  blocos  ( chunksize )  ou  formatos colunares como Parquet.

## Arquivo como cache de outra fonte

Uma prática comum - e usada no exemplo desta aula - é salvar em arquivo o resultado de uma chamada de API ou de uma consulta a banco:

```
import json with open("dados/cnes_rn_amostra.json", "w", encoding="utf-8") as f: json.dump(resposta_da_api, f, ensure_ascii=False, indent=1)
```

Isso  transforma  uma  fonte  instável  e  dependente  de  rede  (API)  em  uma  fonte  estável  e reproduzível (arquivo). O preço é que o arquivo é uma fotografia : se o cadastro do CNES

mudar amanhã, o arquivo salvo hoje não vai refletir isso - por isso é essencial registrar a data da coleta junto com os dados (Capítulo 6).

## Arquivos não são só "tabelas"

Um DataFrame é a abstração mais usada em ciência de dados, mas nem todo arquivo é tabular por natureza: um JSON aninhado (Capítulo 4), um XML com hierarquias profundas, ou um GeoJSON com polígonos de fronteiras territoriais (usado no mapa desta aula) exigem uma etapa de "achatamento" (fl attening ) antes de virarem linhas e colunas - por exemplo, com pd.json\_normalize .

## 1.3 Bancos de dados: quando o dado mora em tabelas relacionadas

Um banco  de  dados  relacional  guarda  os  dados  em  tabelas  conectadas  por  chaves,  e  a forma de "puxar" dados dele não é um método de leitura de arquivo - é uma consulta SQL .  A diferença central para arquivos e APIs: o banco pode processar, filtrar e juntar os dados antes de  entregá-los,  o  que  muitas  vezes  é  bem  mais  eficiente  do  que  trazer  tudo para o Python e filtrar depois.

## Conectando o Python a um banco

Cada  banco  tem  seu  driver  ( psycopg2 / psycopg para  PostgreSQL, pymysql para  MySQL, pyodbc para  SQL  Server,  o  módulo sqlite3 -  da  biblioteca  padrão  -  para  SQLite).  O Pandas abstrai boa parte disso com duas funções:

```
import sqlite3 import pandas as pd conexao = sqlite3.connect("dados/exemplo.db") df = pd.read_sql("SELECT * FROM estabelecimentos WHERE municipio = 'Natal'", conexao) df.to_sql("estabelecimentos", conexao, index=False, if_exists="replace")
```

read\_sql traz o resultado de uma consulta como DataFrame; to\_sql faz o caminho inverso, gravando um DataFrame como tabela. É assim que o exemplo prático desta aula cria uma mini base SQLite em memória a partir dos dados do CNES e roda uma consulta agrupando estabelecimentos por município e tipo - o mesmo GROUP BY que a Aula 05 fez em Pandas, agora escrito em SQL.

## SQL ou Pandas - quem faz o quê?

- Filtros,  agregações  e  junções  simples  podem  ser  feitos  em  qualquer  um  dos  dois  -  a régua é onde o dado já está e o volume envolvido.
- Se a tabela tem 200 milhões de linhas no banco, filtrar dentro do banco com WHERE antes de trazer o resultado para o Python evita transportar dados que serão descartados.
- Depois  que  o  resultado  já  é  pequeno  e  está  em  memória,  Pandas  costuma  ser  mais produtivo para exploração, limpeza e visualização.

## Uma API também pode ser "um banco disfarçado"

Muitos serviços expõem, por trás de uma API REST, o mesmo tipo de filtro que um banco ofereceria ( WHERE codigo\_municipio = ... vira  um  parâmetro  de  URL).  A  diferença  é  que você não controla o schema, não pode fazer JOIN livremente entre tabelas do provedor, e está sujeito às regras de uso do serviço - o próximo capítulo detalha essa fonte.

## 1.4 APIs REST: dados sob demanda, com regras do dono do serviço

Uma API REST é um contrato: o provedor define endereços (endpoints), parâmetros aceitos e o formato de resposta (quase sempre JSON); você faz requisições HTTP e recebe dados de volta. A biblioteca requests é o padrão em Python para isso.

## Anatomia de uma requisição

```
import requests url = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos" parametros = {"codigo_municipio": 240810, "limit": 20} resposta = requests.get(url, params=parametros, timeout=10) resposta.raise_for_status() dados = resposta.json()
```

params vira  a query  string da  URL  ( ?codigo\_municipio=240810&amp;limit=20 ); resposta.json() converte  o  corpo  da  resposta  (texto)  em  listas  e  dicionários  Python; raise\_for\_status() levanta  uma  exceção  se  o  servidor  devolveu  um  código  de  erro  (4xx  ou  5xx)  em  vez  de sucesso (2xx).

## Duas armadilhas reais, descobertas testando a API do CNES

- Parâmetros  aceitos  silenciosamente,  mas  ignorados. Tentar  filtrar  por uf=RN ou codigo\_uf=24 não  gera  erro  -  a  API  simplesmente  devolve  dados  de  qualquer  estado, como se o filtro não existisse. Só o parâmetro correto ( codigo\_municipio ,  com o código IBGE de 6 dígitos)  filtra  de  verdade.  A  lição: sempre inspecionar o retorno ,  nunca supor que um parâmetro "razoável" funcionou só porque não deu erro.
- Limite de página fixo pelo servidor. Pedir limit=1000 devolve no máximo 20 registros - o servidor ignora limites  maiores  que  o  seu  teto  interno.  Para  reunir  mais  dados  é preciso paginar ,  repetindo a chamada com offset=20 , offset=40 ,  e  assim  por  diante, até a resposta vir vazia.

## Autenticação e limites de uso (rate limiting)

A API usada nesta aula é pública e não exige chave de acesso - mas a maioria das APIs comerciais exige uma API key ou token OAuth, enviado em um cabeçalho HTTP ( headers= {"Authorization":  "Bearer  ..."} ).  Praticamente  toda  API  pública  impõe  algum  limite  de requisições por minuto/hora ( rate limit ); ultrapassá-lo costuma devolver o código HTTP 429 Too Many Requests . Um bom cliente de API trata isso com espera ( backoff ) e nova tentativa, em vez de martelar o servidor.

## JSON aninhado precisa de "achatamento"

A  resposta  de  uma  API  raramente  já  é  uma  tabela:  é  comum  vir  como  uma  lista  de dicionários, às vezes com dicionários dentro de dicionários. pd.json\_normalize(dados["estabelecimentos"]) resolve o caso simples; estruturas  mais profundas  (como  a  API  de  municípios  do  IBGE,  que  aninha  microrregião  dentro  de mesorregião  dentro  de  UF)  exigem  escolher  manualmente  quais  níveis  "puxar"  para colunas.

## AS DUAS ARMADILHAS DA API DO CNES, EM RESUMO

(1) Parâmetros com nome plausível ( uf , codigo\_uf ) são aceitos sem erro HTTP e silenciosamente  ignorados -  só  o  parâmetro  correto  ( codigo\_municipio )  filtra  de  verdade,  e isso só se descobre inspecionando o conteúdo da resposta. (2) O servidor ignora um limit maior que 20: pedir limit=1000 continua devolvendo, no máximo, 20 registros por chamada. Para coletar os 160 estabelecimentos desta aula (20 por município × 8 municípios) foi necessário paginar com offset , uma chamada por município. Nenhuma das duas armadilhas está documentada de forma óbvia - ambas só apareceram testando a API e comparando o que foi pedido com o que voltou.

## 1.5 Web scraping: o último recurso, com responsabilidade

Web scraping é extrair dados do HTML de uma página feita para ser lida por humanos, não consumida por máquinas. É a fonte mais frágil (qualquer redesign visual quebra o código) e a mais delicada do ponto de vista legal - por isso vem por último na lista, e só deve ser considerada quando não existe arquivo, banco ou API disponíveis.

## Antes de escrever uma linha de código

- Existe  uma API para os mesmos dados? Muitos  sites  que  parecem  exigir  scraping têm  uma  API  não  documentada  (visível  na  aba  "Network"  do  navegador)  ou  uma  API oficial - sempre vale procurar antes.
- O que diz o robots.txt ? Todo site pode publicar em /robots.txt quais partes permite ou  proíbe  que  robôs  acessem.  Não  é  uma  barreira  técnica,  mas  ignorá-lo  é  uma  falta ética e, em alguns contextos, uma evidência de má-fé.
- O  que  dizem  os  Termos  de  Uso? Muitos  sites  proíbem  explicitamente  coleta automatizada,  mesmo  de  páginas  tecnicamente  acessíveis.  Termos  de  uso  são  um contrato - violá-los pode ter consequências, independentemente do robots.txt.
- Sob  que  licença  está  o  conteúdo? Dado  acessível  não  é  dado  livre  para  reuso (Capítulo 6).

## Extraindo uma tabela com BeautifulSoup

```
from bs4 import BeautifulSoup import requests html = requests.get("https://pt.wikipedia.org/wiki/...").text sopa = BeautifulSoup(html, "html.parser") tabela = sopa.find("table", {"class": "wikitable"}) linhas = [] for tr in tabela.find_all("tr")[1:]: colunas = [td.get_text(strip=True) for td in tr.find_all("td")] if colunas: linhas.append(colunas)
```

find localiza o primeiro elemento que casa com o seletor (aqui, uma tabela com a classe wikitable ); find\_all devolve todos os elementos que casam - aqui, todas as linhas ( tr ). get\_text(strip=True) extrai  o  texto  visível  de  cada  célula,  descartando  as  tags  HTML.  O [1:] pula a primeira linha, que costuma ser o cabeçalho da tabela, não um dado.

## Por que a Wikipédia é um bom laboratório para praticar

A Wikipédia publica seu conteúdo sob licença Creative Commons AtribuiçãoCompartilhaIgual  (CC  BY-SA),  permite  expressamente  reuso  -  inclusive  automatizado, dentro de limites razoáveis - e documenta isso claramente. É um dos poucos casos em que scraping  educacional  está  sobre  uma  base  legal  e  ética  confortável.  Ainda  assim,  boas práticas  seguem  valendo:  identificar  o  seu  programa  no  cabeçalho  HTTP  ( User-Agent ), espaçar as requisições no tempo e nunca sobrecarregar o servidor.

## Fragilidade estrutural

Diferente de uma API, cujo contrato de dados é (em teoria) estável, uma página HTML pode ser redesenhada sem aviso - uma classe CSS renomeada quebra o scraper inteiro. Por isso scraping deve ser tratado como uma fonte de último recurso e, quando usado, isolado em um módulo próprio, fácil de consertar quando (não se) a página mudar.

## 1.6 Formatos de dados, licença e proveniência

Depois de decidir a fonte, resta decidir (ou descobrir) o formato - e entender sob quais regras  aquele  dado  pode  ser  usado.  Os  dois  assuntos  parecem  distantes,  mas  aparecem juntos na prática: o formato afeta o quão fácil é registrar a proveniência de um dado, e a licença determina o que você tem permissão de fazer com ele depois de convertê-lo.

## CSV - simples, universal, sem metadados

Texto puro, uma linha por registro, colunas separadas por um caractere (vírgula, ponto e vírgula,  tabulação).  Vantagem:  qualquer  ferramenta  lê.  Desvantagem:  não  guarda  tipos (tudo é texto até alguém decidir o contrário), nem estrutura hierárquica, nem metadados sobre a fonte.

## JSON - estrutura e aninhamento, sem tipagem de colunas

O formato padrão das APIs REST modernas: objetos ( {} ),  listas  ( [] ),  pares  chave-valor, aninhamento arbitrário. Permite representar estruturas que um CSV não representa bem (um estabelecimento com uma lista de serviços especializados, por exemplo) - mas exige "achatamento" para virar uma tabela (Capítulo 4). É comum - e recomendável - usar um JSON  para  guardar  não  só  os  dados,  mas  também  metadados  de  proveniência  (fonte, endpoint, data da coleta, licença), como neste exemplo:

```
{ "fonte": "Ministério da Saúde - API de Dados Abertos (CNES)", "endpoint": "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos", "data_coleta": "2026-09-28", "licenca": "Dados abertos governamentais (Lei 12.527/2011)", "registros": [ ... ] }
```

## XML - a estrutura mais verbosa

Antecessor do JSON como formato de troca de dados na web, ainda comum em sistemas legados,  notas  fiscais  eletrônicas  e  alguns  webservices  governamentais  brasileiros.  Usa tags abrindo e fechando ( &lt;municipio&gt;Natal&lt;/municipio&gt; ),  o  que  o  torna  bem  mais  verboso que JSON para representar o mesmo dado - no exemplo desta aula, os mesmos 3 registros em XML ocupam proporcionalmente mais espaço do que em JSON.

## Parquet - formato colunar, feito para grandes volumes

Diferente de CSV e JSON (orientados a linha), o Parquet guarda os dados por coluna e de forma  binária  comprimida.  Resultado:  arquivos  bem  menores  (no  exemplo  desta  aula,  o mesmo conjunto de 160 estabelecimentos ocupa menos espaço em Parquet do que em CSV, e  uma  fração  do  tamanho  do  JSON  com  metadados)  e  leitura  seletiva  de  colunas  sem precisar  ler  o  arquivo  inteiro.  É  o  formato  preferido  para  grandes  volumes  de  dados tabulares no ecossistema de ciência de dados (Spark, pandas com PyArrow, data lakes).

## GeoJSON - um caso especial de JSON para dados geográficos

Usado no mapa desta aula (contorno do Rio Grande do Norte, obtido da API de Malhas do IBGE):  um  JSON  com  uma  estrutura  padronizada  para  representar  pontos,  linhas  e polígonos  geográficos,  com  coordenadas  de  longitude  e  latitude.  É  o  formato  de  troca padrão entre ferramentas de mapas (QGIS, Leaflet, geopandas).

## Licença: o que você pode fazer com o dado

- Dados públicos governamentais brasileiros (como o CNES e o IBGE, usados nesta aula) são regidos pela Lei de Acesso à Informação (Lei 12.527/2011) e por políticas de dados abertos - via de regra, uso livre, inclusive comercial, com boa prática de citar a fonte.
- Creative Commons (CC) - família de licenças usada por Wikipédia (CC BY-SA, usada nesta aula), bancos de imagens e alguns datasets acadêmicos. As variações importam: BY exige  atribuição, SA ( share-alike )  exige  que  derivados  usem  a  mesma licença, NC proíbe uso comercial, ND proíbe modificações.

- Termos de uso proprietários -  comuns  em  APIs  comerciais  e  redes  sociais:  podem proibir  redistribuição,  uso  comercial,  ou  exigir  que  os  dados  sejam  apagados  após  um prazo.
- Ausência de licença explícita não significa domínio público - na dúvida, o dado deve ser tratado como protegido por padrão.

## Proveniência: a rastreabilidade que sustenta a confiança

Um  dado  sem  proveniência  registrada  é,  na  prática,  inutilizável  para  qualquer  decisão séria: ninguém pode auditar, reproduzir ou saber se ainda é válido. Registrar proveniência custa  poucas  linhas  (como  no  JSON  acima)  e  paga  dividendos  toda  vez  que  alguém  - inclusive você, seis meses depois - precisar responder "de onde veio esse número?".

## LICENÇA NÃO É O MESMO QUE PROVENIÊNCIA

Licença responde "o que eu posso fazer com este dado?" (usar, redistribuir, modificar, cobrar por ele). Proveniência responde  "de  onde  este  dado  veio,  quando  e  como?"  (fonte,  endpoint  ou consulta, data da coleta, versão). São perguntas independentes: um dado pode ter licença livre e proveniência nenhuma  registrada (e então ninguém  consegue  auditá-lo), ou proveniência impecável e licença nenhuma esclarecida (e então ninguém sabe se pode usá-lo). Um processo de aquisição de dados maduro registra as duas coisas, sempre, no mesmo lugar.

## Parte II - Tópicos de estudo dirigido

Roteiro de leitura individual, correspondente ao livro "T ópicos de Estudo - Aula 06" no Moodle

O livro da Aula 06 no AVA reproduz, capítulo a capítulo, o conteúdo da Parte I acima, com exercícios curtos de fixação ao final de cada um. Não é leitura nova: é a mesma Parte I, em formato de estudo dirigido, para revisar antes do laboratório e do formulário avaliativo.

|   Cap. | Domine                                                                                                                              | Erro frequente a evitar                                                                                                    |
|--------|-------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
|      1 | As quatro famílias de fontes e por que a ordem arquivo → banco → API → scraping reflete risco crescente.                            | Escolher web scraping por familiaridade, sem checar antes se existe API ou arquivo para o mesmo dado.                      |
|      2 | As quatro perguntas de todo arquivo (encoding, separador/decimal, cabeçalho, tamanho) e o uso de arquivo como cache de outra fonte. | Ler um arquivo sem declarar o encoding, confiando no padrão da biblioteca.                                                 |
|      3 | read_sql / to_sql ; quando filtrar dentro do banco (SQL) em vez de trazer tudo para o Pandas.                                       | Trazer uma tabela inteira para o Python só para filtrar depois, quando um WHERE resolveria com muito menos dado trafegado. |
|      4 | Anatomia de uma requisição com requests ; paginação com offset ; parâmetros ignorados silenciosamente.                              | Supor que um parâmetro "funcionou" só porque a chamada não deu erro HTTP.                                                  |
|      5 | Checklist antes de raspar (API existente, robots.txt , termos de uso); BeautifulSoup.find / find_all .                              | Tratar "tecnicamente acessível" como sinônimo de "permitido coletar".                                                      |
|      6 | Diferenças entre CSV, JSON, XML, Parquet e GeoJSON; a distinção entre licença e proveniência.                                       | Confundir "dado público" com "dado sem restrição de uso" - ausência de licença explícita não é domínio público.            |

## AUTOAVALIAÇÃO RÁPIDA

Você está pronto para o laboratório quando conseguir, de memória, (1) listar as quatro famílias de fontes em ordem de risco crescente, (2) escrever uma chamada requests.get com parâmetros e checagem de erro, (3) explicar como paginar uma API que limita o tamanho da resposta, (4) gravar um  DataFrame  em  SQLite  e  consultá-lo  com  SQL,  e  (5)  apontar  a  diferença  entre  licença  e proveniência de um conjunto de dados.

| Fonte          |              | Quando usar                                                                                                 | Risco principal                                                                                                |
|----------------|--------------|-------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Arquivo JSON…) | (CSV, Excel, | O dado já foi extraído entregue como arquivo - situação mais comum exercícios e boa parte do trabalho real. | e a em Encoding, separador e cabeçalho declarados errado; arquivo desatualizado sem data de coleta registrada. |
| Banco de dados |              | O dado vive em um sistema relacional ao qual você tem acesso direto (interno à organização, por exemplo).   | Trazer volume desnecessário para o Python em vez de filtrar com SQL.                                           |
| API REST       |              | Um provedor externo expõe os dados via HTTP, sob demanda, possivelmente em tempo real.                      | Parâmetros ignorados silenciosamente; limites de página e de taxa (rate limit); contrato pode mudar sem aviso. |
| Web scraping   |              | Último recurso: não existe arquivo, banco nem API para o mesmo dado.                                        | Estrutura frágil (quebra a qualquer redesign); questões legais/éticas (robots.txt, termos de uso).             |

| Formato   | Natureza                                         | Quando usar                                                                              |
|-----------|--------------------------------------------------|------------------------------------------------------------------------------------------|
| CSV       | Texto, tabular, sem metadados                    | Troca simples entre ferramentas; quando não há estrutura aninhada a preservar.           |
| JSON      | Texto, aninhado, sem tipagem de coluna           | Resposta de APIs; quando é preciso guardar metadados de proveniência junto com os dados. |
| XML       | Texto, aninhado, tags abrindo/fechando (verboso) | Integração com sistemas legados e alguns webservices governamentais brasileiros.         |
| Parquet   | Binário, colunar, comprimido                     | Grandes volumes de dados tabulares; quando desempenho de leitura importa.                |
| GeoJSON   | JSON com estrutura padronizada para geometria    | Pontos, linhas e polígonos geográficos; troca com ferramentas de mapas.                  |

## Parte III - Laboratório guiado

Estabelecimentos de saúde do Rio Grande do Norte (CNES) - dados reais, coletados em 28/09/2026 - todas as saídas abaixo foram produzidas pelo código apresentado

O script completo está em exemplo\_fontes\_dados.py , disponível no AVA. Os arquivos que ele lê e produz ficam na pasta dados/ : o snapshot da API ( cnes\_rn\_amostra.json ), o contorno do RN em GeoJSON ( rn\_contorno.json ) e o HTML salvo da Wikipédia ( wikipedia\_municipios\_rn.html ).  A  chamada HTTP real à API do CNES está comentada no início do script - os dados já foram coletados ao vivo em 28/09/2026 e salvos em dados/ , prontos para uso sem depender de rede durante a aula.

## Passo 1 - Carregando o snapshot da API (fonte: arquivo)

```
with open(DADOS / "cnes_rn_amostra.json", encoding="utf-8") as f: payload = json.load(f) print(f"  fonte      : {payload['fonte']}") print(f"  endpoint   : {payload['endpoint']}") print(f"  coletado em: {payload['data_coleta']}") print(f"  licença    : {payload['licenca']}") print(f"  observação : {payload['observacao']}") df = pd.DataFrame(payload["registros"]) print(f"\n  {df.shape[0]} estabelecimentos, {df['municipio'].nunique()} municípios") print(df.groupby("municipio").size().sort_values(ascending=False))
```

```
fonte      : Ministério da Saúde - DEMAS API de Dados Abertos (CNES) endpoint   : https://apidadosabertos.saude.gov.br/cnes/estabelecimentos coletado em: 2026-09-28 licença    : Dados abertos governamentais (Lei de Acesso à Informação, Lei 12.527/2011) - uso livre com citação da fonte observação : Amostra: 20 primeiros estabelecimentos retornados pela API para cada um dos 8 municípios (limite fixo do servidor, ignora limit>20). Não é o total de estabelecimentos do CNES no município. 160 estabelecimentos, 8 municípios municipio Acu             20 Caico           20 CearaMirim      20 CurraisNovos    20 Mossoro         20 Natal           20 Parnamirim      20 PauDosFerros    20 dtype: int64
```

Os  160  registros  (20  ×  8  municípios)  são  exatamente  o  efeito  da  paginação  descrita  no Capítulo 4: cada município exigiu uma chamada separada à API, já que limit não passa de 20 por chamada. A observação salva no próprio JSON deixa isso explícito - não é o total de estabelecimentos de cada município, é uma amostra limitada pelo servidor.

## Passo 2 - Banco de dados: gravando em SQLite e consultando com SQL

```
con = sqlite3.connect(":memory:") df.to_sql("estabelecimentos", con, index=False, if_exists="replace") consulta = """ SELECT municipio, descricao_tipo_unidade, COUNT(*) AS n FROM estabelecimentos WHERE descricao_tipo_unidade IN ('HOSPITAL GERAL', 'CENTRO DE SAUDE/UNIDADE BASICA') GROUP BY municipio, descricao_tipo_unidade ORDER BY n DESC """ resultado_sql = pd.read_sql(consulta, con) print(resultado_sql.to_string(index=False)) con.close()
```

```
municipio         descricao_tipo_unidade  n CearaMirim CENTRO DE SAUDE/UNIDADE BASICA  6 Parnamirim CENTRO DE SAUDE/UNIDADE BASICA  5 CurraisNovos CENTRO DE SAUDE/UNIDADE BASICA  2 Acu CENTRO DE SAUDE/UNIDADE BASICA  1 Mossoro CENTRO DE SAUDE/UNIDADE BASICA  1 PauDosFerros                 HOSPITAL GERAL  1
```

to\_sql gravou o DataFrame como tabela em um banco SQLite em memória ( :memory: ); a seguir, read\_sql devolveu  o  resultado  de  uma  consulta  SQL  comum  como  um  novo DataFrame - o mesmo padrão de groupby +  contagem  da  Aula  05,  agora  expresso  em GROUP BY .

## Passo 3 - Web scraping: extraindo uma tabela HTML com BeautifulSoup

```
from bs4 import BeautifulSoup with open(DADOS / "wikipedia_municipios_rn.html", encoding="utf-8") as f: soup = BeautifulSoup(f.read(), "html.parser") linhas = [] tabela = soup.find("table") for tr in tabela.find_all("tr")[1:]: cols = [td.get_text(strip=True) for td in tr.find_all("td")] if cols: linhas.append({"municipio": cols[1], "codigo_ibge": cols[2]}) df_scraping = pd.DataFrame(linhas) print(df_scraping.to_string(index=False))
```

```
municipio codigo_ibge Acari     2400109 Afonso Bezerra     2400307 Água Nova     2400406 Alexandria     2400505 Almino Afonso     2400604 Alto do Rodrigues     2400703 Licença da fonte: CC BY-SA 4.0 (Wikipédia) - uso permitido, exige atribuição Antes de raspar um site: checar robots.txt e os termos de uso.
```

O  HTML  salvo  em dados/wikipedia\_municipios\_rn.html é  um  trecho  reduzido  (6  das centenas de linhas da tabela real da Wikipédia), coletado em 28/09/2026 e mantido local para que o exemplo rode sem depender de rede durante a aula - o código de scraping é idêntico ao que rodaria contra a página ao vivo.

## Passo 4 - O mesmo conjunto em diferentes formatos

```
df.to_csv(DADOS / "cnes_rn_amostra.csv", index=False, sep=";", decimal=",", encoding="utf8") df.to_parquet(DADOS / "cnes_rn_amostra.parquet", index=False) # XML manual (mostra a estrutura verbosa e aninhada, típica de XML) root = ET.Element("estabelecimentos") for _, row in df.head(3).iterrows(): el = ET.SubElement(root, "estabelecimento") for campo in ["municipio", "descricao_tipo_unidade", "latitude", "longitude"]: sub = ET.SubElement(el, campo) sub.text = str(row[campo]) ET.ElementTree(root).write(DADOS / "cnes_amostra_3linhas.xml", encoding="utf-8", xml_declaration=True)
```

```
CSV     : 12451 bytes Parquet : 7868 bytes XML (3 linhas, ilustrativo): 694 bytes Comparação de tamanho (mesmos 160 registros, formatos diferentes): Parquet                             7868 bytes CSV                                12451 bytes JSON (bruto, com metadados)        36809 bytes
```

Os mesmos 160 estabelecimentos ocupam 7.868 bytes em Parquet contra 12.451 bytes em CSV e 36.809 bytes em JSON - o JSON é o maior porque carrega, além dos dados, os metadados de proveniência (fonte, endpoint, data, licença, observação) descritos no Passo 1. O XML de apenas 3 linhas já ocupa 694 bytes: extrapolando a mesma razão de bytes por registro, 160 linhas em XML ficariam proporcionalmente maiores que o CSV equivalente - exatamente o padrão de verbosidade descrito no Capítulo 6.

## Passo 5 - Mapa: contorno do RN (IBGE) + estabelecimentos (CNES)

```
with open(DADOS / "rn_contorno.json", encoding="utf-8") as f: contorno = json.load(f)   # GeoJSON: lista de coordenadas [longitude, latitude] fig, ax = plt.subplots(figsize=(7, 6.5)) ax.plot(xs, ys, color="#00693e", linewidth=1.5) ax.fill(xs, ys, color="#00693e", alpha=0.05) for municipio, grupo in df.groupby("municipio"): ax.scatter(grupo["longitude"], grupo["latitude"], s=28, alpha=0.85, color=cores.get(municipio, "gray"), label=f"{municipio} ({len(grupo)})") fig.savefig("mapa_estabelecimentos_rn.png", dpi=150)
```

Figura 1 - Contorno do Rio Grande do Norte (GeoJSON, API de Malhas do IBGE) e os 160 estabelecimentos de saúde do CNES (20 por município), coloridos por município. Dados reais, coletados em 28/09/2026.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula06_Fontes_de_Dados_artifacts/image_000000_808ca1e1cb18eaa7a389a18c978892813740c216564e7dc979b8e3ad24fe9095.png)

Este mapa combina, em uma única figura, três das quatro fontes de dados desta aula: o contorno do estado veio de uma API REST (Malhas do IBGE, em GeoJSON) e os pontos vieram  de  um arquivo (o  snapshot  salvo  da  API  do  CNES).  É  o  fechamento  natural  do laboratório:  os  mesmos  conceitos  de  aquisição  de  dados,  aplicados  até  a  etapa  de visualização.

## Parte IV - Exercício prático avaliativo

Entrega obrigatória no Moodle · notebook ou script executado · prazo: 13/10/2026

O exercício está no arquivo aula06\_exercicio.ipynb ,  disponível no AVA junto com a pasta dados/ .  O  objetivo  é  repetir,  com  um  município diferente dos  8  já  usados  no  exemplo (Natal, Mossoró, Parnamirim, Caicó, Pau dos Ferros, Açu, Ceará-Mirim e Currais Novos), o mesmo percurso completo: arquivo → banco → formatos → discussão de licença.

## Passo a passo

1. Escolha  um  município  do  RN que  não  esteja  entre  os  8  já  usados.  Descubra  seu codigo\_municipio de  6  dígitos:  pegue  o  código  IBGE  de  7  dígitos  do  município  (por exemplo, na tabela raspada da Wikipédia no Passo 3, ou em https://servicodados.ibge.gov.br/api/v1/localidades/municipios ) e remova o último dígito (o dígito verificador ) - é assim que 2408102 (Natal) vira 240810 ,  o valor usado no exemplo do Capítulo 4.
2. Obtenha os dados do CNES para esse município. Em um ambiente com acesso à internet, use o mesmo padrão do Capítulo 4: requests.get(url, params= {"codigo\_municipio":  SEU\_CODIGO,  "limit":  20}) .  Se  a  resposta  tiver  mais  de  20 estabelecimentos, implemente a paginação com offset até a resposta vir vazia. Salve o resultado  em  um  arquivo  JSON  próprio  ( dados/cnes\_SEUMUNICIPIO.json ),  incluindo  os metadados  de  proveniência:  fonte,  endpoint,  parâmetros  usados,  data  da  coleta  e licença - no mesmo formato do arquivo usado no Passo 1 desta apostila.
3. Carregue o JSON em um banco SQLite com to\_sql e escreva uma consulta SQL que agrupe os estabelecimentos por descricao\_tipo\_unidade , contando quantos existem de cada tipo, em ordem decrescente de contagem.
4. Exporte o resultado da consulta (ou o DataFrame completo) para CSV e para Parquet, e compare o tamanho em bytes dos  dois  arquivos,  explicando a diferença em uma frase.
5. Escreva de 3 a 5 frases discutindo  a  licença  e  a  proveniência  dos  dados  que  você usou:  sob  que  licença  o  CNES  publica  esses  dados,  o  que  essa  licença  permite  (ou exige) e por que registrar a data da coleta importa para um cadastro que muda ao longo do tempo.

## Formato de entrega

Envie um único arquivo .py ou .ipynb (se notebook, já executado, com as saídas visíveis), nomeado aula06\_SEUNOME.ipynb (ou .py ),  na  tarefa "Exercício  Prático  -  Aula  06" do Moodle.

## Critérios de correção

| Critério                                | Peso   | O que se avalia                                                                                                   |
|-----------------------------------------|--------|-------------------------------------------------------------------------------------------------------------------|
| API / arquivo (Passos 1-2 do exercício) | 25%    | Requisição correta com requests , paginação quando necessária, JSON salvo com metadados de proveniência completos |
| Banco de dados                          | 25%    | to_sql usado corretamente; consulta SQL com GROUP BY produzindo o resultado pedido                                |
| Formatos                                | 25%    | Exportação correta para CSV e Parquet; comparação de tamanho presente e corretamente interpretada                 |
| Licença e proveniência                  | 25%    | Discussão escrita, correta e específica sobre a licença do CNES e a importância da data de coleta                 |

## PRAZO

O exercício prático e o formulário avaliativo (Parte V) fecham no mesmo prazo: 13/10/2026 (202610-13),  15  dias  a  partir  da  liberação  desta  aula.  Entregas  após  essa  data  seguem  a  política  de atrasos do curso.

## Parte V - Formulário avaliativo

10 questões objetivas · respondidas no Moodle · consulta ao material permitida · prazo: 13/10/2026

O  formulário  é  respondido  no  AVA,  na  atividade "Formulário  Avaliativo  -  Aula  06" .  As questões estão reproduzidas abaixo para que você possa prepará-las antes. Cada questão vale 1,0 ponto e admite uma única alternativa correta. O formulário fecha no mesmo prazo do exercício prático: 13/10/2026 (2026-10-13).

## Questão 01

Qual é a principal diferença entre consumir dados de um banco de dados e  de  uma API REST ?

- A. No banco, você fala diretamente a linguagem de consulta (SQL) sobre as tabelas; na API, você  depende  do  contrato  de  endpoints  e  parâmetros  que  o  provedor  do  serviço  decidiu expor.
- B. Não há diferença prática: os dois sempre devolvem exatamente os mesmos dados no mesmo formato.
- C. Banco de dados sempre exige internet; API REST nunca exige.
- D. API REST é apenas um apelido para banco de dados na nuvem.

## Questão 02

Um CSV exportado  de  um  sistema  legado  brasileiro  é  aberto  com encoding="utf-8" , mas o arquivo foi salvo em latin-1 . O que costuma acontecer?

- A. A  leitura  pode  não  gerar  erro  algum,  mas  os  acentos  aparecem  corrompidos  (ex.: "informa\u00e7\u00e3o" vira "informaÃ§Ã£o").
- B. O Python sempre recusa abrir o arquivo e levanta um erro imediato.
- C. O encoding é irrelevante para arquivos CSV , só importa para imagens.
- D. O arquivo é automaticamente convertido para o encoding correto pelo pandas.

## Questão 03

Uma API pública devolve no máximo 20 registros por chamada, mesmo quando se pede limit=1000 . Qual é a forma correta de obter mais registros?

- A. Repetir  a  chamada  avançando  um  parâmetro  de  deslocamento  (por  exemplo, offset=20 , depois offset=40 ) até a resposta vir vazia.
- B. Enviar a mesma chamada várias vezes em paralelo até algum retorno vir maior.
- C. Trocar limit por size , que costuma não ter teto.
- D. É impossível obter mais de 20 registros dessa API.

## Questão 04

Ao chamar uma API de estabelecimentos de saúde com ?uf=RN , a resposta não muda e continua trazendo estabelecimentos de qualquer estado. O que isso revela sobre testar APIs?

- A. Parâmetros com nome plausível podem ser aceitos sem erro e simplesmente ignorados; é preciso inspecionar o conteúdo da resposta, não só o código de status HTTP , para confirmar que um filtro funcionou de verdade.
- B. Isso significa que a API está fora do ar.
- C. Toda API sempre devolve erro quando um parâmetro é digitado errado.
- D. O parâmetro correto nunca pode ser descoberto sem ler o código-fonte do servidor.

## Questão 05

Antes de escrever um scraper para um site, quais verificações a aula recomenda?

- A. Procurar se já existe uma API para os mesmos dados, checar o robots.txt do site e ler os Termos de Uso.
- B. Nenhuma - scraping é sempre permitido em qualquer página pública.
- C. Basta usar um navegador automatizado para que a coleta se torne legal.
- D. É necessário pedir uma chave de API antes de fazer scraping.

## Questão 06

No trecho tabela.find\_all("tr")[1:] , usado para extrair linhas de uma tabela HTML, o que faz o [1:] ?

- A. Pula a primeira linha ( tr ) da tabela, geralmente o cabeçalho.
- B. Seleciona apenas a primeira linha da tabela.
- C. Converte a tabela inteira para um DataFrame automaticamente.
- D. Remove todas as linhas que contêm números.

## Questão 07

Sobre os quatro formatos vistos na aula, qual afirmação é correta?

- A. Parquet é um formato colunar e binário, tende a ser bem menor que CSV ou JSON para o mesmo conjunto de dados, além de permitir ler apenas algumas colunas sem abrir o arquivo inteiro.
- B. XML é sempre mais compacto que JSON para representar a mesma informação.
- C. CSV consegue representar diretamente estruturas aninhadas, como listas dentro de listas.
- D. JSON é um formato binário, por isso não pode ser lido em um editor de texto.

## Questão 08

Para que serve o formato GeoJSON, usado para desenhar o contorno do Rio Grande do Norte no mapa desta aula?

- A. É  um  JSON  com  estrutura  padronizada  para  representar  pontos,  linhas  e  polígonos geográficos  (com  coordenadas  de  longitude/latitude),  usado  para  troca  de  dados  entre ferramentas de mapas.
- B. É uma variação do CSV especializada em coordenadas geográficas.
- C. É um formato exclusivo do Google Maps, incompatível com outras ferramentas.
- D. Serve apenas para armazenar imagens de satélite.

## Questão 09

Um dataset está sob licença CC BY-SA . O que isso exige de quem reutiliza os dados?

- A. Dar crédito à fonte original ( Attribution ) e, se distribuir uma versão derivada, licenciá-la sob os mesmos termos ( ShareAlike ).
- B. Nenhuma exigência - CC BY-SA equivale a domínio público irrestrito.
- C. Proíbe qualquer uso comercial dos dados.
- D. Proíbe qualquer modificação do conteúdo original.

## Questão 10

Por que a aula recomenda salvar, junto com os dados coletados, metadados como fonte, endpoint, data da coleta e licença (como no JSON do exemplo desta aula)?

- A. Porque  um  dado  sem  proveniência  registrada  não  pode  ser  auditado,  reproduzido  nem verificado como ainda válido - a rastreabilidade é o que sustenta a confiança na análise.
- B. Porque isso é uma exigência técnica do formato JSON, que não funciona sem esses campos.
- C. Porque isso reduz o tamanho do arquivo em disco.
- D. Porque isso substitui a necessidade de validar os dados depois.

## Apêndice A - Colinha de comandos

## Arquivos e formatos

| Comando                                                        | Faz                                                            |
|----------------------------------------------------------------|----------------------------------------------------------------|
| pd.read_csv(caminho, sep=";", decimal=",", encoding="utf-8")   | Lê CSV declarando separador, decimal e encoding explicitamente |
| df.to_json(caminho, orient="records") / pd.read_json(caminho)  | Grava/lê JSON tabular                                          |
| pd.json_normalize(lista_de_dicts)                              | Achata JSON aninhado em colunas                                |
| df.to_parquet(caminho, index=False) / pd.read_parquet(caminho) | Grava/lê Parquet (colunar, binário, requer pyarrow )           |
| ET.ElementTree(root).write(caminho, encoding="utf-8")          | Grava uma árvore XML montada com xml.etree.ElementTree         |

## Banco de dados

| Comando                                                    | Faz                                                           |
|------------------------------------------------------------|---------------------------------------------------------------|
| con = sqlite3.connect("arquivo.db") (ou ":memory:" )       | Abre conexão com um banco SQLite em arquivo ou em memória     |
| df.to_sql("tabela", con, index=False, if_exists="replace") | Grava um DataFrame como tabela do banco                       |
| pd.read_sql("SELECT ...", con)                             | Executa uma consulta SQL e devolve o resultado como DataFrame |

## API REST e web scraping

| Comando                                      | Faz                                                       |
|----------------------------------------------|-----------------------------------------------------------|
| requests.get(url, params={...}, timeout=10)  | Faz uma requisição GET com parâmetros de query string     |
| resposta.raise_for_status()                  | Levanta exceção se o status HTTP indicar erro (4xx/5xx)   |
| resposta.json()                              | Converte o corpo da resposta em listas/dicionários Python |
| Paginação: repetir com offset=0, 20, 40, ... | Contorna um limit máximo imposto pelo servidor            |
| BeautifulSoup(html, "html.parser")           | Faz o parsing de um HTML                                  |
| soup.find("table", {"class": "wikitable"})   | Localiza o primeiro elemento que casa com o seletor       |
| tabela.find_all("tr")[1:]                    | Todas as linhas, pulando o cabeçalho                      |
| https://dominio.com/robots.txt               | Checar antes de qualquer scraping                         |

## Apêndice B - Referências e leituras recomendadas

- MINISTÉRIO  DA  SAÚDE. API  de  Dados  Abertos  -  CNES  (Cadastro  Nacional  de Estabelecimentos de Saúde) . apidadosabertos.saude.gov.br . Fonte dos dados de

estabelecimentos de saúde usados nesta aula.

- IBGE. API de Malhas Territoriais . servicodados.ibge.gov.br . Fonte do contorno geográfico do Rio Grande do Norte (GeoJSON) usado no mapa desta aula.
- WIKIPÉDIA. Lista  de  municípios  do  Rio  Grande  do  Norte . pt.wikipedia.org .  Conteúdo sob licença Creative Commons Atribuição-CompartilhaIgual 4.0 (CC BY-SA 4.0).
- BRASIL. Lei nº 12.527, de 18 de novembro de 2011 (Lei de Acesso à Informação) - base legal do regime de dados abertos governamentais citado nesta aula.
- McKINNEY,  Wes. Python  para  Análise  de  Dados .  3.  ed.  São  Paulo:  Novatec,  2023. Capítulo 6 (Leitura e escrita de dados em diferentes formatos). A 3ª edição em inglês está disponível gratuitamente em wesmckinney.com/book .
- PANDAS DEVELOPMENT TEAM. Pandas User Guide - seções IO tools (text, CSV , HDF5, …) e SQL queries . pandas.pydata.org/docs/user\_guide/
- REQUESTS. Requests:  HTTP  for  Humans -  documentação  oficial da biblioteca requests . requests.readthedocs.io
- RICHARDSON, Leonard. Beautiful Soup Documentation . www.crummy.com/software/BeautifulSoup/bs4/doc

## O que vem na próxima aula

Limpeza e tratamento de dados ausentes :  a  Unidade 2 continua a partir daqui - com os dados já adquiridos e sua proveniência registrada, a próxima aula trata de como identificar, entender e tratar valores ausentes, duplicados e inconsistentes antes de qualquer análise.

Aula 06 - Processos e Fontes de Dados · Análise e Ciência de Dados · Especialização em Ciência de Dados · IFRN