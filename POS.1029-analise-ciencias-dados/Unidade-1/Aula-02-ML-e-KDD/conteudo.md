# Aula 02 — Introdução ao ML e KDD (Teórica)

> Semana de 24/08/2026. Paradigmas de ML: supervisionado, não supervisionado e por reforço; processo KDD; overfitting/underfitting; métricas de avaliação básicas.
> Materiais: livro da aula, exemplo prático de pré-processamento (notebooks KDD passos 1–3 + PDF "Detalhamento Atividade Prática") e formulário avaliativo.

---

# Livro — Tópicos de Estudo

Paradigmas de Aprendizado de Máquina, o processo KDD, overfitting e underfitting, métricas de avaliação básicas e um exemplo prático de classificador construído do zero.

## Capítulo 1 — Paradigmas de Aprendizado de Máquina

Aprendizado de Máquina (ML) é o subcampo da Ciência de Dados em que algoritmos aprendem padrões a partir de exemplos, em vez de seguirem regras explicitamente programadas. Os problemas de ML se organizam em três paradigmas principais.

### Aprendizado Supervisionado

O algoritmo aprende a partir de exemplos **rotulados**: cada entrada vem acompanhada da resposta correta (o "rótulo" ou "target"). O objetivo é aprender uma função que generalize para exemplos novos, ainda não vistos.

- **Classificação:** o rótulo é uma categoria (ex.: escola de desempenho "alto", "médio" ou "baixo").
- **Regressão:** o rótulo é um valor numérico contínuo (ex.: prever a nota média de um aluno).

### Aprendizado Não Supervisionado

Não há rótulos: o algoritmo busca estrutura nos dados por conta própria — grupos de exemplos semelhantes (clustering), redução de dimensionalidade ou padrões de associação. Ex.: agrupar escolas do RN por perfil de desempenho sem informar previamente categorias.

### Aprendizado por Reforço

Um agente aprende por tentativa e erro, interagindo com um ambiente e recebendo recompensas ou penalidades por suas ações — usado em jogos, robótica e sistemas de recomendação adaptativos. Foge do escopo prático desta disciplina, mas é importante reconhecer o paradigma.

### Onde estamos nesta disciplina?

Na Unidade 4 (Aprendizado de Máquina Aplicado) você praticará classificação, regressão e clustering com scikit-learn. Nesta aula, para entender os fundamentos, construiremos um classificador do zero, sem bibliotecas de ML — o KNN.

## Capítulo 2 — O Processo KDD

KDD (Knowledge Discovery in Databases — Descoberta de Conhecimento em Bases de Dados) é o processo mais amplo do qual a Mineração de Dados é apenas uma etapa. Foi formalizado nos anos 1990 e continua sendo a base conceitual por trás de metodologias mais recentes, como o CRISP-DM (Aula 01).

### As cinco etapas do KDD

1. **Seleção:** escolher, dentre todos os dados disponíveis, o subconjunto relevante para o problema. Ex.: dos microdados nacionais do ENEM, selecionar apenas os registros de escolas do RN.
2. **Pré-processamento:** tratar ruído, valores ausentes e inconsistências. Ex.: remover registros sem código de escola; tratar notas vazias de alunos faltosos.
3. **Transformação:** converter os dados para um formato adequado ao algoritmo — normalização, criação de atributos derivados. Ex.: calcular a média geral de cada aluno a partir das cinco notas.
4. **Mineração de Dados:** aplicar algoritmos (classificação, clustering, regras de associação) para extrair padrões. É aqui que entram os algoritmos de ML propriamente ditos.
5. **Interpretação / Avaliação:** validar se os padrões encontrados são úteis, novos e compreensíveis — e não artefatos do processo (ruído ou viés).

### KDD × Mineração de Dados

É comum confundir os dois termos. A Mineração de Dados é a **etapa 4** — a aplicação de algoritmos. O KDD é o **processo completo**, incluindo a preparação cuidadosa que antecede a mineração e a validação que a sucede. Sem essas etapas, um algoritmo sofisticado produz resultados enganosos a partir de dados mal preparados — o princípio conhecido como *garbage in, garbage out*.

## Capítulo 3 — Overfitting e Underfitting

Um modelo de ML não deve apenas memorizar os dados de treino — ele precisa **generalizar** para dados novos. Dois problemas opostos ameaçam essa generalização.

### Overfitting (sobreajuste)

O modelo aprende demais sobre os dados de treino, incluindo seu ruído e suas particularidades — e perde a capacidade de generalizar. Sintoma clássico: desempenho excelente no treino, ruim em dados novos.

*Analogia:* um aluno que decora as respostas de uma prova específica, mas não entende o conteúdo, vai bem naquela prova e mal em qualquer prova diferente.

### Underfitting (subajuste)

O modelo é simples demais para capturar os padrões relevantes dos dados — desempenho ruim tanto no treino quanto em dados novos.

*Analogia:* um aluno que estudou tão pouco que erra tanto na prova de treino quanto em qualquer prova nova.

### Por que separar treino e teste?

Avaliar um modelo apenas nos dados usados para treiná-lo é enganoso — ele pode estar apenas memorizando. Por isso, o procedimento padrão é dividir os dados:

- **Conjunto de treino:** usado para o modelo aprender os padrões.
- **Conjunto de teste:** dados nunca vistos pelo modelo durante o treino, usados apenas para medir sua capacidade de generalização.

### O parâmetro certo

Muitos algoritmos têm um parâmetro que controla a complexidade do modelo — no KNN, por exemplo, o número de vizinhos *k* considerados. Poucos vizinhos (*k* pequeno) tendem a overfitting; muitos vizinhos (*k* grande) tendem a underfitting. Encontrar o equilíbrio é parte do trabalho do cientista de dados.

## Capítulo 4 — Métricas de Avaliação Básicas

### Classificação

- **Acurácia:** proporção de previsões corretas sobre o total. Simples, mas enganosa em bases desbalanceadas (ex.: se 90% das escolas são "médio desempenho", prever sempre "médio" já dá 90% de acurácia sem aprender nada útil).
- **Matriz de confusão:** tabela que cruza classe prevista × classe real, revelando exatamente onde o modelo erra.
- **Precisão e Revocação (precision/recall):** métricas mais robustas para classes desbalanceadas — vistas em detalhe na Unidade 4.

### Regressão

- **Erro Absoluto Médio (MAE):** média das diferenças absolutas entre valor previsto e valor real.
- **Erro Quadrático Médio (RMSE):** penaliza mais fortemente erros grandes, por elevar as diferenças ao quadrado.
- **R² (coeficiente de determinação):** mede a proporção da variação dos dados explicada pelo modelo.

### Neste capítulo, o essencial

No exemplo prático usaremos a acurácia:

```
acurácia = (nº de previsões corretas) / (nº total de previsões no conjunto de teste)
```

Reforçando o Capítulo 3: sempre calcule a métrica no **conjunto de teste**, nunca apenas no treino — senão você mede memorização, não aprendizado.

## Capítulo 5 — Estudo de Caso: KNN do Zero nos Dados do RN

Para fixar os conceitos, vamos construir um classificador **KNN** (K-Nearest Neighbors — K-vizinhos mais próximos) inteiramente do zero, em Python puro, sem bibliotecas de ML.

### Como o KNN funciona

1. Para classificar um exemplo novo, calcule sua **distância** até todos os exemplos do conjunto de treino;
2. Selecione os ***k*** exemplos de treino mais próximos (os "vizinhos");
3. Atribua ao novo exemplo a classe mais frequente entre esses *k* vizinhos (voto majoritário).

Não há "treinamento" no sentido tradicional — o KNN apenas memoriza os dados de treino e faz todo o cálculo no momento da previsão (por isso é chamado de algoritmo preguiçoso, ou *lazy learner*).

### O problema deste estudo de caso

Usando as médias das escolas do RN calculadas na Aula 01, classificar cada escola em uma faixa de desempenho — "Alto", "Médio" ou "Baixo" — a partir de duas variáveis simples: a média geral da escola e o número de participantes. O objetivo não é obter o melhor modelo possível, e sim ver o KDD e o ML em ação: dados → preparação → algoritmo → avaliação → discussão crítica.

### O que você vai observar no exemplo

- Como separar treino e teste a partir de uma lista de escolas;
- Como calcular distância euclidiana entre exemplos (a essência do KNN);
- Como a acurácia muda ao variar o valor de *k* — e como isso ilustra overfitting (*k*=1) e underfitting (*k* muito grande);
- Por que normalizar as variáveis antes de calcular distâncias é importante quando elas têm escalas diferentes.

---

# Exemplo Prático — Pré-processamento de Dados (Aula 02)

> Texto do AVA: "Pré-Processamento de dados, em Python puro, para diminuir dados inconsistentes no dataset do ENEM 2025. Reaproveita o microdado `RESULTADOS_2025_RN.csv` já disponível na Aula 01."

Recursos:
- **Detalhamento Atividade Prática** (PDF, 5 p.) — transcrito em `atividade/README.md`.
- **Notebooks KDD Passos de 1 a 3** (ZIP: `aula2_passo1_selecao.ipynb`, `aula2_passo2_preprocessamento.ipynb`, `aula2_passo3_transformacao.ipynb`) — código consolidado em `atividade/aula02_kdd_passos1a3_colab.ipynb`.

> Observação: o livro descreve um KNN do zero (Cap. 5), mas o material prático publicado cobre as etapas 1–3 do KDD (seleção, pré-processamento, transformação) com Pandas/scikit-learn. O passo 4 (mineração) é referenciado no código ("Execute o passo4_mineracao.py em seguida"), mas não foi publicado na seção.

---

# Formulário Avaliativo — Aula 02

Questionário sobre ML, KDD e o exemplo do classificador KNN. Compõe as atividades semanais da Unidade 1.
