INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE ESPECIALIZAÇÃO   EM   CIÊNCIA   DE   DADOS   ·   DISCIPLINA:   ANÁLISE   E   CIÊNCIA   DE   DADOS   ·   MATERIAL COMPLEMENTAR DA AULA 12

## Correlação de Spearman: do conceito à aplicação

Correlação com postos: para relações monotônicas, variáveis ordinais e dados com outliers, usando os dados da Aula 12

| Relação com a aula   | Complementa a Aula 12 - Laboratório: Matplotlib, Seaborn e Plotly (gráfico de dispersão e mapa de calor)                                         |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
| Como está organizado | Progressivo: por que outro coeficiente → postos → cálculo à mão (sem e com empates) → Spearman × Pearson → aplicações → exercícios com respostas |
| Pré-requisitos       | Material complementar de Pearson (leia antes); mediana e quartis (Aula 11)                                                                       |
| Dados                | Os mesmos da Aula 12 (sintéticos): 600 pedidos da hamburgueria Brasa & Pão e 240 usuários do app de música                                       |
| Ferramentas          | pandas ( rank , corr(method="spearman") ), scipy.stats.spearmanr , seaborn                                                                       |
| Professor            | Plácido Antônio de Souza Neto                                                                                                                    |

## Objetivos de aprendizagem

Ao final deste material, espera-se que o estudante seja capaz de:

- Explicar o que é uma relação monotônica e por que, às vezes, o Pearson não é a melhor medida. 1.
- Transformar valores em postos , inclusive com empates (posto médio). 2.
- Calcular o ρ de Spearman à mão - pela fórmula das diferenças de postos e como Pearson dos postos - e conferir em Python. 3.
- Comparar Spearman e Pearson e escolher o   coeficiente   adequado   ao   tipo   de variável e à forma da relação. 4.
- Aplicar o Spearman aos datasets da aula: variáveis ordinais, subgrupos, matrizes e dados agregados. 5.

## Como estudar este material

| Nível          | Seções   | Você vai…                                                                             |
|----------------|----------|---------------------------------------------------------------------------------------|
| 1 · Motivação  | 1 e 2    | ver três situações em que o Pearson não basta e entender o que é monotonicidade       |
| 2 · Cálculo    | 3 a 6    | transformar valores em postos, calcular o ρ à mão (sem e com empates) e interpretá-lo |
| 3 · Comparação | 7 a 10   | comparar Spearman e Pearson: outliers, variáveis ordinais e relações não monotônicas  |
| 4 · Aplicações | 11 a 15  | usar o Spearman nos dois datasets, em subgrupos, matrizes e dados agregados           |
| 5 · Prática    | Parte IV | resolver 8 exercícios progressivos (respostas no Apêndice B)                          |

## SOBRE OS DADOS

Os mesmos conjuntos sintéticos da Aula 12: 600 pedidos de delivery (distância, tempo, taxa, itens, valor, avaliação de 1 a 5 , bairro, veículo, chuva, turno) e 240 usuários de um app de música (idade, plano, horas por semana, playlists, anúncios por semana e satisfação de 0 a 10). Nenhum registro é real.

## Parte I - Conceito e cálculo

Trocar valores por posições: a ideia central do Spearman

## 1. Por que outro coeficiente? NÍVEL 1

- O Pearson mede quão bem os pontos se ajustam a uma reta e usa os valores numéricos diretamente. Isso cria três situações delicadas:
- A relação é crescente (ou decrescente), mas não é uma reta. Ex.: as músicas favoritadas crescem rápido nos primeiros dias de uso e depois se estabilizam. 1.
- A variável é ordinal. Ex.: a avaliação de 1 a 5 do delivery. A diferença entre 1 e 2 estrelas não é necessariamente "igual" à diferença entre 4 e 5 - só a ordem é confiável. 2.
- Há outliers. Ex.: um pedido trocado que levou 71 minutos para percorrer 1,8 km. 3.

O coeficiente   de   correlação   de   Spearman   (ρ,   letra   grega   "rô") resolve   as   três situações com uma única ideia: em vez dos valores, usar as posições (postos) de cada observação.

Figura 1 - Linear: os dois coeficientes concordam. Monotônica não linear: o ρ (0,89) capta melhor a relação que o r (0,84). Não monotônica (sobe e desce): nenhum dos dois serve.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000000_ee40cb54edfc21b5639d740c4f9822123eb3f77b6d786694ba956b70b9d0e4a6.png)

## 2. Relação monotônica NÍVEL 1

Uma relação é monotônica crescente quando, à medida que x aumenta, y nunca diminui (tende a aumentar) - mas não precisa aumentar sempre na mesma taxa. É monotônica decrescente quando y tende sempre a diminuir. Toda relação linear é monotônica, mas nem toda relação monotônica é linear.

| Forma da relação                                      | Exemplo                                            | Pearson (r)   | Spearman (ρ)   |
|-------------------------------------------------------|----------------------------------------------------|---------------|----------------|
| Linear                                                | distância × tempo de entrega                       | adequado      | adequado       |
| Monotônica não linear (curva que só sobe ou só desce) | dias de uso × músicas favoritadas                  | subestima     | adequado       |
| Não monotônica (sobe e desce)                         | hora do pedido × tempo na cozinha (pico no jantar) | inadequado    | inadequado     |

O   ρ   responde: "quando   x   aumenta,   y   tende   a   aumentar   (ou   diminuir)   de   forma consistente?" . O r responde: "os pontos estão próximos de uma reta?" .

## 3. Postos (ranks) NÍVEL 2

Ordenar os valores do menor para o maior e substituir cada um pela sua posição: o menor recebe   posto   1,   o   seguinte   posto   2,   e   assim   por   diante.   Cada   variável   é   ordenada separadamente .

Empates: valores iguais recebem a média das posições que ocupariam. Em [3, 5, 4, 4, 2] : o 2 fica com posto 1; o 3 com posto 2; os dois "4" ocupariam as posições 3 e 4, então ambos recebem (3 + 4) / 2 = 3,5 ; o 5 fica com posto 5.

```
import pandas as pd pd.Series([3, 5, 4, 4, 2]).rank()            # [2.0, 5.0, 3.5, 3.5, 1.0]  (padrão: posto médio)
```

```
pd.Series([3, 5, 4, 4, 2]).rank(ascending=False)  # ordem inversa, se precisar
```

## O QUE SE PERDE E O QUE SE GANHA

Ao trocar valores por postos perdemos a distância entre os valores (88 min e 50 min viram apenas "1º e 2º mais demorados"). Em troca, o resultado fica imune à escala, a curvas monotônicas e a valores extremos.

## 4. Calculando à mão (sem empates): 6 usuários NÍVEL 2

Seis usuários do app de música: x = idade, y = horas ouvidas por semana. Não há valores repetidos.

1 Postos de cada variável (1 = menor). 2 Diferença d = posto(x) - posto(y) e seu quadrado.

| Usuário     |   Idade |   Posto idade | Horas/sem.   |   Posto horas |   d |   d² |
|-------------|---------|---------------|--------------|---------------|-----|------|
| U1 (id 45)  |      29 |             3 | 22,5         |             5 |  -2 |    4 |
| U2 (id 18)  |      48 |             6 | 11,8         |             1 |  +5 |   25 |
| U3 (id 170) |      16 |             1 | 23,6         |             6 |  -5 |   25 |
| U4 (id 100) |      43 |             5 | 16,9         |             3 |  +2 |    4 |
| U5 (id 136) |      33 |             4 | 16,4         |             2 |  +2 |    4 |
| U6 (id 234) |      20 |             2 | 19,4         |             4 |  -2 |    4 |
| Soma        |         |               |              |               |   0 |   66 |

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000001_21daa05a95ec7af0d4f2145337846a54f1170b2988125b839a9d46d3be8b09d3.png)

## 3 Fórmula de Spearman (válida quando não há empates ):

<!-- formula-not-decoded -->

ρ = 1 - 6 × 66 / [6 × (36 - 1)] = 1 - 396 / 210 = -0,886 . Para comparar, o Pearson desses mesmos valores é r = -0,849.

Por que a fórmula funciona? Se os postos coincidissem (o mais novo é quem ouve menos, e assim por diante), todos os d seriam 0 e ρ = 1. Se fossem exatamente invertidos, Σd² atingiria o máximo e ρ = -1. Aqui os postos estão quase invertidos: relação negativa forte.

```
from scipy import stats idade = [29, 48, 16, 43, 33, 20] horas = [22.5, 11.8, 23.6, 16.9, 16.4, 19.4] stats.spearmanr(idade, horas).statistic    # -0,886
```

## 5. Com empates: Spearman = Pearson dos postos NÍVEL 2

A definição geral do ρ é simples: calcule os postos e aplique a fórmula de Pearson aos postos . A fórmula com Σd² é apenas um atalho que dá o mesmo resultado quando não há empates. Com empates, ela erra.

Oito pedidos do delivery (avaliação 1-5 × tempo). As avaliações em ordem são 3, 3, 4, 4, 4, 5, 5, 5: os três "4" ocupariam as posições 3, 4 e 5 e recebem posto médio 4; os três "5" ocupariam 6, 7 e 8 e recebem 7; os dois "3" recebem 1,5.

|   Pedido |   Avaliação | Posto avaliação   |   Tempo (min) | Posto tempo   |
|----------|-------------|-------------------|---------------|---------------|
|      196 |           4 | 4                 |            45 | 6,5           |
|      156 |           5 | 7                 |            31 | 4             |
|       41 |           3 | 1,5               |            45 | 6,5           |
|      213 |           4 | 4                 |            38 | 5             |
|       53 |           5 | 7                 |            24 | 1             |
|      530 |           4 | 4                 |            29 | 3             |
|      112 |           3 | 1,5               |            51 | 8             |
|      259 |           5 | 7                 |            28 | 2             |

Pearson dos postos: ρ = -0,843 - é o que stats.spearmanr calcula. A fórmula Σd² aplicada aos mesmos postos daria -0,732: um erro grande, porque há muitos empates.

```
p8["posto_aval"] = p8["avaliacao"].rank()            # posto médio nos empates p8["posto_tempo"] = p8["tempo_entrega_min"].rank() stats.pearsonr(p8["posto_aval"], p8["posto_tempo"]).statistic   # -0,843 stats.spearmanr(p8["avaliacao"], p8["tempo_entrega_min"]).statistic  # -0,843 p8["avaliacao"].corr(p8["tempo_entrega_min"], method="spearman")   # -0,843
```

Figura 2 - Os 600 pedidos em valores (esquerda) e em postos (direita). O ρ de Spearman (0,72) é exatamente o Pearson calculado no gráfico da direita.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000002_4ee6d5f6a535b46c716a3a9bbc7e46e60265fe6e3141a9dc6337af87512a21f7.png)

## 6. Interpretando o ρ NÍVEL 2

- Varia de -1 a +1 , com a mesma leitura de sinal e força do Pearson (a tabela de faixas do material de Pearson também serve como referência). ·

- ρ = +1: a ordem de x é exatamente a ordem de y (relação monotônica crescente perfeita), mesmo que a curva não seja uma reta. ·
- ρ = -1: a ordem é exatamente inversa. ·
- ρ ≈ 0: não há tendência monotônica - o que não exclui uma relação em "U" ou "∩". ·
- O ρ² não deve ser lido   como   "porcentagem   da   variação   explicada"   dos   valores originais; ele se refere aos postos. Reporte o ρ. ·

## Parte II - Spearman × Pearson

Quando os dois concordam, quando discordam e por quê

## 7. Robustez a outliers NÍVEL 3

Em postos, um valor extremo é apenas "o maior" (ou "o menor"): sua distância até os outros desaparece. Por isso o ρ muda pouco quando um outlier entra ou sai.

| Cenário (pedidos de até 3 km)   | Pearson r   | Spearman ρ   | Variação de r   | Variação de ρ   |
|---------------------------------|-------------|--------------|-----------------|-----------------|
| 12 pedidos de até 3 km          | 0,58        | 0,61         | -               | -               |
| + 1 pedido distante (14 km)     | 0,87        | 0,69         | +0,29           | +0,08           |
| + 1 atraso (1,8 km, 71 min)     | 0,15        | 0,45         | -0,43           | -0,16           |

Figura 3 - O pedido atrasado (laranja) está longe de todos os outros nos valores, mas nos postos ele é só o posto 13 do tempo.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000003_d5e8a49314b4a39b29568b2762ff5320a3bc7e6ba909b53b6609db7993b5a8dd.png)

## ROBUSTO NÃO É IMUNE

O ρ também caiu com o atraso (de 0,61 para 0,45): com só 13 pontos, um posto fora do lugar ainda pesa. A robustez aumenta com o tamanho da amostra. E o Spearman não substitui a investigação do outlier.

## 8. Variáveis ordinais: a avaliação do cliente NÍVEL 3

A avaliação (1 a 5 estrelas) é ordinal : sabemos que 5 é melhor que 4, mas não que a "distância" entre 4 e 5 é igual à entre 1 e 2. O Pearson trata os números como medidas; o Spearman usa apenas a ordem - por isso é a escolha adequada para escalas de satisfação, notas por conceito, níveis de escolaridade etc.

Figura 4 - Tempo de entrega por nota recebida. Cada estrela a menos corresponde a entregas mais demoradas.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000004_0a99d6fac43383f758e3dc2beff9dbc2c149d57e8072ebb57033361d8a4f237e.png)

Avaliação × tempo: ρ = -0,537 (Pearson: -0,594). Avaliação × distância: ρ = -0,404 (Pearson: -0,435). Os valores são parecidos, mas só o ρ tem interpretação garantida para uma escala ordinal. Repare também nos empates : só existem 5 valores possíveis para 600 pedidos - 294 pedidos receberam nota 4 e dividem o mesmo posto médio.

## E O TAU DE KENDALL?

Com muitos empates ou amostras pequenas ,   outra opção é o τ (tau) de Kendall ( stats.kendalltau ), que compara todos os pares de observações e conta quantos estão "na mesma ordem". Ele costuma dar valores menores em módulo que o ρ e tem a mesma leitura de sinal.

## 9. Relações monotônicas não lineares NÍVEL 3

Na Figura 1 (centro), as músicas favoritadas crescem rápido no início e depois estabilizam. A relação é perfeitamente "consistente" - mais dias de uso nunca significam menos favoritas -, mas não é uma reta. O Pearson (0,84) penaliza a curvatura; o Spearman (0,89) mede justamente a consistência da ordem. Curvas desse tipo são comuns: aprendizagem, saturação de mercado, crescimento populacional, retornos decrescentes.

## 10. Limitação: relações não monotônicas NÍVEL 3

Spearman não resolve relações que sobem e depois descem. Um exemplo nos dados da aula: dia da semana (1 = segunda … 7 = domingo) × valor do pedido.

Figura 5 - O ticket médio sobe na sexta, sábado e domingo e é menor de segunda a quinta (com um pico na quarta). ρ = 0,18.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000005_d1857f14e165e8b2795d6194e6ab0e4a4a27586af2c0fa33eb3623b0744a9d3f.png)

Há um padrão claro (fim de semana mais caro), mas o ρ = 0,18 é fraco, porque a relação com a ordem dos dias não é consistente. Aqui o certo é tratar o dia como categoria e comparar grupos (gráfico de barras, boxplot), e não calcular uma correlação. Antes de qualquer coeficiente: olhe o gráfico .

## Parte III - Aplicações nos datasets da aula

Matrizes, subgrupos, escalas ordinais e dados agregados

## 11. Matriz de Spearman e comparação com Pearson NÍVEL 4

Com o pandas, basta trocar o método: df[colunas].corr(method="spearman") .

Figura 6 - Matrizes de Spearman dos dois datasets (compare com as de Pearson no material irmão).

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000006_496aa93e4f7145401af30a41a40d4cb28f5b1744670d62af6bbadf94c45da433.png)

Na maioria dos pares, ρ e r são muito parecidos - sinal de relações aproximadamente lineares e sem outliers decisivos. Vale olhar onde eles mais diferem :

| Dataset   | Par                  | Pearson r   | Spearman ρ   | ρ - r   |
|-----------|----------------------|-------------|--------------|---------|
| Música    | Anúncios × Horas     | -0,01       | 0,05         | 0,06    |
| Música    | Satisfação × Horas   | 0,21        | 0,15         | -0,06   |
| Delivery  | Avaliação × Tempo    | -0,59       | -0,54        | 0,06    |
| Música    | Playlists × Horas    | 0,54        | 0,50         | -0,04   |
| Música    | Anúncios × Playlists | -0,32       | -0,28        | 0,04    |
| Delivery  | Valor × Taxa         | 0,03        | -0,01        | -0,04   |

Como ler: diferenças   pequenas   (menos   de   0,1)   não   mudam   a   conclusão.   Quando   a diferença é grande, investigue: outliers (r maior que ρ, puxado por poucos pontos), curvas monotônicas (ρ maior que r) ou variáveis com muitos empates/discretas (como a avaliação e as playlists).

```
dif = (df[cols].corr("spearman") - df[cols].corr("pearson")).round(2) dif.where(dif.abs() >= 0.05)      # mostra só as diferenças relevantes
```

## 12. O que pesa na nota do cliente? Spearman por subgrupo NÍVEL 4

Como a avaliação é ordinal, o ρ é a medida adequada para relacioná-la com o tempo de entrega. Calculado por subgrupo:

Figura 7 - A relação tempo × avaliação em cada subgrupo.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Spearman_artifacts/image_000007_38d83b0aee86dad457c9f3d8a7f082b0e0358d0daae928814aa64b777fca4d65.png)

```
for col in ["chuva", "turno", "veiculo"]: for nome, g in df.groupby(col): rho = stats.spearmanr(g["tempo_entrega_min"], g["avaliacao"]).statistic print(col, nome, len(g), round(rho, 2))
```

Leitura: a relação é negativa em todos os grupos. É mais fraca na bicicleta (ρ = -0,30), que só faz entregas curtas - de novo a restrição de amplitude : com pouca variação no tempo, a ordem das notas fica menos previsível. No jantar a relação é mais forte que no almoço.

## 13. App de música: escalas, contagens e grupos NÍVEL 4

| Par                   | Grupo       | Pearson r   | Spearman ρ   | Comentário                                                                 |
|-----------------------|-------------|-------------|--------------|----------------------------------------------------------------------------|
| Anúncios × satisfação | todos       | -0,82       | -0,81        | inflado pelo plano (Premium: 0 anúncios e satisfação alta)                 |
| Anúncios × satisfação | só Gratuito | -0,42       | -0,39        | relação real, moderada; satisfação 0-10 é quase ordinal: ρ é o mais seguro |
| Playlists × horas     | todos       | 0,54        | 0,50         | playlists é uma contagem com só 13 valores distintos (muitos empates)      |
| Idade × horas         | todos       | -0,65       | -0,66        | relação aproximadamente linear: os dois concordam                          |

O Spearman não resolve variáveis de confusão: o ρ geral de anúncios × satisfação (-0,81) é tão inflado pelo plano quanto o r. Estratificar (calcular por grupo) continua necessário.

## 14. Cuidado com dados agregados NÍVEL 4

Agrupando os pedidos por bairro (5 bairros), calculamos a distância média e a mediana do tempo de cada um. O resultado: ρ = 1 entre distância média e tempo mediano, e ρ = -1 entre distância média e avaliação média.

```
b = df.groupby("bairro").agg(dist=("distancia_km", "mean"), tempo=("tempo_entrega_min", "median"), aval=("avaliacao", "mean")) b.corr(method="spearman")      # ρ = 1 e ρ = -1 com apenas 5 linhas
```

## CORRELAÇÃO PERFEITA COM 5 PONTOS

(1) Com n = 5, ρ = ±1 acontece com facilidade: basta a ordem dos bairros coincidir. O p-valor   que   o   SciPy   devolve   nesse   caso   não   é   confiável.   (2)   Agregar esconde a variação dentro dos grupos : no nível dos pedidos, distância × tempo tem ρ = 0,72, não 1. Concluir sobre indivíduos a partir de médias de grupos é a falácia ecológica .

## 15. Pearson ou Spearman? Quadro de decisão

| Situação                                                                         | Use                                 | Por quê                                                                |
|----------------------------------------------------------------------------------|-------------------------------------|------------------------------------------------------------------------|
| Duas variáveis numéricas, relação aproximadamente linear, sem outliers decisivos | Pearson (pode reportar os dois)     | usa toda a informação dos valores; liga-se à reta de regressão e ao r² |
| Pelo menos uma variável ordinal (notas, escalas, níveis)                         | Spearman                            | só a ordem é confiável                                                 |
| Relação monotônica, mas curva                                                    | Spearman                            | mede consistência da ordem, não ajuste a uma reta                      |
| Outliers que você não pode (ou não deve) remover                                 | Spearman (e investigue os outliers) | postos limitam a influência de valores extremos                        |
| Muitos empates ou amostra pequena                                                | Spearman ou Kendall                 | Kendall lida bem com empates                                           |
| Relação em "U" ou "∩", ou variável categórica nominal                            | nenhum dos dois                     | use gráficos e comparação de grupos                                    |

Boa prática: calcule   os   dois.   Se   concordam,   a   conclusão   é   robusta.   Se   discordam,   a diferença é uma pista: volte ao gráfico.

## Parte IV - Exercícios progressivos

Do conceitual à aplicação; respostas no Apêndice B

## Exercício 1 NÍVEL 1

Classifique cada relação como linear, monotônica não linear ou não monotônica: (a) distância × taxa de entrega, em que cada km a mais soma sempre o mesmo valor à taxa; (b) horas de estudo × nota, que sobe rápido e depois se estabiliza perto de 10; (c) idade × horas de sono, maior em bebês e idosos e menor em adultos.

## Exercício 2 NÍVEL 1

Atribua postos (com posto médio nos empates) às avaliações [3, 5, 4, 4, 2, 5, 4].

## Exercício 3 NÍVEL 2

Calcule à mão o ρ de Spearman para x = [2, 4, 6, 8, 10, 12] e y = [3,0; 2,5; 5,0; 4,5; 8,0; 7,0] usando a fórmula com Σd². Confira com stats.spearmanr .

## Exercício 4 NÍVEL 2

Por que a fórmula ρ = 1 - 6Σd² / [n(n² - 1)] não deve ser usada quando há muitos empates? O que fazer nesse caso?

## Exercício 5 NÍVEL 3

Para cada situação, escolha Pearson, Spearman ou nenhum: (a) avaliação (1-5) × tempo de entrega; (b) distância × taxa de entrega; (c) dia da semana (1-7) × valor do pedido; (d) horas ouvidas × satisfação (0-10) com alguns usuários extremos.

## Exercício 6 NÍVEL 3

Um colega encontrou r = 0,87 e ρ = 0,69 em 13 pedidos. O que essa diferença sugere? O que ele deveria fazer?

## Exercício 7 NÍVEL 4

No dataset de delivery, calcule em Python o ρ entre avaliação e valor do pedido. Interprete o resultado e compare com a relação avaliação × tempo.

## Exercício 8 NÍVEL 4

No nível dos bairros, distância média × tempo mediano tem ρ = 1, mas no nível dos pedidos ρ = 0,72. Explique a diferença e qual dos dois números usar para prever o tempo de um pedido específico.

## Apêndice A - Colinha de Spearman em Python

```
import pandas as pd from scipy import stats df["x"].rank()                                  # postos (empates: posto médio) df["x"].corr(df["y"], method="spearman")        # ρ (pandas) res = stats.spearmanr(df["x"], df["y"])          # ρ + p-valor res.statistic, res.pvalue stats.pearsonr(df["x"].rank(), df["y"].rank())   # mesmo ρ: Pearson dos postos df[colunas].corr(method="spearman")             # matriz de Spearman df[colunas].corr("spearman") - df[colunas].corr("pearson")   # onde diferem for nome, g in df.groupby("grupo"):              # ρ por subgrupo print(nome, stats.spearmanr(g["x"], g["y"]).statistic) stats.kendalltau(df["x"], df["y"])               # alternativa com muitos empates
```

## Apêndice B - Respostas dos exercícios

1. (a) linear (e, portanto, também monotônica) - Pearson e Spearman concordam; (b) monotônica não linear - use Spearman; (c) não monotônica (∪) - nenhum coeficiente resume bem; mostre o gráfico ou compare faixas etárias.
2. Ordenando: 2, 3, 4, 4, 4, 5, 5. Postos: 2 → 1; 3 → 2; os três "4" ocupam 3, 4, 5 → 4; os dois "5" ocupam 6 e 7 → 6,5. Na ordem original: [2; 6,5; 4; 4; 1; 6,5; 4].
3. Postos de x: 1 a 6. Postos de y: 3,0 → 2; 2,5 → 1; 5,0 → 4; 4,5 → 3; 8,0 → 6; 7,0 → 5. d = -1, +1, -1, +1, -1, +1 → Σd² = 6. ρ = 1 - 6 × 6 / (6 × 35) = 1 - 36/210 = 0,829 . stats.spearmanr(x, y).statistic → 0,829.
4. A fórmula com Σd² é um atalho derivado supondo postos 1, 2, …, n sem repetição. Com empates, os postos médios mudam as variâncias dos postos e a fórmula fica imprecisa (na Seção 5 deu -0,73 em vez de -0,84). Calcule o Pearson dos postos - é o que spearmanr e corr(method="spearman") fazem.
5. (a) Spearman (avaliação é ordinal); (b) Pearson (numéricas, relação linear - e quase redundantes);   (c)   nenhum:   o   padrão   não   é   monotônico;   compare   os   dias   como categorias; (d) Spearman (e investigue os extremos), ou os dois para comparar.
6. r bem maior que ρ sugere que poucos pontos extremos estão "puxando" o Pearson (Seção 7 do material de Pearson: um pedido a 14 km). Ele deve olhar o gráfico, identificar e investigar o ponto, reportar r com e sem ele e considerar o ρ como medida principal.

7. df["avaliacao"].corr(df["valor\_pedido"], method="spearman") = -0,021: praticamente nenhuma relação - o valor do pedido não influencia a nota. Já avaliação × tempo tem ρ = -0,54: a nota depende da demora, não do tamanho do pedido.
8. As médias/medianas por bairro eliminam a variação entre pedidos do mesmo bairro, e com apenas 5 pontos uma ordem perfeita é fácil de ocorrer. Para prever o tempo de um pedido   específico   vale   a   relação   individual   (ρ   =   0,72,   ou   o   Pearson   e   a   reta   de regressão), que mostra quanta incerteza existe pedido a pedido. O ρ = 1 descreve só a ordem dos bairros.

## Referências

- SPEARMAN, C. The proof and measurement of association between two things. The American Journal of Psychology , v. 15, n. 1, p. 72-101, 1904. ·
- BUSSAB, W. O.; MORETTIN, P . A. Estatística Básica . 9. ed. São Paulo: Saraiva, 2017. ·
- FIELD, A. Descobrindo a estatística usando o SPSS . 2. ed. Porto Alegre: Artmed, 2009 - cap. Correlação (Spearman e Kendall). ·
- SIEGEL, S.;   CASTELLAN JR.,   N.   J. Estatística   não-paramétrica   para   ciências   do comportamento . 2. ed. Porto Alegre: Artmed, 2006. ·
- SciPy - documentação de scipy.stats.spearmanr e kendalltau ; pandas - Series.rank e DataFrame.corr . ·