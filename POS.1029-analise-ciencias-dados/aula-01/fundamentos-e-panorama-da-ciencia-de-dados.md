# **Title:** Tópicos de Estudo — Fundamentos e Panorama da Ciência de Dados

**Source:** [https://presencial.ava.ifrn.edu.br/mod/book/tool/print/index.php?id=67908](https://presencial.ava.ifrn.edu.br/mod/book/tool/print/index.php?id=67908)

---

## Sumário

- [**Title:** Tópicos de Estudo — Fundamentos e Panorama da Ciência de Dados](#title-tópicos-de-estudo--fundamentos-e-panorama-da-ciência-de-dados)
  - [Sumário](#sumário)
  - [Descrição](#descrição)
  - [1. Capítulo 1 — O que é Ciência de Dados?](#1-capítulo-1--o-que-é-ciência-de-dados)
      - [Uma definição de trabalho](#uma-definição-de-trabalho)
      - [Dado, informação e conhecimento](#dado-informação-e-conhecimento)
      - [Por que agora?](#por-que-agora)
  - [2. Capítulo 2 — Ciência de Dados, BI e Aprendizado de Máquina](#2-capítulo-2--ciência-de-dados-bi-e-aprendizado-de-máquina)
      - [Business Intelligence (BI)](#business-intelligence-bi)
      - [Ciência de Dados (CD)](#ciência-de-dados-cd)
      - [Aprendizado de Máquina (ML)](#aprendizado-de-máquina-ml)
      - [Resumo comparativo](#resumo-comparativo)
  - [3. Capítulo 3 — Perfis Profissionais e Mercado](#3-capítulo-3--perfis-profissionais-e-mercado)
      - [Competências transversais](#competências-transversais)
      - [No contexto desta disciplina](#no-contexto-desta-disciplina)
  - [4. Capítulo 4 — O Ciclo de Vida: CRISP-DM](#4-capítulo-4--o-ciclo-de-vida-crisp-dm)
  - [5. Capítulo 5 — Ferramentas do Ecossistema](#5-capítulo-5--ferramentas-do-ecossistema)
      - [Linguagem e ambiente](#linguagem-e-ambiente)
      - [Bibliotecas principais](#bibliotecas-principais)
      - [A biblioteca padrão também resolve](#a-biblioteca-padrão-também-resolve)
  - [6. Capítulo 6 — Estudo de Caso: Ranking das Escolas do RN (ENEM 2025)](#6-capítulo-6--estudo-de-caso-ranking-das-escolas-do-rn-enem-2025)
      - [O problema (fase 1 do CRISP-DM)](#o-problema-fase-1-do-crisp-dm)
      - [Os dados (fase 2)](#os-dados-fase-2)
      - [Preparação e métricas (fases 3 e 4)](#preparação-e-métricas-fases-3-e-4)
      - [Avaliação e implantação (fases 5 e 6)](#avaliação-e-implantação-fases-5-e-6)

---

<table><tbody><tr><td>Site:</td><td>AVA-Presencial</td></tr><tr><td>Curso:</td><td>Análise e Ciência de Dados</td></tr><tr><td>Livro:</td><td>Tópicos de Estudo — Fundamentos e Panorama da Ciência de Dados</td></tr></tbody></table>

<table><tbody><tr><td>Impresso por:</td><td>Iuri Guerra de Freitas Pereira</td></tr><tr><td>Data:</td><td>domingo, 27 set. 2026, 22:56</td></tr></tbody></table>

## Descrição

Conteúdo teórico da Aula 01 em formato de livro: o que é Ciência de Dados, diferenças entre CD, BI e ML, perfis profissionais, ciclo de vida CRISP-DM, ferramentas do ecossistema e o estudo de caso do ranking das escolas do RN.

## 1\. Capítulo 1 — O que é Ciência de Dados?

A **Ciência de Dados** (Data Science) é o campo interdisciplinar que combina **estatística**, **computação** e **conhecimento de domínio** para extrair conhecimento e apoiar decisões a partir de dados. Ela nasce da confluência de três movimentos: o barateamento do armazenamento, a explosão na geração de dados (web, sensores, sistemas transacionais, redes sociais) e o amadurecimento de algoritmos de aprendizado.

#### Uma definição de trabalho

> _Ciência de Dados é o processo sistemático de coletar, preparar, explorar, modelar e comunicar dados para responder perguntas e apoiar decisões._

Repare que a definição descreve um **processo**, não uma ferramenta. Programar em Python ou usar um algoritmo de ML são meios; o fim é **responder uma pergunta relevante com evidências extraídas de dados**.

#### Dado, informação e conhecimento

- **Dado:** registro bruto, sem interpretação (ex.: a linha de um aluno no CSV do ENEM com suas notas).
- **Informação:** dado contextualizado (ex.: a média de matemática de uma escola em 2025).
- **Conhecimento:** padrão ou relação que apoia decisão (ex.: escolas de determinado perfil apresentam desempenho sistematicamente maior — o que orienta políticas públicas).

#### Por que agora?

Órgãos públicos brasileiros publicam **dados abertos** em larga escala (INEP, IBGE, DataSUS, dados.gov.br). Só os microdados do ENEM contêm milhões de registros por edição — matéria-prima abundante para análise. Ao longo desta disciplina usaremos um recorte real: os resultados do **ENEM 2025 no Rio Grande do Norte**.

## 2\. Capítulo 2 — Ciência de Dados, BI e Aprendizado de Máquina

Três termos aparecem juntos com frequência e é importante distingui-los.

#### Business Intelligence (BI)

O BI é voltado ao **passado e ao presente**: consolida dados de sistemas transacionais em painéis e relatórios que descrevem _o que aconteceu_ (vendas do trimestre, evasão do semestre, média das escolas). As perguntas são conhecidas de antemão e as respostas são agregações e indicadores.

#### Ciência de Dados (CD)

A CD engloba o descritivo, mas avança para o **diagnóstico, a predição e a prescrição**: _por que aconteceu? o que tende a acontecer? o que devemos fazer?_ Envolve formulação de hipóteses, experimentação e modelagem estatística — inclusive quando a pergunta ainda não está bem definida.

#### Aprendizado de Máquina (ML)

O ML é um **conjunto de técnicas** usado dentro da CD: algoritmos que aprendem padrões a partir de exemplos, sem serem explicitamente programados para cada regra. Classificação, regressão e agrupamento são suas tarefas clássicas — serão vistas na Unidade 4.

#### Resumo comparativo

|                       | BI                          | Ciência de Dados                   | ML                             |
| --------------------- | --------------------------- | ---------------------------------- | ------------------------------ |
| **Foco**              | O que aconteceu             | Por quê / o que acontecerá         | Aprender padrões               |
| **Perguntas**         | Conhecidas                  | Abertas e exploratórias            | Definidas pela tarefa          |
| **Saída típica**      | Dashboards, relatórios      | Análises, modelos, decisões        | Modelos preditivos             |
| **Exemplo (ENEM RN)** | Painel de médias por escola | Que fatores explicam o desempenho? | Prever nota a partir do perfil |

## 3\. Capítulo 3 — Perfis Profissionais e Mercado

A área de dados se organizou em papéis complementares. Em equipes pequenas uma mesma pessoa acumula vários deles; em organizações maduras, são funções distintas.

- **Analista de Dados:** explora dados e produz análises e painéis para responder perguntas de negócio. Domina SQL, planilhas, visualização e estatística descritiva.
- **Cientista de Dados:** formula hipóteses, desenha experimentos e constrói modelos estatísticos/ML. Domina Python/R, estatística inferencial e aprendizado de máquina.
- **Engenheiro de Dados:** constrói e mantém a infraestrutura que coleta, armazena e disponibiliza dados (pipelines, bancos, data lakes). Domina engenharia de software e sistemas distribuídos.
- **Engenheiro de ML (MLOps):** leva modelos à produção com monitoramento, versionamento e escala.
- **Especialista de domínio:** conhece profundamente o problema (educação, saúde, indústria) e valida se as análises fazem sentido — papel frequentemente subestimado e essencial.

#### Competências transversais

Independentemente do papel: **pensamento crítico** (desconfiar dos dados e das próprias conclusões), **comunicação** (traduzir análise em decisão) e **ética** (privacidade, viés, uso responsável — tema da Unidade 5).

#### No contexto desta disciplina

Você exercitará principalmente os papéis de _analista_ e _cientista de dados_: coleta (U2), preparação (U2), análise exploratória (U3), modelagem (U4) e comunicação (U5).

## 4\. Capítulo 4 — O Ciclo de Vida: CRISP-DM

Projetos de dados seguem um ciclo. O modelo mais difundido é o **CRISP-DM** (_Cross-Industry Standard Process for Data Mining_), com seis fases **iterativas** — é comum voltar a fases anteriores à medida que se aprende sobre o problema.

1.  **Entendimento do negócio:** qual é a pergunta? Que decisão será apoiada? Ex.: _"como se distribuem os desempenhos das escolas do RN no ENEM 2025 por dependência administrativa?"_
2.  **Entendimento dos dados:** que dados existem? Qual sua origem, cobertura e qualidade? Ex.: microdados do ENEM (INEP) + catálogo de escolas.
3.  **Preparação dos dados:** limpeza, tratamento de ausentes, junções e agregações — tipicamente 60–80% do esforço do projeto. Ex.: descartar registros sem escola, tratar notas vazias, juntar resultados com nomes de escolas.
4.  **Modelagem:** aplicar técnicas estatísticas ou de ML. Em análises descritivas, a "modelagem" pode ser a definição de métricas — como a média geral por aluno e o ranking por escola.
5.  **Avaliação:** os resultados respondem à pergunta? Há vieses? Ex.: comparar médias sem considerar o nº de participantes por escola pode enganar.
6.  **Implantação:** entregar valor — relatório, painel, aplicação. Ex.: página HTML interativa com o ranking das escolas.

O exemplo prático desta aula percorre, em miniatura, **todas as seis fases** — do problema à página final.

## 5\. Capítulo 5 — Ferramentas do Ecossistema

O ecossistema de Ciência de Dados é amplo. Nesta disciplina usaremos o "kit padrão" baseado em Python — hoje a linguagem dominante na área.

#### Linguagem e ambiente

- **Python 3.10+** — linguagem principal do curso;
- **Jupyter Notebook/Lab** — documentos interativos que misturam código, resultados e texto: o "caderno de laboratório" do cientista de dados;
- **VS Code** — editor com suporte a notebooks e scripts;
- **Git (GitHub/GitLab)** — versionamento de todo o material produzido.

#### Bibliotecas principais

- **NumPy** — arrays e computação numérica vetorizada;
- **Pandas** — DataFrames: leitura, filtragem, agregação e junção de dados tabulares;
- **Matplotlib / Seaborn / Plotly** — visualização estática e interativa;
- **Scikit-learn** — aprendizado de máquina;
- **Requests / BeautifulSoup4** — coleta via APIs e web scraping;
- **Streamlit** — dashboards e aplicações de dados.

#### A biblioteca padrão também resolve

Nem tudo exige bibliotecas externas: o exemplo desta aula usa apenas **a biblioteca padrão do Python** (`csv`, `json`, `statistics`, `pathlib`) para processar 30 mil registros e gerar uma página HTML interativa. A lição: entenda o problema e os dados primeiro; a ferramenta é consequência.

## 6\. Capítulo 6 — Estudo de Caso: Ranking das Escolas do RN (ENEM 2025)

Para tornar os conceitos concretos, esta aula traz um estudo de caso completo com **dados reais**: os microdados do ENEM 2025 das escolas do Rio Grande do Norte.

#### O problema (fase 1 do CRISP-DM)

_Como se distribui o desempenho das escolas do RN no ENEM 2025, por escola, município e dependência administrativa (federal, estadual, municipal, privada)?_

#### Os dados (fase 2)

- **RESULTADOS\_2025\_RN.csv** — microdados com um registro por participante: escola, município, presença e notas das quatro provas objetivas (CN, CH, LC, MT) e da redação. ~30 mil registros, separados por `;`, codificação `latin1`.
- **catalogo\_escolas\_rn.csv** — catálogo com código (`CO_ESCOLA`) e nome (`NO_ESCOLA`) de ~5 mil escolas, separado por vírgula, codificação `utf-8`.

Observe: fontes diferentes, formatos diferentes. Integrá-las exige uma **chave comum** — o código da escola.

#### Preparação e métricas (fases 3 e 4)

1.  Ler os resultados, descartando registros sem código de escola;
2.  Converter notas para número, tratando valores ausentes (alunos faltosos);
3.  Calcular a **média geral por aluno** (média das notas válidas);
4.  Agrupar alunos por escola e juntar com o catálogo para obter os nomes;
5.  Ordenar alunos e escolas — o ranking.

#### Avaliação e implantação (fases 5 e 6)

O resultado é uma **página HTML interativa** com o ranking das escolas, filtros por tipo e município. Ao analisá-la, discutiremos em sala: médias de escolas com poucos participantes são comparáveis às de escolas grandes? O que o recorte "melhores N alunos" muda no ranking? Que cuidados éticos um ranking de escolas exige?

**Próximo passo:** explore a seção _Exemplo Prático_ desta aula, baixe os microdados e execute o código você mesmo.
