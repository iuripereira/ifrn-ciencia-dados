# aula04_laboratorio.ipynb

# Aula 04 — Laboratório NumPy e Pandas I

**Disciplina:** Análise e Ciência de Dados
**Curso:** Especialização em Ciência de Dados — IFRN
**Professor:** Plácido Antônio de Souza Neto

---

## Antes de começar

1. Renomeie este arquivo para `aula04_SEUNOME.ipynb`.
2. Mantenha a pasta `dados/` ao lado do notebook, com os arquivos
   `matriculas_ifrn_2026.csv` e `campi_ifrn.xlsx`.
3. Responda **na célula indicada**, sem apagar os enunciados.
4. Execute tudo do zero antes de entregar (`Kernel → Restart & Run All`)
   e confira se não há erros.
5. Entregue o `.ipynb` **já executado** (com as saídas visíveis) no Moodle.

> Os dados são **sintéticos**: nomes de campi e cursos são reais, mas
> matrículas, nomes de estudantes e notas foram gerados aleatoriamente.
> Nenhuma conclusão sobre o IFRN pode ser tirada deles.

## Dicionário de dados — `matriculas_ifrn_2026.csv`

| Coluna | Tipo | Descrição |
|---|---|---|
| `matricula` | texto | Identificador do estudante (8 dígitos, **não é número**) |
| `nome` | texto | Nome fictício do estudante |
| `campus` | texto | Campus do IFRN |
| `curso` | texto | Nome do curso |
| `modalidade` | texto | `Presencial` ou `EaD` |
| `turno` | texto | `Matutino`, `Vespertino` ou `Noturno` |
| `ano_ingresso` | inteiro | Ano de ingresso (2023–2026) |
| `semestre` | inteiro | Semestre de ingresso (1 ou 2) |
| `idade` | inteiro | Idade em anos |
| `nota_final` | decimal | Nota final de 0 a 100 (**tem ausentes**) |
| `frequencia` | decimal | Frequência em % (**tem ausentes**) |
| `situacao` | texto | `Aprovado`, `Reprovado por nota`, `Reprovado por falta`, `Trancado`, `Em curso` |

O arquivo usa **`;` como separador** e **vírgula como separador decimal**.

## Dicionário de dados — `campi_ifrn.xlsx`

Planilha `campi`: `campus`, `cidade`, `regiao`, `ano_criacao`, `num_docentes`
Planilha `cursos`: `curso`, `eixo_tecnologico`, `nivel`, `carga_horaria`


## Questão 1 — Leitura correta do CSV (1,0 ponto)

Leia `dados/matriculas_ifrn_2026.csv` em um DataFrame chamado `df`, de modo que:

- as colunas `nota_final` e `frequencia` fiquem **numéricas** (`float64`);
- a coluna `matricula` fique como **texto**.

Em seguida, mostre o formato (`shape`) do DataFrame.

> **Dica:** os parâmetros `sep`, `decimal` e `dtype` de `pd.read_csv`.

```python
import pandas as pd
import numpy as np

# ESCREVA SEU CÓDIGO AQUI
df = ...

```

_Sua resposta escrita:_



## Questão 2 — Inspeção inicial (1,0 ponto)

Usando `head()`, `info()` e `describe()`, responda **em uma célula de texto**:

a) Quantas linhas e quantas colunas o arquivo tem?
b) Quais colunas possuem valores ausentes e quantos?
c) Qual a nota final **média** e qual a **mediana**? O que a diferença
   entre as duas sugere sobre a distribuição?

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 3 — Limpeza mínima (1,0 ponto)

O arquivo tem dois defeitos propositais:

1. alguns valores de `campus` vêm com **espaços em branco** nas bordas;
2. existem **linhas duplicadas**.

Corrija os dois problemas e comprove o resultado mostrando, antes e depois,
`df["campus"].nunique()` e `df.duplicated().sum()`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 4 — `iloc`: seleção por posição (1,0 ponto)

Sem usar `loc`, exiba:

a) as **5 últimas** linhas do DataFrame;
b) as linhas de **posição** 10 a 14 (inclusive), apenas das colunas
   `nome`, `campus` e `nota_final` (use as posições das colunas, não os nomes);
c) o valor da célula na **última linha**, coluna `situacao`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 5 — `loc`: seleção por rótulo (1,0 ponto)

a) Defina `matricula` como índice do DataFrame (em uma cópia chamada `dfm`).
b) Usando `loc`, mostre `nome`, `curso` e `nota_final` da matrícula `20261250`.
c) Explique **em uma frase** por que `dfm.loc["20261250"]` funciona
   mas `dfm.iloc["20261250"]` dá erro.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 6 — Filtragem booleana (1,5 ponto)

Crie e mostre o tamanho (`len` ou `.shape`) de cada subconjunto:

a) estudantes do turno **Noturno** com `nota_final` maior ou igual a 70;
b) estudantes da modalidade **EaD** que ingressaram em **2025 ou 2026**;
c) estudantes **aprovados** com `frequencia` abaixo de 80 —
   quantos são? O que esse número diz sobre a regra de aprovação?
d) estudantes cujo `curso` contém a palavra "Sistemas" **ou** "Redes".

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 7 — Valores ausentes (1,5 ponto)

a) Quantos estudantes estão sem `nota_final`? Qual a `situacao` deles?
   (use `value_counts()` sobre o subconjunto filtrado)
b) Preencha os ausentes de `frequencia` com a **mediana** da coluna,
   usando `loc` para atribuir.
c) **Não** preencha `nota_final`. Justifique em uma frase por que
   inventar nota é pior do que inventar frequência aqui.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 8 — Coluna derivada com NumPy (1,0 ponto)

Crie a coluna `faixa` com `np.where`, segundo a regra:

- `nota_final` >= 85 → `"Excelente"`
- 70 <= `nota_final` < 85 → `"Bom"`
- 60 <= `nota_final` < 70 → `"Regular"`
- `nota_final` < 60 → `"Insuficiente"`

**Cuidado:** quem está sem nota deve ficar com `NaN` em `faixa`, e não cair
na última categoria. Mostre `df["faixa"].value_counts(dropna=False)`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 9 — Cruzando com o Excel (1,0 ponto)

a) Leia a planilha `campi` de `dados/campi_ifrn.xlsx` em `campi`.
b) Mostre os campi da região **Oeste**.
c) Quantos estudantes do `df` estudam em campi da região Oeste?
   (use `isin` com a lista obtida no item b — **não** digite os nomes à mão)

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 10 — Uma pergunta respondida com dados (1,0 ponto)

Responda, com código **e** com uma frase de interpretação:

> **Os estudantes do turno noturno têm desempenho diferente dos demais?**

Calcule a nota média por turno, a quantidade de estudantes em cada turno e
a taxa de aprovação por turno. Depois escreva, em uma célula de texto, o que
os números mostram — e **uma limitação** dessa conclusão.

> Lembre-se: os dados são sintéticos. Avalia-se o raciocínio, não a conclusão.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



---

## Entrega

- Arquivo: `aula04_SEUNOME.ipynb`, **executado do início ao fim**.
- Prazo e local: tarefa **"Exercício Prático — Aula 04"** no Moodle.
- Critérios: código correto e legível (60%), uso adequado de `loc`/`iloc`
  e filtragem (20%), interpretação escrita dos resultados (20%).


