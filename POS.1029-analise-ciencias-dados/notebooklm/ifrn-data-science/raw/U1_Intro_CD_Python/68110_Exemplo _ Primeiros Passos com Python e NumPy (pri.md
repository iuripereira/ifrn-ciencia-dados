# Exemplo — Primeiros Passos com Python e NumPy (pri

### Exemplo Prático — Primeiros Passos com Python e NumPy

Este exemplo aplica, na prática, os quatro tópicos do livro da aula: uma pequena lista de dicionários representando escolas, três funções que operam sobre ela, a mesma análise refeita com arrays NumPy, e uma comparação de desempenho entre as duas abordagens.

#### Como executar

- Certifique-se de ter Python 3.10+ e NumPy instalados (`pip install numpy`, ou já incluído se você usa Anaconda);
- Salve o script como `primeiros_passos.py` — não depende de nenhum arquivo externo;
- Execute com `python primeiros_passos.py` ou rode célula por célula em um notebook Jupyter.

#### O que observar em cada parte

- Parte 1 (Python puro): uma lista de 8 dicionários (as "linhas" da nossa mini-tabela) e três funções — `media_geral`, `filtrar_por_tipo` e `escola_com_maior_media` — cada uma isolando uma responsabilidade específica.
- Parte 2 (NumPy): os mesmos dados convertidos em arrays. Note como `medias.mean()`, a indexação booleana (`medias > medias.mean()`) e a média ponderada substituem várias linhas de loop por poucas linhas vetorizadas.
- Parte 3 (desempenho): a mesma soma de 1 milhão de números calculada com um loop Python puro e com `array.sum()` do NumPy — cronometradas com `time.perf_counter()`.

#### Resultado obtido (ambiente de testes)

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

#### Para discutir em aula

- Por que a média geral (559,0) é diferente da média ponderada (544,6)? O que isso revela sobre escolas com poucos participantes puxarem a média simples para cima?
- Reescreva `escola_com_maior_media` usando `max(escolas, key=lambda e: e["media"])` — uma alternativa mais "pythônica" ao loop manual.
- O ganho de ~300x com NumPy só aparece em operações grandes (1 milhão de números). Por que, para os dados de apenas 8 escolas, a diferença de tempo seria imperceptível?

#### primeiros_passos.py

```
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

Última atualização: sexta-feira, 7 ago. 2026, 18:03