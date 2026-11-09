UNIDADE 4 — APRENDIZADO DE MÁQUINA APLICADO · AULA 14

# scikit-learn: Fluxo de Trabalho em ML

API (fit / predict / transform) · treino e teste · validação cruzada · pipelines · métricas de classificação (acurácia, F1, ROC-AUC) e de regressão (RMSE, R²)

ROTEIRO DA AULA

# Agenda e objetivos

1

Dados, pergunta e alvo   0–10 min

Ao final, você será capaz de

• separar treino e teste sem vazamento

• montar um Pipeline com ColumnTransformer

• ler matriz de confusão, F1 e ROC-AUC

• comparar modelos com validação cruzada

• avaliar regressões com RMSE e R²

2

A API do scikit-learn   10–20 min

3

Treino/teste e baseline   20–30 min

4

Pipeline   30–45 min

5

Métricas de classificação   45–60 min

6

Validação cruzada   60–75 min

7

Regressão e fechamento   75–90 min

2

PANORAMA

# Aprendizado supervisionado: dois tipos de pergunta

Classificação

O alvo é uma categoria.

Quem vai cancelar o app? (sim/não)

O cliente ficará insatisfeito?

Métricas: acurácia, precisão, recall, F1, ROC-AUC

Regressão

O alvo é um número.

Quantos minutos a entrega vai levar?

Qual será o valor do pedido?

Métricas: MAE, RMSE, R²

Nos dois casos: aprendemos com exemplos em que a resposta (y) é conhecida, a partir dos atributos (X).

3

O CAMINHO

# O fluxo de trabalho em oito etapas

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000000_a231e2ecbc7192110b89a50c84181c264f2e88f333c3d08e48eefffdec98fb59.png)

Por que a ordem importa

Cada etapa protege a seguinte: o teste fica guardado, o pré-processamento aprende só no treino e a escolha do modelo é feita na validação cruzada. Assim, o desempenho reportado é o que o modelo terá com dados novos.

4

A API DO SCIKIT-LEARN

# Todo objeto segue o mesmo contrato

Estimador (modelo)

fit(X, y) aprende · predict(X) prevê

predict\_proba(X) dá probabilidades

LogisticRegression, RandomForestClassifier

modelo = LogisticRegression(

    max\_iter=1000)

modelo.fit(X\_treino, y\_treino)

modelo.predict(X\_teste)

modelo.predict\_proba(X\_teste)[:, 1]

modelo.coef\_   # aprendido: termina em \_

Transformador

fit(X) aprende · transform(X) aplica

fit\_transform(X) faz os dois

StandardScaler, OneHotEncoder, SimpleImputer

5

TREINO E TESTE

# Avalie o modelo em dados que ele não viu

X\_treino, X\_teste, y\_treino, y\_teste = train\_test\_split(

    X, y, test\_size=0.25, stratify=y, random\_state=42)

Cuidado: vazamento

O modelo não pode receber informação que não teria no uso real.

• Ajustar padronização ou imputação em TODOS os dados antes de dividir

• Usar uma variável que contém a resposta (ou vem depois dela)

1.125

375

26,9%

usuários no treino

no teste (25%)

cancelaram — igual nos dois (stratify)

6

BASELINE

# O paradoxo da acurácia

73,1%

0

82,7%

acurácia do DummyClassifier: chuta sempre "ficou"

cancelamentos encontrados (recall = 0)

acurácia da regressão logística — e encontra 55 dos 101 que cancelaram

Lição

Com classes desbalanceadas, acurácia alta pode esconder um modelo inútil. Calcule sempre um baseline e escolha a métrica pelo objetivo — aqui, encontrar quem vai cancelar.

7

PRÉ-PROCESSAMENTO + MODELO

# Pipeline: um único estimador

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000001_ae82e9cc43383ea5a98ed30b17cd3851e3417a4bae19f316e0a94711bee95f68.png)

Sem vazamento (inclusive na validação cruzada) · um fit, um predict · trocar o modelo é trocar uma linha

8

O QUE O MODELO APRENDEU

# Quem tem mais risco de cancelar?

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000002_fb3d72761169d250bc9cf7ed8a5cbaa44d6f55e9a5a72a2e3849c9d6fe0fcfc1.png)

Aumentam o risco

plano gratuito

dias sem acessar

chamados ao suporte

Diminuem o risco

satisfação

meses de conta

plano Premium

Coeficientes de variáveis padronizadas: comparáveis entre si. Associação, não causa.

9

MÉTRICAS DE CLASSIFICAÇÃO

# Tudo começa na matriz de confusão

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000003_ce9d4ef1d9257bb068e0618d2f694785e44acc3f1a8a3e9b995b6c395518dec4.png)

VP = 55

cancelaram e o modelo apontou

FN = 46

cancelaram e o modelo NÃO viu — o erro caro

FP = 19

falso alarme: ficariam, mas foram apontados

VN = 255

ficaram e o modelo acertou

10

PRECISÃO, RECALL E F1

# Cada métrica responde a uma pergunta

| Métrica   | Fórmula              | Pergunta                           | Baseline   |   Logística |
|-----------|----------------------|------------------------------------|------------|-------------|
| Acurácia  | (VP + VN) / total    | quantos acertos no geral?          | 0,731      |       0,827 |
| Precisão  | VP / (VP + FP)       | dos apontados, quantos cancelaram? | —          |       0,743 |
| Recall    | VP / (VP + FN)       | dos que cancelaram, quantos achei? | 0,000      |       0,545 |
| F1        | 2·P·R / (P + R)      | equilíbrio entre precisão e recall | 0,000      |       0,629 |
| ROC-AUC   | área sob a curva ROC | o modelo ordena bem o risco?       | 0,500      |       0,831 |

Conferindo: precisão = 55 / (55 + 19) = 0,743 · recall = 55 / (55 + 46) = 0,545

11

ROC-AUC E LIMIAR DE DECISÃO

# O limiar é uma decisão de negócio

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000004_9ee9f539dc779ee15be563b845569d67dc7c9140b432cb6a2fd48b5f68af41b6.png)

Precisão × recall por limiar

<!-- image -->

Line chart

|     |   Precisão |   Recall |
|-----|------------|----------|
| 0,2 |       0.46 |    0.802 |
| 0,3 |       0.53 |    0.703 |
| 0,4 |      0.639 |    0.614 |
| 0,5 |      0.743 |    0.545 |
| 0,6 |      0.875 |    0.416 |
| 0,7 |      0.943 |    0.327 |

AUC = 0,83: em 83% dos pares, quem cancelou recebe risco maior. Limiar 0,3 encontra 70% dos cancelamentos (contra 55% em 0,5), com mais falsos alarmes.

12

VALIDAÇÃO CRUZADA

# Comparar modelos sem tocar no teste

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000006_9f4fbff3c6159b8a47d671bd6bf0cc769fb1d35223dd45729600db44fa9326de.png)

ROC-AUC média (± 0,03 entre folds)

<!-- image -->

Bar chart

|               |   ROC-AUC média (5 folds) |
|---------------|---------------------------|
| Baseline      |                       0.5 |
| Logística     |                     0.845 |
| Árvore        |                     0.778 |
| Random forest |                     0.838 |

cv = StratifiedKFold(n\_splits=5,

        shuffle=True, random\_state=42)

r = cross\_validate(modelo, X\_treino,

        y\_treino, cv=cv,

        scoring=["accuracy", "f1", "roc\_auc"])

13

MÉTRICAS DE REGRESSÃO

# Prevendo o tempo de entrega da hamburgueria

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula14_Slides_scikit_learn_Fluxo_ML_artifacts/image_000008_08d0ce1abad708ce80769de608628849a0b59e8c02e07ce72c820fb4222cdb39.png)

3,9 min

6,8 min

0,59

MAE: erro típico

RMSE (baseline: 10,8 min)

R²

Como ler

MAE: erro médio, na unidade do alvo. RMSE: pune erros grandes — bem acima do MAE indica poucos atrasos enormes. R²: proporção da variação explicada (0 = prever sempre a média).

na validação cruzada:

scoring="neg\_root\_mean\_squared\_error"

14

FECHANDO O RACIOCÍNIO

# Seis erros que o fluxo evita

Avaliar no treino ou reusar o teste para ajustar

Padronizar ou imputar antes de dividir os dados

1

2

Reportar só acurácia em dados desbalanceados

Esquecer stratify=y e random\_state

3

4

Atributo que carrega a resposta (vazamento)

Validação cruzada sem desvio-padrão

5

6

15

DEPOIS DA AULA

# Próximos passos

Trabalho prático (entrega)

Aula14\_Trabalho\_Pratico.ipynb

Classifique os clientes insatisfeitos (nota ≤ 3) da hamburgueria: baseline, pipeline, 2 modelos, validação cruzada e conclusão.

Entregue o .ipynb executado no Moodle.

Formulário avaliativo

10 questões objetivas sobre a aula. Pode consultar o material.

Prazo de ambos

23/11/2026, 23:59

16

AULA 14 — SCIKIT-LEARN: FLUXO DE TRABALHO EM ML

# Dúvidas?

Obrigado pela atenção. Materiais no Moodle: livro, apostila, slides, pacote com notebooks e dados.