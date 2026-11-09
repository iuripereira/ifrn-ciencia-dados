# Tópicos de Estudo — Aula 10

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 10

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 10  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:23  |

## Índice

- 1. Pipeline ETL: dos dados brutos ao dataset limpo
- 2. Transformação de tipos e padronização
- 3. Juntando fontes e engenharia de atributos
- 4. Codificação de variáveis categóricas
- 5. Pipeline do scikit-learn, exportação e documentação

## 1. Pipeline ETL: dos dados brutos ao dataset limpo

Na Aula 09 corrigimos problemas de qualidade um a um. Num projeto real, essas correções precisam ser repetíveis: no mês seguinte chegam novos arquivos e tudo deve rodar de novo. Para isso organizamos o trabalho num pipeline — uma sequência fixa de etapas.

#### ETL

- Extract — ler as fontes (CSV, JSON de uma API, planilhas, banco de dados) sem alterá-las;
- Transform — corrigir tipos, padronizar categorias, remover duplicatas, juntar tabelas, criar atributos e codificar categorias;
- Load — gravar o resultado no destino (arquivo CSV/Parquet, banco de dados), com documentação.

#### O cenário do laboratório (dados sintéticos)

Uma rede hospitalar fictícia do RN tem dois sistemas: o cadastro (`pacientes.csv`, 200 pacientes) e o sistema de internações, que entrega um JSON (`internacoes.json`, 304 registros). Nenhum registro é de paciente real.

O primeiro diagnóstico com `dtypes` mostra que todas as colunas chegaram como texto — inclusive datas, custos e a coluna de UTI. Além disso há grafias diferentes (`F`, `f`, `Feminino`), 4 internações duplicadas e 3 internações de pacientes que não existem no cadastro.

```
pacientes = pd.read_csv(DADOS / "pacientes.csv")
internacoes = pd.read_json(DADOS / "internacoes.json")
internacoes.dtypes        # tudo texto (str/object)
```

Boas práticas: trabalhar em cópias (`df.copy()`), organizar cada etapa em uma função e verificar regras com `assert` — se algo inesperado aparecer, o pipeline para em vez de gerar um dataset errado.

## 2. Transformação de tipos e padronização

#### Datas

Datas em dois formatos (`1993-10-22` e `22/10/1993`) são convertidas com cada formato e combinadas:

```
iso = pd.to_datetime(txt, format="%Y-%m-%d", errors="coerce")
br = pd.to_datetime(txt, format="%d/%m/%Y", errors="coerce")
p["data_nascimento"] = iso.fillna(br)      # 185 + 15 = 200 datas
```

#### Moeda brasileira → número

```
(serie.str.replace("R$", "", regex=False).str.strip()
      .str.replace(".", "", regex=False)     # tira o ponto de milhar
      .str.replace(",", ".", regex=False)    # vírgula decimal vira ponto
      .astype(float))                        # "R$ 15.764,91" vira 15764.91
```

A ordem importa: se a vírgula virar ponto antes de remover os pontos, o separador decimal também some.

#### Texto com número dentro

`"62 anos"` ou `"37 min"`: `s.str.extract(r"(\d+)")[0].astype(int)` pega só os dígitos.

#### Categorias e booleanos

```
p["sexo"] = p["sexo"].str.strip().str[0].str.upper()          # F, f, Feminino → F
mapa = {"sim": True, "s": True, "não": False, "nao": False, "n": False}
p["plano_saude"] = p["plano_saude"].str.strip().str.lower().map(mapa)
i["gravidade"] = i["gravidade"].str.capitalize()               # leve → Leve
```

Com `map`, um valor fora do dicionário vira `NaN` — ótimo para descobrir grafias inesperadas na conferência. Colunas Sim/Não viram booleanas, que ocupam menos memória e deixam claro que só há duas respostas.

## 3. Juntando fontes e engenharia de atributos

#### Junção com verificação

```
base = i.merge(p, on="id_paciente", how="left",
               validate="many_to_one", indicator=True)
base["_merge"].value_counts()     # both 297 · left_only 3
```

- `validate="many_to_one"` confere que cada paciente aparece uma única vez no cadastro;
- `indicator=True` revela internações órfãs (paciente inexistente) — um problema de integridade referencial que deve ser registrado e tratado.

#### Atributos derivados

```
base["tempo_internacao_dias"] = (base["data_alta"] - base["data_entrada"]).dt.days
base["idade"] = ((base["data_entrada"] - base["data_nascimento"]).dt.days // 365.25).astype(int)
```

Os 5 custos ausentes foram imputados pela mediana do mesmo diagnóstico e gravidade.

#### Binning (discretização)

   Função |  Como define as faixas |  Exemplo da aula |
  `pd.cut` |  limites escolhidos por você → quantidades diferentes por faixa |  faixas etárias 0-17, 18-39, 40-59, 60-79, 80+ |
  `pd.qcut` |  quantis → mesma quantidade por faixa |  quartis de custo: Baixo, Médio, Alto, Muito alto (≈74 cada) |

Com os novos atributos, a análise fica direta: o tempo médio de internação é 4,8 dias nos casos leves e 10,9 dias nos graves; a proporção de UTI sobe de 2% para 45%.

## 4. Codificação de variáveis categóricas

Modelos de machine learning trabalham com números. A forma de transformar categorias em números depende do tipo:

   Tipo |  Exemplo |  Técnica |
  Nominal (sem ordem) |  diagnóstico, município, sexo |  one-hot: `pd.get_dummies` / `OneHotEncoder` |
  Ordinal (com ordem) |  gravidade: Leve < Moderada < Grave |  dicionário explícito ou `OrdinalEncoder(categories=[...])` |
  Alvo (o que se quer prever) |  UTI sim/não |  `LabelEncoder` |

#### One-hot encoding

```
pd.get_dummies(base["diagnostico_principal"], prefix="diag", dtype=int)
```

Cria uma coluna 0/1 por categoria, sem criar ordem. Numerar diagnósticos (0 a 4) faria um modelo "achar" que existe uma ordem — e até médias — entre eles.

Armadilha da variável dummy: as colunas sempre somam 1, então uma delas é redundante. Com `drop_first=True`, município gera 3 colunas e Caicó vira a referência (todas 0).

#### Label encoding × codificação ordinal

O `LabelEncoder` numera em ordem alfabética: Grave = 0, Leve = 1, Moderada = 2 — que não é a ordem clínica. Para atributos ordinais, informe a ordem:

```
ordem = {"Leve": 0, "Moderada": 1, "Grave": 2}
base["gravidade_cod"] = base["gravidade"].map(ordem)
# ou: OrdinalEncoder(categories=[["Leve", "Moderada", "Grave"]])
```

## 5. Pipeline do scikit-learn, exportação e documentação

#### ColumnTransformer + Pipeline

```
preprocessador = ColumnTransformer([
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False), nominais),
    ("ordinal", OrdinalEncoder(categories=[["Leve", "Moderada", "Grave"]]), ["gravidade"]),
    ("escala", StandardScaler(), ["idade", "tempo_internacao_dias"]),
])
pipeline = Pipeline([("preprocessamento", preprocessador)])
Xt_treino = pipeline.fit_transform(X_treino)   # aprende SÓ com o treino
Xt_teste = pipeline.transform(X_teste)         # aplica ao teste
```

- Vazamento de dados (data leakage): médias, desvios e listas de categorias devem ser aprendidos apenas no treino; o teste só recebe `transform`.
- `handle_unknown="ignore"`: uma categoria nova (ex.: município Assu) vira zeros em vez de erro.

#### Load: CSV × Parquet

     |  CSV |  Parquet |
  Formato |  texto, universal |  binário, colunar, compactado |
  Tipos |  perdidos (datas e categorias voltam como texto) |  preservados |
  Tamanho no laboratório |  42 KB |  27 KB |

#### Dicionário de dados

Todo dataset limpo deve ir acompanhado de um dicionário: coluna, tipo, descrição e transformação aplicada (ex.: "custo_total — float — texto convertido; 5 ausentes imputados pela mediana do diagnóstico e gravidade").

#### Atividade de entrega

Aplique o pipeline completo ao arquivo `exames_laboratoriais.csv` e entregue o dataset limpo e o notebook documentado na Tarefa da aula (prazo 30/10/2026). Os requisitos e critérios estão na apostila e no notebook-modelo.