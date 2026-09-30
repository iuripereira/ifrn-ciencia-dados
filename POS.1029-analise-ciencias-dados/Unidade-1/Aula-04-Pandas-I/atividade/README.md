# Atividade — Aula 04: Exercício Prático (entrega do notebook)

## Entrega

| Item | Valor |
|---|---|
| Tarefa no Moodle | https://presencial.ava.ifrn.edu.br/mod/assign/view.php?id=73158 |
| Aberta desde | 12/09/2026 00:00 · 2 tentativas |
| Arquivo | `aula04_SEUNOME.ipynb` **executado** do início ao fim, saídas visíveis |
| Pontuação | 10 questões · 10,0 pts |
| Critérios | 60% código correto · 20% `loc`/`iloc` e filtragem **sem indexação encadeada** · 20% interpretação escrita + limitações |
| Também vale nota | Formulário Avaliativo — Aula 04 (10 questões objetivas, consulta liberada) |

Questões de interpretação exigem **texto** na célula "_Sua resposta escrita:_", não só código.

## Passo a passo no Colab (~2h)

1. Baixe o ZIP do laboratório: https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73155 (`aula04_laboratorio_dados.zip`, 20 KB).
2. Abra `aula04_SEUNOME.ipynb` desta pasta no Colab e renomeie com seu nome (Arquivo → Renomear).
3. Rode a célula **SETUP COLAB**: envie o ZIP; ela extrai e confere `dados/matriculas_ifrn_2026.csv` e `dados/campi_ifrn.xlsx`.
4. Resolva Q1→Q10 nas células `# ESCREVA SEU CÓDIGO AQUI` + texto em "_Sua resposta escrita:_".
5. **Ambiente de execução → Reiniciar e executar tudo**; confira que não há erro.
6. **Arquivo → Baixar → Baixar .ipynb** e envie na tarefa.

> O notebook desta pasta = notebook original do ZIP + 1 célula de setup para o Colab. Enunciados preservados. Se preferir, use o original do ZIP e cole a célula de setup nele.

## Guia por questão (caminho + como conferir)

Valores "confira" vêm do Exemplo Prático oficial (`../conteudo.md`) — servem de gabarito de sanidade, não de resposta.

| Q | Pts | Caminho | Confira |
|---|---|---|---|
| 1 | 1,0 | `pd.read_csv(..., sep=";", decimal=",", encoding="utf-8", dtype={"matricula": "string"})` + `df.shape` | `(482, 12)`; `df.dtypes`: `nota_final`/`frequencia` = float64 |
| 2 | 1,0 | `head()`, `info()`, `describe()`; texto com a/b/c | 482×12; `nota_final` 41 ausentes, `frequencia` 9; média 69,15 × mediana 69,70 → ~simétrica |
| 3 | 1,0 | `str.strip()` em `campus`; `drop_duplicates().reset_index(drop=True)`; mostrar antes/depois | `nunique` 19→12; `duplicated().sum()` 2→0; shape final (480, 12) |
| 4 | 1,0 | a) `iloc[-5:]` b) `iloc[10:15, [pos_nome, pos_campus, pos_nota]]` (use `df.columns.get_loc`) c) `iloc[-1, pos_situacao]` | 10:15 = posições 10–14 (fim excluído) |
| 5 | 1,0 | `dfm = df.set_index("matricula")`; `dfm.loc["20261250", [...]]`; frase: `iloc` só aceita posição inteira | — |
| 6 | 1,5 | máscaras com `&`, `\|`, parênteses; `.isin([2025, 2026])`; `str.contains("Sistemas\|Redes", na=False)`; `len()` | d) ≈107 (valor do exemplo, após limpeza). c) interpretar: aprovado com freq < 80 → regra não exige 80%? ou inconsistência dos dados |
| 7 | 1,5 | a) `df.loc[df["nota_final"].isna(), "situacao"].value_counts()` b) `df.loc[df["frequencia"].isna(), "frequencia"] = df["frequencia"].median()` c) frase | a) 41: Trancado 27 + Em curso 14 → nota **não existe ainda**; b) `isna().sum()` → 0 |
| 8 | 1,0 | `np.where` aninhado (85/70/60) **+** `.mask(df["nota_final"].isna())`; `value_counts(dropna=False)` | 41 `NaN` em `faixa` (sem o mask, caem em "Insuficiente") |
| 9 | 1,0 | `pd.read_excel("dados/campi_ifrn.xlsx", sheet_name="campi")`; filtro `regiao == "Oeste"`; `df["campus"].isin(campi_oeste["campus"])` | não digitar nomes à mão |
| 10 | 1,0 | `groupby("turno")` → média, `size()`, taxa de aprovação `(situacao == "Aprovado").mean()*100` + texto com **1 limitação** | ref. (Aula 05): Noturno 66,76 / 55,1% · Matutino 70,90 / 65,3% · Vespertino 71,62 / 56,0% |

> Q10 usa `groupby`, tema da Aula 05 — alternativa sem `groupby`: filtrar cada turno com máscara e calcular à mão.

## Armadilhas que tiram ponto

1. **Indexação encadeada** (`df[mask]["col"] = x`) → perde os 20% de `loc`. Sempre `df.loc[mask, "col"] = x`.
2. `and`/`or` em máscaras → `ValueError`. Use `&`/`|` com parênteses.
3. `np.where` sem `.mask(...)` → sem-nota vira "Insuficiente".
4. Preencher `nota_final` (Q7c pede para **não** preencher).
5. Entregar sem executar tudo do zero.
6. Colab: `openpyxl` já vem instalado; se `read_excel` reclamar, rode `!pip install openpyxl`.
