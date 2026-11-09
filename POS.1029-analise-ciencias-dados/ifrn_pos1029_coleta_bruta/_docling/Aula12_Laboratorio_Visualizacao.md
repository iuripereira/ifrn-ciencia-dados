INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE ESPECIALIZAÇÃO EM CIÊNCIA DE DADOS · DISCIPLINA: ANÁLISE E CIÊNCIA DE DADOS

## Aula 12 - Laboratório: Matplotlib, Seaborn e Plotly

Gráficos univariados (histograma, boxplot, violino); bivariados (dispersão, barras, mapa de calor de correlação); customização e paletas de cores

| Unidade        | Unidade 3 - Análise Exploratória de Dados e Visualização (Aula 12, segunda aula da unidade)                                  |
|----------------|------------------------------------------------------------------------------------------------------------------------------|
| Natureza       | Aula prática (laboratório) em Jupyter Notebook                                                                               |
| Duração        | 1h30 - laboratório guiado (≈ 75 min) + fechamento e início do exercício (≈ 15 min)                                           |
| Pré-requisitos | Aulas 04-05 (Pandas) e Aula 11 (estatística descritiva e correlação)                                                         |
| Recursos       | Jupyter Notebook, matplotlib , seaborn , plotly , pandas , scipy ; dados sintéticos                                          |
| Avaliação      | Formulário avaliativo (10 questões) - prazo 16/11/2026, 23:59. O exercício prático é para treino e não precisa ser entregue. |
| Professor      | Plácido Antônio de Souza Neto                                                                                                |

## Objetivos de aprendizagem

Ao final desta aula, espera-se que o estudante seja capaz de:

- Escolher o gráfico adequado à pergunta e ao tipo das variáveis (univariado ou bivariado; numérica ou categórica). 1.
- Construir histogramas, boxplots e violinos e anotar neles média, mediana, quartis, IQR e outliers. 2.
- Construir gráficos de dispersão, de barras e mapas de calor e anotar r de Pearson/ Spearman, reta de regressão, intervalo de confiança e tamanho de amostra ( n ). 3.
- Customizar figuras   com   a   interface   orientada   a   objetos   do   Matplotlib:   títulos, rótulos, anotações, destaque, painéis e exportação. 4.
- Selecionar paletas qualitativas, sequenciais e divergentes adequadas aos dados e seguras para daltônicos. 5.
- Criar gráficos interativos com Plotly Express e exportá-los para HTML. 6.

## Sumário

## Parte I - Fundamentos

- 1.1 Por que visualizar · 1.2 As três bibliotecas · 1.3 Anatomia de uma figura · 1.4 Qual gráfico usar
- 1.5 Histograma · 1.6 Boxplot · 1.7 Violino · 1.8 Dispersão · 1.9 Barras · 1.10 Mapa de calor
- 1.11 Paletas de cores · 1.12 Customização · 1.13 Plotly: gráficos interativos

## Parte II - Laboratório guiado: delivery da hamburgueria

Parte III - Exercício prático: app de música (sem entrega)

Parte IV - Formulário avaliativo

Apêndice A - Colinha de visualização · Apêndice B - Referências

## SOBRE OS DADOS USADOS NESTA AULA

Os dois conjuntos são sintéticos e foram escolhidos por serem de fácil entendimento: 600 pedidos de delivery de uma hamburgueria fictícia ( Brasa &amp; Pão ),   com bairro, distância, veículo, chuva, turno, valor, tempo de entrega e avaliação; e 240 usuários de um aplicativo de música fictício  (idade,   plano,   gênero   favorito,   horas   ouvidas, anúncios e satisfação). Foram gerados por gerar\_dados.py (semente fixa) para que cada gráfico tenha algo a mostrar: uma distribuição assimétrica, outliers, uma relação linear forte,   uma   variável   redundante   e   uma   variável   de   confusão.   Nenhum   registro corresponde a pessoa ou empresa real.

## Parte I - Fundamentos

Cada gráfico responde a uma pergunta - e deve trazer o número que sustenta a resposta

## 1.1 Por que visualizar?

Na Aula 11 resumimos os dados com números. Mas números iguais podem esconder dados muito diferentes: o quarteto de Anscombe (1973) são quatro conjuntos com a mesma média, a mesma variância e o mesmo r ≈ 0,82 - e, no gráfico, um é linear, outro é uma curva,   outro   tem   um   único   outlier   que   cria   a   correlação.   Por   isso,   na   AED resumo numérico e gráfico andam juntos :   o   gráfico mostra a forma; o número dá a medida precisa. Nesta aula, todo gráfico traz escrito o valor que justifica a sua leitura.

## 1.2 As três bibliotecas

| Biblioteca            | Nível                                         | Ponto forte                                                                        | Use quando                                                       |
|-----------------------|-----------------------------------------------|------------------------------------------------------------------------------------|------------------------------------------------------------------|
| Matplotlib ( plt )    | baixo - controle total de cada elemento       | customização fina, anotações, painéis, exportação para relatório                   | precisar ajustar detalhes ou montar a figura final               |
| Seaborn ( sns )       | alto - recebe um DataFrame e nomes de colunas | gráficos estatísticos prontos: calcula médias, IC, KDE, regressão; temas e paletas | explorar rapidamente relações e distribuições                    |
| Plotly Express ( px ) | alto - uma linha por gráfico                  | interatividade ( hover , zoom, filtro pela legenda), exportação para HTML          | explorar interativamente ou compartilhar com quem não usa Python |

Seaborn é construído sobre o Matplotlib: todo gráfico do Seaborn é desenhado em um Axes do Matplotlib, que pode ser customizado depois. O Plotly é independente e gera gráficos para o navegador.

## 1.3 Anatomia de uma figura no Matplotlib

A Figure é a folha inteira (tamanho, título geral, exportação); cada Axes é uma área de plotagem com seus eixos, título, rótulos e legenda. Use sempre a interface orientada a objetos , que deixa explícito em qual gráfico cada comando atua:

```
fig, ax = plt.subplots(figsize=(9, 4))            # 1 Figure + 1 Axes sns.histplot(df["tempo_entrega_min"], ax=ax)      # Seaborn desenha DENTRO do Axes ax.axvline(df["tempo_entrega_min"].median(), ls="--", label="mediana") ax.set(title="Tempo de entrega", xlabel="Tempo (min)", ylabel="Pedidos") ax.legend() fig.savefig("figuras/histograma.png", dpi=200, bbox_inches="tight") fig, axes = plt.subplots(2, 2, figsize=(12, 8))   # grade 2×2: axes[0, 0], axes[0, 1]...
```

## 1.4 Qual gráfico usar - e que número colocar nele

| Pergunta                                    | Variáveis               | Gráfico       | Estatística no gráfico                           |
|---------------------------------------------|-------------------------|---------------|--------------------------------------------------|
| Como os valores se distribuem?              | 1 numérica              | histograma    | média, mediana, desvio-padrão, assimetria        |
| Há outliers? Como grupos se comparam?       | numérica × categórica   | boxplot       | mediana, Q1, Q3, IQR, n por grupo                |
| Qual a forma da distribuição em cada grupo? | numérica × categórica   | violino       | quartis ( inner="quart" ), mediana               |
| Duas numéricas se relacionam?               | numérica × numérica     | dispersão     | r de Pearson e/ou Spearman, reta de regressão    |
| Qual a média ou a contagem por categoria?   | categórica (× numérica) | barras        | média ± IC 95% (ou desvio-padrão - diga qual), n |
| Como várias numéricas se relacionam?        | várias numéricas        | mapa de calor | matriz de r, escala de -1 a 1                    |

## 1.5 Histograma

Divide a variável em classes ( bins )   e   mostra quantas observações caem em cada uma. Revela o centro , a dispersão , a assimetria e se há mais de um pico. Marque média e mediana com linhas verticais: se a média fica à direita da mediana, há cauda à direita (assimetria positiva). O número de classes muda a leitura - comece com bins="auto" e ajuste.

Figura 1 - Tempo de entrega: média 37,4 min, mediana 36 min, skew = 1,18. A faixa sombreada é média ± 1 desvio-padrão.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000000_a2c21497abda9ae850398bc98bcaca68c4dfead79bb9208b9ff9653eb81af753.png)

```
sns.histplot(t, bins=range(15, 92, 3), ax=ax) ax.axvline(t.mean(), color="C3", label=f"média = {t.mean():.1f} min") ax.axvline(t.median(), color="C2", ls="--", label=f"mediana = {t.median():.0f} min") ax.axvspan(t.mean() - t.std(), t.mean() + t.std(), alpha=0.07)
```

## 1.6 Boxplot

Resume a distribuição em cinco números: a caixa vai do Q1 (25%) ao Q3 (75%) - sua altura é o IQR ; a linha interna é a mediana ; os bigodes vão até o último valor dentro de Q1 - 1,5·IQR e Q3 + 1,5·IQR; os pontos além disso são outliers (critério de Tukey). É o melhor gráfico para comparar grupos .   Limitação: esconde o tamanho da amostra e a forma (dois picos, por exemplo) - escreva o n no rótulo e, se necessário, sobreponha os pontos com stripplot .

Figura 2 - Tempo por bairro. Para todos os pedidos: Q1 = 30, mediana = 36, Q3 = 43, IQR = 13 min; outliers acima de 62,5 min.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000001_a62500954f5e206037e302b029b73fe2c7f4afdc226c6de9a2221a7aa76fdf88.png)

## 1.7 Violino

Combina o boxplot com uma estimativa de densidade (KDE) : a largura do violino indica onde os valores se concentram. inner="quart" desenha Q1, mediana e Q3; split=True põe dois grupos (ex.: com e sem chuva) em metades do mesmo violino; cut=0 impede que a curva ultrapasse os valores observados.

Figura 3 - Com chuva, a distribuição inteira sobe: no almoço a mediana passa de 31 para 39 min; no jantar, de 36 para 40 min.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000002_2991615699634d74790c264c9498c3c8597d3e14f2e75dd02e05ca3cbd634d3f.png)

## 1.8 Dispersão (scatter)

Cada ponto é uma observação com duas medidas numéricas. Acompanhe o gráfico de: r de Pearson (força da relação linear ), ρ de Spearman (relação monotônica, robusta a outliers) e a reta de regressão ( sns.regplot ; a faixa sombreada é o IC 95% da reta). Cor ( hue ) e forma ( style ) acrescentam uma terceira e uma quarta variável.

Figura 4 - Distância × tempo: r = 0,71, ρ = 0,72, tempo ≈ 25,8 + 2,80 × km (R² = 0,51).

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000003_4488d2c8aea0402d9530372a11d1b71640ddcdde2fc5426d3275b90e39c48a84.png)

## VARIÁVEL DE CONFUSÃO NO GRÁFICO

No boxplot, a bicicleta parece mais rápida (mediana 33 × 36 min da moto). Mas a bicicleta só faz entregas de até 3 km. Comparando apenas entregas de até 3 km, a bicicleta é mais lenta (mediana 33 × 29 min). A distância confunde a comparação - e a dispersão colorida por veículo, restrita às entregas curtas, mostra isso.

## 1.9 Gráfico de barras

No Seaborn, barplot calcula uma estatística por categoria (média, por padrão) e desenha uma barra de erro; countplot apenas conta linhas. Sempre informe qual barra de erro foi usada e, ao comparar grupos, o n de cada um. Barras devem começar no zero.

| Parâmetro                    | O que a barra de erro mostra                                                 |
|------------------------------|------------------------------------------------------------------------------|
| errorbar=("ci", 95) (padrão) | intervalo de confiança de 95% da média (bootstrap) - incerteza sobre a média |
| errorbar="sd"                | média ± 1 desvio-padrão - dispersão dos dados                                |
| errorbar="se"                | média ± 1 erro-padrão                                                        |
| estimator="median"           | troca a média pela mediana                                                   |

Figura 5 - (a) Ticket médio por dia com IC 95% e n; sexta a domingo em destaque. (b) Contagem de pedidos por bairro, ordenada, com rótulos diretos.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000004_3999800328e6dbd7205d154cb79e25414ff2504d838b539ee5bd84f124ad143c.png)

## 1.10 Mapa de calor da correlação

Mostra, de uma vez, a matriz de r entre todas as variáveis numéricas. Boas práticas: paleta divergente centrada no zero ( cmap="vlag", center=0, vmin=-1, vmax=1 ), valores escritos em cada célula   ( annot=True,   fmt=".2f" )   e   máscara   do   triângulo   superior,   pois   a   matriz   é simétrica. Mapas de calor também servem para tabelas dinâmicas (ex.: mediana do tempo por bairro × turno) - nesse caso, com paleta sequencial.

Figura 6 - Distância × taxa = 0,99 (redundantes); distância × tempo = 0,71; tempo × avaliação = -0,59; itens × valor = 0,92.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000005_dd934b9b5e21cfbc6900aa6fb714b7a5c73928c4adfbe18b4949bfb623aa1bac.png)

```
corr = df[colunas_numericas].corr() mask = np.triu(np.ones_like(corr, dtype=bool), k=1) sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, center=0, square=True, linewidths=1, ax=ax)
```

## 1.11 Paletas de cores

A paleta deve seguir o tipo de dado , e a cor deve ter significado (identificar um grupo, codificar uma intensidade ou destacar a mensagem) - nunca ser só decoração.

| Tipo        | Quando usar                                | Exemplos                                                       |
|-------------|--------------------------------------------|----------------------------------------------------------------|
| Qualitativa | "colorblind" ,                             | categorias sem ordem (bairro, plano, veículo) "Set2" , "tab10" |
|             | densidade) "viridis" , "Greens" , "rocket" | Sequencial valores que só crescem (contagem, tempo,            |
| Divergente  | "vlag" , "RdBu" , "coolwarm"               | valores com ponto central significativo (correlação,           |

Figura 7 - Paletas por tipo de dado. O arco-íris (jet) cria fronteiras falsas e falha para daltônicos e em impressão em tons de cinza.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000006_ba7a117df47b82eb3ca7dc5f838a3b07a53bf98059d052277fbf16be03fdf579.png)

## ACESSIBILIDADE

Cerca de 8% dos homens têm alguma deficiência na percepção de cores. Prefira sns.set\_theme(palette="colorblind") ou viridis ,   e   nunca   dependa   só   da   cor:   use também forma do marcador ( style= ), rótulos diretos e legendas.

## 1.12 Customização: do gráfico padrão ao gráfico que comunica

Customizar é tirar o que não ajuda e destacar o que importa : ordenar as categorias pelo valor, rotular as barras diretamente ( ax.bar\_label ), usar cinza para o contexto e uma única cor para o destaque, escrever no título a conclusão e indicar a fonte.

Figura 8 - Antes: ordem alfabética, cores sem significado, título = nome da coluna. Depois: ordenado, destaque, rótulos diretos e título com a mensagem.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000007_0d322483f5450dc3f2fe0e35f06edf057579222ee074bddf9eb82cea7caa59cd.png)

| Elemento                 | Comando                                                                                         |
|--------------------------|-------------------------------------------------------------------------------------------------|
| Tema e paleta globais    | sns.set_theme(style="whitegrid", palette="colorblind")                                          |
| Título, rótulos, limites | ax.set(title=..., xlabel=..., ylabel=..., ylim=(0, 140))                                        |
| Linha de referência      | ax.axvline(x) , ax.axhline(y) , faixa: ax.axvspan(a, b)                                         |
| Texto e seta             | ax.text(x, y, "...") , ax.annotate("...", xy=..., xytext=..., arrowprops=dict(arrowstyle="->")) |
| Rótulos nas barras       | ax.bar_label(ax.containers[0], padding=3)                                                       |
| Remover bordas           | sns.despine(ax=ax, left=True)                                                                   |
| Painel e título geral    | fig, axes = plt.subplots(2, 2) , fig.suptitle(...) , fig.tight_layout()                         |
| Exportar                 | fig.savefig("fig.png", dpi=200, bbox_inches="tight")                                            |

## 1.13 Plotly: gráficos interativos

O Plotly Express gera em uma linha os mesmos gráficos, agora interativos : passar o mouse mostra os valores ( hover ), é possível dar zoom, esconder grupos clicando na legenda e exportar para um arquivo HTML que abre em qualquer navegador. No boxplot do Plotly, o hover já mostra mínimo, Q1, mediana, Q3, máximo e as cercas.

| Gráfico           | Plotly Express     | Parâmetros úteis                                                   |
|-------------------|--------------------|--------------------------------------------------------------------|
| Histograma        | px.histogram       | nbins , marginal="box" ou "violin"                                 |
| Boxplot / violino | px.box / px.violin | points="all" ou "outliers" ; box=True no violino                   |
| Dispersão         | px.scatter         | color , symbol , hover_data=[...]                                  |
| Barras            | px.bar             | text_auto=True , error_y                                           |
| Mapa de calor     | px.imshow          | text_auto=True , zmin=-1, zmax=1 , color_continuous_scale="RdBu_r" |

```
fig = px.scatter(df, x="distancia_km", y="tempo_entrega_min", color="chuva", hover_data=["bairro", "valor_pedido", "avaliacao"], title="Distância × tempo (r = 0,71)") fig.add_vline(x=4.1, line_dash="dash")                     # linhas de referência fig.write_html("graficos/dispersao.html", include_plotlyjs="cdn") fig.show()
```

## Parte II - Laboratório guiado: delivery da hamburgueria

Notebook Aula12\_Visualizacao\_Laboratorio.ipynb · 1h30

O notebook guiado segue o roteiro abaixo. Execute célula por célula, leia o resultado e responda à pergunta de cada parte antes de seguir. As figuras desta apostila foram geradas por ele (pasta figuras/ ), e os gráficos interativos ficam em graficos/ .

| Tempo     | Parte do notebook        | O que fazer                                                                                      | Resultado de referência                                       |
|-----------|--------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| 0-10 min  | 0. Preparação e anatomia | importar bibliotecas, definir tema e paleta, carregar o CSV; gráfico de linha de pedidos por dia | 600 × 13; média de 10,7 pedidos/dia, picos de sexta a domingo |
| 10-20 min | 1.1 Histograma           | calcular resumo; marcar média, mediana e média ± dp; comparar bins                               | média 37,4; mediana 36; dp 10,4; skew 1,18                    |
| 20-28 min | 1.2 Boxplot              | calcular Q1, Q3, IQR e limites de Tukey; boxplot por bairro com n e medianas                     | IQR 13 min; 15 outliers (> 62,5 min); medianas 29 → 46 min    |
| 28-35 min | 1.3 Violino              | violino dividido por chuva; comparar box × violino × pontos                                      | chuva: +8 min no almoço, +4 no jantar (medianas)              |
| 35-47 min | 2.1 Dispersão            | r, ρ e reta; investigar bicicleta × moto                                                         | r = 0,71; 2,8 min/km; bicicleta mais lenta até 3 km           |
| 47-53 min | 2.2 Barras               | ticket médio por dia com IC 95% e n ; contagem por bairro                                        | R$ 89 (seg) a R$ 118 (sáb)                                    |
| 53-60 min | 2.3 Mapa de calor        | matriz de correlação com máscara; tabela dinâmica bairro × turno                                 | maiores &#124;r&#124;: 0,99; 0,92; 0,71; -0,59                |
| 60-75 min | 3. Customização          | paletas; antes × depois; painel 2×2 exportado                                                    | 09_painel_gerencia.png                                        |
| 75-85 min | 4. Plotly                | histograma com box marginal, dispersão com hover , box/violino, mapa de calor; exportar HTML     | 3 arquivos em graficos/                                       |
| 85-90 min | Fechamento               | revisar o quadro "qual gráfico usar" e o checklist; apresentar o exercício                       | -                                                             |

Figura 9 - Painel 2×2 para a gerência, produto final da Parte 3 do laboratório.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula12_Laboratorio_Visualizacao_artifacts/image_000008_f19f81eb2306a6a41e808382ebb0f4e0d3ba885e76205ceec67581edd63c2d03.png)

## Parte   III   -   Exercício   prático:   app   de   música   (sem entrega)

Notebook Aula12\_Exercicio\_Pratico.ipynb · gabarito em Aula12\_Exercicio\_Gabarito.ipynb

Aplique o mesmo roteiro aos 240 usuários de um aplicativo de música fictício. Cada passo traz o resultado esperado para conferência. O exercício é para treino e não precisa ser entregue .

|   Passo | Tarefa                                               | Resultado esperado                                                 |
|---------|------------------------------------------------------|--------------------------------------------------------------------|
|       1 | Carregar e conhecer os dados                         | 240 × 9; 151 Gratuito e 89 Premium                                 |
|       2 | Histograma de horas_semana com média e mediana       | média 16,5 h; mediana 16,2 h; skew 0,29 (quase simétrica)          |
|       3 | Boxplot de horas por plano, com n e medianas         | Gratuito 15,3 h; Premium 18,5 h; 1 outlier no conjunto             |
|       4 | Violino da satisfação por plano                      | medianas 3,6 (Gratuito) e 7,3 (Premium)                            |
|       5 | Dispersão idade × horas com r e reta                 | r = -0,65; horas ≈ 25,0 - 0,21 × idade                             |
|       6 | Barras de horas médias por gênero (IC 95%, n )       | Eletrônica 19,6 h (maior); Rock 15,0 h (menor)                     |
|       7 | Mapa de calor da correlação + desafio                | anúncios × satisfação = -0,82; só Gratuito: -0,42 (plano confunde) |
|       8 | Painel 2×2 customizado e exportado                   | figuras/exercicio_painel.png                                       |
|       9 | Plotly: dispersão com hover e boxplot; exportar HTML | graficos/exercicio_dispersao.html                                  |

## Parte IV - Formulário avaliativo

Moodle · 10 questões objetivas · prazo 16/11/2026, 23:59

O formulário avaliativo da Aula 12 tem 10 questões objetivas sobre a escolha e a leitura dos   gráficos   (histograma,   boxplot,   violino,   dispersão,   barras   e   mapa   de   calor),   as estatísticas que os acompanham (média × mediana, IQR e outliers, r e reta de regressão, IC 95%), paletas de cores, a interface orientada a objetos do Matplotlib e o Plotly. Várias questões usam as situações do laboratório guiado. Você pode consultar este material e os notebooks. Prazo de envio: até 16/11/2026, às 23:59 .

## Apêndice A - Colinha de visualização

```
import matplotlib.pyplot as plt, seaborn as sns, plotly.express as px sns.set_theme(style="whitegrid", palette="colorblind") # ---------- UNIVARIADOS ---------- sns.histplot(df, x="var", bins="auto", kde=False, ax=ax)          # histograma ax.axvline(df["var"].mean()); ax.axvline(df["var"].median(), ls="--") sns.boxplot(df, x="grupo", y="var", showmeans=True, ax=ax)          # boxplot sns.violinplot(df, x="grupo", y="var", hue="h", split=True, inner="quart", cut=0, ax=ax)                        # violino sns.stripplot(df, x="grupo", y="var", alpha=.4, jitter=.25, ax=ax)  # pontos # ---------- BIVARIADOS ---------- sns.scatterplot(df, x="x", y="y", hue="cat", style="cat2", ax=ax)   # dispersão sns.regplot(df, x="x", y="y", scatter=False, ax=ax)                # reta + IC 95% r = stats.pearsonr(df.x, df.y)[0]; rho = stats.spearmanr(df.x, df.y)[0] sns.barplot(df, x="cat", y="var", errorbar=("ci", 95), capsize=.2, ax=ax) sns.countplot(df, y="cat", order=df["cat"].value_counts().index, ax=ax) sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="vlag", center=0, vmin=-1, vmax=1, ax=ax)          # correlação # ---------- CUSTOMIZAÇÃO ---------- ax.set(title="Conclusão em uma frase", xlabel="x (unidade)", ylabel="y (unidade)") ax.bar_label(ax.containers[0], fmt="%.0f"); sns.despine(ax=ax) ax.annotate("texto", xy=(x0, y0), xytext=(x1, y1), arrowprops=dict(arrowstyle="->")) fig.suptitle("Título do painel"); fig.tight_layout() fig.savefig("figura.png", dpi=200, bbox_inches="tight") # ---------- PLOTLY ---------- px.histogram(df, x="var", marginal="box"); px.box(df, x="g", y="var", points="all") px.scatter(df, x="x", y="y", color="cat", hover_data=["col1", "col2"]) px.imshow(corr, text_auto=".2f", zmin=-1, zmax=1, color_continuous_scale="RdBu_r") fig.write_html("grafico.html", include_plotlyjs="cdn")
```

## Checklist de um bom gráfico

- O título diz a conclusão , não só o nome da variável. 1.
- Eixos com nome e unidade (min, km, R$, h). 2.
- A estatística mostrada está identificada : média? mediana? IC 95%? desvio-padrão? 3.
- Ao comparar grupos, o n de cada grupo aparece. 4.
- Paleta adequada ao tipo de dado, segura para daltônicos, e cor com significado. 5.
- Barras começam no zero; evite 3D, pizza com muitas fatias e dois eixos y. 6.
- Fonte dos dados no rodapé. 7.

## Apêndice B - Referências

- HUNTER, J. D. Matplotlib: a 2D graphics environment. Computing in Science &amp; Engineering , v. 9, n. 3, p. 90-95, 2007. Documentação: matplotlib.org. ·
- WASKOM, M. L. seaborn: statistical   data   visualization. Journal   of   Open   Source Software , v. 6, n. 60, 3021, 2021. Documentação: seaborn.pydata.org. ·
- PLOTLY   TECHNOLOGIES. Plotly   Python   Open   Source   Graphing   Library . Documentação: plotly.com/python. ·

- VANDERPLAS, J. Python Data Science Handbook . 2. ed. O'Reilly, 2023 - capítulos de visualização com Matplotlib. ·
- WILKE, C. O. Fundamentals of Data Visualization .   O'Reilly,   2019   (disponível   em clauswilke.com/dataviz). ·
- KNAFLIC, C. N. Storytelling com Dados . Alta Books, 2019. ·
- ANSCOMBE, F. J. Graphs in statistical analysis. The American Statistician , v. 27, n. 1, p. 17-21, 1973. ·
- TUKEY, J. W. Exploratory Data Analysis . Addison-Wesley, 1977. ·