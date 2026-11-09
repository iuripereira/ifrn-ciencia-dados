# Tópicos de Estudo — Aula 09: Qualidade de Dados e 

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 09: Qualidade de Dados e Limpeza

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 09: Qualidade de Dados e Limpeza  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:23  |

## Índice

- 1. Qualidade de dados e o processo de limpeza
- 2. Valores ausentes: isna, dropna e fillna
- 3. Duplicatas e inconsistências
- 4. Outliers: IQR e z-score
- 5. Normalização, padronização e tidy data

## 1. Qualidade de dados e o processo de limpeza

Dados obtidos de arquivos, APIs ou web scraping (Aulas 06 a 08) quase nunca chegam prontos para análise. Limpeza de dados é o conjunto de etapas que transforma um conjunto "sujo" em um conjunto confiável — e costuma consumir boa parte do tempo de um projeto de ciência de dados.

#### Dimensões de qualidade

- Completude — os valores estão presentes? (ausentes)
- Unicidade — cada fato aparece uma única vez? (duplicatas)
- Consistência — o mesmo valor é escrito sempre do mesmo jeito? ("Natal", "natal", " NATAL")
- Validade — o valor respeita regras do domínio? (idade de −3 anos, pressão de 1.300 mmHg)
- Acurácia — o valor corresponde à realidade? (altura digitada em metros numa coluna em cm)

#### Primeiro meça, depois corrija

```
df.isna().sum()          # ausentes por coluna
df.duplicated().sum()    # linhas repetidas
df.describe()            # mínimo e máximo denunciam erros
df["municipio"].value_counts()   # variações de escrita
```

No dataset sintético da aula (250 atendimentos em UBS do RN), esse diagnóstico revela em poucos segundos: 10 duplicatas, 24 glicemias ausentes, idade máxima de 205 anos, peso máximo de 90.900 kg e "Natal" escrito de quatro formas.

Regra de ouro: nunca altere o arquivo original. Leia, limpe numa cópia e salve um novo arquivo — junto com um pequeno relatório do que foi feito.

## 2. Valores ausentes: isna, dropna e fillna

Um valor ausente aparece no Pandas como `NaN` (números/texto) ou `NaT` (datas).

- `isna()` / `notna()` — identificam os ausentes; `df.isna().sum()` conta por coluna;
- `dropna()` — remove linhas (padrão) ou colunas (`axis=1`) com ausentes; `subset=[...]` limita a verificação a algumas colunas e `thresh=n` exige um mínimo de valores presentes;
- `fillna(valor)` — preenche (imputa).

#### Remover ou preencher?

No laboratório, 50 das 240 linhas tinham algum ausente — quase sempre em uma só coluna. Um `dropna()` jogaria fora 21% dos atendimentos. Preferimos imputar:

```
df["idade"] = df["idade"].fillna(df["idade"].median())
df["glicemia_mg_dl"] = df["glicemia_mg_dl"].fillna(
    df.groupby("diagnostico")["glicemia_mg_dl"].transform("median"))
```

- A mediana é mais resistente a valores extremos que a média.
- Imputar por grupo respeita diferenças reais: a glicemia mediana de quem tem diabetes (≈169 mg/dL) é muito maior que a dos demais (≈97 mg/dL).
- Para variáveis categóricas, prefira uma categoria explícita ("Não informado") a inventar um valor.

#### Ausentes disfarçados: códigos sentinela

Sistemas costumam gravar "não medido" como 999, −1 ou 0. Esses números não são medidas: troque-os por ausente com `replace(999, np.nan)`. No laboratório, isso fez a média da glicemia cair de 129,5 para 109,1 mg/dL.

## 3. Duplicatas e inconsistências

#### Duplicatas

```
df.duplicated().sum()                    # quantas linhas repetem uma anterior
df[df.duplicated(keep=False)]            # mostra todas as cópias
df = df.drop_duplicates().reset_index(drop=True)
df["id_atendimento"].is_unique          # o identificador ficou único?
```

Por padrão a comparação usa todas as colunas e mantém a primeira ocorrência (`keep="first"`). Com `subset=["id_atendimento"]` a comparação usa apenas o identificador.

#### Texto inconsistente

Para o computador, "Natal", "natal", " NATAL" e "Natal " são quatro valores diferentes. A receita: tirar espaços, uniformizar maiúsculas e mapear o que sobrar.

```
df["municipio"] = (df["municipio"].str.strip().str.title()
    .replace({"Mossoro": "Mossoró", "Caico": "Caicó", "Pau Dos Ferros": "Pau dos Ferros"}))
```

#### Datas e unidades

- Datas em formatos misturados: converta cada formato com `pd.to_datetime(..., format="%d/%m/%Y", errors="coerce")` e combine os resultados com `fillna`.
- Unidades trocadas: alturas abaixo de 3 estavam em metros (multiplique por 100); pesos acima de 1.000 estavam em gramas (divida por 1.000). Use `df.loc[condição, coluna]` para corrigir só as linhas afetadas.

## 4. Outliers: IQR e z-score

Um outlier é um valor muito distante dos demais. Pode ser um erro (pressão de 1.300 mmHg) ou um caso raro real (crise hipertensiva de 205 mmHg). Métodos estatísticos apontam candidatos; quem decide é o conhecimento do domínio.

#### Método do IQR

```
q1, q3 = s.quantile([0.25, 0.75])
iqr = q3 - q1
suspeitos = s[(s < q1 - 1.5*iqr) | (s > q3 + 1.5*iqr)]
```

Na pressão sistólica: Q1 = 119, Q3 = 141, IQR = 22 → limites 86 e 174 mmHg. Foram sinalizados 12, 83, 179, 205, 410 e 1.300. Destes, só 12, 410 e 1.300 são impossíveis (viram NaN); os demais são valores reais de pacientes.

#### Método do z-score

z = (x − média) / desvio-padrão; costuma-se marcar |z| > 3. É simples, mas os próprios outliers inflam a média e o desvio: na idade, 150 e 205 anos foram marcados, mas −3 anos (z ≈ −2,4) passou despercebido.

#### Na prática

- Use IQR, z-score e boxplot para encontrar candidatos;
- Aplique regras de domínio (idade entre 0 e 110; pressão entre 60 e 260) para decidir;
- Erro corrigível (vírgula esquecida: 375 → 37,5) → corrija; erro sem correção → NaN e depois impute; caso real → mantenha.

## 5. Normalização, padronização e tidy data

#### Normalização e padronização

   Técnica |  Fórmula |  Resultado |
  Normalização (min-max) |  (x − mín) / (máx − mín) |  valores entre 0 e 1 |
  Padronização (z-score) |  (x − média) / desvio |  média 0, desvio 1 |

Elas mudam a escala, não a forma da distribuição, e são importantes para algoritmos baseados em distância (k-NN, k-means) — tema da Unidade 4. Aplique depois de tratar os outliers: um único 1.300 mmHg esmagaria todos os outros valores perto de zero no min-max. Na Aula 10 usaremos `MinMaxScaler` e `StandardScaler` do scikit-learn.

#### Tidy data

Um conjunto é tidy (Wickham) quando: cada variável é uma coluna; cada observação é uma linha; cada tipo de unidade observacional é uma tabela.

A planilha de vacinação `municipio, mar, abr, mai, jun` não é tidy: a variável "mês" está nos nomes das colunas.

```
longa = larga.melt(id_vars="municipio", var_name="mes", value_name="doses")   # largo → longo
larga2 = longa.pivot(index="municipio", columns="mes", values="doses")          # longo → largo
```

No formato longo, perguntas como "total de doses por mês" ou "mês de pico em cada município" viram uma linha de `groupby`.