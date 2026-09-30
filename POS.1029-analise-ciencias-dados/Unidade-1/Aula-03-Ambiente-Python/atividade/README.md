# Atividade — Aula 03

## O que é avaliado

| # | Item | Tipo | Onde |
|---|---|---|---|
| 1 | Formulário Avaliativo — Aula 03 (ambiente, listas, dicionários, funções, NumPy) | **Nota** | AVA |
| 2 | Exemplo guiado `primeiros_passos.py` + 3 perguntas de discussão | Prática (sem entrega) | `aula03_primeiros_passos_colab.ipynb` |

Sem arquivos externos: o notebook roda direto no Colab (~15 min).

## Passo a passo

1. Abra `aula03_primeiros_passos_colab.ipynb` no Colab.
2. Rode as Partes 1, 2 e 3; compare com o "Resultado obtido" em `../conteudo.md` (tempos da Parte 3 variam por máquina — o que importa é a ordem de grandeza).
3. Resolva as 3 células de discussão (reescrever com `max(..., key=lambda ...)`, explicar média simples × ponderada, explicar por que o ganho some com 8 itens).
4. Opcional: rode a célula `%timeit` para medir com mais rigor.

## Nota sobre o ambiente (Cap. 1 e 2 do livro)

O Colab já é um Jupyter hospedado com NumPy/Pandas instalados — dispensa Anaconda/venv. Para o formulário, saiba mesmo assim:

| Tema | Resposta curta |
|---|---|
| Anaconda × venv | Anaconda = tudo pronto, pesado; venv = leve, isolado por projeto, instala via pip |
| Ativar venv | `source .venv/bin/activate` (Linux/macOS) · `.venv\Scripts\activate` (Windows) |
| Notebook × Lab | Lab = múltiplos notebooks + arquivos + terminal |
| Kernel | processo Python que executa as células; reiniciar limpa o estado |
