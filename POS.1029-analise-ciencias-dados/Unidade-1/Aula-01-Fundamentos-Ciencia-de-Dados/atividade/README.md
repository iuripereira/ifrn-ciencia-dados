# Atividade — Aula 01

## O que é avaliado

| # | Item | Tipo | Onde |
|---|---|---|---|
| 1 | Formulário Avaliativo — Aula 01 (8 questões, livro + exemplo) | **Nota** | AVA (conferir link na seção da Unidade 1) |
| 2 | Executar o exemplo do ranking das escolas | Prática (sem entrega) | `aula01_ranking_escolas_colab.ipynb` |

Não há tarefa de upload nesta aula. A prática serve para responder as questões do formulário sobre o exemplo.

## Passo a passo no Colab (~20 min)

1. Baixe do AVA: `RESULTADOS_2025_RN.csv` (16 MB), `catalogo_escolas_rn.csv` e o ZIP **Exemplo Análise Escolas** (contém `template_escolas.html`).
2. Abra `aula01_ranking_escolas_colab.ipynb` no Colab.
3. Célula SETUP: envie os 3 arquivos (CSV, CSV, ZIP). A célula cria `microdados/` e extrai o template.
4. Rode as demais células. Saída esperada: número de escolas processadas + download de `escolas_rn.html`.
5. Abra o HTML no navegador e responda as perguntas de discussão (célula final).

## Adaptações para o Colab (em relação ao `main.py` original)

| Original | Colab | Motivo |
|---|---|---|
| `Path(__file__).parent` | `Path(".")` | notebook não tem `__file__` |
| `webbrowser.open(...)` | `files.download("escolas_rn.html")` | Colab não abre navegador local |

## Checklist para o formulário (8 questões)

1. Definição de CD como **processo** (coletar → preparar → explorar → modelar → comunicar).
2. Dado × informação × conhecimento (exemplos do ENEM).
3. BI × CD × ML (tabela comparativa: foco, perguntas, saída).
4. Papéis: analista, cientista, engenheiro de dados, engenheiro de ML, especialista de domínio.
5. CRISP-DM: 6 fases e a qual fase cada passo do exemplo pertence (preparação = 60–80% do esforço).
6. Formatos heterogêneos: resultados `;` + `latin1`; catálogo `,` + `utf-8`.
7. Ausentes: nota vazia → `None`; média só das notas válidas.
8. Chave de junção `CO_ESCOLA`; injeção de dados no template via `json.dumps` no marcador `__DADOS_ESCOLAS__`.
