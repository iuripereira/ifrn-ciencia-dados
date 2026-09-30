# Atividade — Aula 05: Exercício Prático (entrega do notebook)

## Entrega

| Item | Valor |
|---|---|
| Tarefa no Moodle | https://presencial.ava.ifrn.edu.br/mod/assign/view.php?id=73623 |
| Aberta desde | 21/09/2026 00:00 |
| Arquivo | `aula05_SEUNOME.ipynb` **executado** do início ao fim, saídas visíveis |
| Pontuação | 10 questões · 10,0 pts |
| Critérios | 60% código correto · 20% `groupby`/`agg`/`pivot_table`/`merge` **sem confundir `size()` com `count()` nem esquecer `validate`** · 20% interpretação escrita + limitações |
| Também vale nota | Formulário Aula 05 (10 questões, refazível, vale a maior): https://presencial.ava.ifrn.edu.br/mod/quiz/view.php?id=73625 |

## Passo a passo no Colab (~2h)

1. Baixe o ZIP: https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73620 (`aula05_laboratorio_dados.zip`).
   ⚠️ Este ZIP traz `matriculas_ifrn_2026.csv` e `campi_ifrn.xlsx` **na raiz, sem pasta `dados/`** — a célula SETUP corrige isso.
2. Abra `aula05_SEUNOME.ipynb` no Colab e renomeie com seu nome.
3. Rode **SETUP COLAB** (upload do ZIP) → rode a **Preparação padrão** (esperado: `(480, 12) (12, 5) (10, 4)`).
4. Resolva Q1→Q10. Q7, Q8 e Q9 dependem de `df_completo` criado na **Q5** — faça em ordem.
5. **Ambiente de execução → Reiniciar e executar tudo**; sem erros.
6. **Arquivo → Baixar → Baixar .ipynb** e envie.

## Guia por questão (caminho + como conferir)

Valores "confira" vêm do Exemplo Prático oficial (`../conteudo.md`).

| Q | Pts | Caminho | Confira |
|---|---|---|---|
| 1 | 1,0 | a) `groupby("turno")["nota_final"].mean()` b) `groupby("modalidade").size()` c) frase size × count | a) Matutino 70,90 · Noturno 66,76 · Vespertino 71,62 |
| 2 | 1,0 | `groupby(["campus","turno"])["nota_final"].mean()`; `type(r.index)`; `r.unstack()` | `MultiIndex`; ex.: Apodi 69,9 / 72,0 / 73,7 |
| 3 | 1,5 | `groupby("campus").agg(n_estudantes=("matricula","count"), nota_media=..., nota_desvio=..., taxa_aprovacao=("situacao", lambda s: (s=="Aprovado").mean()*100))` + `sort_values(..., ascending=False)` | 12 linhas; soma de `n_estudantes` = 480 |
| 4 | 1,5 | a) `pivot_table(values="nota_final", index="campus", columns="situacao", aggfunc="mean", fill_value=0)` b) `values="matricula", aggfunc="count", fill_value=0, margins=True, margins_name="Total"` c) frase | b) linha Total: 281 · 14 · 72 · 86 · 27 · **480** |
| 5 | 1,5 | `df.merge(campi, on="campus", how="left", validate="m:1")` → `df_campi`; idem com `cursos` on `"curso"` → `df_completo`; `isna().sum()` nas colunas novas | todas 0; d) sem `validate`, duplicata em `campi` duplicaria estudantes silenciosamente → com `validate` vira `MergeError` |
| 6 | 1,0 | `cursos_parcial = cursos[cursos["eixo_tecnologico"] != "Informação e Comunicação"]`; merge inner × left; `len()` | inner **271** · left **480** (209 com `NaN`) |
| 7 | 1,0 | a) `.apply(lambda s: s == "Aprovado")` b) `df_completo["situacao"] == "Aprovado"`; `.equals()` c) frase | `True` na comparação; 281 aprovados |
| 8 | 1,0 | `def classificar_carga(linha)` com `linha["carga_horaria"]`; `df_completo.apply(classificar_carga, axis=1)`; `value_counts()` | soma = 480 |
| 9 | 1,5 | **uma** expressão `resultado = (df_completo.query(...).assign(aprovado=lambda d: ...).groupby([...]).agg(n=..., taxa_aprovacao=...).query("n >= 10").sort_values(...))`; `.head()` | 1º: Metropolitana · Produção Industrial · n=12 · 0,917 |
| 10 | 1,0 | `pd.cut(df_completo["carga_horaria"], bins=[0,1200,1800,3000], labels=["Até 1200h","1201–1800h","Acima de 1800h"])`; `groupby("carga_faixa", observed=True)["nota_final"].mean()` + texto com **1 limitação** (confundidores: curso, nível, turno, campus) | 3 faixas |

## Armadilhas que tiram ponto

1. `size()` vs `count()` (Q1c): size conta linhas; count ignora `NaN` da coluna.
2. Esquecer `validate="m:1"` (Q5) — citado explicitamente nos critérios.
3. Q9 com variáveis intermediárias → perde o requisito "uma única cadeia".
4. `assign` com a coluna direta em vez de `lambda d:` — use o `d` da cadeia, não `df_completo`.
5. `groupby` sobre `Categorical` sem `observed=True` (Q10) → aviso/linhas vazias.
6. Ler o CSV com os caminhos sem `dados/` (ZIP da Aula 05 não tem a pasta) → `FileNotFoundError`. O SETUP resolve.
