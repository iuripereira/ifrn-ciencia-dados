# Aula 12 — Laboratório: Matplotlib, Seaborn e Plotly

Especialização em Ciência de Dados · Análise e Ciência de Dados · IFRN
Unidade 3 — Análise Exploratória de Dados e Visualização (segunda aula)

## Conteúdo do pacote

| Arquivo | O que é |
|---|---|
| `Aula12_Visualizacao_Laboratorio.ipynb` | **Exemplo guiado** (delivery da hamburgueria fictícia *Brasa & Pão*, 600 pedidos), já executado, com todas as saídas e gráficos |
| `Aula12_Exercicio_Pratico.ipynb` | **Exercício prático** (240 usuários de um app de música fictício): 9 passos com o resultado esperado em cada um — treino, **não precisa ser entregue** |
| `Aula12_Exercicio_Gabarito.ipynb` | Gabarito comentado do exercício (tente antes de abrir!) |
| `dados/delivery_hamburgueria.csv` | dados do exemplo guiado |
| `dados/app_musica_usuarios.csv` | dados do exercício |
| `gerar_dados.py` | script que gera os dois CSVs (semente fixa) |
| `figuras/` | PNGs exportados pelo exemplo guiado (`savefig`) |
| `graficos/` | gráficos interativos do Plotly exportados em HTML (abrem no navegador) |
| `requirements.txt` | bibliotecas necessárias |

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook                  # ou abra a pasta no VS Code (extensões Python e Jupyter)
```

Abra os notebooks **a partir desta pasta** (os caminhos `dados/...` são relativos).
Se os gráficos do Plotly não aparecerem no VS Code, troque a linha do renderizador por
`pio.renderers.default = "vscode"`; no Jupyter clássico, por `"notebook"`.

Todos os dados são **sintéticos**: nenhum registro corresponde a pessoa ou empresa real.
