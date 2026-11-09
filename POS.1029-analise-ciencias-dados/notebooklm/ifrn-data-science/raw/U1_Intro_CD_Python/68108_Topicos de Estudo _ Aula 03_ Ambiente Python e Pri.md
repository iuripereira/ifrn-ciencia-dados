# Tópicos de Estudo — Aula 03: Ambiente Python e Pri

Ir para o conteúdo principal

[imagem: Imprimir o livro todo]Imprimir o livro todo

# Tópicos de Estudo — Aula 03: Ambiente Python e Primeiros Passos

   Site:  |   AVA-Presencial  |
   Curso:  |   Análise e Ciência de Dados  |
   Livro:  |   Tópicos de Estudo — Aula 03: Ambiente Python e Primeiros Passos  |

   Impresso por:  |   Iuri Guerra de Freitas Pereira  |
   Data:  |   domingo, 1 nov. 2026, 01:22  |

## Descrição

Conteúdo teórico da Aula 03, em formato de livro: instalação do ambiente Python (Anaconda ou venv), uso do Jupyter Notebook/Lab, estruturas fundamentais de Python (listas, dicionários, funções) e introdução ao NumPy (arrays e operações vetorizadas).

## Índice

- 1. Capítulo 1 — Instalando o Ambiente Python
- 2. Capítulo 2 — Jupyter Notebook e Jupyter Lab
- 3. Capítulo 3 — Listas e Dicionários em Python
- 4. Capítulo 4 — Funções em Python
- 5. Capítulo 5 — Introdução ao NumPy: Arrays e Operações Vetorizadas

## 1. Capítulo 1 — Instalando o Ambiente Python

Antes de programar, é preciso montar o ambiente de trabalho. Existem dois caminhos principais para isso, e vale entender a diferença.

#### Anaconda Distribution

Um pacote completo que já vem com Python, Jupyter, e centenas de bibliotecas científicas pré-instaladas (NumPy, Pandas, Matplotlib, scikit-learn etc.), além do Anaconda Navigator (interface gráfica) e do gerenciador de ambientes conda.

- Vantagem: tudo pronto em uma única instalação, ideal para quem está começando.
- Desvantagem: instalação pesada (vários GB) e pode incluir muito mais do que o necessário para um projeto específico.

#### venv (ambiente virtual nativo do Python)

O módulo `venv`, incluído na instalação padrão do Python, cria um ambiente isolado e leve para cada projeto — você instala apenas as bibliotecas que aquele projeto específico precisa, via `pip`.

```
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

pip install numpy pandas jupyter
```

- Vantagem: leve, isola dependências entre projetos diferentes, evita conflitos de versão.
- Desvantagem: exige instalar cada biblioteca manualmente.

#### Qual escolher?

Para esta disciplina, qualquer um dos dois funciona. Recomendação: se você está começando agora, use Anaconda pela simplicidade; se já tem familiaridade com Python e quer ambientes mais leves e organizados por projeto, use venv. Os exemplos da disciplina funcionam em ambos.

## 2. Capítulo 2 — Jupyter Notebook e Jupyter Lab

O Jupyter é o ambiente de desenvolvimento mais usado em Ciência de Dados. Ele organiza o trabalho em notebooks (arquivos `.ipynb`): documentos interativos que misturam código executável, resultados (tabelas, gráficos) e texto explicativo (Markdown) na mesma tela.

#### Por que notebooks, e não só scripts .py?

- Execução por células: você roda pequenos blocos de código isoladamente, inspeciona o resultado, e ajusta — ideal para explorar dados de forma iterativa.
- Resultados inline: tabelas e gráficos aparecem logo abaixo do código que os gerou, sem precisar abrir arquivos externos.
- Narrativa: células de Markdown permitem documentar o raciocínio junto ao código — essencial para comunicar uma análise (retome o Capítulo 5 da Aula 01, sobre o ciclo CRISP-DM).

#### Jupyter Notebook × Jupyter Lab

Jupyter Notebook é a interface clássica, focada em um notebook por vez. Jupyter Lab é a evolução: um ambiente completo, com múltiplos notebooks, um explorador de arquivos e terminal integrado na mesma janela — recomendado para o dia a dia.

#### Como abrir

```
# Se instalado via Anaconda ou pip:
jupyter lab
# ou, para a interface clássica:
jupyter notebook
```

O comando abre o Jupyter no navegador. Você também pode usar notebooks diretamente dentro do VS Code, com a extensão Jupyter — outra opção comum e usada nesta disciplina.

#### Estrutura básica de um notebook

- Células de código: executadas com `Shift+Enter`; o resultado aparece logo abaixo.
- Células de Markdown: texto formatado (títulos, listas, fórmulas) para documentar o notebook.
- Kernel: o processo Python que executa o código; pode ser reiniciado se o notebook "travar" ou entrar em um estado inconsistente.

## 3. Capítulo 3 — Listas e Dicionários em Python

Duas estruturas de dados cobrem a maior parte das necessidades de um cientista de dados antes mesmo de conhecer o Pandas: listas e dicionários.

#### Listas

Uma lista é uma coleção ordenada e mutável de itens, criada com colchetes:

```
notas = [512.3, 610.7, 645.1, 470.5]
notas.append(598.4)          # adiciona ao final
print(notas[0])              # 512.3 — acesso por índice (começa em 0)
print(notas[-1])             # 598.4 — índice negativo acessa do final
print(len(notas))            # 5 — quantidade de itens
maiores = [n for n in notas if n > 550]   # list comprehension: filtragem
```

List comprehensions (a última linha) são uma forma concisa e "pythônica" de criar listas a partir de outras, substituindo um laço `for` explícito.

#### Dicionários

Um dicionário guarda pares chave-valor, criado com chaves. É a estrutura ideal para representar um registro (como uma linha de uma tabela):

```
escola = {"nome": "Escola A", "tipo": "Estadual", "media": 512.3}
print(escola["nome"])         # "Escola A" — acesso por chave
escola["participantes"] = 180 # adiciona uma nova chave
print(escola.get("uf", "RN")) # acesso seguro, com valor padrão se a chave não existir
```

#### Combinando as duas: lista de dicionários

Uma lista de dicionários é a forma mais natural de representar uma pequena tabela em Python puro — cada dicionário é uma linha (registro), e a lista reúne todas as linhas. É exatamente essa estrutura que usaremos no exemplo prático desta aula, e que será substituída por um `DataFrame` do Pandas a partir da Aula 04.

```
escolas = [
    {"nome": "Escola A", "media": 512.3},
    {"nome": "Escola B", "media": 610.7},
]
for e in escolas:
    print(e["nome"], e["media"])
```

## 4. Capítulo 4 — Funções em Python

Uma função encapsula um bloco de código reutilizável, evitando repetição e organizando o raciocínio em passos nomeados — essencial à medida que os scripts de análise crescem.

#### Definindo uma função

```
def media_geral(lista_escolas):
    """Calcula a média das médias das escolas."""
    total = 0
    for escola in lista_escolas:
        total += escola["media"]
    return total / len(lista_escolas)

resultado = media_geral(escolas)   # chamando a função
```

- def inicia a definição; o nome deve descrever o que a função faz.
- Parâmetros (aqui, `lista_escolas`) são as entradas da função.
- Docstring (texto entre `"""`) documenta o propósito — boa prática sempre.
- return devolve o resultado; sem ele, a função retorna `None`.

#### Por que usar funções em análise de dados?

- Reuso: a mesma lógica de cálculo pode ser aplicada a diferentes conjuntos de dados sem copiar e colar código.
- Testabilidade: é mais fácil verificar se uma função pequena está correta do que validar um script inteiro de uma vez.
- Legibilidade: nomes de função bem escolhidos (`filtrar_por_tipo`, `escola_com_maior_media`) tornam o código autoexplicativo.

#### Funções com múltiplos parâmetros e valores padrão

```
def filtrar_por_tipo(lista_escolas, tipo="Estadual"):
    return [e for e in lista_escolas if e["tipo"] == tipo]

filtrar_por_tipo(escolas)              # usa o padrão "Estadual"
filtrar_por_tipo(escolas, "Privada")   # sobrescreve o padrão
```

No exemplo prático desta aula, você verá três funções trabalhando juntas sobre a mesma lista de dicionários: uma calcula uma média, outra filtra registros, e outra encontra um extremo — o mesmo tipo de composição que reaparecerá, com Pandas, a partir da Aula 04.

## 5. Capítulo 5 — Introdução ao NumPy: Arrays e Operações Vetorizadas

O NumPy (Numerical Python) é a base de praticamente todo o ecossistema científico em Python — Pandas, Matplotlib e scikit-learn são construídos sobre ele. Sua estrutura central é o array.

#### Array x lista: qual a diferença?

Um array do NumPy parece uma lista, mas é fundamentalmente diferente: armazena elementos do mesmo tipo em um bloco contíguo de memória, o que permite operações matemáticas muito mais rápidas e diretas.

```
import numpy as np

medias = np.array([512.3, 610.7, 645.1, 470.5])
print(medias.mean())    # 559.65 — média, sem escrever um loop
print(medias.std())     # desvio padrão
print(medias.max())     # valor máximo
print(medias * 1.1)     # multiplica CADA elemento por 1.1, de uma vez
```

#### Operações vetorizadas

Isso é vetorização: aplicar uma operação a todos os elementos de um array simultaneamente, sem escrever um laço `for` explícito. O código fica mais curto, mais legível e — como veremos no exemplo prático — muito mais rápido.

```
# Sem NumPy (Python puro): precisa de um loop
resultado = []
for nota in medias_lista:
    resultado.append(nota * 1.1)

# Com NumPy: a operação já é vetorizada
resultado = medias_array * 1.1
```

#### Indexação booleana

Um dos recursos mais úteis do NumPy é filtrar dados usando condições diretamente sobre o array:

```
acima_da_media = medias > medias.mean()   # array de True/False
print(medias[acima_da_media])              # só os valores que satisfazem a condição
```

#### O que vem a seguir

NumPy trabalha bem com números, mas dados reais também têm texto, datas e valores ausentes — é para isso que existe o Pandas, construído sobre o NumPy, que você conhecerá a partir da Aula 04. Por ora, o objetivo é entender por que a vetorização importa — o exemplo prático desta aula compara diretamente o tempo de um cálculo feito em loop puro contra o mesmo cálculo vetorizado.