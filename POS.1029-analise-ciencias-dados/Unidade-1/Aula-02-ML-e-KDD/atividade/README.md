# Atividade — Aula 02: KDD passos 1–3 no ENEM 2025 RN

## O que é avaliado

| # | Item | Tipo | Onde |
|---|---|---|---|
| 1 | Formulário Avaliativo — Aula 02 (ML, KDD, KNN) | **Nota** | AVA |
| 2 | Atividade prática KDD — Seleção → Pré-processamento → Transformação | Prática (sem tarefa de upload publicada) | `aula02_kdd_passos1a3_colab.ipynb` |

## Pergunta de pesquisa (definida pelo professor)

> "Conseguimos prever o nível de desempenho de um aluno do ENEM 2025 (RN) com base nas notas das provas objetivas e no perfil da escola?"

## Passo a passo no Colab (~40 min)

1. Baixe do AVA `RESULTADOS_2025_RN.csv` e `catalogo_escolas_rn.csv` (mesmos da Aula 01).
2. Abra `aula02_kdd_passos1a3_colab.ipynb` no Colab e rode a célula SETUP (upload dos 2 CSV).
3. Execute em ordem: **Passo 1** (gera `dados_selecionados.csv`) → **Passo 2** (`dados_preprocessados.csv` + boxplots) → **Passo 3** (`dados_transformados.csv` + histograma/pizza).
4. Confira os números de referência (tabela abaixo). Divergência grande = erro de leitura/filtro.
5. Responda as questões de reflexão na última célula (preparação para o formulário).

## Números de referência (do PDF)

| Métrica | Valor |
|---|---|
| Registros no arquivo de resultados | 30.449 |
| Colunas nos microdados | 70 |
| Escolas no catálogo | 4.938 |
| Presentes nos 4 dias/provas (CN, CH, LC, MT) | 25.965 |
| Saída passo 1 | `dados_selecionados.csv` — 25.965 registros, 11 colunas |
| Distribuição-alvo aproximada | Insuficiente ~8% · Regular ~38% · Bom ~41% · Excelente ~13% |

## Armadilhas encontradas nos notebooks originais (já corrigidas no notebook desta pasta)

| # | Onde | Problema | Correção aplicada |
|---|---|---|---|
| 1 | Passo 1 | Catálogo lido com `encoding="latin1"`, mas o dicionário de dados diz `utf-8` → nomes com acento corrompidos | `encoding="utf-8"` |
| 2 | Passo 1/3 | Usa `TIPO_ESCOLA`, coluna que não existe no dicionário de dados (catálogo só tem `CO_ESCOLA`, `NO_ESCOLA`) → `KeyError` | Cria `TIPO_ESCOLA` mapeando `TP_DEPENDENCIA_ADM_ESC` (1=Federal … 4=Privada) se a coluna não existir |
| 3 | Passo 2 | `plt.savefig()` depois de `plt.show()` → PNG salvo em branco | `savefig` antes de `show` |
| 4 | Passo 2 | Figura criada duas vezes (célula sobrando) | Removida a duplicata |
| 5 | Passo 3 | `plt.close()` sem `show()` → gráfico não aparece no notebook | `plt.show()` após `savefig` |
| 6 | Passo 2 | `CO_ESCOLA.astype(str)` em coluna float vira `"24012345.0"` | Converte via `Int64` antes de `str` |

---

## Detalhamento da Atividade Prática (transcrição do PDF do AVA)

**IFRN — Especialização em Ciência de Dados · KDD e Aprendizagem de Máquina**
Ciclo completo de descoberta de conhecimento aplicado ao desempenho dos alunos do ENEM 2025 no Rio Grande do Norte.

### O que é KDD?

KDD (Knowledge Discovery in Databases) é um processo sistemático para extrair conhecimento útil de grandes volumes de dados. Ele não é apenas "rodar um algoritmo de ML" — é uma pipeline estruturada com cinco etapas, cada uma com decisões técnicas que impactam diretamente a qualidade do conhecimento gerado: **1 Seleção → 2 Pré-processamento → 3 Transformação → 4 Mineração → 5 Avaliação**.

Nesta aula, seguiremos cada etapa usando dados reais: os microdados do ENEM 2025 filtrados para o RN. Ao final, teremos um modelo capaz de prever o nível de desempenho de um aluno — e saberemos por que ele funciona (ou não).

**Dataset:** o arquivo de resultados contém registros de todos os candidatos inscritos, independentemente de ter comparecido ou não à prova (números na tabela acima).

### Passo 1 — Seleção

Antes de qualquer tratamento, precisamos definir qual pergunta queremos responder — porque é ela que determina quais dados selecionar. Sem uma pergunta clara, corremos o risco de selecionar dados de forma oportunista e chegar a padrões espúrios.

Dos 70 atributos disponíveis, a maioria é irrelevante: gabaritos, sequências de respostas, códigos de prova. A seleção também envolve filtro de registros: candidatos ausentes não têm notas significativas. Mantemos apenas os 25.965 presentes nos dois dias de prova.

Colunas selecionadas:
- `CO_ESCOLA` — chave para join com o catálogo de escolas
- `NO_MUNICIPIO_ESC` — município da escola
- `TP_DEPENDENCIA_ADM_ESC` — 1=Federal, 2=Estadual, 3=Municipal, 4=Privada
- `TP_LOCALIZACAO_ESC` — 1=Urbana, 2=Rural
- `NU_NOTA_CN / CH / LC / MT / REDACAO` — as cinco notas

```python
# Filtro de presença completa (operador bitwise &)
presenca_completa = (
    (df_raw["TP_PRESENCA_CN"] == 1) &
    (df_raw["TP_PRESENCA_CH"] == 1) &
    (df_raw["TP_PRESENCA_LC"] == 1) &
    (df_raw["TP_PRESENCA_MT"] == 1)
)
df_presentes = df_raw[presenca_completa].copy()

# Enriquecer com nome da escola (left join mantém candidatos sem escola)
df_sel = df_presentes[COLUNAS].merge(df_cat, on="CO_ESCOLA", how="left")
```

> **Conceito-chave: viés de seleção.** Ao filtrar apenas alunos presentes, excluímos os ausentes. Isso é correto para o nosso problema, mas cria um viés: o modelo aprende sobre quem faz a prova, não sobre quem se inscreve. Essa limitação deve ser documentada.

Saída: `dados_selecionados.csv` com 25.965 registros e 11 colunas.

### Passo 2 — Pré-processamento

Dados do mundo real sempre contêm imperfeições. O pré-processamento não é uma etapa "fácil" — decisões erradas aqui contaminam todas as etapas subsequentes e podem invalidar completamente os resultados do modelo.

- **Problema A — Notas zero suspeitas.** Candidatos presentes com nota zero nas provas objetivas são estatisticamente improváveis (a TRI do ENEM dificilmente converge para zero). Esses zeros são tratados como NaN — ausência de informação confiável, não desempenho real.
- **Problema B — NaN em notas.** Para classificação supervisionada, não imputamos notas de alunos presentes (seria fabricar dados). Removemos esses registros. Perda aceitável: menor que 15% do conjunto selecionado.
- **Problema C — Escolas sem match no catálogo.** Mantemos o registro, mas sinalizamos com "Escola não identificada". O código da escola ainda é útil como atributo de agrupamento.

```python
# Substituir zeros por NaN (candidatos presentes com nota inválida)
for col in NOTAS:
    df[col] = df[col].replace(0, np.nan)

# Remover registros com qualquer nota ausente
df_clean = df.dropna(subset=NOTAS).copy()

# Verificar e remover duplicatas
if df_clean.duplicated().sum():
    df_clean = df_clean.drop_duplicates()
```

> **Armadilha: imputação ingênua.** Substituir notas ausentes pela média da turma cria um efeito artificial. Para dados de avaliação, remoção é geralmente preferível quando a porcentagem de ausentes é baixa.

Saída: `dados_preprocessados.csv` com dados limpos e notas garantidamente válidas.

### Passo 3 — Transformação

Algoritmos de ML não entendem "escola estadual" ou "área rural" como texto — precisam de números. Além disso, features bem definidas carregam mais informação do que os atributos brutos originais.

Atributos derivados:
- `MEDIA_OBJETIVAS` — média aritmética das 4 provas objetivas
- `MEDIA_GERAL` — média ponderada igualitária das 5 provas (inclui redação)
- `DESVIO_NOTAS` — desvio-padrão das notas do aluno (mede consistência entre áreas)
- `MELHOR_AREA` / `PIOR_AREA` — área com maior e menor nota (codificadas numericamente)
- `LOCALIZACAO_RURAL` — binária: 1 se escola rural, 0 se urbana

**Variável-alvo `NIVEL_DESEMPENHO`**, baseada na `MEDIA_GERAL`. Os cortes refletem a escala do ENEM: abaixo de 400 raramente indica proficiência suficiente para acesso ao Ensino Superior; acima de 700, o candidato compete em cursos mais concorridos.

| Nível | Média Geral | % Candidatos |
|---|---|---|
| Insuficiente | < 400 | ~8% |
| Regular | 400–549 | ~38% |
| Bom | 550–699 | ~41% |
| Excelente | ≥ 700 | ~13% |

```python
df["MEDIA_GERAL"] = (df[NOTAS_OBJ].sum(axis=1) + df["NU_NOTA_REDACAO"]) / 5
df["DESVIO_NOTAS"] = df[NOTAS_TODAS].std(axis=1)

df["NIVEL_DESEMPENHO"] = pd.cut(
    df["MEDIA_GERAL"],
    bins=[0, 400, 550, 700, 1001],
    labels=["Insuficiente", "Regular", "Bom", "Excelente"],
    right=False
)

dummies = pd.get_dummies(df["TIPO_ESCOLA"], prefix="ESCOLA")   # One-Hot

scaler = MinMaxScaler()                                          # KNN e afins
df_norm[...] = scaler.fit_transform(df[COLUNAS_NORM])
```

### Por que One-Hot e não Label Encoding?

Label Encoding atribui números às categorias (1=Federal, 2=Estadual…), implicando uma ordem que não existe (`Estadual ←1→ Federal ←1→ Municipal ←1→ Privada`). One-Hot trata cada tipo como binário independente — matematicamente correto para variáveis nominais como tipo de escola:

```
Estadual  = [1, 0, 0, 0]
Federal   = [0, 1, 0, 0]
Municipal = [0, 0, 1, 0]
Privada   = [0, 0, 0, 1]
```
