# Tópicos de Estudo — Aula 11

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 11

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 11  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:23  |

## Descrição

Resumo dos principais tópicos da Aula 11 — Fundamentos de AED e Estatística Descritiva, em 5 capítulos curtos.

## Índice

- 1. Análise exploratória e tipos de variáveis
- 2. Medidas de tendência central
- 3. Medidas de dispersão
- 4. Distribuições: forma, assimetria e boxplot
- 5. Correlação, matriz de correlação e hipóteses

## 1. Análise exploratória e tipos de variáveis

A Análise Exploratória de Dados (AED) — Exploratory Data Analysis, termo popularizado por John Tukey — é a etapa em que olhamos os dados com resumos numéricos e gráficos simples antes de qualquer modelo. O objetivo é conhecer os dados, encontrar padrões e problemas e, principalmente, formular boas perguntas.

#### O dataset da aula (sintético)

300 estudantes de um curso fictício: horas de estudo por semana, horas de sono, tempo de celular, faltas, deslocamento, mês de nascimento, turno, se trabalha e nota final (0 a 10). No exercício, 90 dias de uma sorveteria fictícia.

#### Tipos de variáveis

   Tipo |  Subtipo |  Exemplo |
  Qualitativa |  nominal (sem ordem) |  turno, trabalha |
  Qualitativa |  ordinal (com ordem) |  conceito A/B/C, satisfação |
  Quantitativa |  discreta (contagem) |  faltas, sorvetes vendidos |
  Quantitativa |  contínua (medida) |  horas de sono, temperatura, nota |

Atenção: o tipo no Pandas não é o tipo estatístico. `mes_nascimento` é `int64`, mas a "média do mês de nascimento" não tem significado útil.

```
df.dtypes
df["turno"].value_counts(normalize=True)   # proporções de uma variável qualitativa
```

## 2. Medidas de tendência central

Respondem à pergunta "qual é o valor típico?"

- Média (`mean`) — soma ÷ quantidade; usa todos os valores, mas é sensível a extremos.
- Mediana (`median`) — valor central dos dados ordenados; robusta a extremos.
- Moda (`mode`) — valor mais frequente; a única que serve para variáveis nominais.

   Variável |  Média |  Mediana |
  nota final |  5,69 |  5,80 |
  horas de sono |  7,06 |  7,10 |
  horas de estudo/semana |  7,34 |  6,25 |
  deslocamento (min) |  26,0 |  23,0 |

Quando a média é bem maior que a mediana, há uma cauda à direita: poucos valores altos puxam a média. Nesse caso, a mediana descreve melhor o caso típico.

#### Um único valor extremo

Incluir um registro errado de 150 h de estudo muda a média de 7,34 para 7,81 h; a mediana vai de 6,25 para 6,30 h. Na sorveteria, o dia do festival (1.150 sorvetes) eleva a média de 166,7 para 177,6 sorvetes, enquanto a mediana fica em torno de 174.

## 3. Medidas de dispersão

Duas turmas podem ter a mesma média e ser muito diferentes. A dispersão mede o quanto os valores se espalham.

   Medida |  Ideia |  Pandas |
  Amplitude |  máximo − mínimo (frágil: usa 2 valores) |  `s.max() - s.min()` |
  Variância |  média dos quadrados dos desvios (unidade²) |  `s.var()` |
  Desvio-padrão |  raiz da variância (mesma unidade) |  `s.std()` |
  Coeficiente de variação |  desvio ÷ média × 100% (sem unidade) |  `s.std() / s.mean() * 100` |
  Intervalo interquartil |  Q3 − Q1 (50% centrais; robusto) |  `s.quantile(.75) - s.quantile(.25)` |

O Pandas usa a versão amostral (divide por n − 1).

#### No laboratório

- Sono: desvio 0,86 h e CV ≈ 12% — quase todos dormem entre 6 e 8 h.
- Estudo: desvio 5,04 h e CV ≈ 69% — muita variação entre estudantes.
- Nota: Q1 = 4,7, Q3 = 6,6 → IQR = 1,9.

Regra prática: distribuição aproximadamente simétrica → média e desvio-padrão; assimétrica ou com extremos → mediana e IQR. O `describe()` traz os cinco números de Tukey (mínimo, Q1, mediana, Q3, máximo), a média e o desvio.

## 4. Distribuições: forma, assimetria e boxplot

A distribuição mostra como os valores se espalham na escala. Use histogramas e boxplots.

- Simétrica — média ≈ mediana; assimetria (`skew`) ≈ 0. Ex.: horas de sono (0,20).
- Assimétrica à direita — cauda para valores altos; média > mediana; skew > 0. Ex.: horas de estudo (1,51), chuva diária (2,3).
- Assimétrica à esquerda — cauda para valores baixos; média < mediana; skew < 0.

A curtose (`kurt`, excesso em relação à normal) indica caudas mais pesadas (> 0) ou mais leves (< 0).

#### Regra 68–95–99,7

Em uma distribuição aproximadamente normal, cerca de 68%, 95% e 99,7% dos valores ficam a 1, 2 e 3 desvios da média. Para o sono (média 7,06 h, desvio 0,86 h): 64,7% entre 6,21 e 7,92 h; 95,3% entre 5,35 e 8,78 h. A regra não vale bem para distribuições assimétricas.

#### Boxplot

A caixa vai de Q1 a Q3, a linha interna é a mediana, os bigodes vão até o último valor dentro de 1,5·IQR e os pontos além disso são candidatos a outlier. Boxplots lado a lado comparam grupos: quem trabalha tem nota mediana 5,10; quem não trabalha, 6,05.

```
df.groupby("trabalha")["nota_final"].agg(["mean", "median", "std"])
```

## 5. Correlação, matriz de correlação e hipóteses

O gráfico de dispersão vem primeiro. A correlação resume força e direção da associação entre −1 e +1.

   Coeficiente |  Mede |  Pandas |
  Pearson (r) |  associação linear |  `x.corr(y)` |
  Spearman (ρ) |  associação monotônica (Pearson nos postos) |  `x.corr(y, method="spearman")` |

Leitura aproximada de |r|: < 0,1 desprezível · 0,1–0,3 fraca · 0,3–0,5 moderada · 0,5–0,7 forte · > 0,7 muito forte.

- Estudo × nota: r = 0,68 e ρ = 0,72 — relação crescente, mas curva (ganho decrescente).
- Faltas × nota: ρ = −0,40 (negativa moderada). Mês de nascimento × nota: ≈ 0.
- Sorveteria: temperatura × sorvetes deu r = 0,32 e ρ = 0,80 por causa de um dia de festival; sem ele, r = 0,85.
- r ≈ 0 indica ausência de relação linear — uma relação em U pode ter r ≈ 0.

#### Matriz de correlação

```
df[numericas].corr(method="spearman")   # simétrica, diagonal = 1
```

#### Correlação não é causalidade

O turno da noite tem notas menores, mas, separando quem trabalha, as diferenças entre turnos quase somem: trabalhar é uma variável de confusão.

#### Hipóteses exploratórias

A AED termina com hipóteses específicas, mensuráveis e verificáveis. Ex.: "Mais horas de estudo estão associadas a notas maiores, com ganho decrescente" (ρ = 0,72). São evidências exploratórias, não provas: serão investigadas nas próximas análises.