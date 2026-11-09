## KDD e Aprendizagem de Máquina

Ciclo completo de descoberta de conhecimento aplicado ao desempenho dos alunos do ENEM 2025 no Rio Grande do Norte

## O que é KDD?

KDD (Knowledge Discovery in Databases) é um processo sistemático para extrair conhecimento útil de grandes volumes de dados. Ele não é apenas 'rodar um algoritmo de ML' - é uma pipeline estruturada com cinco etapas, cada uma com decisões técnicas que impactam diretamente a qualidade do conhecimento gerado.

Nesta aula, seguiremos cada etapa usando dados reais: os microdados do ENEM 2025 filtrados para o estado do RN. Ao final, teremos um modelo capaz de prever o nível de desempenho de um aluno - e saberemos por que ele funciona (ou não).

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Detalhamento_Atividade_Pratica_artifacts/image_000000_36dbd824b7363a5301822e151047b6afbbfca75791181a0fca8ae1ac193108e6.png)

| 1 Seleção   | 2 Pré-processamento   | 3 Transformação   | 4 Mineração   | 5 Avaliação   |
|-------------|-----------------------|-------------------|---------------|---------------|

## Dataset: ENEM 2025 - Rio Grande do Norte

Os dados utilizados nesta aula são os microdados do ENEM 2025 disponibilizados pelo INEP, já filtrados para o RN. O arquivo de resultados contém registros de todos os candidatos inscritos, independentemente de ter comparecido ou não à prova.

|   Quantidade | Descrição                                                 |
|--------------|-----------------------------------------------------------|
|       30.449 | Registros de candidatos no arquivo                        |
|           70 | Colunas disponíveis nos microdados                        |
|        4.938 | Escolas no catálogo RN                                    |
|       25.965 | Candidatos presentes nos dois dias                        |
|            5 | Notas disponíveis por candidato (CN, CH, LC, MT, Redação) |

## Passo 1  -  Seleção

Antes de qualquer tratamento, precisamos definir qual pergunta queremos responder - porque é ela que determina quais dados selecionar. Sem uma pergunta clara, corremos o risco de selecionar dados de forma oportunista e chegar a padrões espúrios.

## PROBLEMA DE PESQUISA DESTA AULA

"Conseguimos prever o nível de desempenho de um aluno do ENEM 2025 (RN) com base nas notas das provas objetivas e no perfil da escola?"

Com a pergunta definida, selecionamos apenas os dados que a respondem. Dos 70 atributos disponíveis, a maioria é irrelevante: gabaritos, sequências de respostas, códigos de prova. A seleção também envolve filtro de registros: candidatos ausentes não têm notas significativas. Mantemos apenas os 25.965 presentes nos dois dias de prova.

## Colunas selecionadas

- CO\_ESCOLA - chave para join com o catálogo de escolas
- NO\_MUNICIPIO\_ESC - município da escola
- TP\_DEPENDENCIA\_ADM\_ESC - 1=Federal, 2=Estadual, 3=Municipal, 4=Privada
- TP\_LOCALIZACAO\_ESC - 1=Urbana, 2=Rural
- NU\_NOTA\_CN / CH / LC / MT / REDACAO - as cinco notas

## passo1\_selecao.py pandas · merge · filtragem condicional

📄

```
# Filtro de presença completa (operador bitwise &) presenca_completa = ( (df_raw["TP_PRESENCA_CN"] == 1) & (df_raw["TP_PRESENCA_CH"] == 1) & (df_raw["TP_PRESENCA_LC"] == 1) & (df_raw["TP_PRESENCA_MT"] == 1) ) df_presentes = df_raw[presenca_completa].copy() # Enriquecer com nome da escola (left join mantém candidatos sem escola) df_sel = df_presentes[COLUNAS].merge(df_cat, on="CO_ESCOLA", how="left")
```

## CONCEITO-CHAVE: VIÉS DE SELEÇÃO

Ao filtrar apenas alunos presentes, excluímos os ausentes. Isso é correto para o nosso problema, mas cria um viés: o modelo aprende sobre quem faz a prova, não sobre quem se inscreve. Essa limitação deve ser documentada.

Saída: dados\_selecionados.csv com 25.965 registros e 11 colunas.

## Passo 2  -  Pré-processamento

Dados do mundo real sempre contêm imperfeições. O pré-processamento não é uma etapa 'fácil' - decisões erradas aqui contaminam todas as etapas subsequentes e podem invalidar completamente os resultados do modelo.

## Problemas identificados e estratégias adotadas

## PROBLEMA A - NOTAS ZERO SUSPEITAS

Candidatos presentes com nota zero nas provas objetivas são estatisticamente improváveis (a TRI do ENEM dificilmente converge para zero). Esses zeros são tratados como NaN - ausência de informação confiável, não desempenho real.

## PROBLEMA B - NAN EM NOTAS

Para classificação supervisionada, não imputamos notas de alunos presentes (seria fabricar dados). Removemos esses registros. Perda aceitável: menor que 15% do conjunto selecionado.

## PROBLEMA C - ESCOLAS SEM MATCH NO CATÁLOGO

Mantemos o registro, mas sinalizamos com 'Escola não identificada'. O código da escola ainda é útil como atributo de agrupamento.

📄

## passo2\_preprocessamento.py pandas · numpy · matplotlib

```
# Substituir zeros por NaN (candidatos presentes com nota inválida) for col in NOTAS: df[col] = df[col].replace(0, np.nan) # Remover registros com qualquer nota ausente df_clean = df.dropna(subset=NOTAS).copy() # Verificar e remover duplicatas if df_clean.duplicated().sum(): df_clean = df_clean.drop_duplicates()
```

## ARMADILHA: IMPUTAÇÃO INGÊNUA

Substituir notas ausentes pela média da turma cria um efeito de 'ruim'. Para dados de avaliação, remoção é geralmente preferível quando a porcentagem de ausentes é baixa.

Saída: dados\_preprocessados.csv com dados limpos e notas garantidamente válidas.

## Passo 3  -  Transformação

Algoritmos de ML não entendem 'escola estadual' ou 'área rural' como texto - precisam de números. Além disso, features bem definidas carregam mais informação do que os atributos brutos originais.

## Atributos derivados criados

- MEDIA\_OBJETIVAS - média aritmética das 4 provas objetivas
- MEDIA\_GERAL - média ponderada igualitária das 5 provas (inclui redação)
- DESVIO\_NOTAS - desvio-padrão das notas do aluno (mede consistência entre áreas)
- MELHOR\_AREA / PIOR\_AREA - área com maior e menor nota (codificadas numericamente)
- LOCALIZACAO\_RURAL - binária: 1 se escola rural, 0 se urbana

## Variável-alvo: NIVEL\_DESEMPENHO

Baseada na MEDIA\_GERAL. Os cortes abaixo refletem a escala do ENEM: abaixo de 400 raramente indica proficiência suficiente para acesso ao Ensino Superior; acima de 700, o candidato compete em cursos mais concorridos.

| Nível        | Média Geral   | % Candidatos   | Cor de referência   |
|--------------|---------------|----------------|---------------------|
| Insuficiente | < 400         | ~8%            |                     |
| Regular      | 400-549       | ~38%           |                     |
| Bom          | 550-699       | ~41%           |                     |
| Excelente    | ≥ 700         | ~13%           |                     |

📄

## passo3\_transformacao.py pandas · sklearn.preprocessing · matplotlib

```
# Atributos derivados numéricos df["MEDIA_GERAL"]   = (df[NOTAS_OBJ].sum(axis=1) + df["NU_NOTA_REDACAO"]) / 5 df["DESVIO_NOTAS"] = df[NOTAS_TODAS].std(axis=1) # Variável-alvo por corte (pd.cut) df["NIVEL_DESEMPENHO"] = pd.cut( df["MEDIA_GERAL"], bins=[0, 400, 550, 700, 1001], labels=["Insuficiente", "Regular", "Bom", "Excelente"], right=False ) # One-Hot Encoding para tipo de escola (evita ordinalidade implícita) dummies = pd.get_dummies(df["TIPO_ESCOLA"], prefix="ESCOLA") # Normalização Min-Max (para KNN e outros algoritmos sensíveis à escala) scaler = MinMaxScaler() df_norm[...] = scaler.fit_transform(df[COLUNAS_NORM])
```

POR QUE ONE-HOT E NÃO LABEL ENCODING? Label Encoding atribui números às categorias (1=Federal, 2=Estadual...), implicando uma ordem que não existe. One-Hot trata cada tipo como binário independente - matematicamente correto para variáveis nominais como tipo de escola. Label Encoding imagina isso: Estadual ←1→ Federal ←1→ Municipal ←1→ Privada One-Hot não impõe nenhuma distância: Estadual = [1, 0, 0, 0] Federal = [0, 1, 0, 0] Municipal = [0, 0, 1, 0] Privada = [0, 0, 0, 1]