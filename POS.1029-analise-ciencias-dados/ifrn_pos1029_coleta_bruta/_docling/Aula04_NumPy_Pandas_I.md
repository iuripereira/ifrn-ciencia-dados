INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO RIO GRANDE DO NORTE ESPECIALIZAÇÃO EM CIÊNCIA DE DADOS  ·  DISCIPLINA: ANÁLISE E CIÊNCIA DE DADOS

## Aula 04 - Laboratório NumPy e Pandas I

Criação e manipulação de DataFrames, seleção e filtragem, leitura de CSV/Excel e inspeção básica

Unidade

Natureza Unidade 1 - Introdução à Ciência de Dados e Python (Aulas 01-05)

Aula prática (laboratório)

Carga horária

4 h/a - 1 h de exposição guiada + 3 h de laboratório

Pré-

requisitos

Recursos Aula  03  -  ambiente  Python  instalado,  Jupyter  funcionando,  noções  de  listas, dicionários, funções e arrays NumPy Jupyter Notebook/Lab, pandas , numpy , openpyxl , conjuntos de dados de exemplo

Avaliação Exercício prático entregue no Moodle + formulário avaliativo (10 questões)

Professor Plácido Antônio de Souza Neto

## Objetivos de aprendizagem

Ao final desta aula, espera-se que o estudante seja capaz de:

1. Explicar a relação entre o ndarray do NumPy e as estruturas Series e DataFrame do Pandas, identificando o que cada camada acrescenta.
2. Criar DataFrames a partir de dicionários, listas de dicionários, listas de tuplas e arrays NumPy, escolhendo a forma adequada a cada situação.
3. Ler arquivos  CSV  e  Excel  do  mundo  real,  ajustando  separador,  separador  decimal, codificação, tipos de coluna e marcadores de valor ausente.
4. Inspecionar um conjunto de dados desconhecido com shape , head , info , describe , isna e value\_counts , e relatar o que foi encontrado.
5. Selecionar linhas e colunas com loc e iloc , distinguindo com segurança seleção por rótulo e por posição.
6. Filtrar dados  com  máscaras  booleanas  compostas, isin , between , str.contains e query .
7. Atribuir valores de forma segura, reconhecendo e evitando o SettingWithCopyWarning .
8. Interpretar o resultado de uma análise inicial e apontar suas limitações.

## Sumário

## Parte I - Fundamentos teóricos

- 1.1 Por que Pandas existe: da lista ao DataFrame
- 1.2 NumPy: o alicerce numérico
- 1.3 Anatomia da Series e do DataFrame

- 1.4 Criando DataFrames: cinco caminhos
- 1.5 Lendo arquivos: CSV, Excel e outros formatos
- 1.6 Inspeção básica: as primeiras sete perguntas
- 1.7 Seleção: [] , loc , iloc , at , iat
- 1.8 Filtragem com máscaras booleanas
- 1.9 Atribuição segura e o SettingWithCopyWarning
- 1.10 Valores ausentes: NaN não é zero
- 1.11 Erros mais comuns e como corrigi-los
- 1.12 Boas práticas de laboratório

Parte II - Tópicos de estudo dirigido (roteiro de leitura)

Parte III - Laboratório guiado: matrículas do IFRN

Parte IV - Exercício prático avaliativo (entrega no Moodle)

Parte V - Formulário avaliativo (10 questões)

Apêndice A - Colinha de comandos

Apêndice B - Referências e leituras recomendadas

## SOBRE OS DADOS USADOS NESTA AULA

Todos os exemplos usam um conjunto de dados sintético ( matriculas\_ifrn\_2026.csv e campi\_ifrn.xlsx ). Os nomes de campi e cursos são reais; matrículas, nomes de estudantes, notas, frequências  e  situações  foram  gerados  aleatoriamente  com  semente  fixa. Nenhuma conclusão sobre o IFRN pode ser extraída desses números. A escolha por dados sintéticos é deliberada: ela  permite inserir,  de  propósito,  os  defeitos  que  aparecem em dados reais - valores ausentes, espaços sobrando, linhas duplicadas e tipos mal inferidos - sem expor informação de nenhuma pessoa.

## Parte I - Fundamentos teóricos

Conceitos necessários para entender o que o código faz, e não apenas repeti-lo

## 1.1 Por que Pandas existe: da lista ao DataFrame

Na Aula 03 representamos uma pequena tabela como uma lista de dicionários . Funciona, e  é  instrutivo  -  mas  experimente  responder,  com  Python  puro,  a  pergunta "qual  a  nota média dos estudantes do turno noturno, por campus, ignorando quem está sem nota?" .  O código resultante tem três laços aninhados, um dicionário acumulador e várias verificações de None . Em Pandas, a mesma pergunta cabe em uma linha.

A  diferença  não  é  apenas  de  digitação.  É  de nível  de  abstração .  Existem  três  camadas empilhadas, e é importante saber em qual delas se está trabalhando:

| Camada                    | O que oferece                                                                                                                             | Limitação                                                                                   |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Python puro list , dict   | Flexibilidade total; qualquer tipo em qualquer posição.                                                                                   | Lento: cada elemento é um objeto separado na memória. Toda operação exige laço explícito.   |
| NumPy ndarray             | Bloco contíguo de memória, tipo único, operações vetorizadas em C.                                                                        | Um só tipo por array; sem nomes de coluna; sem suporte nativo a dados ausentes em inteiros. |
| Pandas Series , DataFrame | Colunas nomeadas e de tipos diferentes , índice rotulado, alinhamento automático, tratamento de ausentes, leitura de dezenas de formatos. | Mais memória e alguma sobrecarga; ainda é preciso entender a camada NumPy por baixo.        |

A  frase  que  vale  a  pena  guardar: Pandas  é  NumPy  com  rótulos,  tipos  mistos  e tratamento de dados faltantes. Quase tudo o que causa confusão em Pandas - o índice, o NaN , o dtype object , o SettingWithCopyWarning - aparece exatamente nos pontos em que essas três adições encostam no NumPy de baixo.

## O ciclo de trabalho desta aula

Toda análise de dados começa com os mesmos cinco movimentos, na mesma ordem. Esta aula cobre os quatro primeiros; a Aula 05 avança sobre o quinto.

|   # | Movimento   | Pergunta que responde                          | Ferramentas                           |
|-----|-------------|------------------------------------------------|---------------------------------------|
|   1 | Ler         | Consigo carregar o arquivo corretamente ?      | read_csv , read_excel                 |
|   2 | Inspecionar | O que existe aqui dentro? O que está quebrado? | shape , head , info , describe , isna |
|   3 | Selecionar  | Quais linhas e colunas me interessam?          | [] , loc , iloc                       |
|   4 | Filtrar     | Qual subconjunto responde à minha pergunta?    | máscaras booleanas, isin , query      |
|   5 | Resumir     | O que os dados dizem?                          | groupby , agg , pivot_table (Aula 05) |

## 1.2 NumPy: o alicerce numérico

Pandas  guarda  os  dados  de  cada  coluna  em  arrays  NumPy.  Entender  o  array  explica  o comportamento do DataFrame.

## O ndarray e o dtype

Um array  NumPy é  um  bloco  contíguo  de  memória  com um único tipo ( dtype )  e  uma forma ( shape ). É essa uniformidade que permite ao NumPy delegar o cálculo para código compilado em C.

```
import numpy as np notas = np.array([72.5, 68.0, 91.3, 55.4, 80.1]) notas.dtype # dtype('float64')  -> todos os elementos são float de 64 bits notas.shape # (5,)              -> vetor de 5 posições, 1 dimensão notas.ndim # 1 notas.size # 5 notas.nbytes # 40  -> 5 elementos x 8 bytes
```

## Vetorização

Vetorizar é aplicar uma operação a todos os elementos de uma vez, sem escrever o laço em Python. O laço continua existindo - apenas passou a rodar em C.

```
# Python puro: o laço está no seu código, interpretado bonus = [] for n in lista_notas: bonus.append(n * 1.05) # NumPy: o laço está dentro da biblioteca, compilado bonus = notas * 1.05
```

Além de mais curto, o segundo é tipicamente 10 a 100 vezes mais rápido para  arrays grandes.  A  regra  prática  em  análise  de  dados  é  direta: se  você  escreveu  um for percorrendo  linhas  de  um  DataFrame,  quase  certamente  existe  uma  forma  vetorizada melhor.

## Broadcasting

Quando os operandos têm formas diferentes, o NumPy "estica" o menor até casar com o maior, sem copiar dados. É por isso que notas * 1.05 funciona: o escalar 1.05 é difundido sobre os cinco elementos.

```
pesos  = np.array([0.4, 0.6]) # shape (2,) provas = np.array([[70., 80.], [90., 65.], [50., 75.]]) # shape (3, 2) media_ponderada = (provas * pesos).sum(axis=1) # array([76., 75., 65.])  -> o vetor de pesos foi aplicado a cada linha
```

## Indexação booleana

Este é o mecanismo que sustenta toda a filtragem em Pandas. Uma comparação sobre um array produz outro array, de dtype bool , do mesmo tamanho - a máscara . Usar a máscara como índice devolve apenas as posições True .

```
notas >= 70 # array([ True, False,  True, False,  True]) notas[notas >= 70] # array([72.5, 91.3, 80.1]) (notas >= 70).sum() # 3   -> True vale 1, False vale 0 (notas >= 70).mean() # 0.6 -> proporção de aprovados
```

## TRUQUE ÚTIL

Como True  ==  1 , mascara.sum() conta  quantos  casos  satisfazem  a  condição  e mascara.mean() devolve a proporção deles.  Você  usará  isso  o  tempo  todo  para  calcular  taxas  (de  aprovação,  de evasão, de valores ausentes).

## Funções que ignoram ausentes

O NaN ( Not a Number ) contamina qualquer cálculo comum: np.mean de um array com NaN devolve NaN . As variantes com prefixo nan ignoram esses valores.

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula04_NumPy_Pandas_I_artifacts/image_000000_8b7f0076a960a247ecf414bd04c1fcba18673cfa24ba850ed8ae661fe87a33b7.png)

Diferença importante: em NumPy, ignorar ausentes é opcional e explícito; em Pandas, é o comportamento padrão . Isso é conveniente, mas perigoso: uma média calculada sobre 441 de 482 estudantes não é a média da turma, e o Pandas não avisa.

## 1.3 Anatomia da Series e do DataFrame

## Series: um vetor com rótulos

Uma Series é  um  array  unidimensional  acompanhado  de  um índice (os  rótulos  das posições) e de um nome .

```
import pandas as pd s = pd.Series([72.5, 68.0, 91.3], index=["20261000", "20261001", "20261002"], name="nota_final") s.values # array([72.5, 68. , 91.3])  -> o ndarray NumPy por baixo s.index # Index(['20261000', '20261001', '20261002'], dtype='object') s.name # 'nota_final' s.dtype # dtype('float64')
```

O índice não é decoração. Ele governa o alinhamento automático :  quando duas Series são combinadas, o Pandas casa os rótulos, não as posições.

```
a = pd.Series([10, 20, 30], index=["x", "y", "z"]) b = pd.Series([ 1,  2,  3], index=["z", "y", "x"]) # ordem invertida! a + b # x    13    <- 10 + 3, casado pelo rótulo "x", não pela posição # y    22 # z    31
```

## CONSEQUÊNCIA PRÁTICA

Se você somar duas colunas vindas de DataFrames com índices diferentes, o resultado pode vir cheio de NaN -  não  porque os dados estejam errados, mas porque os rótulos não casaram. Ao concatenar  ou  reordenar  DataFrames,  use .reset\_index(drop=True) para  reconstruir  um  índice limpo.

## DataFrame: um dicionário ordenado de Series

Um DataFrame é  uma  tabela  bidimensional:  várias  Series  que compartilham  o  mesmo índice . A forma mais precisa de imaginá-lo é "um dicionário ordenado cujas chaves são os nomes das colunas e cujos valores são Series".

| Atributo   | O que devolve                                              |
|------------|------------------------------------------------------------|
| df.shape   | Tupla (linhas, colunas)                                    |
| df.columns | Index com os nomes das colunas                             |
| df.index   | Index com os rótulos das linhas                            |
| df.dtypes  | Series com o tipo de cada coluna                           |
| df.values  | O conteúdo como array NumPy (com tipos mistos, vira object |
| df.size    | Número total de células ( linhas × colunas )               |
| len(df)    | Número de linhas                                           |

## Os tipos ( dtypes ) que você vai encontrar

| dtype          | Guarda                             | Observação                                                                 |
|----------------|------------------------------------|----------------------------------------------------------------------------|
| int64          | Inteiros                           | Não aceita NaN ; um único ausente converte a coluna inteira para float64 . |
| float64        | Decimais                           | Tipo padrão de qualquer coluna numérica com ausentes.                      |
| object / str   | Texto e tipos mistos               | Lento e vago; frequentemente sinaliza número lido como texto.              |
| bool           | True / False                       | Resultado de toda comparação.                                              |
| datetime64[ns] | Datas e horas                      | Só aparece com parse_dates= ou pd.to_datetime() .                          |
| category       | Texto com poucos valores distintos | Economiza muita memória em colunas como turno ou campus .                  |

## O SINTOMA MAIS COMUM DE LEITURA MALFEITA

Uma coluna que deveria ser numérica aparece como object em df.dtypes . Causas quase sempre: vírgula decimal não declarada ( decimal="," ),  separador de milhar ( thousands="." ),  ou  um  texto como "N/D" no meio dos números ( na\_values=["N/D"] ).

## 1.4 Criando DataFrames: cinco caminhos

Na  prática  profissional  você  quase  sempre lê um  arquivo.  Mas  saber  construir  um DataFrame à mão é essencial para testar hipóteses, montar exemplos mínimos e escrever testes.

## (a) Dicionário de listas - o mais usado

As chaves viram colunas. Todas as listas precisam ter o mesmo comprimento.

```
df = pd.DataFrame({ "campus": ["Natal-Central", "Mossoró", "Caicó"], "alunos": [96, 52, 31], "nota":   [68.1, 71.7, 70.0], })
```

## (b) Lista de dicionários - um registro por linha

Formato natural de quem vem de JSON ou de uma API. Chaves ausentes viram NaN .

```
registros = [ {"campus": "Natal-Central", "alunos": 96, "nota": 68.1}, {"campus": "Mossoró",       "alunos": 52}, # sem "nota" -> NaN ] df = pd.DataFrame(registros)
```

## (c) Lista de tuplas + columns

```
linhas = [("Natal-Central", 96, 68.1), ("Mossoró", 52, 71.7)] df = pd.DataFrame(linhas, columns=["campus", "alunos", "nota"])
```

## (d) Array NumPy - quando tudo é numérico

```
matriz = np.random.default_rng(42).normal(70, 10, size=(5, 3)).round(1) df = pd.DataFrame(matriz, columns=["prova1", "prova2", "prova3"])
```

## (e) Com índice significativo

Sempre  que  houver  um  identificador  natural  (matrícula,  CPF,  código  do  campus),  vale promovê-lo a índice - a seleção com loc fica muito mais legível.

```
df = pd.DataFrame( {"nota": [68.1, 71.7]}, index=pd.Index(["20261000", "20261001"], name="matricula"), ) # ou, a partir de uma coluna existente: df = df.set_index("matricula") df = df.reset_index() # desfaz, devolvendo a coluna
```

## 1.5 Lendo arquivos: CSV, Excel e outros formatos

## read\_csv - os parâmetros que realmente importam

O CSV é o formato mais comum e o mais traiçoeiro: é apenas texto, sem esquema, e cada sistema o gera à sua maneira. Ler um CSV brasileiro com os parâmetros padrão quase sempre  dá  errado ,  porque  o  padrão  do  Pandas  é  o  formato  norte-americano  (vírgula separando campos, ponto decimal).

| Parâmetro   | Para que serve                      | Exemplo                                    |
|-------------|-------------------------------------|--------------------------------------------|
| sep         | Separador de campos                 | sep=";" (padrão brasileiro)                |
| decimal     | Separador decimal                   | decimal=","                                |
| thousands   | Separador de milhar                 | thousands="."                              |
| encoding    | Codificação do texto                | "utf-8" , "latin-1" , "cp1252"             |
| dtype       | Força o tipo de colunas específicas | dtype={"matricula": "string"}              |
| usecols     | Lê só as colunas necessárias        | usecols=["nome","nota_final"]              |
| nrows       | Lê só as N primeiras linhas         | nrows=1000 (para espiar um arquivo enorme) |
| na_values   | Textos a tratar como ausente        | na_values=["N/D", "-", "sem informação"]   |
| parse_dates | Converte colunas para data          | parse_dates=["data_matricula"]             |
| index_col   | Usa uma coluna como índice          | index_col="matricula"                      |
| skiprows    | Pula linhas de cabeçalho sujo       | skiprows=3                                 |

```
df = pd.read_csv( "dados/matriculas_ifrn_2026.csv", sep=";", # campos separados por ponto e vírgula decimal=",", # 72,5 é um número, não texto encoding="utf-8", dtype={"matricula": "string"}, # identificador NÃO é número )
```

## POR QUE A MATRÍCULA NÃO PODE SER INTEIRO

Identificadores  lidos  como int64 perdem  zeros  à  esquerda  ( "00123" vira 123 ),  estouram  a precisão em códigos muito longos e passam a aceitar operações sem sentido, como somar duas matrículas. Regra: se não faz sentido calcular a média, não é número - é texto. Vale para CPF, CEP , código de escola, número de processo e SIAPE.

## Descobrindo a codificação e o separador

Antes de insistir em parâmetros, olhe o arquivo cru. As três primeiras linhas revelam quase tudo:

```
# No terminal head -3 dados/matriculas_ifrn_2026.csv # Ou em Python, sem carregar o arquivo inteiro with open("dados/matriculas_ifrn_2026.csv", encoding="utf-8") as f: for _ in range(3): print(f.readline().rstrip())
```

Se  aparecerem  caracteres  estranhos  no  lugar  dos  acentos  ( MossorÃ³ ),  a  codificação declarada está errada - tente latin-1 ou cp1252 . Se o Pandas devolver uma única coluna gigante, o sep está errado.

## read\_excel

Requer o pacote openpyxl para arquivos .xlsx ( pip install openpyxl ). A grande diferença em relação ao CSV é a existência de planilhas (abas) .

```
campi  = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi") cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos") # sheet_name=None devolve um DICIONÁRIO {nome_da_aba: DataFrame} todas = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name=None) todas.keys() # dict_keys(['campi', 'cursos']) # Planilha com título nas primeiras linhas: df = pd.read_excel("relatorio.xlsx", sheet_name=0, skiprows=4, header=0)
```

## EXCEL NÃO É UM FORMATO DE DADOS

Planilhas  costumam  trazer  células  mescladas,  títulos  decorativos,  totais  no  meio  da  tabela  e colunas com formatação que engana o Pandas. Sempre confira df.head() e df.dtypes logo após ler um .xlsx .

## Outros formatos e a escrita

| Formato   | Leitura           | Escrita                            |
|-----------|-------------------|------------------------------------|
| CSV       | pd.read_csv()     | df.to_csv("x.csv", index=False)    |
| Excel     | pd.read_excel()   | df.to_excel("x.xlsx", index=False) |
| JSON      | pd.read_json()    | df.to_json()                       |
| Parquet   | pd.read_parquet() | df.to_parquet()                    |
| Banco SQL | pd.read_sql()     | df.to_sql()                        |
| HTML      | pd.read_html(url) | df.to_html()                       |

Ao  gravar  CSV,  lembre-se  de index=False -  caso  contrário  o  índice  vira  uma  coluna anônima extra, que reaparece como Unnamed: 0 na próxima leitura.

## 1.6 Inspeção básica: as primeiras sete perguntas

Diante  de  um  arquivo  desconhecido,  a  sequência  abaixo  deve  ser automática .  Ela  leva menos de um minuto e evita horas de análise sobre dados quebrados.

|   # | Comando                            | Pergunta que responde                                           |
|-----|------------------------------------|-----------------------------------------------------------------|
|   1 | df.shape                           | Quantas linhas e colunas? O número bate com o esperado?         |
|   2 | df.head() / df.tail() df.sample(5) | / Com o que esses dados se parecem? O cabeçalho foi lido certo? |
|   3 | df.info()                          | Que tipo tem cada coluna? Quantos não nulos? Quanta memória?    |
|   4 | df.describe()                      | As estatísticas fazem sentido? Há mínimos ou máximos absurdos?  |
|   5 | df.isna().sum()                    | Onde estão os buracos e qual o tamanho deles?                   |
|   6 | df["col"].value_counts()           | Que categorias existem? Há grafias divergentes?                 |
|   7 | df.duplicated().sum()              | Há linhas repetidas?                                            |

## O que ler em cada saída

## head()

Mostra as 5 primeiras linhas ( head(10) para dez). Procure por: cabeçalho virado linha de dados, colunas deslocadas, números aparecendo com aspas, acentos corrompidos. sample(5) é  frequentemente  mais  honesto:  arquivos  costumam  ser  ordenados,  e  as primeiras linhas podem não representar o conjunto.

## info()

A saída mais informativa do Pandas. Três colunas importam:

- Non-Null  Count -  comparando  com  o  total  de  linhas,  revela  imediatamente  quais colunas têm ausentes e quantos.
- Dtype - se uma coluna que deveria ser numérica está como object ,  a  leitura precisa ser corrigida antes de qualquer análise.
- memory usage - use df.info(memory\_usage="deep") para o tamanho real das colunas de texto.

## describe()

Por padrão resume apenas as colunas numéricas, com oito estatísticas: count , mean , std , min , 25% , 50% (mediana), 75% e max .

- count menor que len(df) denuncia valores ausentes naquela coluna.
- Média muito distante da mediana sugere assimetria ou outliers .
- min ou max impossíveis (idade  0,  nota  999,  frequência  negativa)  indicam  erro  de coleta ou código de ausência disfarçado de número.
- df.describe(include="object") resume  as  colunas  de  texto  com count , unique , top e freq . include="all" combina os dois.

## ATENÇÃO À VERSÃO

A partir do Pandas 3.0, colunas de texto passaram a ter o dtype dedicado str , e describe(include="object") emite  um  aviso  de  compatibilidade.  Se  você  estiver  no  Pandas  3.x, prefira df.describe(include="all") . Verifique sua versão com pd.\_\_version\_\_ .

## value\_counts()

Conta as ocorrências de cada valor distinto de uma coluna. É a ferramenta número um para detectar  sujeira  em  categorias: "Natal-Central" , "natal-central" e "  Natal-Central  " aparecem como três categorias diferentes.

```
df["turno"].value_counts() # contagem absoluta df["turno"].value_counts(normalize=True) # proporção (0 a 1) df["turno"].value_counts(dropna=False) # inclui os NaN na contagem df["campus"].nunique() # quantos valores distintos df["campus"].unique() # quais são
```

## 1.7 Seleção: [] , loc , iloc , at , iat

Este é o ponto em que a maioria dos iniciantes escorrega. A confusão desaparece com uma única distinção:

## A REGRA QUE RESOLVE TUDO

loc trabalha com RÓTULOS (o que está escrito no índice e nos nomes das colunas). iloc trabalha com POSIÇÕES (números inteiros de 0 a n-1, como em listas Python).

## Colchetes simples []

```
df["nota_final"] # uma COLUNA -> Series df[["nome", "nota_final"]] # várias colunas -> DataFrame df[0:5] # fatia de LINHAS por posição (confuso!) df[df["nota_final"] > 90] # filtragem booleana de LINHAS
```

Note a ambiguidade: com um texto, [] seleciona coluna; com uma fatia ou uma máscara, seleciona linhas. Por isso, para qualquer seleção que não seja "uma ou mais colunas inteiras", prefira loc ou iloc .

## loc - por rótulo

```
df.loc[0] # linha de RÓTULO 0 -> Series df.loc[0, "nome"] # uma célula df.loc[0:2] # rótulos 0, 1 E 2 -> fim INCLUÍDO df.loc[0:2, ["nome", "campus"]] # linhas x colunas escolhidas df.loc[:, "nome":"curso"] # todas as linhas, faixa de colunas df.loc[df["turno"] == "Noturno", "nota_final"] # filtro + coluna
```

## iloc - por posição

```
df.iloc[0] # PRIMEIRA linha, seja qual for o rótulo df.iloc[0, 1] # 1ª linha, 2ª coluna df.iloc[0:3] # posições 0, 1, 2 -> fim EXCLUÍDO df.iloc[0:3, 0:4] # 3 primeiras linhas, 4 primeiras colunas df.iloc[-1] # última linha df.iloc[[0, 5, 10], [1, 9]] # listas de posições
```

## A tabela que vale memorizar

| Aspecto                     | loc                               | iloc                               |
|-----------------------------|-----------------------------------|------------------------------------|
| Indexa por                  | Rótulo do índice / nome da coluna | Posição inteira (0-based)          |
| Fatia a:b                   | Inclui b                          | Exclui b (como em listas)          |
| Aceita máscara booleana     | Sim                               | Só array NumPy de bool, não Series |
| Aceita nome de coluna       | Sim ( "nota_final" )              | Não (só 9 )                        |
| Serve para atribuir         | Sim - é a forma recomendada       | Sim                                |
| Índice numérico embaralhado | Segue o rótulo                    | Segue a posição física             |

## A PEGADINHA CLÁSSICA

Com o índice padrão (0, 1, 2, …), df.loc[0:2] devolve três linhas e df.iloc[0:2] devolve duas . Não é bug: loc fatia rótulos (intervalo fechado), iloc fatia posições (intervalo semiaberto, como toda fatia Python).

## Quando o índice não é 0, 1, 2…

Depois de filtrar, o índice deixa de ser contínuo - e a diferença entre rótulo e posição deixa de ser acadêmica:

```
noturno = df[df["turno"] == "Noturno"] noturno.index[:5] # Index([0, 1, 5, 8, 10], ...)  -> com buracos noturno.loc[5] # a linha cujo RÓTULO é 5  (a 3ª deste subconjunto) noturno.iloc[5] # a 6ª linha deste subconjunto (rótulo qualquer) noturno = noturno.reset_index(drop=True) # renumera 0..n-1
```

![Image](/tmp/claude-1000/-home-iuri-code-20-areas-27-estudo-26-ifrn/f473d664-f29c-4af2-8014-9c6c66cfc5fe/scratchpad/docling/Aula04_NumPy_Pandas_I_artifacts/image_000001_54a6f01f660224f30fcdf658442de510943f52084c9e3c4e0c5ccb547977a3e1.png)

Versões  otimizadas  de loc / iloc para  acessar um  único  valor  escalar .  Mais  rápidas, porém mais restritas.

```
df.at[0, "nome"] # por rótulo  - equivale a df.loc[0, "nome"] df.iat[0, 1] # por posição - equivale a df.iloc[0, 1]
```

## 1.8 Filtragem com máscaras booleanas

Filtrar é selecionar linhas por uma condição , e não por rótulo ou posição. O mecanismo é o mesmo  do  NumPy:  a  condição  produz  uma  Series  de True / False do  tamanho  do DataFrame, que é usada como índice.

```
mascara = df["nota_final"] >= 70 # Series de bool, 480 elementos df[mascara] # só as linhas True df.loc[mascara, ["nome", "nota_final"]] # filtra E escolhe colunas
```

## Combinando condições

## DOIS ERROS QUE TODO INICIANTE COMETE

1. Usar and / or no lugar de &amp; / | . Os operadores do Python esperam um único valor booleano e disparam ValueError: The truth value of a Series is ambiguous .
2. Esquecer os parênteses. Em Python, &amp; tem precedência maior que &gt;= , então df["a"] &gt; 1 &amp; df["b"] &lt; 2 é interpretado errado. Sempre envolva cada condição em parênteses.

```
# CERTO df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)] # E df[(df["campus"] == "Mossoró") | (df["campus"] == "Apodi")] # OU df[~(df["situacao"] == "Aprovado")] # NÃO # ERRADO df[df["turno"] == "Noturno" and df["nota_final"] >= 80] # ValueError df[df["turno"] == "Noturno" & df["nota_final"] >= 80] # precedência errada
```

## Atalhos que deixam o código legível

| Expressão                                           | O que faz                                                          |
|-----------------------------------------------------|--------------------------------------------------------------------|
| df["campus"].isin(lista)                            | Pertence a um conjunto de valores - substitui uma cadeia de &#124; |
| df["idade"].between(18, 24)                         | Intervalo fechado (inclui as pontas)                               |
| df["curso"].str.contains("Redes", na=False)         | Texto contém o trecho; aceita expressão regular                    |
| df["curso"].str.startswith("Análise")               | Começa com                                                         |
| df["nota_final"].isna() / .notna()                  | É / não é ausente                                                  |
| df.query("turno == 'Noturno' and nota_final >= 80") | Sintaxe em string, sem parênteses nem &                            |
| df.nlargest(10, "nota_final")                       | As 10 maiores - mais direto que ordenar e cortar                   |
| df.sort_values("nota_final", ascending=False)       | Ordena por uma ou mais colunas                                     |

```
metropolitana = ["Natal-Central", "Natal-Zona Norte", "Parnamirim"] df[df["campus"].isin(metropolitana)] # str.contains aceita regex: "Sistemas" OU "Redes" df[df["curso"].str.contains("Sistemas|Redes", na=False)]
```

## NA=FALSE NÃO É OPCIONAL

Em str.contains ,  um  valor  ausente  produz NaN -  e NaN usado  como  máscara  levanta  erro. na=False trata o ausente como "não contém", que é quase sempre o comportamento desejado.

## 1.9 Atribuição segura e o SettingWithCopyWarning

Modificar um DataFrame parece trivial, mas é a origem do aviso mais famoso do Pandas.

```
# ERRADO - "indexação encadeada": dois colchetes em sequência df[df["frequencia"].isna()]["frequencia"] = 85.0 # SettingWithCopyWarning - e, pior, o df original pode não mudar # CERTO - uma única operação com loc: [linhas, coluna] df.loc[df["frequencia"].isna(), "frequencia"] = 85.0
```

Por  quê? df[mascara] pode  devolver  uma cópia ou  uma vista dos  dados  originais  -  o Pandas não garante qual. Se for cópia, a atribuição altera um objeto temporário que será descartado. Com df.loc[linhas, coluna] = valor o Pandas sabe que a intenção é escrever no original e o faz de forma determinística.

Outras formas seguras de criar ou alterar colunas:

```
df["aprovado"] = df["situacao"] == "Aprovado" # coluna nova df["nota_10"]  = (df["nota_final"] / 10).round(1) # derivada # np.where: if/else vetorizado df["faixa"] = np.where(df["nota_final"] >= 70, "Bom", "A melhorar") # assign: encadeável, não modifica o original df2 = df.assign(nota_10=lambda d: d["nota_final"] / 10) # Ao derivar um subconjunto que será alterado, copie explicitamente noturno = df[df["turno"] == "Noturno"].copy()
```

## ARMADILHA DO NP.WHERE COM AUSENTES

NaN &gt;= 70 é False . Logo, np.where(df["nota"] &gt;= 70, "Bom", "A melhorar") classifica silenciosamente todos os estudantes sem nota como "A melhorar". A correção é reinserir o ausente depois: df["faixa"] = df["faixa"].mask(df["nota"].isna()) .

## 1.10 Valores ausentes: NaN não é zero

Ausente significa "não sei", e isso é diferente de "zero" e de "vazio". Confundir os três é uma das formas mais rápidas de produzir uma análise errada com aparência correta.

| Operação                             | Efeito                                          |
|--------------------------------------|-------------------------------------------------|
| df.isna().sum()                      | Quantos ausentes por coluna                     |
| df.isna().sum().sum()                | Total de células ausentes                       |
| df.isna().mean().round(3)            | Proporção de ausentes por coluna                |
| df.dropna()                          | Remove linhas com qualquer ausente (agressivo!) |
| df.dropna(subset=["nota_final"])     | Remove só quem falta naquela coluna             |
| df["col"].fillna(valor)              | Preenche com um valor fixo                      |
| df["col"].fillna(df["col"].median()) | Preenche com a mediana (robusta a outliers)     |
| df["col"].ffill()                    | Repete o último valor válido (séries temporais) |

A  pergunta  certa  não  é  "como  remover  os NaN ?",  e  sim "por  que  eles  estão  ali?" .  No conjunto desta aula, os 41 estudantes sem nota\_final estão em situação Trancado (27) ou Em curso (14): a nota não existe ainda - não foi perdida. Preenchê-la com a média criaria desempenho  fictício  e  distorceria  qualquer  comparação  entre  campi.  Já  a frequencia ausente  em  9  registros  é  plausivelmente  falha  de  registro,  e  imputar  a  mediana  é defensável - desde que a decisão seja documentada .

## 1.11 Erros mais comuns e como corrigi-los

| Mensagem / sintoma                                   | Causa provável                                           | Correção                                                                               |
|------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------------------------------------|
| ValueError: The truth value of a Series is ambiguous | Uso de and , or ou not com Series                        | Trocar por & , &#124; , ~ e pôr parênteses                                             |
| KeyError: 'nota final'                               | Nome de coluna com espaço, acento ou maiúscula diferente | Conferir df.columns ; padronizar com df.columns.str.strip().str.lower()                |
| SettingWithCopyWarning                               | Indexação encadeada df[...] [...] = ...                  | Usar df.loc[linhas, coluna] = ... ; .copy() ao derivar subconjunto                     |
| Coluna numérica veio como object                     | Vírgula decimal, milhar, ou texto no meio dos números    | decimal="," , thousands="." , na_values=[...] , ou pd.to_numeric(col, errors="coerce") |
| Acentos corrompidos ( MossorÃ³ )                     | Codificação errada na leitura                            | encoding="latin-1" ou "cp1252"                                                         |
| Uma única coluna gigante após read_csv               | Separador errado                                         | sep=";" (ou sep=None, engine="python" para detectar)                                   |
| Coluna Unnamed: 0 apareceu                           | O índice foi gravado no CSV anterior                     | Gravar com index=False ; ler com index_col=0                                           |
| IndexingError: Unalignable boolean Series            | Máscara com índice diferente do DataFrame                | reset_index(drop=True) nos dois, ou usar .to_numpy()                                   |
| df.loc[0:2] devolveu 3 linhas                        | Não é erro: loc inclui o limite final                    | Usar iloc[0:2] se quiser exatamente duas                                               |
| Média "correta" mas suspeita                         | Ausentes ignorados silenciosamente                       | Sempre reportar count junto da média                                                   |

## 1.12 Boas práticas de laboratório

1. Nunca  sobrescreva  o  arquivo  original. Leia  de dados/ e  grave  resultados  em saida/ .
2. Uma célula, uma ideia. Notebooks longos com uma célula gigante são impossíveis de depurar.
3. Documente decisões, não sintaxe. O comentário útil é "imputamos a mediana porque são 9 registros e a distribuição é assimétrica" , não "preenche os NaN" .
4. Reexecute do zero antes de entregar ( Kernel → Restart &amp; Run All ). Notebook que só funciona fora de ordem não é reprodutível.
5. Cheque o shape depois  de  cada  filtro. Um filtro  que  devolve  0  ou  todas  as  linhas quase sempre esconde um erro de lógica.
6. Prefira vetorização a for . Se precisar iterar, use itertuples() , nunca iterrows() em laços grandes.

7. Fixe  a  semente ( np.random.default\_rng(42) )  sempre  que  houver  aleatoriedade,  para que o resultado seja reproduzível.
8. Declare o que não sabe. Toda análise tem limitação; explicitá-la é sinal de rigor, não de fraqueza.

## Parte II - Tópicos de estudo dirigido

Roteiro de leitura individual, correspondente ao livro "T ópicos de Estudo - Aula 04" no Moodle

O livro da Aula 04 no AVA está dividido em seis capítulos. Esta parte funciona como guia de estudo :  para  cada  capítulo,  o  que  se  espera  que  você  domine,  as  questões  que  deve conseguir  responder  sem  consultar,  e  o  erro  que  costuma  aparecer  na  avaliação.  Estude com o Jupyter aberto - leia um trecho, execute, altere um parâmetro, observe o que muda .

## Capítulo 1 - Do array ao DataFrame

Domine: a  diferença  entre  lista  Python, ndarray e DataFrame ;  o  que  cada  camada acrescenta e a que custo; o conceito de vetorização.

## Responda sem consultar:

- Por que um ndarray é mais rápido que uma lista para somar um milhão de números?
- O que o Pandas acrescenta ao NumPy? Cite três coisas.
- Em que situação uma lista de dicionários ainda é preferível a um DataFrame?

Erro frequente: achar que vetorizar é "escrever menos código". Vetorizar é mover o laço para código compilado; a concisão é consequência, não a causa do ganho.

## Capítulo 2 - Series, DataFrame e o índice

Domine: a anatomia da Series (valores + índice + nome); o DataFrame como conjunto de Series que compartilham índice; alinhamento automático por rótulo; o significado de cada dtype .

## Responda sem consultar:

- O que acontece ao somar duas Series com índices em ordens diferentes?
- Por que uma coluna de inteiros vira float64 quando ganha um ausente?
- Quando vale a pena transformar uma coluna em category ?

Erro frequente: tratar o índice como "número da linha". Ele é um rótulo; após um filtro, deixa de ser sequencial.

## Capítulo 3 - Criação de DataFrames e leitura de arquivos

Domine: as cinco formas de criar um DataFrame; os parâmetros sep , decimal , encoding , dtype , na\_values e usecols de read\_csv ; sheet\_name em read\_excel .

## Responda sem consultar:

- Como ler um CSV brasileiro ( ; e vírgula decimal) sem que as notas virem texto?
- Por que uma matrícula deve ser lida como texto e não como inteiro?
- Como carregar todas as abas de um Excel de uma vez?

Erro frequente: aceitar a leitura padrão sem conferir df.dtypes . Uma coluna numérica em object invalida todo o resto.

## Capítulo 4 - Inspeção básica

Domine: a sequência shape → head → info → describe → isna → value\_counts → duplicated e o que procurar em cada saída.

## Responda sem consultar:

- Como info() revela valores ausentes sem que você chame isna() ?
- O que sugere uma média bem maior que a mediana?
- Por que sample(5) às vezes é mais honesto que head(5) ?

Erro  frequente: ler describe() e  ignorar  a  linha count ,  que  é  justamente  onde  os ausentes aparecem.

## Capítulo 5 - Seleção com loc e iloc

Domine: rótulo × posição; fatia inclusiva do loc × exclusiva do iloc ; seleção simultânea de linhas e colunas; at / iat .

## Responda sem consultar:

- Quantas linhas devolve df.loc[0:2] ? E df.iloc[0:2] ? Por quê?
- Depois de set\_index("matricula") , por que iloc["20261000"] falha?
- Como selecionar, em um só comando, as linhas do turno noturno e apenas duas colunas?

Erro frequente: usar iloc depois  de  um  filtro  esperando  o  "número  original"  da  linha. Após filtrar, posição e rótulo divergem.

## Capítulo 6 - Filtragem, atribuição segura e ausentes

```
Domine: máscaras booleanas; & , | , ~ e parênteses; isin , between , str.contains(na=False) , query ; df.loc[...]  =  ... ;  o  que  fazer  (e  o  que  não  fazer)  com NaN .
```

## Responda sem consultar:

- Por que and não funciona entre duas condições de Series?
- O que é o SettingWithCopyWarning e como evitá-lo definitivamente?
- Em que caso preencher um valor ausente é errado , e não apenas discutível?

Erro frequente: preencher ausentes por reflexo. Imputar sem justificar é inventar dado.

## AUTOAVALIAÇÃO RÁPIDA

Você está pronto para o laboratório quando conseguir, de memória, escrever as linhas que (1) leem um CSV com ; e vírgula decimal mantendo a matrícula como texto, (2) mostram quantos ausentes há em cada coluna, (3) selecionam nome e nota dos estudantes do noturno com nota ≥ 80, e (4) preenchem os ausentes de uma coluna sem disparar aviso.

## Parte III - Laboratório guiado

Matrículas do IFRN (dados sintéticos) - todas as saídas abaixo foram produzidas pelo código apresentado

Arquivos necessários, na pasta dados/ ao lado do notebook:

- matriculas\_ifrn\_2026.csv - 482 linhas, 12 colunas, separador ; , vírgula decimal;
- campi\_ifrn.xlsx - duas planilhas: campi (12 linhas) e cursos (10 linhas).

## Passo 1 - Ler corretamente

```
import numpy as np import pandas as pd df = pd.read_csv( "dados/matriculas_ifrn_2026.csv", sep=";", decimal=",", encoding="utf-8", dtype={"matricula": "string"}, ) print(df.shape)
```

(482, 12)

Compare com o que acontece sem os parâmetros: uma única coluna chamada matricula;nome;campus;... . Vale executar o erro uma vez para reconhecê-lo depois.

## Passo 2 - Inspecionar

```
df.info() <class 'pandas.DataFrame'> RangeIndex: 482 entries, 0 to 481 Data columns (total 12 columns): #   Column        Non-Null Count  Dtype ---  ------        --------------  ----- 0   matricula     482 non-null    string 1   nome          482 non-null    object 2   campus        482 non-null    object 3   curso         482 non-null    object 4   modalidade    482 non-null    object 5   turno         482 non-null    object 6   ano_ingresso  482 non-null    int64 7   semestre      482 non-null    int64 8   idade         482 non-null    int64 9   nota_final    441 non-null    float64 10   frequencia    473 non-null    float64 11   situacao      482 non-null    object
```

Leitura  da  saída: nota\_final tem  441  de  482  (41  ausentes)  e frequencia tem  473  (9 ausentes).  Os  tipos  numéricos  estão  corretos  -  sinal  de  que decimal="," funcionou. matricula é string , como pedido.

print(df.describe().round(2))

|       |         |   ano_ingresso |   semestre |   idade nota_final |   frequencia |
|-------|---------|----------------|------------|--------------------|--------------|
| count |  482.00 |         482.00 |     482.00 |             441.00 |       473.00 |
| mean  | 2024.70 |           1.43 |      23.64 |              69.15 |        85.99 |
| std   |    1.07 |           0.50 |       5.41 |              12.42 |         9.82 |
| min   | 2023.00 |           1.00 |      15.00 |              34.40 |        57.80 |
| 25%   | 2024.00 |           1.00 |      20.00 |              60.60 |        79.40 |
| 50%   | 2025.00 |           1.00 |      24.00 |              69.70 |        86.10 |
| 75%   | 2026.00 |           2.00 |      27.00 |              77.30 |        94.40 |
| max   | 2026.00 |           2.00 |      39.00 |             100.00 |       100.00 |

Média  (69,15)  e  mediana  (69,70)  praticamente  coincidem:  a  distribuição  das  notas  é aproximadamente simétrica. Os limites são plausíveis - idade de 15 a 39, nota de 34,4 a 100.  Se  aparecesse  idade  0  ou  nota  999,  haveria  um  código  de  ausência  disfarçado  de número.

```
print(df.isna().sum()) print("duplicadas:", df.duplicated().sum()) print("campi distintos:", df["campus"].nunique())
```

```
nota_final      41 frequencia       9 (demais colunas: 0) duplicadas: 2 campi distintos: 19
```

## 19 CAMPI?

O IFRN não tem 19 campi neste conjunto - tem 12. A diferença vem de valores com espaços nas bordas : " Mossoró " é, para o Pandas, diferente de "Mossoró" . É exatamente o tipo de defeito que value\_counts() e nunique() revelam e que passaria despercebido em um gráfico.

## Passo 3 - Limpeza mínima

```
df["campus"] = df["campus"].str.strip() df = df.drop_duplicates().reset_index(drop=True) print(df.shape, "| campi:", df["campus"].nunique())
```

```
(480, 12) | campi: 12
```

## Passo 4 - Selecionar: iloc e loc

```
df.iloc[0:3, 0:4] # 3 primeiras linhas, 4 primeiras colunas
```

```
matricula                         nome         campus                                  curso 0  20261000  Wagner Cavalcante Fernandes          Apodi  Análise e Desenvolvimento de Sistemas 1  20261001        Zélia Santos Oliveira          Macau                  Redes de Computadores 2  20261002          Zélia Barbosa Costa  Currais Novos                       Ciência de Dados
```

```
df.loc[0:2, ["nome", "campus", "nota_final"]] # atenção: 0:2 inclui o 2
```

```
nome         campus  nota_final 0  Wagner Cavalcante Fernandes          Apodi        34.4 1        Zélia Santos Oliveira          Macau        70.9 2          Zélia Barbosa Costa  Currais Novos        87.8
```

Com a matrícula promovida a índice, a seleção passa a falar a língua do domínio:

```
dfm = df.set_index("matricula")
```

```
dfm.loc["20261042", ["nome", "campus", "nota_final"]]
```

```
nome          Ubiratan Rocha Barbosa campus                 Natal-Central nota_final                      76.4 Name: 20261042, dtype: object
```

## Passo 5 - Filtrar

```
aprovados   = df[df["situacao"] == "Aprovado"] noturno_bom = df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)] metro       = df[df["campus"].isin(["Natal-Central", "Natal-Zona Norte", "Parnamirim"])] jovens      = df[df["idade"].between(18, 24)] ti          = df[df["curso"].str.contains("Sistemas|Redes", na=False)] for rotulo, sub in [("aprovados", aprovados), ("noturno >= 80", noturno_bom), ("3 campi metrop.", metro), ("18 a 24 anos", jovens), ("cursos de TI", ti)]: print(f"{rotulo:<18} {len(sub):>4}")
```

```
aprovados            281 noturno >= 80         35 3 campi metrop.      174 18 a 24 anos         189 cursos de TI         107
```

## Passo 6 - Atribuir com segurança

```
# Imputa a frequência ausente pela mediana - decisão documentada df.loc[df["frequencia"].isna(), "frequencia"] = df["frequencia"].median() print("ausentes em frequencia:", df["frequencia"].isna().sum())
```

```
ausentes em frequencia: 0
```

## Passo 7 - NumPy por baixo do Pandas

```
mask = (df["nota_final"] >= 60).to_numpy() print(type(mask), mask.dtype, mask.sum(), "de", mask.size) notas = df["nota_final"].to_numpy() print("np.nanmean:", round(float(np.nanmean(notas)), 2))
```

```
<class 'numpy.ndarray'> bool 337 de 480 np.nanmean: 69.2
```

## Agora a armadilha do np.where , em duas versões:

```
df["faixa"] = np.where(df["nota_final"] >= 80, "Alta", np.where(df["nota_final"] >= 60, "Média", "Baixa")) print(df["faixa"].value_counts(dropna=False))
```

```
Média    244 Baixa    143     <- inclui, indevidamente, os 41 sem nota Alta      93
```

```
df["faixa"] = df["faixa"].mask(df["nota_final"].isna()) print(df["faixa"].value_counts(dropna=False))
```

```
Média    244 Baixa    102 Alta      93 NaN       41     <- agora "sem nota" é uma categoria própria
```

## Passo 8 - Responder uma pergunta

Em quais campi a nota média supera a média geral?

```
media_geral = df["nota_final"].mean() media_campus = (df.groupby("campus")["nota_final"] .mean().sort_values(ascending=False).round(2)) print(f"média geral: {media_geral:.2f}") print(media_campus[media_campus > media_geral])
```

```
média geral: 69.20 campus Santa Cruz          74.55 Currais Novos       72.28 Apodi               71.69 Mossoró             71.66 Natal-Zona Norte    70.36 Caicó               70.04
```

## LEIA O RESULTADO COM CETICISMO

Seis campi acima da média - e daí? As diferenças são de 1 a 5 pontos, os grupos têm tamanhos muito distintos (Natal-Central tem 98 estudantes; Caicó, 23 - e apenas 21 com nota), e a nota média  ignora  curso,  turno  e  ano  de  ingresso.  Além  disso, estes  dados  são  sintéticos :  a ordenação acima é ruído com aparência de informação. Reportar um ranking a partir daqui seria um erro técnico grave - e é precisamente o erro que a Aula 05 (agrupamentos) e a Unidade 3 (análise exploratória) ensinam a evitar.

## Parte IV - Exercício prático avaliativo

Entrega obrigatória no Moodle · valor 10,0 pontos · notebook executado

O exercício está no arquivo aula04\_laboratorio.ipynb , disponível no AVA junto com a pasta dados/ . As dez questões abaixo são as mesmas do notebook, reproduzidas aqui para leitura offline.

## Instruções de entrega

1. Renomeie o notebook para aula04\_SEUNOME.ipynb .
2. Responda nas células indicadas, sem apagar os enunciados .
3. Execute tudo do zero ( Kernel → Restart &amp; Run All ) e confirme que não há erros.
4. Envie  o .ipynb já  executado ,  com  as  saídas  visíveis,  na  tarefa "Exercício Prático - Aula 04" .
5. Questões que pedem interpretação exigem texto , não apenas código.

## Critérios de correção

| Critério                                  | Peso   | O que se avalia                                                |
|-------------------------------------------|--------|----------------------------------------------------------------|
| Correção técnica do código                | 60%    | O código roda e produz o resultado pedido                      |
| Uso adequado de loc / iloc e de filtragem | 20%    | Escolha correta da ferramenta; ausência de indexação encadeada |
| Interpretação escrita                     | 20%    | Leitura dos resultados e reconhecimento de limitações          |

## As questões

1. Leitura  correta  do  CSV  (1,0). Leia matriculas\_ifrn\_2026.csv em df de  modo  que nota\_final e frequencia fiquem  numéricas  e matricula fique  como  texto.  Mostre  o shape .
2. Inspeção inicial (1,0). Com head , info e describe ,  responda: (a) quantas linhas e colunas;  (b)  quais  colunas  têm  ausentes  e  quantos;  (c)  qual  a  média  e  a  mediana  de nota\_final e o que a diferença entre elas sugere.
3. Limpeza mínima (1,0). Corrija  os  espaços  sobrando  em campus e  remova  as  linhas duplicadas, comprovando o antes e o depois com nunique() e duplicated().sum() .
4. iloc (1,0). Sem usar loc , exiba: (a) as cinco últimas linhas; (b) as linhas de posição 10 a 14 apenas das colunas nome , campus e nota\_final , usando posições de coluna; (c) o valor de situacao na última linha.
5. loc (1,0). Defina matricula como índice em dfm ,  mostre nome , curso e nota\_final da matrícula 20261250 , e explique em uma frase por que dfm.iloc["20261250"] falha.

6. Filtragem booleana (1,5). Obtenha e conte: (a) noturno com nota ≥ 70; (b) EaD com ingresso em 2025 ou 2026; (c) aprovados com frequência abaixo de 80 - e diga o que esse  número  revela  sobre  a  regra  de  aprovação;  (d)  cursos  cujo  nome  contenha "Sistemas" ou "Redes".
7. Valores ausentes (1,5). (a)  Quantos estão sem nota\_final e  qual a situacao deles? (b) Preencha os ausentes de frequencia com a mediana, usando loc . (c) Justifique por que não se deve preencher nota\_final .
8. Coluna derivada com NumPy (1,0). Crie faixa com np.where : ≥ 85 "Excelente", ≥ 70 "Bom", ≥ 60 "Regular", abaixo disso "Insuficiente" - garantindo que quem não tem nota fique com NaN .
9. Cruzando com o Excel (1,0). Leia a planilha campi , liste os campi da região Oeste e conte quantos estudantes estudam neles, usando isin com a lista obtida (sem digitar os nomes à mão).
10. Uma pergunta respondida com dados (1,0). "Os estudantes do turno noturno têm desempenho diferente dos demais?" Calcule nota média, número de estudantes e taxa de aprovação por turno; escreva a interpretação e uma limitação da conclusão.

## SOBRE A QUESTÃO 10

Não existe resposta "certa" quanto ao conteúdo: os dados são sintéticos. Avalia-se o raciocínio - se  os  números  foram  calculados  corretamente,  se  a  leitura  deles  é  coerente  e  se  a  limitação apontada  é  pertinente  (confundimento  com  curso  e  campus,  tamanhos  de  grupo  desiguais, correlação não implicando causa).

## Parte V - Formulário avaliativo

10 questões objetivas · respondidas no Moodle · consulta ao material permitida

O  formulário  é  respondido  no  AVA,  na  atividade "Formulário  Avaliativo  -  Aula  04" .  As questões estão reproduzidas abaixo para que você possa prepará-las antes. Cada questão vale 1,0 ponto e admite uma única alternativa correta.

## Questão 01

O arquivo matriculas\_ifrn\_2026.csv usa ponto e vírgula para separar campos e vírgula como separador decimal. Qual chamada lê o arquivo de modo que a coluna nota\_final fique com dtype float64 ?

```
A. pd.read_csv(p, sep=";", decimal=",") B. pd.read_csv(p) C. pd.read_csv(p, sep=";") D. pd.read_csv(p, sep=",", decimal=";")
```

## Questão 02

Um  DataFrame df tem  índice  padrão  (0,  1,  2,  ...)  e  480  linhas.  Quantas  linhas devolvem, respectivamente, df.loc[0:2] e df.iloc[0:2] ?

A. 3 e 2

B. 2 e 2

C. 3 e 3

D. 2 e 3

## Questão 03

Por que a coluna matricula deve ser lida com dtype={"matricula": "string"} em vez de ser deixada como inteiro?

- A. Porque é um identificador: zeros à esquerda seriam perdidos e operações aritméticas sobre ele não teriam sentido.
- B. Porque o Pandas não consegue ler colunas numéricas de arquivos CSV.
- C. Porque colunas de texto ocupam menos memória que colunas inteiras.
- D. Porque loc só funciona com índices de texto.

## Questão 04

A saída de df.info() mostra RangeIndex: 482 entries e, para a coluna nota\_final , 441 non-null float64 . O que se conclui?

- A. 41 registros estão sem nota final, e a coluna é numérica.
- B. A coluna tem 441 valores distintos.
- C. 41 notas foram lidas como texto.
- D. O arquivo tem 441 linhas.

## Questão 05

A expressão df[df["turno"] == "Noturno" and df["nota\_final"] &gt;= 80] levanta ValueError: The truth value of a Series is ambiguous . Qual é a forma correta?

```
A. df[(df["turno"] == "Noturno") & (df["nota_final"] >= 80)] B. df[df["turno"] == "Noturno" & df["nota_final"] >= 80] C. df[(df["turno"] == "Noturno") and (df["nota_final"] >= 80)] D. df[(df["turno"] == "Noturno") + (df["nota_final"] >= 80)]
```

## Questão 06

Em df.describe() ,  a  linha count de frequencia mostra 473, enquanto idade mostra 482. O que isso indica?

- A. Que frequencia tem  9  valores  ausentes,  ignorados  no  cálculo  das  demais  estatísticas  da coluna.
- B. Que 9 estudantes têm frequência igual a zero.
- C. Que o DataFrame tem 473 linhas.
- D. Que 9 valores estão fora do intervalo de 0 a 100.

## Questão 07

Você  quer  preencher  com  85  os  valores  ausentes  da  coluna frequencia .  Qual  forma evita o SettingWithCopyWarning e garante a alteração do DataFrame original?

```
A. df.loc[df["frequencia"].isna(), "frequencia"] = 85 B. df[df["frequencia"].isna()]["frequencia"] = 85 C. df[df["frequencia"].isna()].frequencia = 85 D. df.iloc[df["frequencia"].isna(), 10] = 85
```

## Questão 08

Após executar df["faixa"] = np.where(df["nota\_final"] &gt;= 60, "Aprovado", "Reprovado") em um DataFrame com 41 notas ausentes, o que acontece com esses 41 registros?

- A. Ficam classificados como "Reprovado", porque NaN &gt;= 60 é False .
- B. Ficam com NaN em faixa , pois o NumPy propaga ausentes.
- C. O comando levanta uma exceção por causa dos ausentes.
- D. Ficam classificados como "Aprovado", pois NaN é tratado como valor alto.

## Questão 09

Qual  expressão  seleciona  os  estudantes  matriculados  em  qualquer  um  dos  campi listados em oeste = ["Mossoró", "Apodi", "Pau dos Ferros"] ?

```
A. df[df["campus"].isin(oeste)] B. df[df["campus"] == oeste] C. df[df["campus"] in oeste] D. df.loc[oeste]
```

## Questão 10

A  nota  média  por  campus,  calculada  sobre  estes  dados,  varia  de  63,8  a  74,6.  Qual conclusão é tecnicamente defensável?

- A. Nenhuma  conclusão  sobre  desempenho  real  é  possível:  os  dados  são  sintéticos  e  a comparação ignora curso, turno, tamanho de turma e valores ausentes.
- B. O campus com maior média oferece ensino de melhor qualidade.
- C. A diferença é pequena, logo os campi são estatisticamente equivalentes.
- D. Os campi com menos estudantes têm médias mais confiáveis, por serem grupos menores.

## Apêndice A - Colinha de comandos

## Leitura e escrita

| Comando                                   | Faz                           |
|-------------------------------------------|-------------------------------|
| pd.read_csv(p, sep=";", decimal=",")      | Lê CSV no padrão brasileiro   |
| pd.read_csv(p, dtype={"id": "string"})    | Força coluna como texto       |
| pd.read_csv(p, usecols=[...], nrows=1000) | Lê só parte do arquivo        |
| pd.read_excel(p, sheet_name="campi")      | Lê uma aba do Excel           |
| pd.read_excel(p, sheet_name=None)         | Lê todas as abas (dicionário) |
| df.to_csv("s.csv", index=False)           | Grava sem o índice            |

## Inspeção

| Comando                                      | Faz                               |
|----------------------------------------------|-----------------------------------|
| df.shape · len(df)                           | (linhas, colunas) · nº de linhas  |
| df.head(n) · df.tail(n) · df.sample(n)       | Espia o conteúdo                  |
| df.info()                                    | Tipos, não nulos, memória         |
| df.describe() · describe(include="all")      | Resumo numérico · com texto       |
| df.dtypes · df.columns · df.index            | Metadados                         |
| df.isna().sum() · .mean()                    | Ausentes: total · proporção       |
| df["c"].value_counts(dropna=False)           | Contagem por categoria            |
| df["c"].nunique() · .unique()                | Quantos · quais valores distintos |
| df.duplicated().sum() · df.drop_duplicates() | Detecta · remove repetidas        |

## Seleção

| Comando                                       | Faz                                      |
|-----------------------------------------------|------------------------------------------|
| df["c"] · df[["a","b"]]                       | Uma coluna (Series) · várias (DataFrame) |
| df.loc[r, "c"]                                | Por rótulo; fatia inclui o fim           |
| df.iloc[i, j]                                 | Por posição; fatia exclui o fim          |
| df.at[r,"c"] · df.iat[i,j]                    | Uma célula, mais rápido                  |
| df.set_index("c") · df.reset_index(drop=True) | Define · renumera índice                 |

## Filtragem e alteração

| Comando                                                   | Faz                                     |
|-----------------------------------------------------------|-----------------------------------------|
| df[(cond1) & (cond2)]                                     | E lógico (parênteses obrigatórios)      |
| df[(cond1) &#124; (cond2)] · df[~cond]                    | OU · NÃO                                |
| df["c"].isin([...]) · .between(a,b)                       | Pertence a · intervalo fechado          |
| df["c"].str.contains("x", na=False)                       | Texto contém (aceita regex)             |
| df.query("a > 1 and b == 'x'")                            | Filtro em string                        |
| df.sort_values("c", ascending=False) · df.nlargest(n,"c") | Ordena · maiores                        |
| df.loc[mascara, "c"] = valor                              | Atribuição segura                       |
| np.where(cond, a, b) · s.mask(cond)                       | if/else vetorizado · vira NaN onde True |
| df["c"].fillna(v) · df.dropna(subset=["c"])               | Preenche · descarta ausentes            |

## Apêndice B - Referências e leituras recomendadas

- McKINNEY,  Wes. Python  para  Análise  de  Dados .  3.  ed.  São  Paulo:  Novatec,  2023. Capítulos 4 (NumPy), 5 (Introdução ao pandas) e 6 (Carregamento e armazenamento de dados). Leitura principal desta aula. A 3ª edição em inglês está disponível gratuitamente em wesmckinney.com/book .
- PANDAS DEVELOPMENT TEAM. Pandas  User  Guide -  seções 10  minutes  to  pandas , Indexing and selecting data e IO tools (text, CSV, HDF5, …) . pandas.pydata.org/docs/user\_guide/
- HARRIS, C. R. et al. Array programming with NumPy. Nature , v. 585, p. 357-362, 2020. Artigo de referência sobre o projeto do ndarray .
- VANDERPLAS, Jake. Python Data Science Handbook . 2. ed. O'Reilly, 2023. Capítulos 2 e 3. Versão on-line gratuita em jakevdp.github.io/PythonDataScienceHandbook/
- PANDAS DEVELOPMENT TEAM. Returning a view versus a copy - documentação oficial sobre o SettingWithCopyWarning .
- WICKHAM,  Hadley.  Tidy  Data. Journal  of  Statistical  Software ,  v.  59,  n.  10,  2014. Fundamento conceitual da organização de tabelas - base para a Aula 05.

## O que vem na Aula 05

Laboratório Pandas II - Agrupamentos e Joins : groupby , agg , pivot\_table , combinação de tabelas com merge / join , apply com lambda e introdução ao method chaining . O groupby usado no Passo 8 deste laboratório será então tratado em profundidade.

Aula 04 - Laboratório NumPy e Pandas I · Análise e Ciência de Dados · Especialização em Ciência de Dados · IFRN