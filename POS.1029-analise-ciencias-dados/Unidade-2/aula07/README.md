# Mini projeto - Aula 07

## Coleta de um dataset real via API

Aberto: segunda-feira, 5 out. 2026, 00:00
Vencimento: terça-feira, 20 out. 2026, 23:59
Mini-Projeto — Aula 07: coleta de um dataset real via API

Escolha uma API pública real (pode ser o IBGE, o TSE, ou qualquer outra API aberta e gratuita de sua preferência) e construa um notebook que colete um dataset real a partir dela, aplicando os conceitos da Aula 07.

### Requisitos mínimos:

- Pelo menos uma requisição GET com requests, com tratamento de status/erro (try/except + raise_for_status()).
- Paginação, se a API escolhida limitar o tamanho da resposta (se a API não paginar, explique por escrito, no próprio notebook, por que não foi necessária).
- Salvar o resultado em JSON e CSV, com um bloco de proveniência (fonte, endpoint, data da coleta, licença, se conhecida).
- Um parágrafo final (em uma célula Markdown) descrevendo: qual API foi usada, quantos registros foram coletados e uma observação sobre os dados.
- Sugestões de APIs públicas e gratuitas (sem necessidade de cartão de crédito):

- IBGE — Localidades (servicodados.ibge.gov.br) ou Agregados/SIDRA
- TSE — Portal de Dados Abertos (dadosabertos.tse.jus.br)
- ViaCEP (viacep.com.br) — endereços por CEP, sem autenticação
- BrasilAPI (brasilapi.com.br) — feriados, bancos, CNPJ, tabela FIPE, sem autenticação
- OpenWeather (openweathermap.org) — previsão do tempo, exige API Key gratuita (boa escolha para praticar autenticação)
- PokéAPI (pokeapi.co) — catálogo grande, ótimo para praticar paginação por cursor

### Entregável

O que entregar: o notebook (.ipynb) já executado, com as saídas visíveis, mais os arquivos JSON/CSV gerados — todos compactados em um único .zip.
