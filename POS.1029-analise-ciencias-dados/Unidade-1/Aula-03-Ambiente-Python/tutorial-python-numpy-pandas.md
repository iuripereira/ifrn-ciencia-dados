# Tutorial de Aula — Python Fundamental + NumPy + Pandas

> Transcrição do PDF "Tutorial - Estudo Orientado Python + Numpy + Pandas" (AVA, Aula 03, 15 p.). Indentação dos códigos reconstruída.

## Objetivos de aprendizagem

Ao final, o aluno será capaz de:

- Criar, acessar e manipular listas em Python.
- Criar e operar dicionários para armazenar dados estruturados.
- Definir e chamar funções com parâmetros, retorno e valores padrão.
- Importar e utilizar a biblioteca NumPy para operações com arrays.
- Criar e manipular DataFrames com Pandas para análise de dados tabulares.
- Aplicar esses conceitos em exemplos práticos do cotidiano.

---

## Módulo 1 — Listas

Uma lista armazena uma sequência **ordenada** de elementos de qualquer tipo — números, textos, booleanos ou outras listas.

### 1.1 Criando e acessando

```python
frutas = ["maçã", "banana", "laranja", "uva"]
numeros = [10, 25, 37, 42, 58]
mista = [1, "Python", True, 3.14]

print(frutas[0])      # maçã   (índice inicia em 0)
print(frutas[1:3])    # ["banana", "laranja"]   [início : fim : passo]
print(numeros[::2])   # [10, 37, 58]
```

💡 Índice negativo: `lista[-1]` retorna o último elemento; `lista[-2]` o penúltimo.

### 1.2 Principais métodos

```python
lista = [3, 1, 4, 1, 5, 9]
lista.append(2)     # adiciona 2 ao final
lista.insert(0, 0)  # insere 0 na posição 0
lista.remove(1)     # remove a primeira ocorrência do valor 1
lista.pop()         # remove e retorna o último elemento
lista.pop(2)        # remove e retorna o índice 2
lista.sort()        # ordena in-place (menor → maior)
lista.reverse()     # inverte a ordem in-place
lista.index(5)      # retorna o índice de 5
lista.count(1)      # conta quantas vezes 1 aparece
len(lista)          # comprimento da lista
```

### 1.3 Iterando

```python
for fruta in frutas:
    print(fruta)

for i, fruta in enumerate(frutas):     # índice + valor
    print(f"{i}: {fruta}")

quadrados = [x**2 for x in range(1, 6)]            # [1, 4, 9, 16, 25]
pares = [x for x in range(10) if x % 2 == 0]       # [0, 2, 4, 6, 8]
```

### 1.4 Exemplo prático — Gerenciador de notas

```python
notas = []
for i in range(5):
    nota = float(input(f"Digite a nota do aluno {i+1}: "))
    notas.append(nota)

media = sum(notas) / len(notas)
maior = max(notas)
menor = min(notas)
aprovados = [n for n in notas if n >= 6.0]

print(f"Notas: {notas}")
print(f"Média: {media:.2f}")
print(f"Maior nota: {maior}")
print(f"Menor nota: {menor}")
print(f"Aprovados: {len(aprovados)} de {len(notas)}")
```

---

## Módulo 2 — Dicionários

Pares **chave → valor**. Chaves únicas e imutáveis (str, int, tuple); valores de qualquer tipo.

### 2.1 Criando e acessando

```python
aluno = {
    "nome": "Ana Paula",
    "idade": 21,
    "curso": "Ciência da Computação",
    "notas": [8.5, 9.0, 7.5],
}
print(aluno["nome"])               # Ana Paula
print(aluno.get("idade"))          # 21
print(aluno.get("email", "—"))     # — (padrão se ausente)

aluno["email"] = "ana@uni.br"      # adicionar
aluno["idade"] = 22                # atualizar
del aluno["email"]                 # remover
matricula = aluno.pop("matricula", None)   # remoção segura
```

### 2.2 Métodos essenciais

```python
pessoa = {"nome": "Carlos", "cidade": "Fortaleza", "idade": 30}
pessoa.keys()      # dict_keys(["nome", "cidade", "idade"])
pessoa.values()    # dict_values(["Carlos", "Fortaleza", 30])
pessoa.items()     # dict_items([("nome", "Carlos"), ...])

"nome" in pessoa   # True
"email" in pessoa  # False

extra = {"email": "carlos@mail.com"}
completo = pessoa | extra          # mesclar
```

### 2.3 Iterando

```python
for chave, valor in aluno.items():
    print(f"{chave}: {valor}")

quadrados = {x: x**2 for x in range(1, 6)}             # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
maiores = {k: v for k, v in quadrados.items() if v > 9}  # {4: 16, 5: 25}
```

### 2.4 Exemplo prático — Catálogo de produtos

```python
catalogo = {
    "notebook": {"preco": 3200.00, "estoque": 15},
    "mouse":    {"preco": 89.90,   "estoque": 40},
    "teclado":  {"preco": 150.00,  "estoque": 8},
}

def exibir_catalogo(cat):
    print(f"{'Produto':<12} {'Preço':>10} {'Estoque':>9}")
    print("-" * 34)
    for produto, info in cat.items():
        print(f"{produto:<12} R${info['preco']:>8.2f} {info['estoque']:>9}")

exibir_catalogo(catalogo)

total = sum(i["preco"] * i["estoque"] for i in catalogo.values())
print(f"\nValor total em estoque: R$ {total:,.2f}")
```

> No PDF as f-strings usam aspas duplas aninhadas (`f"{"Produto":<12}"`), válido só no Python 3.12+. Aqui foram trocadas por aspas simples para rodar em qualquer versão.

---

## Módulo 3 — Funções

```python
def saudacao(nome):
    """Exibe uma mensagem de boas-vindas."""
    print(f"Olá, {nome}! Bem-vindo ao Python.")

saudacao("Maria")
```

💡 **Docstring:** documente funções com string entre aspas triplas logo após o `def` — alimenta o `help()`.

### 3.1 Parâmetros e retorno

```python
def potencia(base, expoente=2):
    return base ** expoente

print(potencia(3))       # 9
print(potencia(2, 10))   # 1024

def estatisticas(nums):
    return min(nums), max(nums), sum(nums) / len(nums)   # retorno múltiplo (tupla)

mi, ma, med = estatisticas([4, 7, 2, 9, 1])
print(f"Min={mi} Max={ma} Média={med}")
```

### 3.2 `*args` e `**kwargs`

```python
def somar(*numeros):
    return sum(numeros)

print(somar(1, 2, 3))          # 6
print(somar(10, 20, 30, 40))   # 100

def apresentar(**dados):
    for chave, valor in dados.items():
        print(f" {chave}: {valor}")

apresentar(nome="Lucas", cidade="Recife", profissao="Dev")
```

### 3.3 Funções de alta ordem e lambda

```python
alunos = [("Ana", 8.5), ("Bruno", 7.0), ("Carla", 9.2)]
ranking = sorted(alunos, key=lambda a: a[1], reverse=True)
# [("Carla", 9.2), ("Ana", 8.5), ("Bruno", 7.0)]

notas = [6.0, 7.5, 8.0, 5.5]
arredondadas = list(map(lambda n: round(n), notas))
aprovados = list(filter(lambda n: n >= 6, notas))
```

### 3.4 Exemplo prático — Calculadora de IMC

```python
def calcular_imc(peso, altura):
    """Calcula o Índice de Massa Corporal."""
    return peso / altura ** 2

def classificar_imc(imc):
    """Retorna a classificação do IMC."""
    if imc < 18.5:
        return "Abaixo do peso"
    elif imc < 25.0:
        return "Peso normal"
    elif imc < 30.0:
        return "Sobrepeso"
    else:
        return "Obesidade"

def relatorio_imc(nome, peso, altura):
    """Gera relatório completo de IMC."""
    imc = calcular_imc(peso, altura)
    classe = classificar_imc(imc)
    print(f"Paciente : {nome}")
    print(f"IMC      : {imc:.2f}")
    print(f"Situação : {classe}")

relatorio_imc("João Silva", 82, 1.75)
```

---

## Módulo 4 — NumPy

NumPy fornece o `ndarray` — array multidimensional eficiente — e funções matemáticas de alto desempenho.

### 4.1 Instalação e importação

```python
# pip install numpy
import numpy as np
print(np.__version__)
```

### 4.2 Criando arrays

```python
v = np.array([1, 2, 3, 4, 5])            # 1-D
M = np.array([[1, 2, 3], [4, 5, 6]])     # 2-D

zeros = np.zeros((3, 4))
uns = np.ones((2, 3))
ident = np.eye(3)
range_ = np.arange(0, 10, 2)     # [0 2 4 6 8]
linsp = np.linspace(0, 1, 5)     # [0.00 0.25 0.50 0.75 1.00]
aleats = np.random.rand(3, 3)    # valores em [0, 1)

print(M.shape)   # (2, 3)
print(M.ndim)    # 2
print(M.dtype)   # int64
print(M.size)    # 6
```

### 4.3 Indexação e fatiamento

```python
A = np.array([[10, 20, 30],
              [40, 50, 60],
              [70, 80, 90]])
print(A[0, 0])     # 10
print(A[2, 1])     # 80
print(A[1, :])     # [40 50 60]
print(A[:, 2])     # [30 60 90]
print(A[:2, 1:])   # [[20 30] [50 60]]

print(A[A > 50])   # [60 70 80 90]   indexação booleana
A[A < 30] = 0      # zera elementos menores que 30
```

### 4.4 Operações matemáticas (broadcasting)

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(a + b)       # [5 7 9]
print(a * b)       # [4 10 18]
print(a ** 2)      # [1 4 9]
print(a + 10)      # [11 12 13]

print(np.sqrt(a))  # [1. 1.41 1.73]
print(np.exp(a))   # [2.72 7.39 20.09]
print(np.log(b))   # [1.39 1.61 1.79]

M1 = np.array([[1, 2], [3, 4]])
M2 = np.array([[5, 6], [7, 8]])
print(M1 @ M2)     # [[19 22] [43 50]]
```

### 4.5 Estatísticas e agregações

```python
dados = np.array([23, 45, 12, 67, 34, 89, 56, 11, 78, 43])
print("Média  :", np.mean(dados))     # 45.8
print("Mediana:", np.median(dados))   # 44.0
print("Desvio :", np.std(dados))      # 25.85
print("Mínimo :", np.min(dados))      # 11
print("Máximo :", np.max(dados))      # 89
print("Soma   :", np.sum(dados))      # 458

M = np.array([[1, 2, 3], [4, 5, 6]])
print(np.sum(M, axis=0))   # [5 7 9]  por coluna
print(np.sum(M, axis=1))   # [6 15]   por linha
```

### 4.6 Reshape e transformações

```python
v = np.arange(1, 13)
M = v.reshape(3, 4)
M2 = v.reshape(2, 2, 3)
print(M.T.shape)           # (4, 3)
print(M.flatten())         # [ 1 2 3 ... 12]

a = np.ones((2, 3))
b = np.zeros((2, 3))
print(np.vstack([a, b]).shape)   # (4, 3)
print(np.hstack([a, b]).shape)   # (2, 6)
```

### 4.7 Exemplo prático — Análise de vendas mensais

```python
import numpy as np

# Linhas: produtos (Notebook, Mouse, Teclado) | Colunas: meses (Jan a Jun)
vendas = np.array([
    [120, 135, 148, 162, 175, 190],
    [340, 298, 312, 400, 390, 420],
    [ 88,  95, 102, 115,  97, 108],
])
produtos = ["Notebook", "Mouse", "Teclado"]
meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]

total_produto = vendas.sum(axis=1)
for prod, total in zip(produtos, total_produto):
    print(f"{prod:<10}: {total} unidades")

media_mes = vendas.mean(axis=0)
for mes, med in zip(meses, media_mes):
    print(f"{mes}: {med:.1f} unidades/produto")

total_mes = vendas.sum(axis=0)
melhor_mes = meses[np.argmax(total_mes)]
print(f"\nMelhor mês: {melhor_mes} ({total_mes.max()} unidades)")

crescimento = (vendas[:, -1] - vendas[:, 0]) / vendas[:, 0] * 100
for prod, cresc in zip(produtos, crescimento):
    print(f"{prod:<10}: {cresc:+.1f}%")
```

---

## Módulo 5 — Pandas

Duas estruturas centrais: **Series** (array 1-D rotulado) e **DataFrame** (tabela 2-D com linhas e colunas nomeadas), construídas sobre o NumPy.

### 5.1 Importação

```python
# pip install pandas
import pandas as pd
import numpy as np
print(pd.__version__)
```

### 5.2 Series

```python
notas = pd.Series([8.5, 7.0, 9.2, 6.3], index=["Ana", "Bruno", "Carla", "Diego"])
print(notas["Ana"])          # 8.5
print(notas.iloc[2])         # 9.2
print(notas * 10)
print(notas[notas >= 7.0])
print(notas.mean())
print(notas.describe())
```

💡 O índice pode ser texto, datas ou qualquer tipo imutável — facilita buscas e joins.

### 5.3 DataFrame

```python
dados = {
    "nome":     ["Ana", "Bruno", "Carla", "Diego"],
    "idade":    [22, 25, 21, 28],
    "nota":     [8.5, 7.0, 9.2, 6.3],
    "aprovado": [True, True, True, False],
}
df = pd.DataFrame(dados)

print(df)
print(df.head(2))
print(df.tail(2))
print(df.shape)    # (4, 4)
print(df.dtypes)
df.info()
```

### 5.4 Seleção e filtragem

```python
print(df["nome"])                        # Series
print(df[["nome", "nota"]])              # DataFrame
print(df.loc[0, "nome"])                 # "Ana"
print(df.loc[1:2, ["nome", "nota"]])     # linhas 1-2 (rótulo, fim incluído)
print(df.iloc[0, 0])                     # "Ana"
print(df.iloc[:2, :3])                   # posição (fim excluído)

aprovados = df[df["aprovado"] == True]
acima8 = df[df["nota"] >= 8.0]
jovens_ap = df[(df["idade"] < 25) & (df["aprovado"])]
```

### 5.5 Operações e transformações

```python
df["nota_ponderada"] = df["nota"] * 1.1
df["conceito"] = df["nota"].apply(lambda n: "A" if n >= 9 else ("B" if n >= 7 else "C"))
df.rename(columns={"nota": "media"}, inplace=True)
df_ord = df.sort_values("media", ascending=False)
resumo = df.groupby("aprovado")["media"].agg(["mean", "min", "max"])
print(resumo)
print(df.describe())
```

### 5.6 Leitura e escrita

```python
df = pd.read_csv("dados.csv", sep=",", encoding="utf-8")
df = pd.read_excel("planilha.xlsx", sheet_name="Plan1")
df.to_csv("saida.csv", index=False)
df.to_excel("saida.xlsx", index=False)

print(df.shape)
print(df.head())
print(df.isnull().sum())
```

### 5.7 Dados ausentes

```python
df2 = pd.DataFrame({"x": [1, None, 3, None, 5], "y": [10, 20, None, 40, 50]})
print(df2.isnull())
print(df2.isnull().sum())
df_limpo = df2.dropna()
df_fill = df2.fillna(0)
df_fill2 = df2.fillna(df2.mean())
```

### 5.8 Exemplo prático — Desempenho de turma

```python
import pandas as pd

df = pd.DataFrame({
    "aluno": ["Ana", "Bruno", "Carla", "Diego", "Elena"],
    "b1":    [8.0, 6.5, 9.5, 5.0, 7.0],
    "b2":    [7.5, 7.0, 8.5, 6.0, 8.0],
    "b3":    [9.0, 5.5, 9.0, 4.5, 8.5],
})

df["media"] = df[["b1", "b2", "b3"]].mean(axis=1).round(2)

def conceito(m):
    if m >= 9.0: return "A"
    if m >= 7.0: return "B"
    if m >= 6.0: return "C"
    return "D (Reprovado)"

df["conceito"] = df["media"].apply(conceito)

print(df[["aluno", "media", "conceito"]].to_string(index=False))
print()
print(f"Média da turma : {df['media'].mean():.2f}")
print(f"Aprovados      : {(df['media'] >= 6).sum()} / {len(df)}")
print(f"Melhor aluno   : {df.loc[df['media'].idxmax(), 'aluno']}")

df.to_csv("relatorio_turma.csv", index=False)
```

---

## Referências

- Documentação oficial Python: https://docs.python.org/3/
- NumPy User Guide: https://numpy.org/doc/stable/user/
- Python Tutor: https://pythontutor.com
- *Python Crash Course* — Eric Matthes (No Starch Press)
- *Python para Análise de Dados* — Wes McKinney (O'Reilly)
- Documentação Pandas: https://pandas.pydata.org/docs/
- 10 Minutes to Pandas: https://pandas.pydata.org/docs/user_guide/10min.html
