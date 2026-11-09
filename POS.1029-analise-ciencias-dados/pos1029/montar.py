#!/usr/bin/env python3
"""Monta pos1029/unidade-N/aula-NN/{conteudo,exercicios,atividades}.ipynb a partir da coleta bruta do Moodle.

    conteudo.ipynb   teoria: livro "Tópicos de Estudo", apostila PDF e slides convertidos
    exercicios.ipynb prática: exemplo prático / laboratório guiado + exercício de treino
    atividades.ipynb o que é avaliado: formulário, tarefa, notebook de entrega

Zips são extraídos na pasta da aula (os caminhos `dados/...` dos notebooks continuam valendo);
PDFs e PPTX originais ficam ao lado. Rode da pasta POS.1029-analise-ciencias-dados:

    python3 -I pos1029/montar.py           # não toca em arquivo que já existe
    python3 -I pos1029/montar.py --force   # regera tudo (apaga o que você escreveu nos notebooks!)
"""
import argparse
import base64
import bisect
import json
import re
import shutil
import subprocess
import sys
import textwrap
import uuid
import zipfile
from pathlib import Path

import fitz  # PyMuPDF
import nbformat
from bs4 import BeautifulSoup
from IPython.core.inputtransformer2 import TransformerManager
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

AQUI = Path(__file__).resolve().parent
COLETA = AQUI.parent / "ifrn_pos1029_coleta_bruta"
CACHE_MD = COLETA / "_docling"  # saída do docling (lenta: ~8 min para tudo), reaproveitada entre execuções
TO_MD = Path.home() / ".claude/scripts/to-md.py"

PAPEIS = ("conteudo", "exercicios", "atividades")
ROTULO = {"conteudo": "Conteúdo", "exercicios": "Exercícios", "atividades": "Atividades"}

# Arquivos que o código da aula espera com outro nome/lugar: main.py (Aula 01) lê microdados/;
# os notebooks KDD (Aula 02) leem da própria pasta — symlink para não duplicar 16 MB.
RENOMEAR = {"Catalogo_Escolas_RN.csv": "microdados/catalogo_escolas_rn.csv",
            "Microdados_ENEM_2025_RN.csv": "microdados/RESULTADOS_2025_RN.csv"}
LINKS = {2: {"RESULTADOS_2025_RN.csv": "../aula-01/microdados/RESULTADOS_2025_RN.csv",
             "catalogo_escolas_rn.csv": "../aula-01/microdados/catalogo_escolas_rn.csv"}}
ZIP_DADOS_NA_RAIZ = {"aula05_laboratorio_dados.zip"}  # dados soltos no zip, mas o notebook lê dados/
ENTREGUES = {"aula04_laboratorio.ipynb", "aula05_laboratorio.ipynb", "Aula08_Exercicio_Pratico.ipynb",
             "Aula10_Entrega_Modelo.ipynb", "Aula14_Trabalho_Pratico.ipynb"}

TM = TransformerManager()
MONO = re.compile(r"Mono|Courier|Consol", re.I)  # fontes de código nos PDFs da disciplina


# ---------------------------------------------------------------- markdown / células

def eh_python(src):
    try:
        compile(TM.transform_cell(src), "<celula>", "exec")
        return True
    except Exception:
        return False


def cerca(src):
    lang = "bash" if re.match(r"\s*(\$ |pip |conda |python3? |jupyter |cd |source |git |uv )", src) else "text"
    return f"```{lang}\n{src.strip(chr(10))}\n```"


def _titulos(md):
    """(índice da linha, nível) de cada título markdown fora de bloco de código."""
    em_cerca = False
    for i, linha in enumerate(md.split("\n")):
        if linha.startswith("```"):
            em_cerca = not em_cerca
        elif not em_cerca and re.match(r"#{1,6} ", linha):
            yield i, len(linha) - len(linha.lstrip("#"))


def niveis(md):
    return {n for _, n in _titulos(md)}


def nivela(md, topo, usados=None):
    """Renumera os títulos a partir de `topo` sem pular nível (o H1 é do notebook, o H2 de cada item)."""
    mapa = {n: min(topo + k, 6) for k, n in enumerate(sorted(usados or niveis(md)))}
    linhas = md.split("\n")
    for i, n in list(_titulos(md)):
        linhas[i] = "#" * mapa[n] + " " + linhas[i].lstrip("#").lstrip()
    return "\n".join(linhas)


def md_celulas(md):
    """Quebra markdown em células: uma por título; bloco de código Python vira célula de código."""
    cells = []
    pedacos = re.split(r"(^```[^\n]*\n.*?^```[ \t]*$)", md, flags=re.S | re.M)
    for i, pedaco in enumerate(pedacos):
        if i % 2:  # bloco cercado
            corpo = re.sub(r"^```[^\n]*\n|\n?```[ \t]*$", "", pedaco)
            lang = pedaco[3:pedaco.index("\n")].strip()
            if lang in ("", "python", "py") and corpo.strip() and eh_python(corpo):
                cells.extend(new_code_cell(c) for c in divide_codigo(corpo))
            else:
                _anexa_md(cells, pedaco)
            continue
        for bloco in re.split(r"\n(?=#{1,6} )", pedaco):
            _anexa_md(cells, bloco, nova=True)
    return cells


def _anexa_md(cells, texto, nova=False):
    texto = texto.strip("\n")
    if not texto.strip():
        return
    if cells and cells[-1].cell_type == "markdown" and not (nova and re.match(r"#{1,6} ", texto)):
        cells[-1].source += "\n\n" + texto
    else:
        cells.append(new_markdown_cell(texto))


def divide_codigo(src, limite=40):
    """Script longo vira várias células, cortando antes de def/class/bloco de comentário no nível 0."""
    src = src.strip("\n")
    linhas = src.split("\n")
    if len(linhas) <= limite:
        return [src]
    partes, atual = [], []
    for i, linha in enumerate(linhas):
        corte = (i > 0 and not linhas[i - 1].strip() and len(atual) >= 5
                 and re.match(r"(def |class |async def |if __name__|@|# )", linha))
        if corte:
            partes.append("\n".join(atual).strip("\n"))
            atual = []
        atual.append(linha)
    partes.append("\n".join(atual).strip("\n"))
    return [p for p in partes if p.strip()]


def corrige_file(src):
    """Path(__file__) não existe em notebook; o cwd do notebook é a pasta da aula.
    A página do main.py (Aula 01) traz as chaves do f-string escapadas como {'{'} — artefato do Moodle."""
    src = src.replace("{'{'}", "{").replace("{'}'}", "}")
    out = []
    for linha in src.split("\n"):
        if "Path(__file__).parent" in linha:
            linha = linha.replace("Path(__file__).parent", "Path.cwd()")
            if "#" not in linha:
                linha += "  # no notebook: cwd = pasta da aula (__file__ não existe)"
        out.append(linha)
    return "\n".join(out)


def html_celulas(html, topo=3, script=False):
    """HTML do Moodle -> células. <pre> sai com o texto exato; saída de exemplo vira bloco de texto."""
    soup = BeautifulSoup(html, "html.parser")
    for lixo in soup.select(".translationhash, script, style, .sr-only"):
        lixo.decompose()
    codigos = []
    for pre in soup.find_all("pre"):
        txt = pre.get_text().replace("\r", "").strip("\n")
        ant = pre.find_previous_sibling()
        dica = ant.get_text(" ", strip=True) if ant else ""
        apos_pre = bool(re.fullmatch(r"XCODEX\d+XCODEX", dica))  # o <pre> anterior já virou marcador
        saida = len(dica) < 80 and bool(re.search(r"sa[íi]da|resultado", dica, re.I))
        if not saida and eh_python(txt):
            codigos.append(("code", corrige_file(txt) if script else txt))
        else:
            rot = "**Saída mostrada no material:**\n\n" if (saida or apos_pre) else ""
            codigos.append(("md", rot + cerca(txt)))
        marca = soup.new_tag("p")
        marca.string = f"XCODEX{len(codigos) - 1}XCODEX"
        pre.replace_with(marca)
    md = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"], input=str(soup),
                        capture_output=True, text=True, check=True).stdout
    md = re.sub(r"</?(div|span)[^>]*>", "", md)
    md = nivela(md, topo)
    cells = []
    for i, pedaco in enumerate(re.split(r"XCODEX(\d+)XCODEX", md)):
        if i % 2 == 0:
            cells.extend(md_celulas(pedaco))
            continue
        tipo, txt = codigos[int(pedaco)]
        if tipo == "code":
            cells.extend(new_code_cell(c) for c in divide_codigo(txt))
        else:
            _anexa_md(cells, txt)
    if script:
        codigo = "\n".join(c.source for c in cells if c.cell_type == "code")
        faltam = [imp for imp, uso in (("import numpy as np", "np."), ("import pandas as pd", "pd."))
                  if uso in codigo and imp not in codigo]
        primeiro = next((i for i, c in enumerate(cells) if c.cell_type == "code"), None)
        if faltam and primeiro is not None:
            cells.insert(primeiro, new_code_cell("# adicionado na conversão: a página assume os imports das aulas anteriores\n"
                                                 + "\n".join(faltam)))
    return cells


def texto_html(path):
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser").get_text(" ", strip=True)


def miolo(path, mod):
    """Só o conteúdo útil da página salva do Moodle."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if mod == "book":
        livro = soup.select_one("div.book")
        for lixo in livro.select(".text-end, .book_info, .book_toc_numbered, .book_title"):
            lixo.decompose()
        return str(livro)
    alvo = soup.select_one("div[role=main] .no-overflow") or soup.select_one(".no-overflow") or soup
    return str(alvo)


# ---------------------------------------------------------------- PDF / PPTX

def linhas_codigo_pdf(pdf):
    """Linhas em fonte monoespaçada do PDF, com indentação e linhas em branco recuperadas pela geometria."""
    linhas = []
    for pagina in fitz.open(pdf):
        corrida = []
        for b in pagina.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if spans and all(MONO.search(s["font"]) for s in spans):
                    corrida.append(ln)
                elif corrida:
                    linhas += _formata(corrida)
                    corrida = []
        linhas += _formata(corrida)
    return linhas


def _formata(corrida):
    if not corrida:
        return []
    x0 = min(ln["bbox"][0] for ln in corrida)
    out, y_ant = [], None
    for ln in corrida:
        sp = next(s for s in ln["spans"] if s["text"].strip())
        larg = (sp["bbox"][2] - sp["bbox"][0]) / max(len(sp["text"]), 1)
        altura = ln["bbox"][3] - ln["bbox"][1]
        if y_ant is not None and ln["bbox"][1] - y_ant > 0.8 * altura:
            out.append("")
        recuo = round((ln["bbox"][0] - x0) / larg) if larg else 0
        out.append(" " * recuo + "".join(s["text"] for s in ln["spans"]).rstrip())
        y_ant = ln["bbox"][3]
    return out + [""]


def _norm(s):
    s = s.translate(str.maketrans({"−": "-", "–": "-", "—": "-", "“": '"', "”": '"', "‘": "'", "’": "'"}))
    return re.sub(r"\s+|\\", "", s)


def corrige_codigo(md, pdf):
    """O docling acerta tabelas e títulos, mas achata o código numa linha; repõe as linhas do PDF."""
    linhas = linhas_codigo_pdf(pdf)
    inicios, fluxo = [], ""
    for ln in linhas:
        inicios.append(len(fluxo))
        fluxo += _norm(ln)
    cursor, falhas = 0, 0

    def troca(m):
        nonlocal cursor, falhas
        alvo = _norm(m.group(2))
        if not alvo:
            return m.group(0)
        pos = fluxo.find(alvo, cursor)
        if pos < 0:
            pos = fluxo.find(alvo)
        if pos < 0:
            if re.match(r"\s*A\. ", m.group(2)):  # alternativas de questão: uma por linha
                return "```text\n" + re.sub(r"\s+(?=[B-H]\. )", "\n", m.group(2).strip()) + "\n```"
            falhas += 1
            return m.group(0)
        fim = pos + len(alvo)
        i = bisect.bisect_right(inicios, pos) - 1
        j = bisect.bisect_left(inicios, fim)
        cursor = fim
        bloco = textwrap.dedent("\n".join(linhas[i:j])).strip("\n")
        return f"{m.group(1)}\n{bloco}\n```"

    md = re.sub(r"(```[^\n]*)\n(.*?)\n```", troca, md, flags=re.S)

    def paragrafo(m):  # código que o docling soltou como parágrafo comum (sem cerca)
        nonlocal cursor
        alvo = _norm(m.group(0))
        pos = fluxo.find(alvo, cursor) if len(alvo) >= 20 else -1
        if pos < 0:
            return m.group(0)
        i = bisect.bisect_right(inicios, pos) - 1
        j = bisect.bisect_left(inicios, pos + len(alvo))
        cursor = pos + len(alvo)
        return "```\n" + textwrap.dedent("\n".join(linhas[i:j])).strip("\n") + "\n```"

    pedacos = re.split(r"(^```.*?^```[ \t]*$)", md, flags=re.S | re.M)
    md = "".join(p if i % 2 else re.sub(r"(?<=\n\n)[^\n|][^\n]*(?=\n\n)", paragrafo, p)
                 for i, p in enumerate(pedacos))
    return md, falhas


AVALIADO = re.compile(r"#+ Parte [IVX]+ - .*(avaliativ|[Aa]tividade de entrega|[Mm]ini-projeto)")


def separa_avaliacao(md):
    """Partes da apostila que são avaliação (exercício/formulário/mini-projeto) -> atividades.ipynb.
    O sumário também vira título no docling, então só vale depois do último "Parte I"."""
    linhas = md.split("\n")
    tit = list(_titulos(md))
    inicio = max((i for i, _ in tit if re.match(r"#+ Parte I - ", linhas[i])), default=0)
    fica, vai = [], []
    destino, titulos = fica, dict(tit)
    for k, linha in enumerate(linhas):
        if k >= inicio and k in titulos and re.match(r"#+ (Parte [IVX]+|Apêndice)", linha):
            novo = vai if AVALIADO.match(linha) else fica
            if novo is vai and destino is fica:
                fica += ["", "> **Parte avaliativa desta apostila → [atividades.ipynb](atividades.ipynb).**", ""]
            destino = novo
        destino.append(linha)
    return "\n".join(fica), "\n".join(vai)


def docling_md(arquivo):
    md = CACHE_MD / (arquivo.stem + ".md")
    if not md.exists():
        CACHE_MD.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(TO_MD), str(arquivo), "-o", str(CACHE_MD)], check=True)
    return md


def documento_celulas(arquivo):
    """PDF/PPTX -> células, com imagens embutidas como anexo da célula (notebook autocontido)."""
    md_path = docling_md(arquivo)
    md = md_path.read_text(encoding="utf-8")
    falhas = 0
    if arquivo.suffix.lower() == ".pdf":
        md, falhas = corrige_codigo(md, arquivo)
    md = md.replace("<!-- image -->", "")
    # texto justificado do PDF sai com espaços duplos; só fora dos blocos de código
    pedacos = re.split(r"(^```.*?^```[ \t]*$)", md, flags=re.S | re.M)
    md = "".join(p if i % 2 else re.sub(r"(?<=\S) {2,}(?=\S)", " ", p) for i, p in enumerate(pedacos))
    md_aval = ""
    if arquivo.suffix.lower() == ".pdf":
        md, md_aval = separa_avaliacao(md)
    cells, aval = md_celulas(nivela(md, 3)), md_celulas(nivela(md_aval, 3)) if md_aval.strip() else []
    for c in cells + aval:
        if c.cell_type != "markdown":
            continue
        anexos = {}

        def anexa(m):
            img = md_path.parent / m.group(2)
            if not img.exists():
                return ""
            nome = img.name[-40:]
            anexos[nome] = {"image/png": base64.b64encode(img.read_bytes()).decode()}
            return f"![{m.group(1)}](attachment:{nome})"

        c.source = re.sub(r"!\[([^\]]*)\]\(([^)]+\.png)\)", anexa, c.source)
        if anexos:
            c.attachments = anexos
    return cells, aval, falhas


# ---------------------------------------------------------------- arquivos

def grava(dest, dados, force):
    if dest.exists() and not force:
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(dados)
    return True


def extrai_zip(zpath, dest, force):
    """Extrai sem lixo de macOS; tira a pasta-raiz única do zip para `dados/` ficar ao lado do notebook."""
    with zipfile.ZipFile(zpath) as z:
        nomes = [n for n in z.namelist() if not n.endswith("/") and "__MACOSX/" not in n
                 and not Path(n).name.startswith("._")]
        topo = {n.split("/")[0] for n in nomes}
        tira = len(topo) == 1 and all("/" in n for n in nomes) and topo != {"dados"}
        saida = []
        for n in nomes:
            rel = Path(*Path(n).parts[1:]) if tira else Path(n)
            if zpath.name in ZIP_DADOS_NA_RAIZ and rel.suffix != ".ipynb":
                rel = Path("dados") / rel
            alvo = (dest / rel).resolve()
            if not alvo.is_relative_to(dest.resolve()):
                sys.exit(f"zip com caminho fora da pasta, abortado: {zpath.name}: {n}")
            grava(alvo, z.read(n), force)
            saida.append(rel)
        return saida


def papel_notebook(nome):
    if "Gabarito" in nome:
        return None  # fica só como arquivo: abra depois de tentar
    return "atividades" if nome in ENTREGUES else "exercicios"


def celulas_notebook(path, titulo):
    nb = nbformat.read(path, as_version=4)
    mds = [c for c in nb.cells if c.cell_type == "markdown"]
    usados = set().union(*(niveis(c.source) for c in mds))
    for c in mds:
        c.source = nivela(c.source, 3, usados)
    cab = new_markdown_cell(f"## {titulo} — `{path.name}`\n\n> Notebook original do professor (cópia intacta ao "
                            f"lado deste arquivo). Rode em ordem; os caminhos `dados/...` são relativos à pasta da aula.")
    return [cab] + nb.cells


# ---------------------------------------------------------------- montagem

def titulo_aula(path):
    h = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser").find(["h2", "h3", "h4", "strong", "b"])
    txt = h.get_text(" ", strip=True) if h else texto_html(path)
    m = re.search(r"Aula \d+ — .+", txt)
    return m.group(0) if m else txt[:80]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="sobrescreve arquivos já existentes")
    args = ap.parse_args()

    manifest = json.loads((COLETA / "manifest.json").read_text(encoding="utf-8"))
    unidades, aulas = {}, {}
    un = aula = None
    relatorio = []

    for it in manifest["items"]:
        base = COLETA / it["base"]
        nome, mod = it["name"], it["mod"]
        htmls = [base / f for f in it["files"] if f.endswith(".html")]

        if mod == "section":
            un = it["sec"] - 2
            # a coleta perdeu o "&" do nome da Unidade 5 ("Resultados  Ética")
            unidades[un] = {"nome": re.sub(r"(?<=\S) {2}(?=\S)", " & ", nome), "desc": base / "desc.html", "aulas": []}
            continue
        m = re.match(r"\S+\s+Aula (\d+) —", nome)
        if mod == "label" and m:
            aula = int(m.group(1))
            pasta = AQUI / f"unidade-{un}" / f"aula-{aula:02d}"
            aulas[aula] = {"un": un, "titulo": titulo_aula(htmls[0]), "pasta": pasta,
                           **{p: [] for p in PAPEIS}, "nbs": {p: [] for p in PAPEIS}, "aval": []}
            unidades[un]["aulas"].append(aula)
            aulas[aula]["conteudo"] += html_celulas(miolo(htmls[0], mod), topo=2)
            continue
        if aula is None:
            continue
        A = aulas[aula]
        pasta = A["pasta"]

        if mod in ("assign", "quiz"):
            papel = "atividades"
        elif mod == "book":
            papel = "conteudo"
        elif mod == "page":
            papel = "conteudo" if "Dicionário" in nome else "exercicios"
        elif mod == "label":
            papel = "atividades" if nome.startswith("✅") else "exercicios"
        else:  # resource: decide pelo arquivo
            arq = next((base / f for f in it["files"] if f.startswith("file/")), None)
            suf = arq.suffix.lower() if arq else ""
            papel = "exercicios" if suf in (".zip", ".ipynb", ".csv") else "conteudo"

        celulas = A[papel]
        if mod != "label":
            celulas.append(new_markdown_cell(f"---\n## {nome}"))
        vistos = set()
        for h in htmls:
            txt = texto_html(h)
            if txt in vistos:  # quiz traz desc e view com o mesmo texto
                continue
            vistos.add(txt)
            if mod == "resource":  # descrição curta do arquivo
                celulas.append(new_markdown_cell(f"> {txt}"))
            else:
                celulas += html_celulas(miolo(h, mod), topo=2 if mod == "label" else 3, script=(mod == "page"))
        if mod in ("assign", "quiz") and not htmls:
            celulas.append(new_markdown_cell("_(sem descrição na coleta do Moodle)_"))

        for f in it["files"]:
            if not f.startswith("file/"):
                continue
            arq = base / f
            suf = arq.suffix.lower()
            if suf == ".zip":
                extraidos = extrai_zip(arq, pasta, args.force)
                nbs = sorted((r for r in extraidos if r.suffix == ".ipynb"),
                             key=lambda r: ("Exercicio" in r.name, r.name))
                celulas.append(new_markdown_cell(
                    f"> Pacote `{arq.name}` extraído nesta pasta: "
                    + ", ".join(f"`{r}`" for r in extraidos if len(r.parts) == 1)
                    + (" e as pastas " + ", ".join(sorted({f"`{r.parts[0]}/`" for r in extraidos if len(r.parts) > 1}))
                       if any(len(r.parts) > 1 for r in extraidos) else "") + "."))
                for r in nbs:
                    p = papel_notebook(r.name)
                    if p:
                        A["nbs"][p] += celulas_notebook(pasta / r, nome)
            elif suf == ".ipynb":
                grava(pasta / arq.name, arq.read_bytes(), args.force)
                p = papel_notebook(arq.name) or papel
                if p == papel:
                    celulas.pop()  # o cabeçalho do notebook já traz o nome do item
                A["nbs"][p] += celulas_notebook(pasta / arq.name, nome)
            elif suf in (".pdf", ".pptx"):
                grava(pasta / arq.name, arq.read_bytes(), args.force)
                doc, aval, falhas = documento_celulas(arq)
                if aval:
                    A["aval"] += [new_markdown_cell(f"---\n## Da apostila: `{arq.name}`")] + aval
                celulas.append(new_markdown_cell(f"> Convertido de [`{arq.name}`]({arq.name}) (o original está nesta "
                                                 f"pasta — confira nele figuras e diagramação)."))
                celulas += doc
                if falhas:
                    relatorio.append(f"aula {aula:02d} {arq.name}: {falhas} bloco(s) de código sem par no PDF")
            else:
                rel = RENOMEAR.get(arq.name, arq.name)
                if not (pasta / rel).exists() or args.force:
                    (pasta / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(arq, pasta / rel)
                celulas.append(new_markdown_cell(f"> Arquivo salvo em `{rel}`."))

    # ---- grava notebooks, links e READMEs
    for n, A in aulas.items():
        pasta = A["pasta"]
        pasta.mkdir(parents=True, exist_ok=True)
        for nome, alvo in LINKS.get(n, {}).items():
            link = pasta / nome
            if not link.is_symlink() and not link.exists():
                link.symlink_to(alvo)
        nome_un = unidades[A["un"]]["nome"].split(" (")[0]
        for papel in PAPEIS:
            outros = " · ".join(f"[{ROTULO[p].lower()}]({p}.ipynb)" for p in PAPEIS if p != papel)
            topo = new_markdown_cell(f"# {A['titulo']} · {ROTULO[papel]}\n\n**{nome_un}** · ver também: {outros}")
            corpo = (A[papel] + (A["aval"] if papel == "atividades" else []) + A["nbs"][papel]) or [new_markdown_cell("_Nenhum material desta categoria no Moodle._")]
            for c in corpo:
                c["id"] = uuid.uuid4().hex[:8]
            nb = new_notebook(cells=[topo] + corpo, metadata={
                "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                "language_info": {"name": "python"}})
            nbformat.validate(nb)
            dest = pasta / f"{papel}.ipynb"
            if grava(dest, nbformat.writes(nb).encode("utf-8"), args.force):
                relatorio.append(f"ok  {dest.relative_to(AQUI)}  ({len(nb.cells)} células)")
            else:
                relatorio.append(f"--  {dest.relative_to(AQUI)} já existe, mantido (use --force)")

    for n, U in unidades.items():
        md = subprocess.run(["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"], input=miolo(U["desc"], "section"),
                            capture_output=True, text=True, check=True).stdout
        md = re.sub(r"</?(div|span|p)[^>]*>", "", md).strip()
        previstas = sorted({int(x) for x in re.findall(r"Aula (\d+) —", texto_html(U["desc"]))})
        faltam = [f"{x:02d}" for x in previstas if x not in U["aulas"]]
        linhas = [f"# {U['nome']}", "", nivela(md, 2), "",
                  f"Coletado do Moodle em {manifest['collected'][:10]}. Pastas: "
                  + (", ".join(f"[aula-{x:02d}](aula-{x:02d}/)" for x in U["aulas"]) or "nenhuma ainda") + "."]
        if faltam:
            linhas.append(f"\nAulas ainda sem material no Moodle nesta coleta: {', '.join(faltam)}.")
        grava(AQUI / f"unidade-{n}" / "README.md", ("\n".join(linhas) + "\n").encode("utf-8"), args.force)

    print("\n".join(relatorio))


if __name__ == "__main__":
    main()
