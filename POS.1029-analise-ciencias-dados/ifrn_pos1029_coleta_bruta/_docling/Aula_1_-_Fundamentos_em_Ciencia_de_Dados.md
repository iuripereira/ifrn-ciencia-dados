## ANÁLISE E CIÊNCIA DE DADOS

## Aula 01 - Fundamentos e Panorama da Ciência de Dados

Definição de Ciência de Dados · Perfis Profissionais · Ferramentas do Ecossistema

IFRN - Instituto Federal do Rio Grande do Norte Professor: Plácido A. Souza Neto

## Apresentação e objetivos de aprendizagem

Este  material  aprofunda  o  conteúdo  apresentado  no  livro  da  Aula  01  disponível  no  AVA,  servindo como texto-base de estudo da disciplina. Ao final da leitura, você deverá ser capaz de:

- Definir Ciência de Dados como um processo e situá-la historicamente;
- Distinguir dado, informação e conhecimento, e classificar tipos de dados e variáveis;
- Diferenciar  Ciência  de  Dados,  Business  Intelligence  (BI)  e  Aprendizado  de  Máquina  (ML), reconhecendo os quatro níveis de análise;
- Descrever os principais  perfis  profissionais  da  área, suas competências e como colaboram em um projeto real;
- Explicar  as  seis  fases  do  CRISP-DM  (modelo  de  6  fases  para  modelagem  e  compreensão  de dados)  e aplicá-las mentalmente a um problema concreto;
- Reconhecer as ferramentas do ecossistema Python usadas na disciplina e o papel de cada uma;
- Analisar criticamente o estudo de caso do ranking das escolas do RN no ENEM 2025, incluindo suas armadilhas metodológicas e implicações éticas.

O s conceitos desta aula serão ilustrados com um recorte de dados reais - os microdados do ENEM 2025 no Rio Grande do Norte . Guarde esse exemplo: ele aparecerá nas próximas unidades.

## 1. O que é Ciência de Dados?

## 1.1 Origens: uma disciplina jovem com raízes antigas

Embora o termo tenha se popularizado apenas na década de 2010, a Ciência de Dados tem raízes que remontam à estatística clássica.  Em  1962,  o  estatístico  John  Tukey  publicou o ensaio The Future of Data Analysis , defendendo que a análise de dados era uma ciência em si - maior do que a estatística matemática que a abrigava. Em 2001, William Cleveland propôs formalmente o nome Data Science para  um  campo  que  ampliaria  a  estatística  com  computação.  O  marco  de  popularização  veio  em 2012, quando Thomas Davenport e D.J. Patil publicaram na Harvard Business Review o  artigo  que chamou o cientista de dados de "a profissão mais sedutora do século XXI".

O que mudou entre Tukey e Davenport não foi a essência - extrair conclusões de dados - mas a escala e a disponibilidade . Três movimentos convergiram:

- Barateamento do armazenamento: guardar um gigabyte custava milhares de dólares nos anos 1980; hoje custa frações de centavo. Tornou-se viável guardar tudo - logs, cliques, sensores - mesmo sem saber, a priori, para que servirá.
- Explosão  na  geração  de  dados: web,  smartphones,  redes  sociais,  sensores  (IoT),  sistemas transacionais  e  governos  digitais  produzem  volumes  de  dados sem precedentes, em formatos variados e em velocidade crescente.
- Amadurecimento dos algoritmos: técnicas de aprendizado de máquina que existiam na teoria desde  os  anos  1950-1990  tornaram-se  práticas  com  hardware  barato  (GPUs),  bibliotecas abertas e grandes conjuntos de dados para treiná-las.

## 1.2 Uma definição de trabalho

Há  dezenas  de  definições  na  literatura.  Nesta  disciplina  adotaremos  uma  definição  operacional, centrada no processo:

Ciência  de  Dados  é  o  processo  sistemático  de  coletar,  preparar,  explorar,  modelar  e comunicar dados para responder perguntas e apoiar decisões.

Três observações importantes sobre essa definição:

- É um processo, não uma ferramenta. Programar em Python, usar Pandas ou treinar um modelo de ML são meios ; o fim é responder uma pergunta relevante com evidências extraídas de dados. Uma análise tecnicamente sofisticada que responde à pergunta errada não tem valor.
- Começa e termina fora do computador. O processo começa com uma pergunta (formulada por pessoas, sobre um problema real) e termina com uma decisão ou comunicação (também entre pessoas). As etapas computacionais estão no meio.
- "Sistemático" implica método e reprodutibilidade. Outro analista, com os mesmos dados e o mesmo  procedimento,  deve  chegar  aos  mesmos  resultados.  Por  isso  versionamos  código, documentamos decisões e registramos as transformações aplicadas aos dados.

A Ciência de Dados é interdisciplinar por natureza. Uma representação clássica (o diagrama de Venn de Drew Conway, 2010) a coloca na interseção de três competências: estatística e matemática (para modelar  e  quantificar  incerteza), computação (para  manipular  dados  em  escala  e  automatizar processos)  e conhecimento de domínio (para formular perguntas relevantes e validar respostas). A ausência  de  qualquer  um  dos  três  enfraquece  o  resultado:  sem  estatística,  corre-se  o  risco  de conclusões numericamente erradas; sem computação, não se escala; sem domínio, produz-se análise tecnicamente correta, porém irrelevante ou enganosa.

Figura 1. Diagrama de Venn de Crew Conway

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula_1_-_Fundamentos_em_Ciencia_de_Dados_artifacts/image_000000_f54d3b37bf100e18ccd9a427085e85dfbbfa3269e9f694d1bbccff387fdd5196.png)

## 1.3 Dado, informação e conhecimento

A distinção entre esses três níveis - às vezes estendida com um quarto nível, sabedoria , na chamada pirâmide DIKW ( Data,  Information,  Knowledge,  Wisdom )  -  é  fundamental  para  entender  o  que  a Ciência de Dados produz em cada etapa:

| Nível        | Definição                                                                         | Exemplo (ENEM 2025 / RN)                                                                                           |
|--------------|-----------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Dado         | Registro bruto, sem interpretação. É o que está gravado no arquivo, sem contexto. | A linha de um aluno no CSV do ENEM: código da escola, presença, notas de CN, CH, LC, MT e redação.                 |
| Informação   | Dado contextualizado, agregado ou comparado - responde "o quê?".                  | A média de matemática de uma escola de Natal em 2025 foi 612,4, acima da média estadual.                           |
| Conhecimento | Padrão ou relação que apoia decisão - responde "e daí?". Escolas de               | determinado perfil apresentam desempenho sistematicamente maior, o que orienta políticas públicas de investimento. |

Note  a  progressão  de  valor:  o  dado  bruto  isolado  não  diz  nada;  a  informação  descreve;  o conhecimento orienta ação. O trabalho do cientista de dados é justamente subir essa escada - e fazê-lo com honestidade metodológica, pois é fácil produzir "conhecimento" falso a partir de análises descuidadas (veremos exemplos concretos no estudo de caso do Capítulo 6).

## 1.4 Tipos de dados e de variáveis

Para preparar e analisar dados corretamente, é preciso reconhecer sua estrutura e natureza. Quanto à estrutura :

- Estruturados: organizados  em  linhas  e  colunas  com  esquema  fixo  -  tabelas  de  bancos relacionais, planilhas, CSVs. Os microdados do ENEM são estruturados.
- Semiestruturados: possuem  organização,  mas  flexível  -  JSON  de  APIs,  XML,  logs.  Ex.:  a resposta de uma API do IBGE.
- Não estruturados: sem esquema tabular - textos livres (redações do ENEM!), imagens, áudio, vídeo. Estima-se que representem a maior parte dos dados gerados no mundo.

Quanto à natureza das variáveis (classificação estatística que usaremos intensamente na Unidade 3):

- Qualitativa  nominal: categorias  sem  ordem  -  dependência  administrativa da escola (federal, estadual, municipal, privada), município.
- Qualitativa ordinal: categorias com  ordem  -  faixa  de  renda  familiar  do  questionário socioeconômico do ENEM.
- Quantitativa discreta: contagens inteiras - número de participantes de uma escola.
- Quantitativa contínua: valores em escala contínua - nota da prova de matemática (0 a 1000).

## 1.5 Por que agora? Dados abertos e o contexto brasileiro

O Brasil ocupa posição de destaque na publicação de dados abertos governamentais. Órgãos públicos disponibilizam bases massivas e gratuitas que constituem matéria-prima excelente para aprendizado e pesquisa:

- INEP - microdados do ENEM, Censo Escolar, ENADE, SAEB. Só os microdados do ENEM contêm milhões de registros por edição , um por participante, com notas, questionário socioeconômico e dados da escola;
- IBGE -  Censo  Demográfico,  PNAD  Contínua,  projeções  populacionais  e  APIs  de  agregados estatísticos;
- DataSUS -  internações,  mortalidade,  nascimentos  e  produção  ambulatorial  do  sistema  de saúde;
- dados.gov.br -  portal  que  cataloga  milhares  de  conjuntos  de  dados  de  todos  os  órgãos federais.

Ao longo desta disciplina usaremos um recorte real dessa riqueza: os resultados do ENEM 2025 no Rio Grande do Norte (cerca de 30 mil participantes e 5 mil escolas catalogadas). Trabalhar com dados reais - com seus problemas de codificação, valores ausentes e inconsistências - é pedagogicamente muito mais rico do que usar bases "limpas" de livro-texto.

## 2. Ciência de Dados, BI e Aprendizado de Máquina

Três termos aparecem juntos com frequência - em vagas de emprego, notícias e ferramentas - e é importante distingui-los com precisão, pois delimitam atividades, perguntas e entregas diferentes.

## 2.1 Business Intelligence (BI)

O  BI  é  voltado  ao passado  e  ao  presente :  consolida  dados  de  sistemas  transacionais  (vendas, matrículas, atendimentos) em painéis e relatórios que descrevem o que aconteceu . Tecnicamente, o BI clássico se apoia em uma separação importante:

- Sistemas  OLTP ( Online  Transaction  Processing ):  os  sistemas  do  dia  a  dia,  otimizados  para registrar transações - o sistema acadêmico que registra matrículas, o caixa que registra vendas;
- Sistemas OLAP ( Online  Analytical  Processing ):  estruturas otimizadas para consulta analítica - data warehouses que consolidam o histórico e alimentam dashboards.

No BI,  as  perguntas  são conhecidas de antemão ("qual a evasão por curso a cada semestre?") e as respostas  são  agregações  e indicadores (somas, médias, percentuais) atualizados periodicamente. É uma atividade essencial - toda organização madura tem BI - mas de natureza descritiva .

## 2.2 Ciência de Dados e os quatro níveis de análise

A Ciência de Dados engloba o descritivo, mas avança. Uma taxonomia útil organiza a análise de dados em quatro níveis de valor e complexidade crescentes:

| Nível       | Pergunta                 | Exemplo (ENEM 2025 / RN)                                                                                     |
|-------------|--------------------------|--------------------------------------------------------------------------------------------------------------|
| Descritiva  | O que aconteceu?         | Painel com a média por escola e por município.                                                               |
| Diagnóstica | Por que aconteceu?       | Que fatores (dependência administrativa, porte, perfil socioeconômico) explicam as diferenças de desempenho? |
| Preditiva   | O que tende a acontecer? | Prever a nota de um aluno a partir do seu perfil; projetar o desempenho de uma escola.                       |
| Prescritiva | O que devemos fazer?     | Onde investir reforço escolar para maximizar o impacto na próxima edição?                                    |

A CD transita por todos os níveis e envolve formulação de hipóteses, experimentação e modelagem estatística -  inclusive  quando  a  pergunta  ainda  não  está  bem  definida.  É comum que um projeto comece  exploratório  ("o  que  esses  dados  podem  nos  dizer?")  e  a  pergunta  se  refine  ao  longo  do caminho. Essa abertura é a diferença de postura mais marcante em relação ao BI.

## 2.3 Aprendizado de Máquina (ML)

O  ML  é  um conjunto  de  técnicas  usado  dentro  da  Ciência  de  Dados :  algoritmos  que  aprendem padrões a partir  de  exemplos, sem serem explicitamente programados para cada regra. A definição clássica de Tom Mitchell (1997) captura a ideia:

Um programa aprende com a experiência E, em relação a uma tarefa T e uma medida de desempenho P, se seu desempenho em T, medido por P, melhora com E.

Em vez de escrever regras ("se a renda for X e a escola for Y, a nota será Z"), fornecemos exemplos históricos e o algoritmo estima as regras. Os três paradigmas clássicos, que estudaremos na Unidade 4:

- Supervisionado: aprende de exemplos rotulados. Inclui classificação (prever categoria: o aluno será aprovado?) e regressão (prever valor numérico: qual será a nota de matemática?);
- Não supervisionado: encontra estrutura em dados sem rótulo. Inclui agrupamento ( clustering ): existem "perfis" naturais de escolas no RN com características semelhantes?;
- Por  reforço: um  agente  aprende  por  tentativa  e  erro,  recebendo  recompensas  -  base  de sistemas de recomendação dinâmicos e jogos (citado aqui por completude; não será foco da disciplina).

Vale  posicionar  também  a Inteligência  Artificial :  IA  é  o  campo  amplo  de  sistemas  que  exibem comportamento  inteligente;  ML  é  hoje  sua  principal  abordagem;  e deep  learning (redes  neurais profundas) é uma família de técnicas de ML. A Ciência de Dados usa ML/IA como ferramenta, mas não se reduz a elas - grande parte do valor de um projeto vem de análises estatísticas bem-feitas e comunicadas.

## 2.4 Resumo comparativo

| BI                           |                                               | Ciência de Dados                        | ML                |
|------------------------------|-----------------------------------------------|-----------------------------------------|-------------------|
| O que aconteceu              | Por quê / o que acontecerá / o que fazer      | Aprender padrões a partir de exemplos   | Foco              |
| Conhecidas de antemão        | Abertas e exploratórias                       | Definidas pela tarefa (T)               | Perguntas         |
| Agregações, indicadores, ETL | Hipóteses, experimentos, modelos estatísticos | Treinamento de algoritmos               | Método típico     |
| Dashboards, relatórios       | Análises, modelos, decisões                   | Modelos preditivos                      | Saída típica      |
| Painel de médias por escola  | Que fatores explicam o desempenho?            | Prever nota a partir do perfil do aluno | Exemplo (ENEM RN) |

Síntese: BI descreve com perguntas fechadas; a Ciência de Dados investiga com perguntas abertas e cobre os quatro níveis de análise;  o  ML  é  o  ferramental  que ela emprega quando a resposta exige aprender padrões dos dados.

## 3. Perfis Profissionais e Mercado

A  área  de  dados se organizou em papéis complementares . Em equipes pequenas (startups, setores públicos enxutos), uma mesma pessoa acumula vários deles; em organizações maduras, são funções distintas com trilhas de carreira próprias. Conhecer os perfis ajuda você a se localizar profissionalmente e a entender como projetos reais são divididos.

## 3.1 Analista de Dados

Explora dados e produz análises e painéis para responder perguntas de negócio . É frequentemente a porta de entrada da carreira e o perfil mais demandado em volume de vagas.

- Responsabilidades típicas: levantar requisitos com  as áreas, consultar bases, construir indicadores, criar dashboards, redigir relatórios analíticos;
- Competências: SQL  (essencial),  planilhas  avançadas,  ferramentas  de  visualização  (Power  BI, Tableau, Looker), estatística descritiva, comunicação com público não técnico;
- No  projeto  ENEM/RN: seria  quem  constrói  o  painel  de  médias  por  escola  e  município  e responde a perguntas como "quais municípios melhoraram em relação a 2024?".

## 3.2 Cientista de Dados

Formula  hipóteses,  desenha  experimentos  e  constrói modelos  estatísticos  e  de  ML .  Vai  além  do descritivo: quantifica incertezas, testa relações causais e produz predições.

- Responsabilidades  típicas: traduzir  problemas  de  negócio  em  problemas  de  modelagem, explorar dados, treinar e validar modelos, comunicar resultados com rigor;
- Competências: Python ou R, estatística inferencial (testes de hipótese, intervalos de confiança), aprendizado de máquina, experimentação (testes A/B);
- No projeto ENEM/RN: seria quem investiga que fatores explicam as diferenças entre escolas e constrói um modelo que prevê a nota a partir do perfil do aluno.

## 3.3 Engenheiro de Dados

Constrói  e  mantém  a infraestrutura que  coleta,  armazena  e  disponibiliza  dados  com  qualidade  e escala. É o alicerce invisível: sem dados confiáveis e acessíveis, analistas e cientistas não trabalham.

- Responsabilidades típicas: pipelines de ingestão (ETL/ELT), bancos de dados, data lakes e data warehouses , qualidade e governança de dados, automação;
- Competências: engenharia de software, SQL avançado, sistemas distribuídos (Spark), orquestradores (Airflow), computação em nuvem;
- No  projeto  ENEM/RN: seria  quem  automatiza  o  download  anual  dos  microdados  do  INEP, padroniza codificações e disponibiliza as tabelas prontas para análise.

## 3.4 Engenheiro de Machine Learning (MLOps)

Leva  modelos  à produção :  um  modelo  que  só  funciona  no  notebook  do  cientista  não  gera  valor contínuo.  O  engenheiro  de  ML  cuida  de  versionamento  de  modelos  e  dados,  monitoramento  de desempenho em produção (o modelo degrada com o tempo?), escalabilidade e reprodutibilidade - disciplina conhecida como MLOps , análoga ao DevOps do software.

No  projeto  ENEM/RN: se  o  modelo  preditivo  de  desempenho  fosse  incorporado  a  um  sistema  da secretaria  de  educação,  seria  esse  perfil  quem  o  manteria  funcionando, monitorado e atualizado a cada edição do exame.

## 3.5 Especialista de domínio

Conhece profundamente o  problema (educação,  saúde,  indústria,  finanças)  e  valida  se  as  análises fazem sentido. É um papel frequentemente subestimado - e essencial. No nosso caso, um educador ou  gestor  escolar  saberia  apontar,  por  exemplo,  que  comparar  a  média  de  uma  escola  com  8 participantes  à  de  uma  com  300  é  injusto,  ou  que  escolas  que  selecionam  alunos  por  prova  de admissão partem de outro patamar. Sem esse olhar, o cientista de dados corre o risco de produzir conclusões estatisticamente corretas e substantivamente erradas.

## 3.6 Síntese dos perfis

| Perfil                  | Pergunta que responde                 | Ferramentas típicas                 | Entrega típica                    |
|-------------------------|---------------------------------------|-------------------------------------|-----------------------------------|
| Analista de Dados       | O que os dados mostram?               | SQL, Excel, Power BI/Tableau        | Dashboards, relatórios            |
| Cientista de Dados      | Por quê? O que acontecerá?            | Python/R, scikit-learn, estatística | Análises, modelos, experimentos   |
| Engenheiro de Dados     | Como disponibilizar dados confiáveis? | SQL, Spark, Airflow, nuvem          | Pipelines, data warehouse         |
| Engenheiro de ML        | Como manter modelos em produção?      | Docker, MLflow, CI/CD, nuvem        | Modelos versionados e monitorados |
| Especialista de domínio | Isso faz sentido na prática?          | Conhecimento do negócio             | Validação, contexto, perguntas    |

## 3.7 Competências transversais

Independentemente do papel, três competências atravessam toda a área:

- Pensamento crítico: desconfiar dos dados (de onde vieram? o que não está registrado?) e das próprias  conclusões  (correlação  não  é  causalidade;  amostras  pequenas  enganam;  vieses  de

coleta  distorcem).  O  bom  profissional  procura ativamente razões pelas quais sua análise pode estar errada;

- Comunicação: traduzir  análise  em  decisão.  Um  resultado  que  o  gestor  não  entende  é  um resultado que não existe. Envolve visualização honesta, escrita clara e adequação da linguagem ao público;
- Ética: privacidade (a LGPD - Lei Geral de Proteção de Dados - regula o tratamento de dados pessoais  no  Brasil),  viés  algorítmico  (modelos  podem  perpetuar  desigualdades  presentes  nos dados  históricos)  e  uso  responsável  de  resultados  (um  ranking  de  escolas  pode  informar políticas ou estigmatizar comunidades - tema da Unidade 5).

## 3.8 No contexto desta disciplina

Você exercitará  principalmente  os  papéis  de analista e cientista de dados , percorrendo o processo completo: coleta (Unidade 2), preparação (Unidade 2), análise exploratória (Unidade 3), modelagem (Unidade 4) e comunicação (Unidade 5). As atividades de engenharia aparecerão em escala didática - ler arquivos, integrar fontes, organizar o projeto - suficiente para você compreender o trabalho dos demais perfis.

## 4. O Ciclo de Vida: CRISP-DM

Projetos de dados não são lineares nem improvisados: seguem um ciclo . O modelo mais difundido é o CRISP-DM ( Cross-Industry Standard Process for Data Mining ), criado no fim dos anos 1990 por um consórcio de empresas europeias e até hoje o padrão de fato da indústria. Ele organiza o trabalho em seis  fases  iterativas -  é  comum (e  esperado)  voltar  a  fases  anteriores  à  medida  que  se  aprende sobre  o  problema.  Existem  alternativas  (KDD,  SEMMA,  e  processos  modernos  como  o  TDSP  da Microsoft), mas todas compartilham a mesma espinha dorsal.

## 4.1 Fase 1 - Entendimento do negócio

Tudo começa com a pergunta: qual decisão será apoiada? Nesta fase definem-se objetivos, critérios de sucesso, restrições e riscos. É a fase mais barata de corrigir - e a mais cara de errar: um projeto que parte da pergunta errada desperdiça todas as fases seguintes.

- Perguntas-guia: quem usará o resultado? Que decisão mudará? Como saberemos que o projeto teve sucesso?
- No nosso caso: "Como se distribuem os desempenhos das escolas do RN no ENEM 2025, por escola, município e dependência administrativa (federal, estadual, municipal, privada)?"

## 4.2 Fase 2 - Entendimento dos dados

Que  dados  existem?  Qual  sua origem,  cobertura  e  qualidade ?  Nesta  fase  coletam-se  os  dados iniciais, descreve-se cada campo (o dicionário de dados ), verificam-se volumes, formatos e problemas evidentes.  Descobertas  aqui  frequentemente  obrigam  a  rever  a  fase  1  -  talvez  os  dados  não permitam responder à pergunta original.

- Perguntas-guia: quem coletou e por quê? O que cada coluna significa? Há valores ausentes? A cobertura é completa?
- No  nosso  caso: microdados  do  ENEM (INEP) com um registro por participante + catálogo de escolas.  Descobrimos,  por  exemplo,  que  os  dois  arquivos  têm  separadores  e  codificações diferentes, e que nem todo participante tem código de escola.

## 4.3 Fase 3 - Preparação dos dados

Limpeza, tratamento de valores ausentes, conversões de tipo, junções e agregações. É a fase menos glamourosa e a mais longa: estudos e pesquisas com profissionais estimam que consome 60-80% do esforço de um projeto típico. A qualidade do que sai daqui determina o teto de qualidade de tudo o que vem depois - vale o ditado garbage in, garbage out .

- Atividades  típicas: remover  ou  imputar  ausentes,  padronizar  categorias,  converter  texto  em número, integrar fontes por chaves comuns, criar variáveis derivadas.
- No  nosso  caso: descartar  registros  sem  escola,  tratar  notas  vazias  (alunos  faltosos),  juntar resultados com o catálogo de nomes de escolas pela chave CO\_ESCOLA .

## 4.4 Fase 4 - Modelagem

Aplicar  técnicas  estatísticas  ou  de  ML  aos dados preparados. Importante: em análises descritivas, a "modelagem" pode ser simplesmente a definição  de  métricas - decidir como medir já é modelar. Escolher  entre  "média  das  notas  válidas  por  aluno"  e  "média  apenas  de quem fez as duas provas" muda os resultados; a escolha deve ser explícita e justificada.

- No nosso caso: definimos a média geral por aluno (média das notas válidas nas quatro provas objetivas e redação) e, a partir dela, a média por escola e o ranking.

## 4.5 Fase 5 - Avaliação

Os resultados respondem à pergunta da fase 1? Há vieses, erros ou limitações que comprometem as conclusões? Esta fase avalia o resultado sob a ótica do negócio, não apenas da técnica - um modelo com boa acurácia pode ainda assim ser inútil ou perigoso para a decisão em questão.

- No nosso caso: comparar  médias  sem  considerar  o  número  de  participantes  por  escola pode enganar - uma escola com 5 alunos excelentes "vence" uma escola sólida com 300. Também discutiremos o efeito do recorte "melhores N alunos" sobre o ranking.

## 4.6 Fase 6 - Implantação

Entregar  valor:  relatório,  painel, aplicação ou modelo em produção. A implantação varia do simples (um  PDF  bem  escrito)  ao  complexo  (um  sistema  com  predições  em  tempo  real).  Inclui  também documentação e um plano de manutenção - dados mudam, e análises envelhecem.

- No nosso caso: uma página HTML interativa com o ranking das escolas, filtros por dependência administrativa e município.

## 4.7 Visão de conjunto

| Fase          | Pergunta central        | Entregável típico                  | No projeto ENEM/RN                                   |
|---------------|-------------------------|------------------------------------|------------------------------------------------------|
| 1. Negócio    | Qual é a pergunta?      | Objetivos e critérios de sucesso   | Distribuição do desempenho por escola/município/rede |
| 2. Dados      | O que temos?            | Dicionário e diagnóstico dos dados | Microdados INEP + catálogo de escolas                |
| 3. Preparação | Como limpar e integrar? | Base analítica pronta              | Filtrar, converter notas, juntar por CO_ESCOLA       |
| 4. Modelagem  | Como medir/modelar?     | Métricas e/ou modelos              | Média por aluno; média e ranking por escola          |
| 5. Avaliação  | Respondemos bem?        | Análise crítica e limitações       | Efeito do porte da escola e dos recortes             |

| 6. Implantação   | Como entregar valor?   | Relatório/painel/aplicaçã o   | Página HTML interativa com filtros   |
|------------------|------------------------|-------------------------------|--------------------------------------|

## 5. Ferramentas do Ecossistema

O  ecossistema  de  Ciência  de  Dados  é  amplo  e  muda  rapidamente;  nomes  de  ferramentas envelhecem, mas as categorias permanecem. Nesta disciplina usaremos o "kit padrão" baseado em Python -  hoje  a  linguagem dominante na área, pela combinação de sintaxe acessível, ecossistema maduro  de  bibliotecas  e  comunidade  enorme.  (O  principal  "concorrente", R ,  permanece forte  em estatística  acadêmica; SQL não  é  concorrente,  e  sim  complemento  indispensável  para  consultar bancos de dados.)

## 5.1 Linguagem e ambiente

- Python  3.10+ -  linguagem  principal  do  curso.  Interpretada,  multiparadigma,  com  biblioteca padrão rica.  Seu  papel  na CD: expressar todo o processo (coleta, preparação, análise, modelo, entrega) em código legível e reprodutível;
- Jupyter  Notebook/Lab -  documentos  interativos  que  misturam  código,  resultados  e  texto narrativo: o "caderno de laboratório" do  cientista de  dados.  Ideal  para  exploração  e comunicação de análises; menos adequado para código de produção;
- VS Code - editor com excelente suporte a Python, notebooks e scripts; será nosso ambiente de referência;
- Git (GitHub/GitLab) - versionamento de todo o material produzido. Em CD, versionar é parte do método científico: permite reproduzir qualquer análise passada e trabalhar em equipe sem conflitos.

## 5.2 Bibliotecas principais

| Biblioteca                    | Para quê serve                                                                | Exemplo de uso na disciplina                                    |
|-------------------------------|-------------------------------------------------------------------------------|-----------------------------------------------------------------|
| NumPy                         | Arrays e computação numérica vetorizada - a fundação numérica do ecossistema. | Operações rápidas sobre as 30 mil notas sem laços explícitos.   |
| Pandas                        | DataFrames: leitura, filtragem, agregação e junção de dados tabulares.        | Ler os CSVs do ENEM, agrupar por escola, juntar com o catálogo. |
| Matplotlib / Seaborn / Plotly | Visualização estática (Matplotlib/Seaborn) e interativa (Plotly).             | Histogramas de notas, boxplots por rede, mapas interativos.     |
| Scikit-learn                  | Aprendizado de máquina: classificação, regressão, agrupamento, validação.     | Modelos preditivos de desempenho (Unidade 4).                   |

| Requests / BeautifulSoup4   | Coleta via APIs HTTP e web scraping de páginas.   | Consumir APIs do IBGE; extrair tabelas de páginas públicas (Unidade 2).   |
|-----------------------------|---------------------------------------------------|---------------------------------------------------------------------------|
| Streamlit                   | Dashboards e aplicações de dados em Python puro.  | Publicar o ranking como aplicação interativa (Unidade 5).                 |

## 5.3 A biblioteca padrão também resolve

Nem tudo exige bibliotecas externas. O exemplo prático desta aula usa apenas a biblioteca padrão do Python - csv , json , statistics , pathlib - para processar 30 mil registros e gerar uma página HTML interativa. Alguns motivos pedagógicos e práticos:

- Entender o que Pandas faz "por baixo" torna você um usuário melhor de Pandas;
- Scripts  sem  dependências  rodam  em  qualquer  máquina  com  Python  -  útil  em  ambientes restritos;
- Para  volumes moderados (dezenas de milhares de linhas), a biblioteca padrão é perfeitamente adequada.

## 5.4 Montando seu ambiente

Para  acompanhar a disciplina, você precisará de: Python 3.10 ou superior; VS Code com a extensão Python; Git.  Recomenda-se criar um ambiente virtual por  projeto  ( python -m venv .venv )  para isolar  dependências,  instalando  bibliotecas com pip install pandas matplotlib . Quem preferir uma instalação "tudo em um" pode usar a distribuição Anaconda .

## 6. Estudo de Caso: Ranking das Escolas do RN (ENEM 2025)

Para  tornar  os conceitos concretos, esta aula traz um estudo de caso completo com dados reais: os microdados  do  ENEM  2025  das  escolas  do  Rio  Grande  do  Norte.  Ele  percorre  as  seis  fases  do CRISP-DM em miniatura e será retomado (e refinado) ao longo de toda a disciplina.

## 6.1 O problema (fase 1)

## Como se distribui o desempenho das escolas do RN no ENEM 2025, por escola, município e dependência administrativa (federal, estadual, municipal, privada)?

Note  as  características  de  uma  boa  pergunta  inicial:  é  específica  (RN,  2025),  tem  dimensões  de análise  claras  (escola,  município,  rede)  e  apoia  decisões  reais  (gestão  educacional,  escolha  de políticas).  Compare  com  uma  pergunta  vaga  como  "analisar  o  ENEM"  -  impossível  saber  quando terminamos.

## 6.2 Os dados (fase 2)

Trabalharemos com dois arquivos:

- `RESULTADOS\_2025\_RN.csv` -  microdados  com um  registro  por  participante :  código  da escola,  município,  presença  e  notas  das  quatro provas objetivas - Ciências da Natureza (CN), Ciências Humanas (CH), Linguagens e Códigos (LC), Matemática (MT) - e da redação. Cerca de 30 mil registros , separados por ; , codificação latin1 ;
- `catalogo\_escolas\_rn.csv` - catálogo com código ( CO\_ESCOLA ) e nome ( NO\_ESCOLA ) de cerca de 5 mil escolas , separado por vírgula, codificação utf-8 .

Observe: fontes diferentes, formatos diferentes. Separador ( ; vs , ) e codificação ( latin1 vs utf-8 ) distintos  são  o  cotidiano  de  quem  integra  dados  reais  -  e  a  primeira  armadilha  prática:  ler  um arquivo latin1 como utf-8 corrompe acentos ("São Gonçalo" vira "SÃ£o GonÃ§alo"). Integrar as duas fontes exige uma chave comum : o código da escola.

## 6.3 Preparação e métricas (fases 3 e 4)

O roteiro de processamento, passo a passo:

1. Ler os resultados, descartando  registros  sem  código  de  escola (participantes  que  não informaram ou concluíram há muitos anos);
2. Converter notas para número ,  tratando  valores  ausentes - alunos faltosos têm nota vazia, e tratar vazio como zero distorceria todas as médias;
3. Calcular a média geral por aluno - média das notas válidas de cada participante;
4. Agrupar  alunos  por  escola e  juntar  com  o  catálogo  (pela  chave CO\_ESCOLA )  para  obter  os nomes;
5. Ordenar alunos e escolas - o ranking.

Em código (usando apenas a biblioteca padrão - ilustrativo, simplificado):

```
import csv from statistics import mean alunos = [] with open('RESULTADOS_2025_RN.csv', encoding='latin1') as f: for linha in csv.DictReader(f, delimiter=';'): if not linha['CO_ESCOLA']: continue                      # passo 1: descartar sem escola notas = [float(linha[c]) for c in ('NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO') if linha[c]]              # passo 2: ignorar notas vazias if notas: alunos.append({'escola': linha['CO_ESCOLA'], 'media': mean(notas)})   # passo 3 por_escola = {} for a in alunos:                          # passo 4: agrupar por escola por_escola.setdefault(a['escola'], []).append(a['media']) ranking = sorted(((cod, mean(ms), len(ms)) for cod, ms in por_escola.items()), key=lambda x: x[1], reverse=True)   # passo 5
```

Cada  linha  desse  script  materializa  uma decisão  metodológica tomada  nas  fases  3  e  4:  o  que descartar,  como tratar ausentes, o que exatamente "média" significa. Decisões diferentes produzem rankings diferentes - por isso devem ser documentadas.

## 6.4 Avaliação e implantação (fases 5 e 6)

O  resultado  é  uma página  HTML  interativa com  o  ranking  das  escolas  e  filtros  por  dependência administrativa e município. Ao analisá-la, discutiremos em sala três questões críticas:

- Médias  de  escolas  com  poucos  participantes  são  comparáveis  às  de  escolas  grandes? Amostras pequenas têm variância alta: uma escola com 5 alunos pode aparecer no topo (ou no fundo) por puro acaso. Soluções possíveis: exigir um número mínimo de participantes, reportar o N junto da média, ou usar métodos de suavização;
- O que o recorte "melhores N alunos" muda no ranking? Rankings divulgados na imprensa às vezes  usam  apenas  os  melhores  alunos  de  cada  escola,  o  que  favorece  escolas  grandes  e seletivas.  A  escolha  do  recorte  é  uma  decisão editorial com  consequências  -  e  deve  ser transparente;
- Que  cuidados  éticos  um  ranking  de  escolas  exige? O  ENEM mede desempenho de alunos, influenciado por fatores socioeconômicos que a escola não controla. Um ranking ingênuo pode estigmatizar  comunidades  e  punir  escolas  que  atendem  populações  vulneráveis.  Além  disso, microdados exigem cuidado com reidentificação de indivíduos (LGPD) - mesmo "anonimizados", registros detalhados podem identificar pessoas em escolas pequenas.

Essas três discussões ilustram a fase 5 (avaliação) em ação: a técnica produz o ranking; o julgamento crítico decide o que ele significa e como pode ser usado com responsabilidade .

Próximo passo: explore a seção Exemplo Prático desta aula no AVA, baixe os microdados e execute o código você mesmo.

## 7. Síntese

- Ciência  de  Dados  é  um processo interdisciplinar  (estatística  +  computação  +  domínio)  para responder  perguntas  e  apoiar  decisões  com  dados  -  não  uma  ferramenta  ou  tecnologia específica;
- Dado → informação → conhecimento: o valor cresce à medida que o contexto e a capacidade de orientar decisão aumentam;
- BI  descreve  o passado com perguntas conhecidas; a CD cobre os níveis descritivo, diagnóstico, preditivo e prescritivo; o ML é o ferramental de aprendizado de padrões usado dentro da CD;
- A  área  se  organiza  em  perfis  complementares  -  analista,  cientista,  engenheiro  de  dados, engenheiro de ML, especialista de domínio - unidos por pensamento crítico, comunicação e ética;
- O CRISP-DM organiza projetos em seis fases iterativas; a preparação de dados consome 60-80% do esforço típico;
- O  ecossistema  Python  (Jupyter,  NumPy,  Pandas,  Matplotlib,  scikit-learn … )  é  o  kit  padrão  da disciplina - mas a ferramenta é consequência do problema, nunca o ponto de partida;
- O estudo de caso ENEM 2025/RN mostra o ciclo completo em miniatura e revela que decisões metodológicas e éticas são inseparáveis da técnica.

## 8. Exercícios e questões para estudo

## 8.1 Fixação

1. Defina Ciência de Dados com suas palavras, destacando por que ela é um processo e não uma ferramenta.
2. Classifique  cada  item  como dado, informação ou conhecimento: (a) "652,3" em uma célula de CSV; (b) "a média de redação do RN em 2025 foi 652,3"; (c) "escolas com laboratório de redação elevam a nota média em X pontos, portanto vale investir neles".
3. Para cada  pergunta  abaixo,  indique  o  nível  de  análise  (descritiva,  diagnóstica,  preditiva, prescritiva): (a) Quantos alunos faltaram à prova de matemática? (b) Qual escola devo reforçar para  maximizar  o  impacto?  (c)  Por  que  as  escolas  do  interior tiveram média menor? (d) Qual será a nota média do RN em 2026?
4. Diferencie  BI,  Ciência  de  Dados  e  ML  usando  um  exemplo  do  contexto  escolar  diferente  dos apresentados no texto.
5. Associe  cada  atividade  ao  perfil  profissional  mais  adequado:  (a)  criar  o  pipeline  que  baixa os microdados todo ano; (b) construir o painel de médias por município; (c) treinar o modelo que prevê a nota; (d) apontar que escolas com prova de admissão não são comparáveis às demais; (e) monitorar o modelo em produção.
6. No script  do estudo de caso, o que aconteceria com o ranking se notas vazias fossem tratadas como zero em vez de ignoradas? Justifique.

## 8.2 Discussão

1. Um  jornal  publica  um  ranking  das  "10  melhores  escolas  do  RN"  usando  a  média  dos  30 melhores  alunos  de  cada  escola.  Analise  criticamente  essa  metodologia:  quem  ela  favorece? Que informação deveria acompanhar o ranking?
2. O diagrama de Conway situa a CD na interseção de três competências. Em qual delas você está mais forte hoje? Que plano de estudo fecharia suas lacunas ao longo da disciplina?
3. "Com dados suficientes, os números falam por si." Argumente contra essa afirmação usando conceitos desta aula (vieses, decisões metodológicas, papel do especialista de domínio).
4. Que  riscos  à  privacidade  (LGPD)  existem  ao  divulgar  microdados  educacionais  mesmo  sem nomes? Considere escolas pequenas do interior.

## 9. Glossário

- CRISP-DM: Processo padrão de seis fases para projetos de mineração/ciência de dados.
- Dado estruturado: Dado organizado em linhas e colunas com esquema fixo (tabelas, CSV).
- DataFrame: Estrutura tabular em memória (linhas × colunas) da biblioteca Pandas.
- Data warehouse: Repositório analítico que consolida dados históricos para consulta (OLAP).
- Dicionário de dados: Documento que descreve o significado, tipo e domínio de cada campo de uma base.
- ETL/ELT: Extração,  transformação  e  carga  -  processo  de  mover  e  preparar  dados  entre sistemas.
- LGPD: Lei  Geral  de  Proteção  de  Dados  (Lei  13.709/2018)  -  regula  o  tratamento  de  dados pessoais no Brasil.
- Microdados: Dados  no  nível  do  registro  individual  (um  participante,  uma  internação),  sem agregação.
- MLOps: Práticas para levar e manter modelos de ML  em  produção (versionamento, monitoramento, escala).
- OLTP / OLAP: Sistemas transacionais do dia a dia / estruturas otimizadas para consulta analítica.
- Pipeline: Sequência automatizada de etapas de processamento de dados.
- Viés: Distorção sistemática nos dados ou na análise que compromete conclusões.
- Web scraping: Extração automatizada de dados de páginas web.

## 10. Referências e leituras recomendadas

- PROVOST,  F.;  FAWCETT,  T. Data  Science  para  Negócios .  Alta  Books,  2016.  (Capítulos  1-2: excelente para a visão de processo e valor de negócio.)
- GRUS, J. Data Science do Zero . 2. ed. Alta Books, 2021. (Constrói as ferramentas "na mão", no espírito da nossa biblioteca padrão.)
- McKINNEY, W. Python para Análise de  Dados . 3. ed. Novatec, 2023. (Referência de Pandas/NumPy, escrita pelo criador do Pandas.)
- VANDERPLAS, J. Python Data Science Handbook . 2. ed. O'Reilly, 2023. Disponível gratuitamente online.
- DAVENPORT, T.; PATIL, D.J. Data Scientist: The Sexiest Job of the 21st Century. Harvard Business Review , out. 2012.
- CHAPMAN, P. et al. CRISP-DM 1.0: Step-by-step data mining guide . SPSS, 2000.
- INEP - Microdados do ENEM: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados
- Portal Brasileiro de Dados Abertos: https://dados.gov.br
- BRASIL. Lei nº 13.709/2018 (LGPD).