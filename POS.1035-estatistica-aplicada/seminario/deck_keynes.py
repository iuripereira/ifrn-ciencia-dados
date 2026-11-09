"""Insere o slide do multiplicador keynesiano (Teoria Geral, cap. 10) no deck do seminário.

Entrada: deck do Drive. Saída: seminario/Turismo no Interior do RN.pptx (slide novo após a hipótese + referência Keynes).
"""
import copy
import sys

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_SHAPE, PP_PLACEHOLDER
from pptx.util import Inches, Pt

SRC = ("/home/iuri/Insync/iuripereira/GoogleDrive/20-areas/27-carreira-formacao/"
       "01.pos-graduacao/02-ifrn-ciencias-dados/Turismo no Interior do RN.pptx")
OUT = "Turismo no Interior do RN.pptx"

# paleta do deck (lida dos slides existentes)
BG, CARD, CARD_HI, INK, BODY, MUTED, KICKER, TEAL, ORANGE = (
    "F8F3EA", "FFFAF2", "FDECD0", "2A2420", "4A3F36", "6B5E52", "9A5B06", "16707F", "E8730F")


def rgb(h):
    return RGBColor.from_string(h)


def text(slide, x, y, w, h, runs, size=14, bold=False, color=BODY, font="Arial", italic=False, spacing=None):
    """runs: str ou lista de (texto, overrides). Um parágrafo por item de lista aninhada."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    paras = runs if isinstance(runs, list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if spacing:
            p.space_after = Pt(spacing)
        for seg in (para if isinstance(para, list) else [(para, {})]):
            t, ov = seg if isinstance(seg, tuple) else (seg, {})
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = ov.get("font", font)
            f.size = Pt(ov.get("size", size))
            f.bold = ov.get("bold", bold)
            f.italic = ov.get("italic", italic)
            f.color.rgb = rgb(ov.get("color", color))
    return tb


def card(slide, x, y, w, h, fill=CARD):
    # cantos e borda iguais aos cards grandes do slide "Dois artigos, duas histórias"
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.adjustments[0] = 0.03784
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    s.line.color.rgb = rgb("E3D7C3")
    s.line.width = Pt(0.5)
    s.shadow.inherit = False
    return s


def build_slide(prs):
    layout = [l for l in prs.slide_layouts if l.name == "Title and body"][0]
    s = prs.slides.add_slide(layout)
    # move para depois do slide 4 (hipótese)
    ids = prs.slides._sldIdLst
    el = list(ids)[-1]
    ids.remove(el)
    ids.insert(4, el)

    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(BG)

    # faixa lateral em gradiente, como nos demais slides
    stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, 101565, prs.slide_height)
    stripe.fill.gradient()
    stripe.fill.gradient_angle = 90
    st = stripe.fill.gradient_stops
    st[0].color.rgb, st[0].position = rgb("B9612F"), 0.0
    st[1].color.rgb, st[1].position = rgb(ORANGE), 1.0
    stripe.line.fill.background()

    # placeholders: título reaproveitado, corpo removido
    for ph in list(s.placeholders):
        if ph.placeholder_format.type == PP_PLACEHOLDER.TITLE:
            ph.left, ph.top, ph.width, ph.height = Inches(1.22), Inches(1.23), Inches(11.44), Inches(1.05)
            tf = ph.text_frame
            tf.word_wrap = True
            for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
                setattr(tf, m, 0)
            r = tf.paragraphs[0].add_run()
            r.text = "Cada real que entra gera k reais de renda, e k depende do quanto fica"
            r.font.name, r.font.size, r.font.bold = "Trebuchet MS", Pt(28), True
            r.font.color.rgb = rgb(INK)
        else:
            ph._element.getparent().remove(ph._element)

    kick = text(s, 1.22, 0.89, 11.56, 0.26, "BASE TEÓRICA · MULTIPLICADOR KEYNESIANO · TEORIA GERAL, CAP. 10",
                size=12, bold=True, color=KICKER)
    kick.text_frame.paragraphs[0].runs[0]._r.rPr.set("spc", "150")  # mesmo tracking dos outros kickers

    # ---- coluna esquerda: fórmula
    card(s, 1.23, 2.45, 5.47, 3.25)
    text(s, 1.53, 2.7, 4.99, 0.26, "A FÓRMULA", size=12, bold=True, color=TEAL)
    text(s, 1.53, 3.0, 4.99, 0.6, "k = 1 / (1 − c)", size=32, bold=True, color=INK, font="Trebuchet MS")
    text(s, 1.53, 3.65, 4.99, 0.72,
         [[("c", {"bold": True}), (" = propensão marginal a consumir: a fração de cada real a mais de renda "
           "que vira consumo. ΔY = k · ΔI (Keynes, 1996, p. 134).", {})]], size=13)
    rows = [("c = 0,9  →  k = 10", "exemplo do próprio Keynes (p. 136)"),
            ("c = 0,8  →  k = 5", "estimativa de Keynes (p. 139)"),
            ("c = 0,5  →  k = 2", "metade de cada real vaza")]
    for i, (a, b) in enumerate(rows):
        y = 4.42 + i * 0.28
        text(s, 1.53, y, 1.95, 0.28, a, size=14, bold=True, color=INK)
        text(s, 3.5, y + 0.02, 3.02, 0.26, b, size=12)
    text(s, 1.53, 5.3, 4.99, 0.38,
         "“Num sistema aberto […] temos de reduzir a cifra do multiplicador.” (p. 138)", size=11, italic=True)

    # ---- coluna direita: gráfico das rodadas
    card(s, 6.98, 2.45, 5.47, 3.25)
    text(s, 7.28, 2.7, 4.99, 0.26, "R$ 100 DO TURISTA, RODADA A RODADA", size=12, bold=True, color=TEAL)
    rounds = list(range(1, 9))
    cd = CategoryChartData()
    cd.categories = [f"{r}ª" for r in rounds]
    for c in (0.8, 0.5):
        cd.add_series(f"c = {c:.1f}".replace(".", ","), [round(100 * c ** (r - 1), 1) for r in rounds])
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.18), Inches(2.97), Inches(5.1), Inches(2.33), cd)
    ch = gf.chart
    ch.font.name, ch.font.size = "Arial", Pt(10)
    ch.font.color.rgb = rgb(BODY)
    ch.has_legend = True
    ch.legend.position, ch.legend.include_in_layout = XL_LEGEND_POSITION.BOTTOM, False
    plot = ch.plots[0]
    plot.gap_width, plot.overlap = 60, -10
    for ser, col in zip(plot.series, (ORANGE, TEAL)):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(col)
    va, ca = ch.value_axis, ch.category_axis
    va.maximum_scale, va.has_major_gridlines = 100, True
    va.major_gridlines.format.line.color.rgb = rgb("E6DCCB")
    va.format.line.fill.background()
    ca.format.line.color.rgb = rgb("E6DCCB")
    text(s, 7.28, 5.34, 4.99, 0.26,
         [[("Soma das rodadas: ", {}), ("R$ 500", {"bold": True, "color": ORANGE}), (" com c = 0,8  ·  ", {}),
           ("R$ 200", {"bold": True, "color": TEAL}), (" com c = 0,5", {})]], size=12)

    text(s, 1.22, 5.85, 11.44, 0.85,
         "No município do interior, c é a parte do gasto do turista que fica: leite, queijo e mão de obra locais "
         "mantêm c alto; insumos e serviços comprados em Natal derrubam c, e k com ele. É o vazamento de Archer (1977) "
         "e Britton (1982), e explica por que o multiplicador de Souza (2014) não chega ao interior descrito por Almada (2019).",
         size=14, bold=True)
    text(s, 1.22, 6.82, 11.44, 0.26,
         "Fonte: Keynes (1996 [1936]), Teoria Geral, cap. 10, p. 133–144, ed. Nova Cultural. "
         "Conceito introduzido por Kahn (1931).", size=12, color=MUTED)

    s.notes_slide.notes_text_frame.text = (
        "Keynes define a propensão marginal a consumir como a fração de um acréscimo de renda que a comunidade "
        "gasta em consumo e deriva o multiplicador: ΔY = k·ΔI, com 1 − 1/k = c, logo k = 1/(1 − c) (p. 134). "
        "Exemplo dele: se a comunidade consome nove décimos do acréscimo, k = 10, e obras públicas geram dez vezes "
        "o emprego primário (p. 136). Para uma “comunidade moderna típica” ele estima c não muito abaixo de 80%, "
        "k perto de 5 (p. 139); a estimativa americana que ele cita dá k ≈ 2,5, c de 60 a 70% (p. 144). "
        "O ponto para nós é o item (iii), p. 138: num sistema aberto parte do multiplicador vaza para fora e "
        "“temos de reduzir a cifra do multiplicador”. Um município do interior é um sistema aberto pequeno: "
        "c é a fração do gasto do turista que fica nele. O gráfico mostra R$ 100 do turista com c = 0,8 "
        "(soma R$ 500) e c = 0,5 (soma R$ 200). Ponte: Souza mede o multiplicador do turismo para o Nordeste "
        "agregado; Almada mostra que a atividade ficou em Natal. Nossa pergunta é o c municipal."
    )
    return s


def add_reference(prs):
    """Insere KEYNES na ordem alfabética do slide de referências (uma caixa por referência)."""
    refs_slide = [sl for sl in prs.slides if any(sh.has_text_frame and "ALMADA" in sh.text_frame.text
                                                  for sh in sl.shapes)][0]
    # duas colunas; KEYNES entra na coluna da direita, depois de IBGE, e empurra SILVA e SOUZA para baixo
    anchor = [sh for sh in refs_slide.shapes if sh.has_text_frame and sh.text_frame.text.startswith("IBGE")][0]
    col = sorted([sh for sh in refs_slide.shapes if sh.has_text_frame and sh.left == anchor.left
                  and sh.top > Inches(1.5)], key=lambda sh: sh.top)
    prev = [sh for sh in col if sh.top < anchor.top][-1]
    gap = anchor.top - (prev.top + prev.height)
    shift = anchor.height + gap  # a nova caixa tem a altura da IBGE (duas linhas)
    new = copy.deepcopy(anchor._element)
    anchor._element.addnext(new)
    new.nvSpPr.cNvPr.id = max(sh.shape_id for sh in refs_slide.shapes) + 1
    ts = new.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}t")
    ts[0].text = ("KEYNES, J. M. A teoria geral do emprego, do juro e da moeda [1936]. São Paulo: Nova Cultural, "
                  "1996. (Os Economistas). Cap. 10, p. 133–144.")
    for t in ts[1:]:
        t.text = ""
    for sh in col:
        if sh.top > anchor.top:
            sh.top += shift
    new.spPr.xfrm.off.y = anchor.top + shift
    last = max(sh.top + sh.height for sh in col)
    print(f"refs: KEYNES em y={(anchor.top + shift)/914400:.2f}in, última caixa termina em {last/914400:.2f}in")


if __name__ == "__main__":
    prs = Presentation(SRC)
    n0 = len(prs.slides)
    build_slide(prs)
    add_reference(prs)
    prs.save(OUT)
    chk = Presentation(OUT)
    assert len(chk.slides) == n0 + 1
    assert "MULTIPLICADOR KEYNESIANO" in "\n".join(sh.text_frame.text for sh in chk.slides[4].shapes if sh.has_text_frame)
    assert any("KEYNES, J. M." in sh.text_frame.text for sh in chk.slides[-1].shapes if sh.has_text_frame)
    print(f"ok: {OUT} com {len(chk.slides)} slides")
