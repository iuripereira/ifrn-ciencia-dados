# Aula 14 — scikit-learn: Fluxo de Trabalho em ML

Especialização em Ciência de Dados · Análise e Ciência de Dados · IFRN
Unidade 4 — Aprendizado de Máquina Aplicado (primeira aula)

## Conteúdo do pacote

| Arquivo | O que é |
|---|---|
| `Aula14_Fluxo_ML_scikit_learn.ipynb` | **Exemplo guiado** (churn do app de música fictício, 1.500 usuários), já executado: API do scikit-learn, treino/teste, baseline, pipeline, métricas de classificação, limiar, validação cruzada, comparação de modelos e um exemplo de regressão (RMSE, R²) |
| `Aula14_Trabalho_Pratico.ipynb` | **Trabalho prático — ENTREGA NO MOODLE até 23/11/2026, 23:59**: classificar pedidos com cliente insatisfeito (avaliação ≤ 3) na hamburgueria da Aula 12 |
| `dados/app_musica_churn.csv` | dados do exemplo guiado |
| `dados/delivery_hamburgueria.csv` | dados do trabalho prático e do exemplo de regressão (o mesmo da Aula 12) |
| `gerar_dados.py` | script que gera `app_musica_churn.csv` (semente fixa) |
| `figuras/` | gráficos exportados pelo exemplo guiado |
| `requirements.txt` | bibliotecas necessárias (scikit-learn 1.4 ou mais recente) |

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook                  # ou abra a pasta no VS Code (extensões Python e Jupyter)
```

Abra os notebooks **a partir desta pasta** (os caminhos `dados/...` são relativos).
Todos os dados são **sintéticos**: nenhum registro corresponde a pessoa ou empresa real.
