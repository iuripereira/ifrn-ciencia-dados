# Aula 03 — Ambiente Python e Primeiros Passos (Teórico-Prática)

> Semana de 31/08/2026. Instalação de Anaconda/venv; Jupyter Notebook/Lab; estruturas Python (listas, dicionários, funções); introdução ao NumPy (arrays, operações vetorizadas).
> Materiais: livro da aula, tutorial "Estudo Orientado Python + NumPy + Pandas" (PDF — transcrito em `tutorial-python-numpy-pandas.md`), exemplo prático guiado e formulário avaliativo.

---

# Livro — Tópicos de Estudo

## Capítulo 1 — Instalando o Ambiente Python

Antes de programar, é preciso montar o ambiente de trabalho. Existem dois caminhos principais.

### Anaconda Distribution

Pacote completo que já vem com Python, Jupyter e centenas de bibliotecas científicas pré-instaladas (NumPy, Pandas, Matplotlib, scikit-learn etc.), além do Anaconda Navigator (interface gráfica) e do gerenciador de ambientes `conda`.

- **Vantagem:** tudo pronto em uma única instalação, ideal para quem está começando.
- **Desvantagem:** instalação pesada (vários GB) e pode incluir muito mais do que o necessário.

### venv (ambiente virtual nativo do Python)

O módulo `venv`, incluído na instalação padrão do Python, cria um ambiente isolado e leve para cada projeto — você instala apenas as bibliotecas que aquele projeto precisa, via `pip`.

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

pip install numpy pandas jupyter
```

- **Vantagem:** leve, isola dependências entre projetos, evita conflitos de versão.
- **Desvantagem:** exige instalar cada biblioteca manualmente.

### Qual escolher?

Qualquer um funciona. Se está começando, Anaconda pela simplicidade; se já tem familiaridade e quer ambientes leves por projeto, venv. Os exemplos da disciplina funcionam em ambos.

## Capítulo 2 — Jupyter Notebook e Jupyter Lab

O Jupyter organiza o trabalho em **notebooks** (`.ipynb`): documentos interativos que misturam código executável, resultados (tabelas, gráficos) e texto explicativo (Markdown).

### Por que notebooks, e não só scripts .py?

- **Execução por células:** rode pequenos blocos isoladamente, inspecione o resultado, ajuste — ideal para explorar dados de forma iterativa.
- **Resultados inline:** tabelas e gráficos aparecem logo abaixo do código.
- **Narrativa:** células de Markdown documentam o raciocínio junto ao código (retome o CRISP-DM da Aula 01).

### Jupyter Notebook × Jupyter Lab

**Notebook** é a interface clássica, um notebook por vez. **Lab** é a evolução: múltiplos notebooks, explorador de arquivos e terminal integrados — recomendado para o dia a dia.

```bash
jupyter lab        # ou
jupyter notebook   # interface clássica
```

Também é possível usar notebooks no VS Code com a extensão Jupyter.

### Estrutura básica

- **Células de código:** executadas com `Shift+Enter`.
- **Células de Markdown:** texto formatado.
- **Kernel:** o processo Python que executa o código; pode ser reiniciado se o notebook ficar inconsistente.

## Capítulo 3 — Listas e Dicionários em Python

### Listas

Coleção ordenada e mutável, criada com colchetes:

```python
notas = [512.3, 610.7, 645.1, 470.5]
notas.append(598.4)        # adiciona ao final
print(notas[0])            # 512.3 — índice começa em 0
print(notas[-1])           # 598.4 — índice negativo acessa do final
print(len(notas))          # 5
maiores = [n for n in notas if n > 550]   # list comprehension: filtragem
```

### Dicionários

Pares chave-valor, criados com chaves — ideal para representar um registro:

```python
escola = {"nome": "Escola A", "tipo": "Estadual", "media": 512.3}
print(escola["nome"])             # "Escola A"
escola["participantes"] = 180     # nova chave
print(escola.get("uf", "RN"))     # acesso seguro com valor padrão
```

### Combinando: lista de dicionários

Forma mais natural de representar uma pequena tabela em Python puro — cada dicionário é uma linha. É a estrutura do exemplo prático, substituída por DataFrame a partir da Aula 04.

```python
escolas = [
    {"nome": "Escola A", "media": 512.3},
    {"nome": "Escola B", "media": 610.7},
]
for e in escolas:
    print(e["nome"], e["media"])
```

## Capítulo 4 — Funções em Python

```python
def media_geral(lista_escolas):
    """Calcula a média das médias das escolas."""
    total = 0
    for escola in lista_escolas:
        total += escola["media"]
    return total / len(lista_escolas)

resultado = media_geral(escolas)
```

- `def` inicia a definição; o nome deve descrever o que a função faz.
- **Parâmetros** são as entradas.
- **Docstring** documenta o propósito.
- `return` devolve o resultado; sem ele, a função retorna `None`.

### Por que usar funções em análise de dados?

- **Reuso** sem copiar e colar.
- **Testabilidade:** é mais fácil verificar uma função pequena do que um script inteiro.
- **Legibilidade:** nomes bem escolhidos (`filtrar_por_tipo`, `escola_com_maior_media`) tornam o código autoexplicativo.

### Parâmetros com valor padrão

```python
def filtrar_por_tipo(lista_escolas, tipo="Estadual"):
    return [e for e in lista_escolas if e["tipo"] == tipo]

filtrar_por_tipo(escolas)             # usa o padrão "Estadual"
filtrar_por_tipo(escolas, "Privada")  # sobrescreve o padrão
```

## Capítulo 5 — Introdução ao NumPy: Arrays e Operações Vetorizadas

O NumPy é a base do ecossistema científico em Python — Pandas, Matplotlib e scikit-learn são construídos sobre ele.

### Array × lista

Um array armazena elementos **do mesmo tipo** em um bloco contíguo de memória, permitindo operações matemáticas muito mais rápidas.

```python
import numpy as np

medias = np.array([512.3, 610.7, 645.1, 470.5])
print(medias.mean())   # 559.65
print(medias.std())    # desvio padrão
print(medias.max())    # valor máximo
print(medias * 1.1)    # multiplica CADA elemento, de uma vez
```

### Operações vetorizadas

Aplicar uma operação a todos os elementos sem laço explícito:

```python
# Python puro: loop
resultado = []
for nota in medias_lista:
    resultado.append(nota * 1.1)

# NumPy: vetorizado
resultado = medias_array * 1.1
```

### Indexação booleana

```python
acima_da_media = medias > medias.mean()   # array de True/False
print(medias[acima_da_media])
```

### O que vem a seguir

Dados reais também têm texto, datas e ausentes — é para isso que existe o Pandas (Aula 04). O exemplo prático compara o tempo de um cálculo em loop puro contra o vetorizado.

---

# Exemplo Prático — Primeiros Passos com Python e NumPy (`primeiros_passos.py`)

Aplica os quatro tópicos do livro: lista de dicionários representando escolas, três funções sobre ela, a mesma análise com arrays NumPy, e comparação de desempenho.

## Como executar

1. Python 3.10+ e NumPy (`pip install numpy`, ou Anaconda);
2. Salve como `primeiros_passos.py` — não depende de arquivo externo;
3. `python primeiros_passos.py` ou célula por célula no Jupyter.

## O que observar

- **Parte 1 (Python puro):** 8 dicionários e três funções — `media_geral`, `filtrar_por_tipo`, `escola_com_maior_media` — cada uma com uma responsabilidade.
- **Parte 2 (NumPy):** `medias.mean()`, indexação booleana e média ponderada substituem várias linhas de loop.
- **Parte 3 (desempenho):** soma de 1 milhão de números com loop × `array.sum()`, cronometrada com `time.perf_counter()`.

## Resultado obtido (ambiente de testes)

```
=== Parte 1: Python puro (listas, dicionários, funções) ===
Média geral (Python puro): 559.0
Escolas estaduais: ['Escola A', 'Escola E', 'Escola H']
Escola com maior média: Escola C (645.1)

=== Parte 2: NumPy (arrays e operações vetorizadas) ===
Array de médias: [512.3 610.7 645.1 470.5 498.9 630.2 598.4 505.6]
Média geral (NumPy): 559.0
Desvio padrão: 64.4
Maior média: 645.1 | Menor média: 470.5
Média ponderada pelo nº de participantes: 544.6
Escolas acima da média geral: ['Escola B', 'Escola C', 'Escola F', 'Escola G']

=== Parte 3: Por que usar NumPy?
Soma de 1.000.000 de valores via loop Python puro: 44.3 ms
Soma de 1.000.000 de valores via NumPy (vetorizada): 0.14 ms
NumPy foi aproximadamente 315x mais rápido
```

## Para discutir em aula

1. Por que a média geral (559,0) é diferente da média ponderada (544,6)? O que isso revela sobre escolas com poucos participantes puxarem a média simples para cima?
2. Reescreva `escola_com_maior_media` usando `max(escolas, key=lambda e: e["media"])`.
3. O ganho de ~300x só aparece em operações grandes. Por que, para 8 escolas, a diferença seria imperceptível?

## `primeiros_passos.py`

```python
import time
import numpy as np

escolas = [
    {"nome": "Escola A", "tipo": "Estadual", "media": 512.3, "participantes": 180},
    {"nome": "Escola B", "tipo": "Federal", "media": 610.7, "participantes": 95},
    {"nome": "Escola C", "tipo": "Privada", "media": 645.1, "participantes": 60},
    {"nome": "Escola D", "tipo": "Municipal", "media": 470.5, "participantes": 40},
    {"nome": "Escola E", "tipo": "Estadual", "media": 498.9, "participantes": 220},
    {"nome": "Escola F", "tipo": "Privada", "media": 630.2, "participantes": 75},
    {"nome": "Escola G", "tipo": "Federal", "media": 598.4, "participantes": 110},
    {"nome": "Escola H", "tipo": "Estadual", "media": 505.6, "participantes": 150},
]

def media_geral(lista_escolas):
    total = 0
    for escola in lista_escolas:
        total += escola["media"]
    return total / len(lista_escolas)

def filtrar_por_tipo(lista_escolas, tipo):
    return [e for e in lista_escolas if e["tipo"] == tipo]

def escola_com_maior_media(lista_escolas):
    maior = lista_escolas[0]
    for escola in lista_escolas[1:]:
        if escola["media"] > maior["media"]:
            maior = escola
    return maior

def parte1_python_puro():
    print("=== Parte 1: Python puro (listas, dicionários, funções) ===")
    print(f"Média geral (Python puro): {media_geral(escolas):.1f}")
    estaduais = filtrar_por_tipo(escolas, "Estadual")
    print(f"Escolas estaduais: {[e['nome'] for e in estaduais]}")
    melhor = escola_com_maior_media(escolas)
    print(f"Escola com maior média: {melhor['nome']} ({melhor['media']})")

def parte2_numpy():
    print("\n=== Parte 2: NumPy (arrays e operações vetorizadas) ===")
    medias = np.array([e["media"] for e in escolas])
    participantes = np.array([e["participantes"] for e in escolas])
    nomes = np.array([e["nome"] for e in escolas])

    print(f"Array de médias: {medias}")
    print(f"Média geral (NumPy): {medias.mean():.1f}")
    print(f"Desvio padrão: {medias.std():.1f}")
    print(f"Maior média: {medias.max():.1f} | Menor média: {medias.min():.1f}")

    peso = participantes / participantes.sum()
    media_ponderada = (medias * peso).sum()
    print(f"Média ponderada pelo nº de participantes: {media_ponderada:.1f}")

    acima_da_media = medias > medias.mean()
    print(f"Escolas acima da média geral: {nomes[acima_da_media].tolist()}")

def parte3_desempenho():
    print("\n=== Parte 3: Por que usar NumPy? ===")
    grande = np.random.default_rng(42).normal(500, 80, 1_000_000)

    inicio = time.perf_counter()
    soma_loop = 0.0
    for valor in grande:
        soma_loop += valor
    tempo_loop = time.perf_counter() - inicio

    inicio = time.perf_counter()
    soma_vetorizada = grande.sum()
    tempo_vetorizado = time.perf_counter() - inicio

    print(f"Soma de 1.000.000 de valores via loop Python puro: {tempo_loop*1000:.1f} ms")
    print(f"Soma de 1.000.000 de valores via NumPy (vetorizada): {tempo_vetorizado*1000:.2f} ms")
    print(f"NumPy foi aproximadamente {tempo_loop/tempo_vetorizado:.0f}x mais rápido")

def main():
    parte1_python_puro()
    parte2_numpy()
    parte3_desempenho()

if __name__ == "__main__":
    main()
```

---

# Formulário Avaliativo — Aula 03

Questionário sobre ambiente Python, estruturas de dados, funções e NumPy. Compõe as atividades semanais da Unidade 1.
