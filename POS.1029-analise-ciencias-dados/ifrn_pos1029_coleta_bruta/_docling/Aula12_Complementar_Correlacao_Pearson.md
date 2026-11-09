| Relação com a aula   | Aprofunda o r de Pearson usado nos gráficos de dispersão e no mapa de calor da Aula 12 - Laboratório: Matplotlib, Seaborn e Plotly   |
|----------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| Como está organizado | Progressivo: intuição → cálculo à mão → interpretação → armadilhas → aplicações nos datasets → exercícios com respostas              |
| Pré-requisitos       | Média e desvio-padrão (Aula 11); gráfico de dispersão (Aula 12)                                                                      |
| Dados                | Os mesmos da Aula 12 (sintéticos): 600 pedidos da hamburgueria Brasa & Pão e 240 usuários do app de música                           |
| Ferramentas          | pandas , scipy.stats , numpy , seaborn                                                                                               |
| Material irmão       | Correlação de Spearman: do conceito à aplicação (leia depois deste)                                                                  |
| Professor            | Plácido Antônio de Souza Neto                                                                                                        |

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000000_54a44aa5e81952c58f2f56fc74fb42e485044b6c8aa6c653f9c6866307938376.png)

## Objetivos de aprendizagem

Ao final deste material, espera-se que o estudante seja capaz de:

- Explicar o que o coeficiente de Pearson mede (força e sentido de uma relação linear ) e o que ele não mede. 1.
- Calcular o r à mão, passo a passo, a partir das médias, dos desvios e da covariância - e conferir em Python. 2.
- Interpretar o valor de r, o r² e a inclinação da reta de regressão no contexto dos dados. 3.
- Reconhecer as armadilhas: relações não lineares, outliers, restrição de amplitude, variáveis de confusão e variância zero. 4.
- Aplicar a   análise   completa   -   gráfico,   r,   intervalo   de   confiança,   subgrupos   e correlação parcial - aos datasets da aula. 5.

## Como estudar este material

| Nível          | Seções   | Você vai…                                                                         |
|----------------|----------|-----------------------------------------------------------------------------------|
| 1 · Intuição   | 1 e 2    | enxergar associação positiva, negativa e nula, e entender a ideia dos quadrantes  |
| 2 · Cálculo    | 3 a 5    | transformar a ideia em fórmula, calcular o r de 8 pedidos à mão e ler o resultado |
| 3 · Armadilhas | 6 a 11   | ver quando o r engana e como se proteger                                          |
| 4 · Aplicações | 12 a 16  | fazer a análise completa nos dois datasets, até a correlação parcial              |
| 5 · Prática    | Parte IV | resolver 8 exercícios progressivos (respostas no Apêndice B)                      |

| SOBRE OS DADOS                                                                                                            |
|---------------------------------------------------------------------------------------------------------------------------|
| Os dois conjuntos são sintéticos (gerados por gerar_dados.py , no pacote da Aula 12).                                     |
| Delivery: 600 pedidos com distância, tempo de entrega, taxa, itens, valor, avaliação (1-                                  |
| 5), bairro, veículo, chuva e turno. App de música: 240 usuários com idade, plano                                          |
| (Gratuito/Premium), horas ouvidas por semana, playlists, anúncios por semana e satisfação (0-10). Nenhum registro é real. |

## Parte I - Intuição e conceito

Do gráfico de dispersão à fórmula do r

## 1. Associação entre duas variáveis NÍVEL 1

Duas variáveis numéricas estão associadas quando conhecer o valor de uma ajuda a prever a outra. O primeiro passo é sempre o gráfico de dispersão : cada ponto é uma observação, com uma variável no eixo x e a outra no eixo y. Três padrões básicos aparecem nos dados da aula:

Figura 1 - Associação positiva (pedidos mais distantes demoram mais), negativa (usuários mais velhos ouvem menos) e praticamente nula (a distância não diz nada sobre o valor do pedido).

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000001_ca379f5b9e0c42a88d1e0b6ed4999251fe449beb0c24f532c659ce23c7c8e624.png)

- Positiva: quando x cresce, y tende a crescer (nuvem 'subindo'). ·
- Negativa: quando x cresce, y tende a diminuir (nuvem 'descendo'). ·
- Nula: a nuvem não tem inclinação; x não ajuda a prever y. ·

O coeficiente de correlação de Pearson (r) resume em um único número, entre -1 e +1, o sentido (sinal)   e   a força (distância   até   ±1)   dessa   tendência   -   desde   que   ela   seja aproximadamente uma linha reta .

## 2. A ideia dos quadrantes NÍVEL 1

Como transformar "a nuvem sobe" em número? Trace uma linha vertical na média de x (x̄) e uma horizontal na média de y (ȳ). O gráfico fica dividido em quatro quadrantes. Para cada ponto, calcule o desvio de cada variável em relação à sua média e multiplique os dois:

- ponto acima e à direita (desvios + e +) ou abaixo e à esquerda (- e -) → produto positivo : 'concorda' com uma relação positiva; ·
- ponto acima e à esquerda ou abaixo e à direita (sinais opostos) → produto negativo : 'concorda' com uma relação negativa. ·

Figura 2 - Oito pedidos de até 3 km. Verdes: produto dos desvios positivo (quadrantes II e III); laranja: produto negativo (I e IV). Há mais pontos verdes, e eles estão mais longe do centro.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000002_3bbcd8658ccba23b8bd8d86bae0fe867f2168bfa3ad4598f3ff29ea18161066f.png)

Somando todos os produtos, o resultado será positivo se predominarem os pontos dos quadrantes II e III, negativo se predominarem os de I e IV, e próximo de zero se eles se equilibrarem. Essa soma (dividida por n - 1) é a covariância .

## 3. Da covariância ao r: padronizar NÍVEL 2

<!-- formula-not-decoded -->

A covariância tem um problema: ela depende das unidades . Medir a distância em metros em vez de quilômetros multiplica a covariância por 1.000, sem mudar em nada a relação. Por isso não dá para dizer se uma covariância de 3,8 é 'grande' ou 'pequena'.

A solução é padronizar : dividir pela variabilidade de cada variável (os desvios-padrão s x e s y ). O resultado não tem unidade e fica sempre entre -1 e +1:

<!-- formula-not-decoded -->

em que z = (valor - média) / desvio-padrão é o escore padronizado de cada observação

A segunda forma mostra o que o r realmente é: praticamente a média dos produtos dos escores-z (a soma é dividida por n - 1). Cada ponto contribui com o quanto ele está, ao mesmo tempo, acima (ou abaixo) da média em x e em y, medido em desvios-padrão.

## 4. Calculando à mão: 8 pedidos NÍVEL 2

Vamos refazer a conta para os 8 pedidos da Figura 2 (x = distância, y = tempo).

- 1 Médias: x̄ = 16,8 / 8 = 2,10 km ; ȳ = 263 / 8 = 32,875 min .
- 2 Desvios e produtos, linha a linha:

| Ponto   |   Pedido | x (km)   |   y (min) | x - x̄   | y - ȳ   | (x - x̄)(y - ȳ)   | z x   | z y   | z x ·z y   |
|---------|----------|----------|-----------|----------|---------|-------------------|-------|-------|------------|
| P1      |       50 | 0,7      |        23 | -1,40    | -9,88   | 13,83             | -1,68 | -1,49 | 2,51       |
| P2      |       82 | 2,4      |        35 | 0,30     | 2,12    | 0,64              | 0,36  | 0,32  | 0,12       |
| P3      |      569 | 1,7      |        30 | -0,40    | -2,88   | 1,15              | -0,48 | -0,43 | 0,21       |
| P4      |      159 | 3,0      |        46 | 0,90     | 13,12   | 11,81             | 1,08  | 1,98  | 2,15       |
| P5      |      149 | 2,2      |        29 | 0,10     | -3,88   | -0,39             | 0,12  | -0,59 | -0,07      |
| P6      |      504 | 2,7      |        31 | 0,60     | -1,88   | -1,13             | 0,72  | -0,28 | -0,20      |
| P7      |       16 | 2,9      |        35 | 0,80     | 2,12    | 1,70              | 0,96  | 0,32  | 0,31       |
| P8      |      287 | 1,2      |        34 | -0,90    | 1,12    | -1,01             | -1,08 | 0,17  | -0,18      |
| Soma    |          | 16,8     |       263 | 0,00     | 0,00    | 26,60             | 0,00  | 0,00  | 4,83       |

- 3 Covariância: 26,60 / (8 - 1) = 3,80 km·min.
- 4 Desvios-padrão: s x = 0,8315 km e s y = 6,6211 min.
- 5 Coeficiente: r = 3,80 / (0,8315 × 6,6211) = 0,690 . Pela outra fórmula: Σ z x z y / 7 = 4,831 / 7 = 0,690.
- 6 Conferência em Python:

```
import numpy as np, pandas as pd from scipy import stats x = np.array([0.7, 2.4, 1.7, 3.0, 2.2, 2.7, 2.9, 1.2]) y = np.array([23, 35, 30, 46, 29, 31, 35, 34]) cov = ((x - x.mean()) * (y - y.mean())).sum() / (len(x) - 1)   # 3,80 r = cov / (x.std(ddof=1) * y.std(ddof=1))                      # 0,690 stats.pearsonr(x, y).statistic                                 # 0,690 np.corrcoef(x, y)[0, 1]                                        # 0,690 pd.Series(x).corr(pd.Series(y))                                # 0,690 (padrão do pandas: Pearson)
```

## ATENÇÃO AO DDOF

O pandas usa n - 1 no desvio-padrão ( ddof=1 ), mas o np.std usa n por padrão. Na fórmula do r, o importante é usar o mesmo denominador na covariância e nos desvios - por isso np.corrcoef e stats.pearsonr dão o mesmo resultado.

## 5. Lendo o valor de r e o r² NÍVEL 2

Figura 3 - Como 'parece' cada valor de r (120 pontos simulados em cada painel). Repare que r = 0,4 já é uma nuvem bem espalhada.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000003_bb3242f9df6b4af0e98ce9539a65de63afa971e55937fa736cc589f77c3002a2.png)

Sinal = sentido da relação. Valor absoluto = quão perto os pontos estão de uma reta. Uma referência comum (não é uma regra fixa; depende da área):

| &#124;r&#124;   | Leitura usual             | Exemplo nos dados da aula                                       |
|-----------------|---------------------------|-----------------------------------------------------------------|
| 0,00 - 0,19     | muito fraca / desprezível | distância × valor do pedido (r = 0,03)                          |
| 0,20 - 0,39     | fraca                     | idade × satisfação (r = 0,20)                                   |
| 0,40 - 0,59     | moderada                  | distância × avaliação (r = -0,43); playlists × horas (r = 0,54) |
| 0,60 - 0,79     | forte                     | distância × tempo (r = 0,71); idade × horas (r = -0,65)         |
| 0,80 - 1,00     | muito forte               | itens × valor (r = 0,92); anúncios × satisfação (r = -0,82)     |

O r² (coeficiente de determinação) é a proporção da variação de y que a reta "explica" a partir de x. Para distância × tempo, r = 0,71 e r² = 0,51: cerca de 51% da variação do tempo de entrega acompanha a distância; os outros 49% vêm de chuva, turno, veículo, atrasos etc.

## R NÃO É PORCENTAGEM

Um erro frequente é ler r = 0,71 como '71% de relação'. A proporção explicada é o r² (51%). E r = 0,4 não é 'metade' de r = 0,8: em termos de r², 0,16 contra 0,64 - quatro vezes menos.

## Parte II - Armadilhas: quando o r engana

O r é um resumo - e todo resumo esconde coisas

## 6. Pearson mede só relação linear NÍVEL 3

O quarteto de Anscombe (1973) tem quatro conjuntos com médias, variâncias, reta de regressão e r = 0,82 iguais . Os gráficos são completamente diferentes:

Figura 4 - Quarteto de Anscombe. I: relação linear (o r descreve bem). II: curva (relação perfeita, mas não linear). III: linear com um outlier. IV: sem relação, com um único ponto criando o r.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000004_68746220c8d8f4ae8c0607bad5f5725f2c196528d03d7443e07989c970c1966e.png)

Lição: nunca reporte um r sem olhar o gráfico de dispersão. Se a relação for curva mas sempre crescente (ou sempre decrescente), use o coeficiente de Spearman (material irmão). Se for em "U", nenhum dos dois coeficientes resume bem a relação.

## 7. Outliers podem criar ou destruir uma correlação NÍVEL 3

Como o r usa os desvios em relação à média, um único ponto muito afastado pode dominar a   soma   dos   produtos.   Veja   o   que   acontece   com   12   pedidos   de   até   3   km   quando acrescentamos um pedido:

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000005_bcc459a5041385f97f268dd3b7127a90a7fe1b2328af0344ce5a37d2403cfe5c.png)

Figura 5 - O mesmo grupo de 12 pedidos (azul) com um ponto a mais (laranja).

| Cenário                     | Pearson r   | Spearman ρ (veja o material irmão)   |
|-----------------------------|-------------|--------------------------------------|
| 12 pedidos de até 3 km      | 0,58        | 0,61                                 |
| + 1 pedido distante (14 km) | 0,87        | 0,69                                 |
| + 1 atraso (1,8 km, 71 min) | 0,15        | 0,45                                 |

Um pedido distante, que até segue a tendência, faz o r saltar de 0,58 para 0,87 (o ponto 'puxa' a reta). Um único atraso faz o r cair para 0,15. O Spearman, que trabalha com postos, varia bem menos.

## O QUE FAZER COM OUTLIERS

- 1) Investigue: é erro de digitação ou um caso real (pedido trocado, endereço errado)?
- 2) Calcule o r com e sem o ponto e reporte os dois. 3) Considere o Spearman. Nunca apague um ponto só porque ele atrapalha o resultado.

## 8. Restrição de amplitude NÍVEL 3

O r depende da faixa de valores observada. Se olharmos só uma 'fatia' do eixo x, a parte previsível da variação diminui e o r cai - mesmo que a relação seja a mesma.

Figura 6 - Todos os pedidos: r = 0,71. Só os pedidos de até 3 km: r = 0,42.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000006_5a0e82797b7e4df139a59612814299a48f6ce17ae2efb0cdd66077debd620be3.png)

Isso explica um resultado curioso da aula: a correlação distância × tempo é 0,53 nas entregas de bicicleta e 0,77 nas de moto .   A   bicicleta   não   é   "menos   afetada"   pela distância - ela só faz entregas de até 3 km, uma faixa estreita. Comparando a mesma faixa (até 3 km), a moto tem r = 0,30.

## 9. Variável de confusão: correlação não é causalidade NÍVEL 3

Uma terceira variável pode criar, aumentar ou esconder uma correlação. No app de música, o plano faz as duas coisas:

Figura 7 - À esquerda, a correlação geral é inflada pelo plano. À direita, a correlação geral é atenuada por ele.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000007_63dc795ce6d545e7bb38b6d7f4340ee9d446f1bc96a565fc2dcef1d09f12ace5.png)

- Anúncios × satisfação: r   geral   =   -0,82.   Mas   os   usuários   Premium   têm zero anúncios e satisfação alta - eles formam a coluna à esquerda e "puxam" a reta. Dentro do plano Gratuito, r = -0,42: a relação existe, mas é bem mais fraca. ·

- Idade × horas: r geral = -0,65, mas dentro de cada plano o r é mais forte (-0,76 e -0,75). Usuários mais velhos tendem a ser Premium, e Premium ouve mais; misturar os grupos 'dilui' a relação. ·

Mesmo um r forte não prova que x causa y.   Causalidade   exige   desenho   de   estudo (experimento, controle de variáveis), não só correlação.

## 10. Variância zero e variáveis redundantes NÍVEL 3

Variância zero: no plano Premium, anuncios\_semana vale 0 para todos. Como s x = 0, a fórmula divide por zero e o r não existe (o pandas devolve NaN e o SciPy emite um aviso). Não é "correlação zero" - é correlação indefinida.

Redundância: distância × taxa de entrega tem r = 0,99, porque a taxa é calculada a partir da distância. Variáveis quase idênticas não trazem informação nova; em modelos (Unidade 4) uma delas costuma ser descartada.

## 11. O r é uma estimativa: p-valor e intervalo de confiança NÍVEL 3

Os 600 pedidos são uma amostra; outro período daria outro r. O scipy.stats.pearsonr devolve, além do r:

- o p-valor do teste "a correlação na população é zero?" - p pequeno (ex.: &lt; 0,05) indica que um r desse tamanho dificilmente apareceria por acaso; ·
- o intervalo de confiança de 95% (via transformação z de Fisher) - a faixa de valores plausíveis para a correlação populacional. ·

```
res = stats.pearsonr(df["distancia_km"], df["tempo_entrega_min"]) res.statistic                  # r = 0,713 res.pvalue                     # p ≈ 4e-94  (praticamente zero) res.confidence_interval()      # IC 95%: (0,671 ; 0,750)
```

## SIGNIFICATIVO NÃO É O MESMO QUE FORTE

Com amostras grandes, até um r = 0,10 pode ter p &lt; 0,05. O p-valor diz se a correlação provavelmente existe ; o valor de r e o IC dizem se ela é importante . Com amostras pequenas (como os 8 pedidos da Seção 4), o IC fica muito largo.

## Parte III - Aplicações nos datasets da aula

A análise completa, do gráfico à correlação parcial

## 12. Distância × tempo, do começo ao fim NÍVEL 4

Um roteiro completo para um par de variáveis:

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000008_d90e246ccc296f267c4579461756c78135f25eec2582c9e37eb738a5885cca8c.png)

1 Gráfico (dispersão) - a relação é aproximadamente linear? Há outliers? 2 r e IC 95% . 3 r² e a reta . 4 Subgrupos : a relação se mantém nas categorias importantes?

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000009_968edda3d625b303fd9bf89ea2247188a391b30aa6c29fff7ea28d6d3188eae2.png)

Figura 8 - A relação é aproximadamente linear, com alguns atrasos excepcionais acima da reta.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000010_e3a22403986a4d0642e358010b1c0506bc656023efd0d465d92f0fd48ef96c3b.png)

- r   = 0,713 ,   IC   95%   [0,671   ;   0,750]   -   relação   positiva   forte,   estimada   com   boa precisão (n = 600). ·
- r² = 0,51 - a distância acompanha metade da variação do tempo. ·
- A inclinação da reta se relaciona com o r: b = r × s y / s x = 0,713 × 10,36 / 2,63 = 2,80 min por km .   O r é a inclinação 'em desvios-padrão': se a distância sobe 1 desvio-padrão, o tempo sobe, em média, 0,71 desvio-padrão. ·
- Por subgrupo: sem chuva r = 0,75, com chuva r = 0,71. A chuva desloca a nuvem para cima (+ minutos), mas mantém a força da relação. ·

```
for chuva, g in df.groupby("chuva"): print(chuva, round(g["distancia_km"].corr(g["tempo_entrega_min"]), 2))
```

## 13. A matriz de correlação NÍVEL 4

Com várias variáveis   numéricas,   calculamos   o   r   de   todos   os   pares   de   uma   vez   com df[colunas].corr() e o exibimos como mapa de calor (Aula 12).

Figura 9 - Matrizes de correlação de Pearson dos dois datasets.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Complementar_Correlacao_Pearson_artifacts/image_000011_4c41de1af09480f68cf65b93317dd70814eee2757b4fb07f9bb3fdcc4f4ce8a4.png)

Como ler   uma   matriz,   em   ordem: (1)   procure   os   |r|   mais   altos;   (2)   separe   os 'óbvios' (taxa × distância, itens × valor: redundâncias ou definições) dos interessantes; (3) para cada par interessante, volte ao gráfico de dispersão e verifique linearidade, outliers e subgrupos - a matriz não mostra nada disso.

| Par                   | r     | Leitura                                                                                        |
|-----------------------|-------|------------------------------------------------------------------------------------------------|
| Distância × taxa      | 0,99  | redundante: a taxa é calculada pela distância                                                  |
| Itens × valor         | 0,92  | esperado: mais itens, pedido mais caro                                                         |
| Distância × tempo     | 0,71  | relação forte e linear (Seção 12)                                                              |
| Tempo × avaliação     | -0,59 | entregas demoradas recebem notas menores - mas avaliação é ordinal (1-5): confira com Spearman |
| Valor × tempo         | 0,05  | o tamanho do pedido quase não afeta o tempo                                                    |
| Anúncios × satisfação | -0,82 | muito forte, mas inflado pelo plano (Seção 9)                                                  |
| Idade × horas         | -0,65 | forte; mais forte ainda dentro de cada plano                                                   |

## 14. Correlação parcial: controlando o plano NÍVEL 4

Na Seção 9 separamos os grupos à mão. A correlação parcial faz isso de forma geral: mede a relação entre x e y depois de remover o efeito de uma terceira variável z. A ideia tem dois passos:

1 Explique x por z com uma regressão e guarde o que sobra (os resíduos de x); faça o mesmo com y. 2 Calcule o Pearson entre os dois resíduos.

Há também uma fórmula direta, a partir das três correlações simples:

<!-- formula-not-decoded -->

Com x = anúncios, y = satisfação e z = plano (Premium = 1, Gratuito = 0): r xy  = -0,821, r xz = -0,883 e r yz = 0,835, o que dá r xy·z = -0,325 .

```
m["premium"] = (m["plano"] == "Premium").astype(int) def residuo(alvo, controle): b1, b0 = np.polyfit(controle, alvo, 1)      # reta alvo ~ controle return alvo - (b0 + b1 * controle) r_parcial = stats.pearsonr(residuo(m["anuncios_semana"], m["premium"]), residuo(m["satisfacao"], m["premium"])).statistic   # -0,325
```

Leitura: de -0,82 (geral) para -0,32 (controlando o plano). A maior parte da correlação original vinha da diferença entre os planos; descontado o plano, sobra uma relação negativa fraca a moderada entre anúncios e satisfação.

## 15. Pearson e a reta de regressão NÍVEL 4

Correlação e regressão linear simples são duas faces da mesma conta:

|          | Correlação (r)                 | Regressão (y = b₀ + b₁·x)                            |
|----------|--------------------------------|------------------------------------------------------|
| Pergunta | quão forte é a relação linear? | quanto y muda, em média, quando x aumenta 1 unidade? |
| Simetria | simétrica: r(x, y) = r(y, x)   | não é simétrica: prever y por x ≠ prever x por y     |
| Unidade  | sem unidade, de -1 a 1         | na unidade de y por unidade de x (2,80 min/km)       |
| Ligação  | r² = proporção explicada       | b₁ = r · s y / s x                                   |

Na Unidade 4 (Aprendizado de Máquina) a regressão volta, com várias variáveis ao mesmo tempo. A matriz de correlação é a primeira ferramenta para escolher quais variáveis usar e quais são redundantes.

## 16. Roteiro de análise de correlação (checklist)

- As duas variáveis são numéricas (contínuas ou discretas com muitos valores)? Se uma for ordinal, prefira Spearman. 1.
- Faça o gráfico de dispersão : a relação é aproximadamente linear? 2.
- Procure outliers ; calcule o r com e sem eles. 3.
- Calcule r, IC 95% e p-valor ; reporte também o n . 4.
- Interprete sentido, força e r² no contexto (com unidades). 5.
- Verifique subgrupos e   possíveis variáveis   de   confusão ;   se   necessário,   use   a correlação parcial. 6.
- Não conclua causalidade a partir da correlação. 7.

## Parte IV - Exercícios progressivos

Do conceitual à aplicação; respostas no Apêndice B

## Exercício 1 NÍVEL 1

Para cada valor de r, diga o sentido e a força da relação: (a) r = -0,85; (b) r = 0,12; (c) r = 0,63; (d) r = -0,35.

## Exercício 2 NÍVEL 1

Um gráfico de dispersão tem a maioria dos pontos nos quadrantes I e IV (acima e à esquerda; abaixo e à direita das médias). O que você espera do sinal da covariância e do r?

## Exercício 3 NÍVEL 2

Calcule à mão o r de Pearson para x = distância (km) = 1, 2, 3, 4, 5 e y = tempo (min) = 20, 26, 27, 33, 34. Confira com np.corrcoef .

## Exercício 4 NÍVEL 2

No app de música, idade × horas tem r = -0,65. Calcule e interprete o r².

## Exercício 5 NÍVEL 3

Por que a correlação distância × tempo é menor nas entregas de bicicleta do que nas de moto? Isso significa que a distância afeta menos a bicicleta?

## Exercício 6 NÍVEL 3

Ao calcular anuncios\_semana × satisfacao apenas para usuários Premium, o pandas devolve NaN . Por quê?

## Exercício 7 NÍVEL 4

Usando o dataset de delivery, calcule em Python o r entre itens e valor do pedido e entre valor do pedido e tempo de entrega. Interprete os dois resultados.

## Exercício 8 NÍVEL 4

No app de música, a correlação geral anúncios × satisfação é -0,82, a correlação só no plano Gratuito é -0,42 e a correlação parcial controlando o plano é -0,32. Explique, em um parágrafo para um gestor do aplicativo, o que esses três números dizem.

## Apêndice A - Colinha de Pearson em Python

```
import numpy as np, pandas as pd, seaborn as sns from scipy import stats df["x"].corr(df["y"])                          # r (pandas: Pearson é o padrão) np.corrcoef(df["x"], df["y"])[0, 1]            # r (NumPy) res = stats.pearsonr(df["x"], df["y"])         # r + p-valor + IC res.statistic, res.pvalue, res.confidence_interval() res.statistic ** 2                             # r² df[colunas].corr()                             # matriz de correlação df.groupby("grupo")[["x", "y"]].corr()         # matriz por subgrupo reg = stats.linregress(df["x"], df["y"])       # reta: reg.intercept + reg.slope * x sns.regplot(data=df, x="x", y="y")             # dispersão + reta + IC 95% da reta sns.heatmap(df[colunas].corr(), annot=True, fmt=".2f", cmap="vlag", center=0, vmin=-1, vmax=1)
```

## Apêndice B - Respostas dos exercícios

1. (a) negativa muito forte; (b) positiva muito fraca/desprezível; (c) positiva forte; (d) negativa fraca.
2. Nos quadrantes I e IV os desvios têm sinais opostos, então os produtos são negativos: covariância negativa e r negativo (relação decrescente).
4. r² = (-0,65)² ≈ 0,42: cerca de 42% da variação das horas ouvidas acompanha a idade; o sinal negativo indica que usuários mais velhos ouvem menos, em média.
5. Restrição de amplitude (Seção 8): a bicicleta só faz entregas de até 3 km, uma faixa estreita de x. Com pouca variação em x, o r fica menor. Não significa que a distância afete menos a bicicleta; na mesma faixa (até 3 km) a moto também tem r baixo (0,30).
6. Todos os Premium têm 0 anúncios: o desvio-padrão de x é zero e a fórmula do r divide por zero. A correlação é indefinida (não é zero).
7. df["itens"].corr(df["valor\_pedido"]) = 0,92   (muito   forte   e   esperado:   o   valor   é praticamente a soma dos itens). df["valor\_pedido"].corr(df["tempo\_entrega\_min"]) = 0,05 (desprezível: pedidos maiores não demoram mais para chegar).

```
3. x̄ = 3; ȳ = 28. Desvios de x: -2, -1, 0, 1, 2; de y: -8, -2, -1, 5, 6. Produtos: 16, 2, 0, 5, 12 → soma = 35; cov = 35/4 = 8,75. Σ(x - x̄)² = 10 → s x = √(10/4) = 1,581; Σ(y - ȳ)² = 64 + 4 + 1 + 25 + 36 = 130 → s y  = √(130/4) = 5,701. r = 8,75 / (1,581 × 5,701) = 0,971 . np.corrcoef([1,2,3,4,5], [20,26,27,33,34])[0, 1] → 0,971.
```

8. Exemplo: "Olhando todos os usuários juntos, parece que os anúncios derrubam fortemente a satisfação (r = -0,82). Mas boa parte disso vem de comparar dois públicos diferentes: os assinantes Premium não ouvem anúncios e já são mais satisfeitos. Entre os usuários do plano gratuito, mais anúncios continuam associados a menos satisfação, porém de forma moderada (r = -0,42); controlando o plano estatisticamente, r = -0,32. Reduzir anúncios pode ajudar, mas o efeito esperado é bem menor do que o número geral sugere - e só um teste (por exemplo, A/B) mostraria causalidade."

## Referências

- ANSCOMBE, F. J. Graphs in statistical analysis. The American Statistician , v. 27, n. 1, p. 17-21, 1973. ·
- BUSSAB, W. O.; MORETTIN, P . A. Estatística Básica . 9. ed. São Paulo: Saraiva, 2017 - cap. sobre análise bidimensional. ·
- FIELD, A. Descobrindo a estatística usando o SPSS . 2. ed. Porto Alegre: Artmed, 2009 - cap. Correlação. ·
- BRUCE, P.; BRUCE, A.; GEDECK, P . Estatística prática para cientistas de dados . 2. ed. Alta Books, 2021. ·
- SciPy - documentação de scipy.stats.pearsonr ; pandas - DataFrame.corr . ·