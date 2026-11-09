# Exemplo — Código do Ranking das Escolas (main.py)

### Exemplo Prático — Ranking das Escolas do RN no ENEM 2025

Este exemplo percorre o ciclo completo visto no livro da aula: lê os microdados, calcula médias por aluno e por escola, junta os dados com o catálogo de nomes e gera uma página HTML interativa com o ranking.

#### Estrutura do projeto

```
projeto/
├── main.py                      ← script principal (anexo nesta seção)
├── template_escolas.html        ← template da página final (anexo)
└── microdados/
    ├── RESULTADOS_2025_RN.csv   ← microdados ENEM 2025 RN (seção Microdados)
    └── catalogo_escolas_rn.csv  ← catálogo de escolas (seção Microdados)
```

#### Como executar

- Baixe os quatro arquivos e organize-os como acima (crie a pasta `microdados/`);
- Execute `python main.py` (Python 3.10+, sem dependências externas);
- O script processa ~30 mil registros e abre `escolas_rn.html` no navegador.

#### Pontos de atenção no código

- Formatos heterogêneos: os resultados usam separador `;` e codificação `latin1`; o catálogo usa vírgula e `utf-8` — situação comum ao integrar fontes reais.
- Valores ausentes: alunos faltosos têm notas vazias; o código converte para `None` e calcula a média apenas das notas válidas.
- Junção por chave: `CO_ESCOLA` liga os dois arquivos — o mesmo papel de um join em SQL ou `merge` no Pandas.
- Separação código/apresentação: os dados são injetados no template HTML via `json.dumps`, substituindo o marcador `__DADOS_ESCOLAS__`.

#### main.py

```
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
    print(f"{'{'}len(escolas){'}'} escolas processadas.")
    print(f"Arquivo gerado: {'{'}OUTPUT_HTML{'}'}")
    webbrowser.open(OUTPUT_HTML.as_uri())

if __name__ == "__main__":
    main()
```

Última atualização: quinta-feira, 6 ago. 2026, 20:52