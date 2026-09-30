# Aula 01 — Fundamentos e Panorama da Ciência de Dados (Teórica)

> Semana de 17/08/2026. Definição de Ciência de Dados; perfis profissionais; ferramentas do ecossistema.
> Materiais: livro da aula, exemplo prático completo (ranking das escolas do RN no ENEM 2025), microdados e formulário avaliativo com 8 questões.

---

# Livro — Tópicos de Estudo

Conteúdo teórico da Aula 01: o que é Ciência de Dados, diferenças entre CD, BI e ML, perfis profissionais, ciclo de vida CRISP-DM, ferramentas do ecossistema e o estudo de caso do ranking das escolas do RN.

## Capítulo 1 — O que é Ciência de Dados?

A Ciência de Dados (Data Science) é o campo interdisciplinar que combina estatística, computação e conhecimento de domínio para extrair conhecimento e apoiar decisões a partir de dados. Ela nasce da confluência de três movimentos: o barateamento do armazenamento, a explosão na geração de dados (web, sensores, sistemas transacionais, redes sociais) e o amadurecimento de algoritmos de aprendizado.

### Uma definição de trabalho

> Ciência de Dados é o processo sistemático de coletar, preparar, explorar, modelar e comunicar dados para responder perguntas e apoiar decisões.

Repare que a definição descreve um **processo**, não uma ferramenta. Programar em Python ou usar um algoritmo de ML são meios; o fim é responder uma pergunta relevante com evidências extraídas de dados.

### Dado, informação e conhecimento

- **Dado:** registro bruto, sem interpretação (ex.: a linha de um aluno no CSV do ENEM com suas notas).
- **Informação:** dado contextualizado (ex.: a média de matemática de uma escola em 2025).
- **Conhecimento:** padrão ou relação que apoia decisão (ex.: escolas de determinado perfil apresentam desempenho sistematicamente maior — o que orienta políticas públicas).

### Por que agora?

Órgãos públicos brasileiros publicam dados abertos em larga escala (INEP, IBGE, DataSUS, dados.gov.br). Só os microdados do ENEM contêm milhões de registros por edição — matéria-prima abundante para análise. Ao longo desta disciplina usaremos um recorte real: os resultados do ENEM 2025 no Rio Grande do Norte.

## Capítulo 2 — Ciência de Dados, BI e Aprendizado de Máquina

### Business Intelligence (BI)

O BI é voltado ao passado e ao presente: consolida dados de sistemas transacionais em painéis e relatórios que descrevem **o que aconteceu** (vendas do trimestre, evasão do semestre, média das escolas). As perguntas são conhecidas de antemão e as respostas são agregações e indicadores.

### Ciência de Dados (CD)

A CD engloba o descritivo, mas avança para o diagnóstico, a predição e a prescrição: **por que aconteceu? o que tende a acontecer? o que devemos fazer?** Envolve formulação de hipóteses, experimentação e modelagem estatística — inclusive quando a pergunta ainda não está bem definida.

### Aprendizado de Máquina (ML)

O ML é um conjunto de técnicas usado **dentro** da CD: algoritmos que aprendem padrões a partir de exemplos, sem serem explicitamente programados para cada regra. Classificação, regressão e agrupamento são suas tarefas clássicas — serão vistas na Unidade 4.

### Resumo comparativo

| | BI | Ciência de Dados | ML |
|---|---|---|---|
| Foco | O que aconteceu | Por quê / o que acontecerá | Aprender padrões |
| Perguntas | Conhecidas | Abertas e exploratórias | Definidas pela tarefa |
| Saída típica | Dashboards, relatórios | Análises, modelos, decisões | Modelos preditivos |
| Exemplo (ENEM RN) | Painel de médias por escola | Que fatores explicam o desempenho? | Prever nota a partir do perfil |

## Capítulo 3 — Perfis Profissionais e Mercado

A área de dados se organizou em papéis complementares. Em equipes pequenas uma mesma pessoa acumula vários deles; em organizações maduras, são funções distintas.

- **Analista de Dados:** explora dados e produz análises e painéis para responder perguntas de negócio. Domina SQL, planilhas, visualização e estatística descritiva.
- **Cientista de Dados:** formula hipóteses, desenha experimentos e constrói modelos estatísticos/ML. Domina Python/R, estatística inferencial e aprendizado de máquina.
- **Engenheiro de Dados:** constrói e mantém a infraestrutura que coleta, armazena e disponibiliza dados (pipelines, bancos, data lakes). Domina engenharia de software e sistemas distribuídos.
- **Engenheiro de ML (MLOps):** leva modelos à produção com monitoramento, versionamento e escala.
- **Especialista de domínio:** conhece profundamente o problema (educação, saúde, indústria) e valida se as análises fazem sentido — papel frequentemente subestimado e essencial.

### Competências transversais

Independentemente do papel: **pensamento crítico** (desconfiar dos dados e das próprias conclusões), **comunicação** (traduzir análise em decisão) e **ética** (privacidade, viés, uso responsável — tema da Unidade 5).

### No contexto desta disciplina

Você exercitará principalmente os papéis de analista e cientista de dados: coleta (U2), preparação (U2), análise exploratória (U3), modelagem (U4) e comunicação (U5).

## Capítulo 4 — O Ciclo de Vida: CRISP-DM

Projetos de dados seguem um ciclo. O modelo mais difundido é o **CRISP-DM** (Cross-Industry Standard Process for Data Mining), com seis fases iterativas — é comum voltar a fases anteriores à medida que se aprende sobre o problema.

1. **Entendimento do negócio:** qual é a pergunta? Que decisão será apoiada? Ex.: "como se distribuem os desempenhos das escolas do RN no ENEM 2025 por dependência administrativa?"
2. **Entendimento dos dados:** que dados existem? Qual sua origem, cobertura e qualidade? Ex.: microdados do ENEM (INEP) + catálogo de escolas.
3. **Preparação dos dados:** limpeza, tratamento de ausentes, junções e agregações — tipicamente 60–80% do esforço do projeto. Ex.: descartar registros sem escola, tratar notas vazias, juntar resultados com nomes de escolas.
4. **Modelagem:** aplicar técnicas estatísticas ou de ML. Em análises descritivas, a "modelagem" pode ser a definição de métricas — como a média geral por aluno e o ranking por escola.
5. **Avaliação:** os resultados respondem à pergunta? Há vieses? Ex.: comparar médias sem considerar o nº de participantes por escola pode enganar.
6. **Implantação:** entregar valor — relatório, painel, aplicação. Ex.: página HTML interativa com o ranking das escolas.

O exemplo prático desta aula percorre, em miniatura, todas as seis fases — do problema à página final.

## Capítulo 5 — Ferramentas do Ecossistema

O ecossistema de Ciência de Dados é amplo. Nesta disciplina usaremos o "kit padrão" baseado em Python — hoje a linguagem dominante na área.

### Linguagem e ambiente

- **Python 3.10+** — linguagem principal do curso;
- **Jupyter Notebook/Lab** — documentos interativos que misturam código, resultados e texto: o "caderno de laboratório" do cientista de dados;
- **VS Code** — editor com suporte a notebooks e scripts;
- **Git** (GitHub/GitLab) — versionamento de todo o material produzido.

### Bibliotecas principais

- **NumPy** — arrays e computação numérica vetorizada;
- **Pandas** — DataFrames: leitura, filtragem, agregação e junção de dados tabulares;
- **Matplotlib / Seaborn / Plotly** — visualização estática e interativa;
- **Scikit-learn** — aprendizado de máquina;
- **Requests / BeautifulSoup4** — coleta via APIs e web scraping;
- **Streamlit** — dashboards e aplicações de dados.

### A biblioteca padrão também resolve

Nem tudo exige bibliotecas externas: o exemplo desta aula usa apenas a biblioteca padrão do Python (`csv`, `json`, `statistics`, `pathlib`) para processar 30 mil registros e gerar uma página HTML interativa. A lição: entenda o problema e os dados primeiro; a ferramenta é consequência.

## Capítulo 6 — Estudo de Caso: Ranking das Escolas do RN (ENEM 2025)

Para tornar os conceitos concretos, esta aula traz um estudo de caso completo com dados reais: os microdados do ENEM 2025 das escolas do Rio Grande do Norte.

### O problema (fase 1 do CRISP-DM)

Como se distribui o desempenho das escolas do RN no ENEM 2025, por escola, município e dependência administrativa (federal, estadual, municipal, privada)?

### Os dados (fase 2)

- `RESULTADOS_2025_RN.csv` — microdados com um registro por participante: escola, município, presença e notas das quatro provas objetivas (CN, CH, LC, MT) e da redação. ~30 mil registros, separados por `;`, codificação `latin1`.
- `catalogo_escolas_rn.csv` — catálogo com código (`CO_ESCOLA`) e nome (`NO_ESCOLA`) de ~5 mil escolas, separado por vírgula, codificação `utf-8`.

Observe: fontes diferentes, formatos diferentes. Integrá-las exige uma chave comum — o código da escola.

### Preparação e métricas (fases 3 e 4)

1. Ler os resultados, descartando registros sem código de escola;
2. Converter notas para número, tratando valores ausentes (alunos faltosos);
3. Calcular a média geral por aluno (média das notas válidas);
4. Agrupar alunos por escola e juntar com o catálogo para obter os nomes;
5. Ordenar alunos e escolas — o ranking.

### Avaliação e implantação (fases 5 e 6)

O resultado é uma página HTML interativa com o ranking das escolas, filtros por tipo e município. Ao analisá-la, discutiremos em sala: médias de escolas com poucos participantes são comparáveis às de escolas grandes? O que o recorte "melhores N alunos" muda no ranking? Que cuidados éticos um ranking de escolas exige?

**Próximo passo:** explore a seção Exemplo Prático desta aula, baixe os microdados e execute o código você mesmo.

---

# Microdados — Dicionário de Dados (ENEM 2025 / RN)

## `RESULTADOS_2025_RN.csv` (~16 MB, separador `;`, codificação `latin1`)

Um registro por participante que concluiu o ensino médio em escola do RN. ~30.450 linhas. Principais colunas:

| Coluna | Descrição |
|---|---|
| `CO_ESCOLA` | Código da escola (chave para junção com o catálogo) |
| `NO_MUNICIPIO_ESC` | Município da escola |
| `TP_DEPENDENCIA_ADM_ESC` | Dependência administrativa: 1=Federal, 2=Estadual, 3=Municipal, 4=Privada |
| `TP_PRESENCA_CN/CH/LC/MT` | Presença em cada prova (0=falta, 1=presença, 2=eliminado) |
| `NU_NOTA_CN` | Nota em Ciências da Natureza |
| `NU_NOTA_CH` | Nota em Ciências Humanas |
| `NU_NOTA_LC` | Nota em Linguagens e Códigos |
| `NU_NOTA_MT` | Nota em Matemática |
| `NU_NOTA_REDACAO` | Nota da redação (0–1000) e notas por competência (COMP1–COMP5) |

Notas vazias indicam ausência do participante na prova.

## `catalogo_escolas_rn.csv` (~220 KB, separador vírgula, codificação `utf-8`)

Catálogo com ~4.938 escolas do RN:

| Coluna | Descrição |
|---|---|
| `CO_ESCOLA` | Código da escola |
| `NO_ESCOLA` | Nome da escola |

## Origem e licença

Recorte derivado dos Microdados do ENEM, publicados pelo INEP como dados abertos (gov.br/inep — dados abertos). Uso educacional. Os dados são anonimizados pelo INEP; ainda assim, discutiremos na Unidade 5 os cuidados éticos ao publicar rankings de escolas.

---

# Exemplo Prático — Ranking das Escolas do RN no ENEM 2025 (`main.py`)

Este exemplo percorre o ciclo completo visto no livro da aula: lê os microdados, calcula médias por aluno e por escola, junta os dados com o catálogo de nomes e gera uma página HTML interativa com o ranking.

## Estrutura do projeto

```
projeto/
├── main.py                    ← script principal
├── template_escolas.html      ← template da página final (ZIP "Exemplo Análise Escolas")
└── microdados/
    ├── RESULTADOS_2025_RN.csv ← microdados ENEM 2025 RN
    └── catalogo_escolas_rn.csv← catálogo de escolas
```

## Como executar

1. Baixe os quatro arquivos e organize-os como acima (crie a pasta `microdados/`);
2. Execute `python main.py` (Python 3.10+, sem dependências externas);
3. O script processa ~30 mil registros e abre `escolas_rn.html` no navegador.

## Pontos de atenção no código

- **Formatos heterogêneos:** os resultados usam separador `;` e codificação `latin1`; o catálogo usa vírgula e `utf-8` — situação comum ao integrar fontes reais.
- **Valores ausentes:** alunos faltosos têm notas vazias; o código converte para `None` e calcula a média apenas das notas válidas.
- **Junção por chave:** `CO_ESCOLA` liga os dois arquivos — o mesmo papel de um `join` em SQL ou `merge` no Pandas.
- **Separação código/apresentação:** os dados são injetados no template HTML via `json.dumps`, substituindo o marcador `__DADOS_ESCOLAS__`.

## `main.py`

```python
import csv
import json
import webbrowser
from pathlib import Path
from statistics import mean

BASE_DIR = Path(__file__).parent
RESULTADOS_CSV = BASE_DIR / "microdados" / "RESULTADOS_2025_RN.csv"
CATALOGO_CSV = BASE_DIR / "microdados" / "catalogo_escolas_rn.csv"
OUTPUT_HTML = BASE_DIR / "escolas_rn.html"

TIPO_DEPENDENCIA = {
    "1": "Federal",
    "2": "Estadual",
    "3": "Municipal",
    "4": "Privada",
}

NOTA_COLUNAS = {
    "NU_NOTA_CN": "cn",
    "NU_NOTA_CH": "ch",
    "NU_NOTA_LC": "lc",
    "NU_NOTA_MT": "mt",
    "NU_NOTA_REDACAO": "redacao",
}


def carregar_catalogo_nomes():
    nomes = {}
    with open(CATALOGO_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            nomes[row["CO_ESCOLA"]] = row["NO_ESCOLA"]
    return nomes


def carregar_escolas():
    nomes = carregar_catalogo_nomes()
    escolas = {}

    with open(RESULTADOS_CSV, encoding="latin1") as f:
        for row in csv.DictReader(f, delimiter=";"):
            codigo = row["CO_ESCOLA"]
            if not codigo:
                continue

            escola = escolas.setdefault(codigo, {
                "codigo": codigo,
                "municipio": row["NO_MUNICIPIO_ESC"],
                "tipo": TIPO_DEPENDENCIA.get(row["TP_DEPENDENCIA_ADM_ESC"], "-"),
                "alunos": [],
            })

            notas_aluno = {}
            for coluna, chave in NOTA_COLUNAS.items():
                valor = row[coluna]
                notas_aluno[chave] = round(float(valor), 1) if valor else None

            validas = [v for v in notas_aluno.values() if v is not None]
            notas_aluno["geral"] = round(mean(validas), 1) if validas else None
            escola["alunos"].append(notas_aluno)

    lista = []
    for escola in escolas.values():
        # aluno sem nenhuma nota valida vai para o final
        alunos_ordenados = sorted(
            escola["alunos"],
            key=lambda a: a["geral"] if a["geral"] is not None else -1,
            reverse=True,
        )
        lista.append({
            "codigo": escola["codigo"],
            "nome": nomes.get(escola["codigo"], ""),
            "municipio": escola["municipio"],
            "tipo": escola["tipo"],
            "alunos": alunos_ordenados,
        })

    return lista


def gerar_html(escolas):
    template = (BASE_DIR / "template_escolas.html").read_text(encoding="utf-8")
    html = template.replace("__DADOS_ESCOLAS__", json.dumps(escolas, ensure_ascii=False))
    OUTPUT_HTML.write_text(html, encoding="utf-8")


def main():
    escolas = carregar_escolas()
    gerar_html(escolas)
    print(f"{len(escolas)} escolas processadas.")
    print(f"Arquivo gerado: {OUTPUT_HTML}")
    webbrowser.open(OUTPUT_HTML.as_uri())


if __name__ == "__main__":
    main()
```

> Indentação reconstruída (o AVA exibe o código sem recuo). Lógica idêntica à original.

---

# Formulário Avaliativo — Aula 01

Questionário com 8 questões sobre o conteúdo da aula (livro + exemplo prático). Responda após estudar o material. Compõe as atividades semanais da Unidade 1.

Material complementar: apostila PDF "Aula 1 - Fundamentos em Ciência de Dados" (link no `README.md` da Unidade).
