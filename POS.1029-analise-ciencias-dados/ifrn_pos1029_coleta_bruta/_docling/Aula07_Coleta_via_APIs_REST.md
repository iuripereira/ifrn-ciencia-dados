INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE ESPECIALIZAÇÃO EM CIÊNCIA DE DADOS  ·  DISCIPLINA: ANÁLISE E CIÊNCIA DE DADOS

## Aula 07 - Laboratório: Coleta via APIs REST

Biblioteca requests ; autenticação (API Key, OAuth básico); paginação; coleta de dados de APIs públicas; salvamento em JSON/CSV

Unidade

Natureza Unidade 2 - Aquisição e Preparação de Dados (Aula 07, segunda aula)

Aula prática (laboratório)

Carga horária

4 h/a - 1h30 de exposição guiada + 2h30 de laboratório

Pré-

requisitos

Recursos Jupyter Notebook/Lab, requests , json (biblioteca padrão)

Avaliação Mini-projeto - coleta de um dataset real via API (prazo: 15 dias após esta aula)

Professor Plácido Antônio de Souza Neto Aula 06 - fontes de dados, formatos, APIs REST (conceito)

## Objetivos de aprendizagem

Ao final desta aula, espera-se que o estudante seja capaz de:

1. Montar e executar uma  requisição  HTTP GET com  a  biblioteca requests ,  incluindo parâmetros de consulta ( params ) e tempo limite ( timeout ).
2. Interpretar o  código de status e o corpo da resposta de uma API REST, convertendo JSON em estruturas Python com response.json() .
3. Implementar paginação para coletar um conjunto de dados maior do que o limite de uma  única  resposta,  usando  o  par  de  parâmetros  mais  comum  ( offset / limit ,  ou equivalente).
4. Explicar os dois mecanismos de autenticação mais comuns em APIs REST - API Key e OAuth 2.0 (fluxo client credentials) - e identificar quando cada um é usado.
5. Tratar erros de requisição (status 4xx/5xx, timeout, indisponibilidade) com try/except e raise\_for\_status() , sem deixar o programa quebrar.
6. Salvar um  conjunto  de  dados  coletado  via  API  nos  formatos  JSON  e  CSV ,  com metadados de proveniência (fonte, endpoint, data da coleta).

## Sumário

## Parte I - Fundamentos teóricos

- 1.1 Anatomia de uma requisição HTTP
- 1.2 A biblioteca requests : do zero ao primeiro GET
- 1.3 Paginação: coletando mais do que uma resposta devolve de uma vez

- 1.4 Autenticação: API Key e OAuth básico
- 1.5 Tratando erros com elegância
- 1.6 Persistência: JSON ou CSV?

Parte II - Laboratório guiado: dados reais do IBGE e do TSE

- Parte III - Exercício prático
- Parte IV - Mini-projeto avaliativo (entrega no Moodle)

Apêndice A - Colinha: status HTTP e padrões de paginação

Apêndice B - Referências e leituras recomendadas

## SOBRE OS DADOS USADOS NESTA AULA

Todos os exemplos desta apostila usam dados reais ,  coletados  ao  vivo  em 05/10/2026 de  duas fontes públicas, sem necessidade de cadastro ou chave de API: o IBGE (API de Localidades) e o TSE -  Tribunal  Superior  Eleitoral  (Portal  de  Dados  Abertos, dadosabertos.tse.jus.br ).  Como  a Aula 06 já cobriu em profundidade os tipos de fontes e formatos de dados, esta aula vai direto ao ponto: como falar HTTP com uma API de verdade, usando a biblioteca requests .

## Parte I - Fundamentos teóricos

O ciclo completo de uma coleta via API REST: requisitar, paginar, autenticar, tratar erros, salvar

## 1.1 Anatomia de uma requisição HTTP

Toda  API  REST  conversa  por  meio  de  requisições  HTTP  -  o  mesmo  protocolo  que  o navegador usa para carregar uma página. Entender as peças dessa conversa é o que torna qualquer API, conhecida ou não, previsível de usar.

## As peças de uma requisição

- Método (verbo) - o que você quer fazer: GET (ler dados, o único que usaremos nesta aula), POST (criar), PUT / PATCH (atualizar), DELETE (remover).
- URL - o endereço do recurso, por exemplo https://servicodados.ibge.gov.br/api/v1/localidades/estados/RN/municipios .
- Parâmetros de consulta (query string) -  pares  chave=valor depois do ? na  URL, usados para filtrar, paginar ou configurar a resposta (ex.: ?rows=5&amp;start=10 ).
- Cabeçalhos (headers) - metadados da requisição, como o formato aceito ( Accept ) ou uma credencial de autenticação ( Authorization ).
- Corpo  (body) -  dados  enviados  junto  da  requisição;  comum  em POST / PUT ,  raro  (e normalmente ausente) em GET .

## E a resposta

O servidor devolve um código de status (um  número  de  três  dígitos  que  resume  o  que aconteceu - ver colinha no Apêndice A), cabeçalhos próprios (como o Content-Type ,  que diz se o corpo é JSON, HTML, etc.) e um corpo - quase sempre JSON no caso de APIs de dados modernas.

## ATENÇÃO

Um erro  comum  de  quem  está  começando  é  checar  apenas  se  a  requisição  "rodou  sem  lançar exceção" e assumir que deu certo. Isso não é suficiente: uma URL errada, um parâmetro inválido ou um servidor fora do ar frequentemente devolvem uma resposta HTTP válida - só que com um status de erro ( 404 , 500 ...). É por isso que checar response.status\_code (ou usar response.raise\_for\_status() , Seção 1.5) é parte do fluxo normal, não um passo opcional.

## 1.2 A biblioteca requests : do zero ao primeiro GET

requests é  a  biblioteca  padrão  de  fato  do  ecossistema Python para HTTP - não vem na biblioteca padrão, mas está presente em praticamente todo ambiente de ciência de dados ( pip install requests ). O  padrão básico para consumir uma  API  pública  e  sem autenticação é sempre o mesmo:

```
import requests resposta = requests.get( "https://servicodados.ibge.gov.br/api/v1/localidades/estados/RN/municipios", timeout=10,            # nunca deixe uma requisição sem prazo - Seção 1.5 ) print(resposta.status_code)   # 200 = sucesso dados = resposta.json()       # converte o corpo JSON em lista/dicionário Python
```

## Enviando parâmetros de consulta

Em vez de concatenar a URL manualmente (propenso a erro com caracteres especiais e acentos), o parâmetro params do requests.get monta a query string para você:

```
# Em vez de montar a URL na mão... url_manual = "https://dadosabertos.tse.jus.br/api/3/action/package_search?q=eleições&rows=5" # ... passe um dicionário em params: resposta = requests.get( "https://dadosabertos.tse.jus.br/api/3/action/package_search", params={"q": "eleições", "rows": 5}, timeout=10, ) print(resposta.url)   # requests monta e escapa a URL final para você
```

## O objeto Response em resumo

| Atributo/método     | O que devolve                                             |
|---------------------|-----------------------------------------------------------|
| .status_code        | o código de status HTTP (inteiro), ex.: 200               |
| .ok                 | True se o status for menor que 400                        |
| .json()             | o corpo da resposta convertido em lista/dicionário Python |
| .text               | o corpo da resposta como texto bruto (útil para HTML/XML) |
| .headers            | dicionário com os cabeçalhos da resposta                  |
| .url                | a URL final, já com os params embutidos                   |
| .raise_for_status() | lança uma exceção se o status for de erro (Seção 1.5)     |

## 1.3 Paginação: coletando mais do que uma resposta devolve de uma vez

Quase toda API que expõe um catálogo grande (dezenas, milhares ou milhões de registros) limita quantos itens devolve por requisição - por desempenho, tanto do servidor quanto da sua  conexão.  Para  trazer  o  conjunto  inteiro,  o  cliente  precisa  pedir  "página  por  página", processo chamado de paginação .

## Os padrões mais comuns

- limit / offset (ou nomes equivalentes, como o rows / start usado pelo TSE) - você diz quantos itens quer ( limit / rows ) e a partir de qual posição ( offset / start ). É o padrão

mais comum em APIs de bancos de dados e catálogos.

- page / per\_page - em vez de uma posição, você pede um número de página e quantos itens  por  página;  matematicamente  equivalente  ao  anterior  ( offset  =  (page  -  1)  * per\_page ).
- Paginação  por  cursor  ( cursor / next\_token ) -  a  própria  resposta  traz  um  "token" apontando para a próxima página, em vez de você calcular a posição. Mais comum em APIs  de  redes  sociais  e  fluxos  de  dados  que  mudam  constantemente  (evita  duplicatas quando itens são inseridos entre uma página e outra).

## A lógica, na prática

Independente do padrão, o algoritmo é sempre o mesmo: peça uma página, veja se ainda há mais, peça a próxima, repita até acabar. Com o padrão rows / start do TSE (Portal de Dados Abertos, construído sobre o motor CKAN):

```
def buscar_pagina(termo, start, rows=5): resposta = requests.get( "https://dadosabertos.tse.jus.br/api/3/action/package_search", params={"q": termo, "rows": rows, "start": start}, timeout=10, ) resposta.raise_for_status() return resposta.json()["result"] todos = [] start = 0 rows = 5 while True: pagina = buscar_pagina("eleições", start=start, rows=rows) todos.extend(pagina["results"]) if start + rows >= pagina["count"]:   # já coletamos tudo break start += rows
```

## ATENÇÃO

O erro mais comum  em  código  de paginação é a condição de parada. Pedir páginas indefinidamente desperdiça requisições (e pode esbarrar em limites de uso); parar cedo demais perde dados. A regra start + rows &gt;= total é  a  mais segura: ela usa o total que a própria API informou na resposta, em vez de supor um número fixo de páginas.

## 1.4 Autenticação: API Key e OAuth básico

As APIs usadas nesta aula (IBGE e TSE) são públicas e não exigem nenhuma credencial - por  isso  foram  escolhidas  para  a  parte  prática.  Mas  a  maioria  das  APIs  comerciais (OpenWeather, redes sociais, serviços de pagamento, APIs corporativas) exige autenticação :  provar,  a  cada  requisição,  quem  está  pedindo  os  dados.  Os  dois  padrões mais comuns:

## API Key

Uma chave fixa, obtida ao se cadastrar no site do provedor, enviada em toda requisição - como parâmetro da URL ou como cabeçalho HTTP:

```
# Opção 1 - a chave como parâmetro de consulta (ex.: OpenWeather) requests.get( "https://api.openweathermap.org/data/2.5/weather", params={"q": "Natal,BR", "appid": API_KEY}, ) # Opção 2 - a chave como cabeçalho (padrão mais comum em APIs mais novas) requests.get( "https://api.exemplo.com/dados", headers={"Authorization": f"Bearer {API_KEY}"}, )
```

É o método  mais simples de autenticação e o mais usado por APIs voltadas  a desenvolvedores individuais. A chave normalmente não expira (ou expira em meses/anos) e dá acesso a tudo que a sua conta permite.

## OAuth 2.0 (fluxo client credentials)

Quando  a  API  exige  mais  segurança  -  por  exemplo,  acesso  a  dados  de  um  usuário específico, ou uma aplicação corporativa - o padrão é o OAuth 2.0 . No fluxo mais simples ( client  credentials ,  usado  quando  a  aplicação  acessa  dados  dela  mesma,  sem  um  usuário por trás), o processo tem duas etapas:

```
# Etapa 1 - troca client_id + client_secret por um token temporário token_resposta = requests.post( "https://api.exemplo.com/oauth/token", data={ "grant_type": "client_credentials", "client_id": "seu_client_id", "client_secret": "seu_client_secret", }, ) token = token_resposta.json()["access_token"] # Etapa 2 - usa o token no cabeçalho das requisições seguintes requests.get( "https://api.exemplo.com/recurso-protegido", headers={"Authorization": f"Bearer {token}"}, )
```

A diferença essencial para a API Key: o token do OAuth é temporário (expira em minutos ou horas) e precisa ser renovado - o que torna o acesso mais seguro (um token vazado tem validade curta) ao custo de mais complexidade no código.

## BOA PRÁTICA: NUNCA ESCREVA CREDENCIAIS NO CÓDIGO

Em projetos reais, chaves e segredos não ficam escritos diretamente no script ou notebook - eles são  lidos  de  variáveis  de  ambiente  ( os.environ["MINHA\_CHAVE"] )  ou  de  um  arquivo .env (com  a biblioteca python-dotenv )  que  é  adicionado  ao .gitignore e  nunca  é  enviado  ao  controle  de versão. Um repositório público com uma chave de API esquecida no código é uma das formas mais comuns de vazamento de credenciais.

## 1.5 Tratando erros com elegância

Coleta  de  dados  via  rede  encontra,  cedo  ou  tarde:  instabilidade  de  conexão,  limite  de requisições excedido, parâmetro inválido, recurso que não existe mais. Um script de coleta robusto antecipa isso.

## Códigos de status que merecem atenção especial

| Status    | Significado                                | O que fazer                                                                 |
|-----------|--------------------------------------------|-----------------------------------------------------------------------------|
| 200       | OK - sucesso                               | seguir normalmente                                                          |
| 400       | Bad Request - parâmetro inválido           | revisar os parâmetros enviados                                              |
| 401       | Unauthorized - credencial ausente/errada   | checar a API Key/token                                                      |
| 403       | Forbidden - sem permissão                  | a credencial é válida, mas não autoriza esse acesso                         |
| 404       | Not Found - recurso não existe             | checar a URL/identificador                                                  |
| 429       | Too Many Requests - limite de uso excedido | esperar e tentar de novo (respeitando o cabeçalho Retry- After , se houver) |
| 500 / 503 | erro do servidor / indisponível            | tentar de novo mais tarde; não é culpa do seu código                        |

## O padrão try / except com requests

```
def buscar_com_seguranca(url, params=None, timeout=10): try: resposta = requests.get(url, params=params, timeout=timeout) resposta.raise_for_status()      # transforma status de erro em exceção return resposta.json() except requests.exceptions.Timeout: print("A API demorou demais para responder.") except requests.exceptions.HTTPError as e: print(f"Erro HTTP: {e}") except requests.exceptions.RequestException as e: print(f"Erro de rede/requisição: {e}") return None
```

Note a ordem das exceções: da mais específica ( Timeout ) para a mais geral ( RequestException , a classe-mãe de todas as exceções do requests ). Isso garante que cada tipo de falha receba o tratamento mais preciso possível, com a exceção genérica como rede de segurança para o que não foi previsto.

## 1.6 Persistência: JSON ou CSV?

Depois de coletados, os dados precisam ser salvos - tanto para não depender de pedir tudo de  novo  à  API,  quanto  para  serem  usados  por  outras  ferramentas  (planilhas,  outros notebooks, dashboards). A escolha entre JSON e CSV depende da forma dos dados:

| Formato                                                                                                                            | Quando usar                                                   | Como gravar   |
|------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|---------------|
| dados aninhados (listas dentro de dicionários, por exemplo), ou quando você quer guardar metadados de proveniência junto dos dados | json.dump(dados, arquivo, ensure_ascii=False, indent=2)       | JSON          |
| dados já "achatados" em linhas e colunas - abre direto em Excel/Google Sheets, é o formato mais universal para dados tabulares     | csv.DictWriter (biblioteca padrão) ou pandas.DataFrame.to_csv | CSV           |

Uma prática recomendada (usada no laboratório desta aula): gravar os dois - o JSON como registro completo e rastreável (com proveniência), o CSV como versão pronta para abrir em qualquer ferramenta de planilha ou carregar com pandas.read\_csv .

## Parte II - Laboratório guiado: dados reais do IBGE e do TSE

Coletado ao vivo em 05/10/2026 - os mesmos passos estão no notebook desta aula

O  notebook Aula07\_Coleta\_via\_APIs\_REST.ipynb (recurso  desta  seção  no  Moodle)  traz  o roteiro completo, executável, com todas as saídas reais abaixo. Esta seção resume os três passos centrais.

## Passo 1 - GET simples: municípios do RN (IBGE)

```
resposta = requests.get( "https://servicodados.ibge.gov.br/api/v1/localidades/estados/RN/municipios", timeout=10, ) municipios = resposta.json() print(len(municipios), "municípios")
```

```
Status code: 200 Total de municípios recebidos: 167 Exemplo: {"id": 2400109, "nome": "Acari", ...}
```

Essa API devolve a lista inteira de uma vez - não pagina, por ser um catálogo pequeno e estável (estados e municípios do Brasil mudam raramente).

## Passo 2 - Paginação real: catálogo de dados do TSE

```
todos_conjuntos = [] start = 0 while True: pagina = buscar_pagina("eleições", start=start, rows=5) todos_conjuntos.extend(pagina["results"]) if start + 5 >= pagina["count"]: break start += 5
```

```
start=0: +5 resultados (total até agora: 5/9) start=5: +4 resultados (total até agora: 9/9) Conjuntos coletados: resultados-eleicoes-suplementares-2024, resultados-eleicoessuplementares-2022, resultados-2020-suplementares, resultados-1998, resultados-1996, resultados-1994, candidatos-1998, candidatos-1996, candidatos-1994
```

O portal de dados abertos do TSE roda sobre o CKAN - o mesmo motor usado por diversos portais de governo aberto no mundo - e no momento da coleta reunia 182 conjuntos de dados em 7 organizações e 12 grupos temáticos.

## Passo 3 - Indo além da busca: package\_show

```
Título: Candidatos - 2026 Total de recursos (arquivos): 92 - Candidatos (CSV): .../consulta_cand/consulta_cand_2026.zip - Candidatos - Informações complementares (CSV): .../consulta_cand_complementar_2026.zip - Bens de candidatos (CSV): .../bem_candidato/bem_candidato_2026.zip
```

O recurso "Candidatos" é o arquivo nacional oficial de candidaturas de 2026 (um ZIP com um CSV por UF) - grande demais para baixar ao vivo nesta aula, mas o notebook mostra o código completo para baixá-lo e filtrar o RN com requests + zipfile + pandas , caso você queira usá-lo no mini-projeto.

## Passo 4 - Salvando em JSON e CSV

```
Gravado dados/municipios_rn.json (13.092 bytes) Gravado dados/municipios_rn.csv (3.728 bytes) Gravado dados/tse_conjuntos_eleicoes.json (899 bytes)
```

Repare a diferença de tamanho entre o CSV (achatado, só codigo\_ibge e municipio )  e  o JSON  (maior,  porque  carrega  também  os  metadados  de  proveniência)  -  o  mesmo compromisso espaço-vs-rastreabilidade discutido na Aula 06.

## Parte III - Exercício prático

Pratique com uma UF e um termo de busca à sua escolha - sem entrega, é aquecimento para o mini-projeto

O  exercício  prático  desta  aula  está  no  notebook Aula07\_Exercicio\_Pratico.ipynb (recurso desta  seção  no  Moodle),  com  instruções  passo  a  passo.  Em  resumo,  você  vai  repetir  os passos do laboratório guiado, mas com dados diferentes:

1. IBGE - escolher um estado diferente do RN e coletar seus municípios, comparando a quantidade com os 167 do RN.
2. TSE - escolher um termo de busca diferente de "eleições" e implementar a paginação completa (não só a primeira página).
3. Tratamento de erro - provocar um erro de propósito (UF inexistente, por exemplo) e tratá-lo sem deixar o programa quebrar.
4. Persistência - salvar os resultados em JSON e CSV, com proveniência.

Esse  exercício  não  é  entregue  nem  avaliado  -  é  a  prática  recomendada  antes  do  miniprojeto, que segue na Parte IV .

## Parte IV - Mini-projeto avaliativo

Avaliação desta aula - entrega no Moodle

## O que fazer

Escolha uma API pública real (pode ser o IBGE, o TSE, ou qualquer outra API aberta e gratuita de sua preferência - veja sugestões abaixo) e construa um notebook que colete um dataset real a partir dela, aplicando os conceitos desta aula.

## Requisitos mínimos

1. Pelo  menos uma  requisição  GET com requests ,  com  tratamento  de  status/erro ( try/except + raise\_for\_status() ).
2. Paginação , se a API escolhida limitar o tamanho da resposta (se a API não paginar - como o endpoint de municípios do IBGE - explique por escrito, no próprio notebook, por que não foi necessária).
3. Salvar  o  resultado  em JSON e CSV ,  com  um  bloco  de  proveniência  (fonte,  endpoint, data da coleta, licença, se conhecida).
4. Um  parágrafo  final  (em  uma  célula  Markdown)  descrevendo:  qual  API  foi  usada, quantos registros foram coletados e uma observação sobre os dados (algo que chamou atenção, uma limitação, um valor inesperado).

## Sugestões de APIs públicas e gratuitas (sem necessidade de cartão de crédito)

- IBGE - Localidades ( servicodados.ibge.gov.br ), já usada nesta aula; também há a API de Agregados (SIDRA), com dados estatísticos.
- TSE - Portal de Dados Abertos ( dadosabertos.tse.jus.br ), já usado nesta aula.
- ViaCEP ( viacep.com.br ) - consulta de endereços por CEP , sem autenticação.
- BrasilAPI ( brasilapi.com.br ) - feriados, bancos, CNPJ, tabela FIPE de veículos, entre outros, sem autenticação.
- OpenWeather ( openweathermap.org )  - previsão do tempo; exige uma API Key gratuita (cadastro simples) - boa escolha se você quiser praticar autenticação de verdade (Seção 1.4).
- PokéAPI ( pokeapi.co )  -  catálogo  grande  e  bem  documentado,  ótimo  para  praticar paginação por cursor.

## Entrega e prazo

O que entregar o  notebook  ( .ipynb )  já  executado,  com  as  saídas  visíveis,  mais  os  arquivos  JSON/CSV gerados - todos compactados em um único .zip

Onde entregar

Prazo atividade "Mini-Projeto - Aula 07" no Moodle

15 dias após esta aula

## ATENÇÃO AO PRAZO

O mini-projeto desta aula deve ser enviado até 20/10/2026 (23h59).  Após  essa  data,  o  envio  é encerrado na plataforma.

## Apêndice A - Colinha: status HTTP e padrões de paginação

| Status HTTP   | Categoria                                        |
|---------------|--------------------------------------------------|
| 2xx           | sucesso ( 200 OK é o mais comum)                 |
| 3xx           | redirecionamento                                 |
| 4xx           | erro do cliente - algo no seu pedido está errado |
| 5xx           | erro do servidor - não é culpa do seu código     |

| Padrão de paginação   | Parâmetros típicos Onde aparece                                                  |
|-----------------------|----------------------------------------------------------------------------------|
| offset/limit          | offset , limit (ou start , rows ) TSE (CKAN), muitas APIs de banco de dados      |
| page/per_page         | page , per_page (ou page_size ) GitHub API, muitas APIs REST "clássicas"         |
| cursor                | cursor , next_token APIs de redes sociais e fluxos de dados em constante mudança |

## Apêndice B - Referências e leituras recomendadas

- REQUESTS. Requests:  HTTP  for  Humans -  documentação  oficial da biblioteca requests . requests.readthedocs.io
- IBGE. API de Localidades - Documentação . servicodados.ibge.gov.br/api/docs/localidades
- TSE. Portal de Dados Abertos . dadosabertos.tse.jus.br
- CKAN. Action API Reference (motor usado pelo portal do TSE). docs.ckan.org/en/latest/api
- MDN WEB DOCS. HTTP response status codes . developer.mozilla.org/enUS/docs/Web/HTTP/Status
- IETF. RFC 6749 - The OAuth 2.0 Authorization Framework . datatracker.ietf.org/doc/html/rfc6749

## O que vem na próxima aula

Laboratório:  Web  Scraping  com  BeautifulSoup -  quando  os  dados  não  estão  disponíveis nem como arquivo nem como API, a próxima aula mostra como extraí-los diretamente do HTML de páginas públicas, de forma ética e dentro dos limites legais.

Aula 07 - Laboratório: Coleta via APIs REST · Análise e Ciência de Dados · Especialização em Ciência de Dados · IFRN