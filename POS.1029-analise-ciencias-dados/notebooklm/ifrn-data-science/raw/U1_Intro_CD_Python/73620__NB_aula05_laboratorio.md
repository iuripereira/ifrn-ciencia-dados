# aula05_laboratorio.ipynb

# Aula 05 — Laboratório Pandas II — Agrupamentos e Joins

**Disciplina:** Análise e Ciência de Dados
**Curso:** Especialização em Ciência de Dados — IFRN
**Professor:** Plácido Antônio de Souza Neto

---

## Antes de começar

1. Renomeie este arquivo para `aula05_SEUNOME.ipynb`.
2. Mantenha a pasta `dados/` ao lado do notebook, com os arquivos
   `matriculas_ifrn_2026.csv` e `campi_ifrn.xlsx` — **os mesmos da Aula 04**.
3. Responda **na célula indicada**, sem apagar os enunciados.
4. Execute tudo do zero antes de entregar (`Kernel → Restart & Run All`)
   e confira se não há erros.
5. Entregue o `.ipynb` **já executado** (com as saídas visíveis) no Moodle.

> Os dados são **sintéticos**, os mesmos da Aula 04: nomes de campi e cursos
> são reais, mas matrículas, nomes de estudantes e notas foram gerados
> aleatoriamente. Nenhuma conclusão sobre o IFRN pode ser tirada deles.

## Preparação padrão (execute antes de tudo)

```python
import numpy as np
import pandas as pd

df = pd.read_csv("dados/matriculas_ifrn_2026.csv", sep=";", decimal=",",
                 encoding="utf-8", dtype={"matricula": "string"})
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)

campi = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")
```

## Dicionário de dados

Igual ao da Aula 04 — veja a apostila se precisar relembrar as colunas de
`matriculas_ifrn_2026.csv`. Novidade desta aula:

| Tabela | Colunas |
|---|---|
| `campi` | `campus`, `cidade`, `regiao`, `ano_criacao`, `num_docentes` |
| `cursos` | `curso`, `eixo_tecnologico`, `nivel`, `carga_horaria` |


```python
import numpy as np
import pandas as pd

df = pd.read_csv("dados/matriculas_ifrn_2026.csv", sep=";", decimal=",",
                 encoding="utf-8", dtype={"matricula": "string"})
df["campus"] = df["campus"].str.strip()
df = df.drop_duplicates().reset_index(drop=True)

campi = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")
cursos = pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="cursos")

print(df.shape, campi.shape, cursos.shape)
```

## Questão 1 — `groupby` simples (1,0 ponto)

Calcule, a partir de `df` já limpo (ver preparação padrão):

a) a nota média por `turno`;
b) o número de estudantes (`size`) por `modalidade`;
c) explique, em uma frase, a diferença entre usar `.size()` e usar
   `.count()` sobre a coluna `nota_final` dentro de um `groupby`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 2 — `groupby` com múltiplas colunas (1,0 ponto)

a) Agrupe por `campus` e `turno` simultaneamente e calcule a nota média.
b) Que tipo de índice o resultado tem? Use `type(resultado.index)` para
   confirmar.
c) Converta o resultado para uma tabela "larga" (campus nas linhas, turno
   nas colunas) usando `unstack()`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 3 — `agg` com named aggregation (1,5 ponto)

Usando `groupby("campus")` e **named aggregation** (a forma
`nome=("coluna", "função")`), produza uma tabela com:

- `n_estudantes` — contagem de matrículas;
- `nota_media` — média de `nota_final`;
- `nota_desvio` — desvio padrão de `nota_final`;
- `taxa_aprovacao` — percentual de `situacao == "Aprovado"` (dica: uma
  função `lambda` que calcula a média de uma comparação booleana, vezes 100).

Ordene o resultado por `taxa_aprovacao`, do maior para o menor.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 4 — `pivot_table` (1,5 ponto)

a) Construa uma `pivot_table` com a nota média, `campus` nas linhas e
   `situacao` nas colunas, preenchendo células vazias com `0`
   (`fill_value=0`).
b) Refaça a mesma tabela, agora contando estudantes (em vez de média de
   nota), e adicione uma linha e uma coluna de **total**
   (`margins=True, margins_name="Total"`).
c) Em uma frase: por que faz mais sentido usar contagem, e não média, na
   pivot_table do item (b)?

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 5 — `merge` muitos-para-um (1,5 ponto)

a) Combine `df` com `campi` pela coluna `campus`, com `how="left"` e
   `validate="m:1"`. Chame o resultado de `df_campi`.
b) Combine `df_campi` com `cursos` pela coluna `curso`, do mesmo jeito.
   Chame o resultado de `df_completo`.
c) Confirme que nenhuma linha ficou com `NaN` nas colunas vindas das
   tabelas `campi` ou `cursos` (dica: `.isna().sum()` nas colunas novas).
d) Por que `validate="m:1"` é uma boa prática aqui? O que ela teria
   acusado se `campi` tivesse duas linhas para o mesmo campus?

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 6 — `how="left"` x `how="inner"` (1,0 ponto)

Crie `cursos_parcial`, removendo de `cursos` as linhas cujo
`eixo_tecnologico` seja `"Informação e Comunicação"`. Em seguida:

a) Faça `df.merge(cursos_parcial, on="curso", how="inner")` e conte as linhas.
b) Faça `df.merge(cursos_parcial, on="curso", how="left")` e conte as linhas.
c) Explique, em uma frase, a diferença entre os dois resultados.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 7 — `apply` com `lambda` (1,0 ponto)

a) Usando `df_completo["situacao"].apply(...)` com uma função `lambda`,
   crie a coluna `aprovado` (booleana: `True` se `situacao == "Aprovado"`).
b) Reescreva o mesmo cálculo **sem** `apply` (de forma vetorizada, em uma
   linha). Confirme que os dois resultados são idênticos.
c) Em uma frase: por que a versão vetorizada é preferível na maioria dos
   casos?

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 8 — `apply(axis=1)` (1,0 ponto)

Escreva uma função `classificar_carga(linha)` que recebe uma linha de
`df_completo` e devolve:

- `"Curso longo"` se `carga_horaria >= 1800`;
- `"Curso médio"` se `1200 <= carga_horaria < 1800`;
- `"Curso curto"` caso contrário.

Aplique com `df_completo.apply(classificar_carga, axis=1)`, salve em uma
coluna `porte_curso` e mostre `value_counts()`.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 9 — Method chaining (1,5 ponto)

Em **uma única cadeia de métodos** (um só `resultado = (...)`, sem
variáveis intermediárias), a partir de `df_completo`:

1. descarte estudantes com `situacao == "Trancado"` (`query`);
2. crie a coluna booleana `aprovado` (`assign`);
3. agrupe por `regiao` e `eixo_tecnologico`;
4. calcule `n` (contagem) e `taxa_aprovacao` (média de `aprovado`) com
   named aggregation;
5. mantenha só grupos com `n >= 10` (`query`);
6. ordene por `taxa_aprovacao` decrescente.

Mostre as 5 primeiras linhas do resultado.

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



## Questão 10 — Uma pergunta respondida com dados (1,0 ponto)

> **Estudantes de cursos com carga horária maior têm nota média mais
> alta?**

a) Use `pd.cut()` para criar uma coluna `carga_faixa` a partir de
   `carga_horaria`, com faixas `[0, 1200]`, `(1200, 1800]` e
   `(1800, 3000]`, rotuladas `"Até 1200h"`, `"1201–1800h"` e
   `"Acima de 1800h"`.
b) Agrupe por `carga_faixa` e calcule a nota média (use
   `observed=True` no `groupby` para evitar aviso).
c) Escreva, em uma célula de texto, o que os números mostram — e **uma
   limitação** dessa conclusão (pense em quais outras variáveis diferem
   entre cursos curtos e longos).

```python
# ESCREVA SEU CÓDIGO AQUI

```

_Sua resposta escrita:_



---

## Entrega

- Arquivo: `aula05_SEUNOME.ipynb`, **executado do início ao fim**.
- Prazo e local: tarefa **"Exercício Prático — Aula 05"** no Moodle.
- Critérios: código correto e legível (60%), uso adequado de `groupby`/
  `agg`/`pivot_table`/`merge` (20%), interpretação escrita dos resultados
  (20%).


