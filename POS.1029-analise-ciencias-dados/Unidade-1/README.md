# Unidade 1 — Introdução à Ciência de Dados e Python (Aulas 01–05)

**Disciplina:** Análise e Ciência de Dados (POS.1029) — Especialização em Ciência de Dados, IFRN
**Carga horária:** 7h30 (25%) · Encontros 01–05
**Fonte:** AVA-Presencial — https://presencial.ava.ifrn.edu.br/course/section.php?id=18871 (extraído em 29/09/2026)

Unidade introdutória: panorama da Ciência de Dados, fundamentos de Aprendizado de Máquina e Mineração de Dados, e preparação do ambiente Python (Jupyter, NumPy e Pandas) usado em todo o curso.

## Mapa das aulas

| Aula | Tema | Tipo | Semana | Avaliação | Pasta |
|---|---|---|---|---|---|
| 01 | Fundamentos e Panorama da Ciência de Dados | Teórica | 17/08/2026 | Formulário (8 questões) | `Aula-01-Fundamentos-Ciencia-de-Dados/` |
| 02 | Introdução ao ML e KDD | Teórica | 24/08/2026 | Formulário + prática KDD (passos 1–3) | `Aula-02-ML-e-KDD/` |
| 03 | Ambiente Python e Primeiros Passos | Teórico-prática | 31/08/2026 | Formulário | `Aula-03-Ambiente-Python/` |
| 04 | Laboratório NumPy e Pandas I | Prática | aberta 12/09/2026 | **Notebook no Moodle (10 pts)** + formulário (10 questões) | `Aula-04-Pandas-I/` |
| 05 | Laboratório Pandas II — Agrupamentos e Joins | Prática | aberta 21/09/2026 | **Notebook no Moodle (10 pts)** + formulário (10 questões, maior nota) | `Aula-05-Pandas-II/` |

## Estrutura de cada aula

```
Aula-0X-.../
├── conteudo.md          ← livro "Tópicos de Estudo" + página de exemplo, transcritos
└── atividade/
    ├── README.md        ← o que entregar, passo a passo no Colab, armadilhas
    └── *.ipynb          ← notebook pronto para abrir no Colab (com célula de setup)
```

## Colab — setup comum

1. Abra https://colab.research.google.com → **Arquivo → Fazer upload de notebook** → escolha o `.ipynb` da pasta `atividade/`.
2. Rode a célula **SETUP COLAB** (primeira célula de código): ela pede o upload dos dados (ZIP/CSV baixados do AVA) e organiza a pasta `dados/`.
3. Arquivos enviados ao Colab somem quando a sessão reinicia. Para não reenviar, use a variante com Google Drive comentada na própria célula.
4. Equivalente Colab de `Kernel → Restart & Run All`: **Ambiente de execução → Reiniciar e executar tudo**.
5. Para entregar: **Arquivo → Baixar → Baixar .ipynb** (com as saídas visíveis) e anexar na tarefa do Moodle.

## Arquivos que precisam ser baixados do AVA (binários — não transcritos)

| Aula | Arquivo | Tamanho | Link (logado no AVA) |
|---|---|---|---|
| 01/02 | Microdados ENEM 2025 RN (`RESULTADOS_2025_RN.csv`) | 16 MB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=67919 |
| 01/02 | Catálogo Escolas RN (`catalogo_escolas_rn.csv`) | 221 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=67918 |
| 01 | Exemplo Análise Escolas (ZIP: `template_escolas.html`, `escolas_rn.html`) | 491 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=67920 |
| 01 | Apostila PDF — Fundamentos em Ciência de Dados | 379 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=68907 |
| 02 | Detalhamento Atividade Prática (PDF) — transcrito em `Aula-02.../atividade/README.md` | 209 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=72204 |
| 02 | Notebooks KDD Passos 1–3 (ZIP) — código transcrito no notebook da atividade | 118 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=72205 |
| 03 | Tutorial Python + NumPy + Pandas (PDF) — transcrito em `Aula-03.../tutorial-python-numpy-pandas.md` | 244 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=72676 |
| 04 | Apostila PDF Aula 04 (31 p.) | 767 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73154 |
| 04 | Laboratório ZIP (`aula04_laboratorio.ipynb` + `dados/`) | 20 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73155 |
| 05 | Apostila PDF Aula 05 (26 p.) | 671 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73619 |
| 05 | Laboratório ZIP (`aula05_laboratorio.ipynb` + CSV + XLSX, **sem** pasta `dados/`) | 20 KB | https://presencial.ava.ifrn.edu.br/mod/resource/view.php?id=73620 |

## Links das atividades avaliativas

- Tarefa Aula 04 (entrega do notebook): https://presencial.ava.ifrn.edu.br/mod/assign/view.php?id=73158
- Tarefa Aula 05 (entrega do notebook): https://presencial.ava.ifrn.edu.br/mod/assign/view.php?id=73623
- Formulário Aula 05: https://presencial.ava.ifrn.edu.br/mod/quiz/view.php?id=73625
- Formulários Aulas 01–04: não apareceram como link na seção durante a extração (possivelmente ocultos/encerrados) — conferir no AVA.
