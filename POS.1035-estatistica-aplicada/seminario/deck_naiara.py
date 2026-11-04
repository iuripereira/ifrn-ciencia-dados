"""Deck da Naiara: "Onde o RN concentra sua economia — e onde pode crescer".

Entrada: NAIARA_*.docx (texto + figuras). Saída: Onde o RN concentra sua economia.pptx.
Identidade visual irmã do deck do Iuri (reusa text/card de deck_keynes), com paleta verde/dourado e títulos em serifa.
Valores dos gráficos: os citados no texto são exatos; os demais foram lidos dos gráficos da autora (aproximados).
"""
import tempfile
import zipfile

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt, Emu

from deck_keynes import text, card as _card

DOCX = "NAIARA_Onde o RN concentra sua economia - apresentação de estatistica.docx"
OUT = "Onde o RN concentra sua economia.pptx"

BG, CARD, CARD_HI, INK, BODY, MUTED = "F6F4EE", "FFFFFF", "EAF1EC", "1C2B26", "3E4A45", "6F7A75"
GREEN, GREEN2, GREEN3, GOLD, GOLD2, KICKER, DARK, LINE = (
    "1F5A45", "4F8A72", "9EC3AF", "D9961A", "E9C57A", "A86D0B", "15302A", "DCE3DF")
HEAD = "Cambria"
MESOS = ["Oeste Potiguar", "Central Potiguar", "Agreste Potiguar", "Leste Potiguar"]


def card(s, x, y, w, h, fill=CARD):
    c = _card(s, x, y, w, h, fill)
    c.line.color.rgb = RGBColor.from_string(LINE)
    return c


def pill(s, x, y, w, h, label, fill=GOLD, color=INK):
    p = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    p.adjustments[0] = 0.5
    p.fill.solid()
    p.fill.fore_color.rgb = RGBColor.from_string(fill)
    p.line.fill.background()
    p.shadow.inherit = False
    text(s, x + 0.2, y + 0.1, w - 0.4, h - 0.2, label, size=13, bold=True, color=color)


def base(prs, kicker, title, dark=False, notes=""):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = RGBColor.from_string(DARK if dark else BG)
    if kicker:
        k = text(s, 0.9, 0.55, 11.5, 0.26, kicker, size=12, bold=True, color=GOLD if dark else KICKER)
        k.text_frame.paragraphs[0].runs[0]._r.rPr.set("spc", "150")
    if title:
        text(s, 0.9, 0.88, 11.5, 1.0, title, size=30, bold=True, color=BG if dark else INK, font=HEAD)
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def fonte(s, txt, y=6.85):
    text(s, 0.9, y, 11.5, 0.3, txt, size=11, color=MUTED)


def style_chart(ch, colors, legend=True):
    ch.font.name, ch.font.size = "Arial", Pt(11)
    ch.font.color.rgb = RGBColor.from_string(BODY)
    ch.has_legend = legend
    if legend:
        ch.legend.position, ch.legend.include_in_layout = XL_LEGEND_POSITION.BOTTOM, False
    for ser, col in zip(ch.plots[0].series, colors):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = RGBColor.from_string(col)
    va, ca = ch.value_axis, ch.category_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor.from_string(LINE)
    va.format.line.fill.background()
    ca.format.line.color.rgb = RGBColor.from_string(LINE)
    return ch


# ---------------------------------------------------------------- slides
def capa(prs):
    s = base(prs, "", "", dark=True)
    k = text(s, 0.9, 1.3, 11.5, 0.3, "SEMINÁRIO · PÓS-GRADUAÇÃO EM CIÊNCIA DE DADOS · IFRN", size=14, bold=True, color=GOLD)
    k.text_frame.paragraphs[0].runs[0]._r.rPr.set("spc", "150")
    text(s, 0.9, 2.0, 11.0, 2.2, "Onde o RN concentra sua economia, e onde pode crescer",
         size=48, bold=True, color=BG, font=HEAD)
    text(s, 0.9, 4.35, 10.0, 0.8, "Diagnóstico territorial e vocações produtivas das mesorregiões do Rio Grande do Norte",
         size=18, color=GREEN3)
    text(s, 0.9, 6.3, 8.0, 0.4, "Naiara · novembro de 2026", size=16, color=BG)
    pill(s, 10.6, 6.2, 1.85, 0.5, "RAIS · IBGE", fill=GOLD)
    s.notes_slide.notes_text_frame.text = (
        "Pergunta do seminário: onde a economia potiguar está concentrada e quais vocações cada mesorregião "
        "tem para crescer. Roteiro: território, base teórica, indicadores, três leituras dos dados e proposta.")


def territorio(prs, img):
    s = base(prs, "CARACTERIZAÇÃO · TERRITÓRIO", "Um estado, quatro mesorregiões", notes=(
        "Mapa das quatro mesorregiões do IBGE. O Leste concentra a Região Metropolitana de Natal; o Oeste tem "
        "Mossoró; o Central, o Seridó e a cerâmica; o Agreste faz a transição para o litoral."))
    card(s, 0.9, 2.05, 6.3, 4.6)
    s.shapes.add_picture(img, Inches(1.1), Inches(2.25), width=Inches(5.9))
    perfis = [("LESTE", "Natal e região metropolitana", "Serviços acima de 80% do VAB; construção civil; polo que atrai migração pendular."),
              ("OESTE", "Mossoró e entorno", "Segundo polo, o mais dinâmico: comércio, serviços, mineral, petróleo e energia."),
              ("CENTRAL", "Seridó e Currais Novos", "Minerais não metálicos (cerâmica estrutural) e comércio em crescimento."),
              ("AGRESTE", "Transição para o litoral", "Agropecuária com QL alto no setor primário e serviços de apoio básico.")]
    for i, (n, sub, desc) in enumerate(perfis):
        y = 2.05 + i * 1.17
        card(s, 7.5, y, 4.95, 1.02, fill=CARD_HI if i % 2 else CARD)
        text(s, 7.75, y + 0.14, 1.3, 0.3, n, size=13, bold=True, color=GREEN)
        text(s, 9.0, y + 0.15, 3.3, 0.3, sub, size=11, color=MUTED, italic=True)
        text(s, 7.75, y + 0.45, 4.5, 0.5, desc, size=12, color=BODY)
    fonte(s, "Fonte: IBGE, divisão em mesorregiões. Mapa: Wikimedia Commons.")


def teoria(prs):
    s = base(prs, "BASE TEÓRICA · CIÊNCIA REGIONAL", "Duas correntes para ler a mesma disparidade", notes=(
        "A Ciência Regional combina a explicação de fora para dentro (base de exportação e polos de crescimento) "
        "com a de dentro para fora (capacidades locais, capital social, territorialidade). Os dois artigos usam as duas."))
    cols = [("DESENVOLVIMENTO EXÓGENO", GOLD, "O motor vem de fora",
             ["Teoria da Base de Exportação: a região cresce quando vende para fora o que produz melhor.",
              "Polos de Crescimento: a indústria motriz puxa fornecedores e serviços ao redor.",
              "Lente para o Leste e para os enclaves de petróleo e energia no Oeste."]),
            ("DESENVOLVIMENTO ENDÓGENO", GREEN, "O motor está no território",
             ["Capacidades locais e capital social sustentam o crescimento sem depender da capital.",
              "Territorialidade: identidade produtiva (cerâmica, fruticultura, agricultura familiar).",
              "Lente para APLs emergentes no Oeste, Central e Agreste."])]
    for i, (k, col, h, items) in enumerate(cols):
        x = 0.9 + i * 5.9
        card(s, x, 2.1, 5.65, 3.5)
        text(s, x + 0.3, 2.35, 5.0, 0.3, k, size=12, bold=True, color=col)
        text(s, x + 0.3, 2.7, 5.0, 0.6, h, size=22, bold=True, color=INK, font=HEAD)
        text(s, x + 0.3, 3.45, 5.05, 2.8, items, size=14, color=BODY, spacing=10)
    fonte(s, "Base: Alves, Lima Júnior e Pereira (2019); Maia e Clementino (2025).")


def metodo(prs):
    s = base(prs, "MÉTODO · INDICADORES", "Cinco índices sobre dados secundários oficiais", notes=(
        "Todos os indicadores vêm de dados do IBGE e da RAIS/MTE. O QL é o principal; os demais medem "
        "concentração, dispersão e mudança no tempo. O ICn combina três deles por componentes principais."))
    rows = [("Quociente Locacional (QL)", "Compara o peso de um setor na região com o do estado. QL > 1 indica especialização regional."),
            ("Participação Relativa (PR)", "Peso percentual do emprego ou VAB local no total do estado: grau de concentração de riqueza."),
            ("Coef. de Localização (CLoc) e IHH", "Dispersão espacial das atividades e capacidade de atrair novos encadeamentos."),
            ("Coef. de Reestruturação (CRest)", "Mudança temporal na estrutura regional: sinaliza polos produtivos emergentes."),
            ("Índice de Concentração (ICn)", "Integra QL, PR e IHH por Análise de Componentes Principais para detectar APLs.")]
    for i, (a, b) in enumerate(rows):
        y = 2.1 + i * 0.86
        card(s, 0.9, y, 11.55, 0.74, fill=CARD_HI if i % 2 else CARD)
        text(s, 1.2, y + 0.22, 3.6, 0.35, a, size=14, bold=True, color=GREEN)
        text(s, 4.9, y + 0.22, 7.3, 0.4, b, size=13, color=BODY)
    fonte(s, "Fontes de dados: IBGE (VAB) e RAIS/MTE (emprego formal). Metodologia: Crocco et al. (2006).")


def ql(prs):
    s = base(prs, "MÉTODO · QUOCIENTE LOCACIONAL", "Como ler o QL", notes=(
        "O QL compara o peso de um setor na mesorregião com o peso desse setor no RN. Maior que 1, a região é "
        "mais especializada que o estado; igual a 1, proporcional; menor que 1, sub-representada."))
    card(s, 0.9, 2.1, 11.55, 1.75)
    text(s, 1.3, 2.55, 1.6, 0.9, "QL =", size=36, bold=True, color=GOLD, font=HEAD)
    text(s, 3.0, 2.4, 9.0, 0.45, "( emprego do setor na mesorregião  ÷  emprego total da mesorregião )", size=15, bold=True, color=INK)
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.0), Inches(2.95), Inches(9.0), Emu(12700))
    ln.fill.solid()
    ln.fill.fore_color.rgb = RGBColor.from_string(GREEN)
    ln.line.fill.background()
    text(s, 3.0, 3.1, 9.0, 0.45, "( emprego do setor no RN  ÷  emprego total no RN )", size=15, color=MUTED)
    casos = [("QL > 1", "Especialização", GOLD, "Vocação: concentração relativa acima da média do estado. Candidata a APL."),
             ("QL = 1", "Proporcional", GREEN, "O setor tem o mesmo peso na mesorregião e no estado."),
             ("QL < 1", "Desconcentrado", MUTED, "Atividade sub-representada; a região tende a importar o que o setor produz.")]
    for i, (a, b, col, d) in enumerate(casos):
        x = 0.9 + i * 3.93
        card(s, x, 4.2, 3.7, 1.8)
        text(s, x + 0.3, 4.45, 3.1, 0.5, [[(a + " · ", {"bold": True, "color": col}), (b, {"bold": True, "color": INK})]], size=18)
        text(s, x + 0.3, 5.05, 3.1, 1.3, d, size=13, color=BODY)
    fonte(s, "Fonte: Alves, Lima Júnior e Pereira (2019); Crocco et al. (2006).")


def emprego(prs):
    s = base(prs, "ANÁLISE · EMPREGO FORMAL 2007 → 2017", "O litoral ainda concentra, mas o interior ganha tração", notes=(
        "Vínculos formais ativos em 31 de dezembro. O Leste reuniu 401.392 empregos em 2017, 55.773 a mais que em 2007. "
        "Todas as mesorregiões cresceram; Oeste e Central ampliaram a base. Valores das outras três lidos do gráfico original."))
    card(s, 0.9, 2.1, 7.9, 4.55)
    cd = CategoryChartData()
    cd.categories = MESOS[::-1]
    cd.add_series("2007", [345_619, 24_000, 36_000, 90_000])  # mesma ordem de MESOS[::-1]
    cd.add_series("2017", [401_392, 29_000, 46_000, 110_000])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(1.1), Inches(2.3), Inches(7.5), Inches(4.2), cd)
    ch = style_chart(gf.chart, [GOLD2, GREEN])
    ch.plots[0].gap_width, ch.plots[0].overlap = 50, -10
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '#,##0', False
    ch.value_axis.maximum_scale = 450_000
    for i, y in enumerate((2.1, 3.65)):
        card(s, 9.1, y, 3.35, 1.3, fill=CARD_HI)
        text(s, 9.4, y + 0.15, 2.9, 0.6, ("401.392", "+55.773")[i], size=32, bold=True, color=(GREEN, GOLD)[i], font=HEAD)
        text(s, 9.4, y + 0.8, 2.9, 0.4, ("empregos formais no Leste em 2017", "vagas a mais no Leste entre 2007 e 2017")[i], size=11, color=BODY)
    text(s, 9.1, 5.25, 3.35, 1.4, "Todas as mesorregiões expandiram os postos formais, com destaque para a ampliação da base no Oeste e no Central.",
         size=13, color=BODY)
    fonte(s, "Fonte: RAIS/MTE (2007 e 2017), vínculos ativos em 31/12, via Alves, Lima Júnior e Pereira (2019). Leste exato; demais lidos do gráfico (aprox.).")


def setorial(prs):
    s = base(prs, "ANÁLISE · ESTRUTURA SETORIAL 2017", "O perfil setorial muda conforme a mesorregião", notes=(
        "Serviços lideram em todas: 68,6% no Agreste, 64,7% no Leste, 52,5% no Oeste e 51,9% no Central. O comércio "
        "avançou em todas; no Agreste cresceu cerca de 72,4% entre 2007 e 2017. A agropecuária pesa no Oeste. "
        "Participações de serviços são as do texto; as demais foram lidas do gráfico."))
    card(s, 0.9, 2.1, 7.9, 4.55)
    cd = CategoryChartData()
    cd.categories = MESOS[::-1]
    dados = {  # % do emprego formal, 2017 — serviços exatos, demais aproximados e normalizados
        "Indústria": [10.8, 7.4, 22.6, 12.8], "Construção civil": [4.0, 2.7, 2.3, 4.2],
        "Comércio": [18.7, 17.3, 20.4, 21.0], "Serviços": [64.7, 68.6, 51.9, 52.5], "Agropecuária": [1.8, 4.0, 2.8, 9.5]}
    for k, v in dados.items():
        cd.add_series(k, v)
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED_100, Inches(1.1), Inches(2.3), Inches(7.5), Inches(4.2), cd)
    ch = style_chart(gf.chart, [GREEN, GREEN2, GREEN3, GOLD, GOLD2])
    ch.plots[0].gap_width, ch.plots[0].overlap = 50, 100
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0%', False
    card(s, 9.1, 2.1, 3.35, 1.3, fill=CARD_HI)
    text(s, 9.4, 2.25, 2.9, 0.6, "68,6%", size=32, bold=True, color=GOLD, font=HEAD)
    text(s, 9.4, 2.9, 2.9, 0.4, "do emprego do Agreste está em serviços", size=11, color=BODY)
    text(s, 9.1, 3.65, 3.35, 3.0,
         [[("Serviços lideram em todas: ", {}), ("64,7%", {"bold": True}), (" no Leste, ", {}), ("52,5%", {"bold": True}),
           (" no Oeste e ", {}), ("51,9%", {"bold": True}), (" no Central.", {})],
          "O comércio avançou em todas as mesorregiões; no Agreste, cresceu cerca de 72,4% entre 2007 e 2017.",
          "A agropecuária mantém peso alto no Oeste e ganha espaço relativo no Agreste."], size=13, color=BODY, spacing=8)
    fonte(s, "Fonte: RAIS/MTE 2017, via Alves, Lima Júnior e Pereira (2019). Serviços conforme o texto; demais setores lidos do gráfico (aprox.).")


def vocacoes(prs):
    s = base(prs, "ANÁLISE · QUOCIENTE LOCACIONAL 2017", "O QL revela quatro vocações territoriais", notes=(
        "QL por setor e mesorregião sobre a RAIS 2017. O Oeste tem base ampla com agropecuária expressiva (QL 2,986). "
        "O Central polariza na indústria (1,896). O Agreste se especializa em serviços e agro; o Leste, em construção e serviços. "
        "Só os dois valores citados são exatos; os demais foram lidos do gráfico."))
    card(s, 0.9, 2.1, 7.9, 4.55)
    cd = CategoryChartData()
    cd.categories = ["Indústria", "Construção civil", "Comércio", "Serviços", "Agropecuária"]
    ql = {"Oeste": [1.09, 1.09, 1.11, 0.85, 2.986], "Central": [1.896, 0.65, 1.09, 0.85, 0.72],
          "Agreste": [0.65, 0.74, 0.90, 1.13, 1.15], "Leste": [0.90, 1.06, 0.99, 1.06, 0.48]}
    for k, v in ql.items():
        cd.add_series(k, v)
    gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1.1), Inches(2.3), Inches(7.5), Inches(4.2), cd)
    ch = style_chart(gf.chart, [GREEN, GREEN2, GOLD, GREEN3])
    ch.plots[0].gap_width, ch.plots[0].overlap = 80, -5
    ch.value_axis.maximum_scale, ch.value_axis.minimum_scale = 3.0, 0
    ch.value_axis.tick_labels.number_format, ch.value_axis.tick_labels.number_format_is_linked = '0.0', False
    for i, (num, lab, col) in enumerate([("2,986", "QL da agropecuária no Oeste", GOLD), ("1,896", "QL da indústria no Central", GREEN)]):
        y = 2.1 + i * 1.55
        card(s, 9.1, y, 3.35, 1.3, fill=CARD_HI)
        text(s, 9.4, y + 0.15, 2.9, 0.6, num, size=32, bold=True, color=col, font=HEAD)
        text(s, 9.4, y + 0.8, 2.9, 0.4, lab, size=11, color=BODY)
    text(s, 9.1, 5.25, 3.35, 1.4, "QL > 1 marca a vocação: agro e base ampla no Oeste, indústria no Central, serviços e agro no Agreste, construção e serviços no Leste.",
         size=13, color=BODY)
    fonte(s, "Fonte: RAIS/MTE 2017, via Alves, Lima Júnior e Pereira (2019). QL do Oeste (agro) e do Central (indústria) exatos; demais lidos do gráfico (aprox.).")


def perfis(prs):
    s = base(prs, "RESULTADOS · PERFIS COMPETITIVOS", "Uma economia espacialmente heterogênea", notes=(
        "Síntese dos quatro perfis competitivos que os índices revelam. Leste centraliza o dinamismo metropolitano e "
        "terciário; o interior (Oeste e Central) mostra reorganização produtiva consistente; o Agreste é agro."))
    ps = [("LESTE", "Metrópole terciária", "Serviços acima de 80% do VAB e construção civil. Centro polarizador: migração pendular e demanda de mão de obra.", "Potencial: adensar serviços avançados; desafio de equidade na renda gerada."),
          ("OESTE", "Segundo polo, o mais dinâmico", "Especialização e atração em comércio, serviços e indústria extrativa, petróleo e energias.", "Potencial: desenvolvimento autônomo e endógeno, menos dependente da capital."),
          ("CENTRAL", "Elo entre litoral e semiárido", "Transformação de minerais não metálicos (cerâmica estrutural) e comércio em crescimento acelerado.", "Potencial: elo logístico e de apoio urbano entre o litoral e o semiárido."),
          ("AGRESTE", "Base agropecuária", "Indicadores elevados na agropecuária (QL expressivo no primário) e serviços de apoio básico.", "Potencial: agricultura familiar moderna, cadeias curtas e integração com a metrópole.")]
    for i, (n, h, d, p) in enumerate(ps):
        x = 0.9 + i * 2.93
        card(s, x, 2.1, 2.75, 4.55)
        text(s, x + 0.25, 2.35, 2.3, 0.3, n, size=12, bold=True, color=KICKER)
        text(s, x + 0.25, 2.65, 2.3, 0.8, h, size=17, bold=True, color=INK, font=HEAD)
        text(s, x + 0.25, 3.55, 2.3, 1.5, d, size=12, color=BODY)
        text(s, x + 0.25, 5.15, 2.3, 1.4, p, size=12, color=GREEN, bold=True)
    fonte(s, "Fonte: Alves, Lima Júnior e Pereira (2019); Maia e Clementino (2025).")


def investir(prs):
    s = base(prs, "PROPOSTA · VOCAÇÕES", "Onde investir primeiro: quatro frentes", notes=(
        "A prioridade não é atrair plantas avulsas, e sim adensar as cadeias que os dados locacionais já comprovam. "
        "Estratégia: adensamento vertical e conexões intrarregionais."))
    text(s, 0.9, 1.95, 11.5, 0.5, "A prioridade econômica não é atrair plantas avulsas, mas adensar as cadeias comprovadas por dados locacionais.",
         size=15, color=BODY)
    fr = [("01", "Oeste", "Agroindústria de fruticultura irrigada, logística salineira, beneficiamento de petróleo e fornecedores de máquinas."),
          ("02", "Central", "Cadeia têxtil e mineral (scheelita e cerâmica vermelha), comércio atacadista e serviços especializados de manutenção."),
          ("03", "Agreste", "Modernização avícola e laticínios, beneficiamento alimentício, comércio vicinal e polos de confecção local."),
          ("04", "Leste", "Construção civil tecnificada, economia do turismo, logística portuária, serviços corporativos de TI e saúde de alta complexidade.")]
    for i, (n, h, d) in enumerate(fr):
        x = 0.9 + i * 2.93
        card(s, x, 2.7, 2.75, 3.2, fill=CARD_HI if i % 2 else CARD)
        text(s, x + 0.25, 2.9, 1.0, 0.4, n, size=20, bold=True, color=GOLD, font=HEAD)
        text(s, x + 0.25, 3.35, 2.3, 0.4, h, size=18, bold=True, color=INK, font=HEAD)
        text(s, x + 0.25, 3.85, 2.3, 1.9, d, size=12, color=BODY)
    pill(s, 0.9, 6.15, 6.3, 0.5, "Estratégia: adensamento vertical e conexões intrarregionais", fill=GREEN, color=BG)
    fonte(s, "Fonte: síntese a partir de Alves, Lima Júnior e Pereira (2019) e Maia e Clementino (2025).")


def conclusao(prs):
    s = base(prs, "CONCLUSÃO", "Converter especialização em crescimento compartilhado", dark=True, notes=(
        "Quatro passos para transformar vocação em crescimento compartilhado. Fechar com a conclusão sintética: "
        "economia heterogênea, Leste terciário, interior em reorganização; política regional deve apoiar APLs "
        "emergentes e mitigar desigualdades de apropriação de renda."))
    passos = ["Mapear municípios e setores com QL alto, participação relevante e escala mínima.",
              "Priorizar infraestrutura, crédito, qualificação e inovação para cada vocação.",
              "Conectar empresas âncora a fornecedores locais e instituições de ensino.",
              "Acompanhar emprego, renda apropriada, diversificação e encadeamentos a cada ciclo."]
    for i, p in enumerate(passos):
        x, y = 0.9 + (i % 2) * 5.9, 2.15 + (i // 2) * 1.5
        text(s, x, y, 0.6, 0.5, str(i + 1), size=28, bold=True, color=GOLD, font=HEAD)
        text(s, x + 0.65, y + 0.08, 5.0, 1.2, p, size=15, color=BG)
    card(s, 0.9, 5.3, 11.55, 1.35, fill="1F4238")
    text(s, 1.2, 5.5, 10.95, 1.0,
         [[("Conclusão sintética. ", {"bold": True, "color": GOLD}),
           ("O RN tem uma economia espacialmente heterogênea: o Leste centraliza o dinamismo metropolitano e terciário; "
            "Oeste e Central mostram reorganização produtiva consistente. A política regional deve apoiar APLs emergentes "
            "e mitigar as desigualdades de apropriação de renda entre regiões.", {})]], size=14, color=BG)
    text(s, 0.9, 6.9, 6.0, 0.3, "Obrigada · perguntas", size=12, color=GREEN3)


def referencias(prs):
    s = base(prs, "", "Referências", notes="Referências conforme o trabalho escrito; conferir ABNT antes da entrega.")
    refs = ["ALVES, D. F.; LIMA JÚNIOR, F. do O' de; PEREIRA, W. E. N. Disparidades locacionais na estrutura produtiva e fragmentação territorial: uma análise das mesorregiões do Rio Grande do Norte. Revista Estudo & Debate, Lajeado, v. 26, n. 3, p. 69–86, 2019. DOI: 10.22410/issn.1983-036X.v2613a2019.2093.",
            "CROCCO, M. A.; GALINARI, R.; SANTOS, F.; LEMOS, M. B.; SIMÕES, R. Metodologia de identificação de aglomerações produtivas locais. Nova Economia, Belo Horizonte, v. 16, n. 2, p. 211–241, maio/ago. 2006.",
            "MAIA, C. M.; CLEMENTINO, M. do L. M. Análise da estrutura produtiva regional dos polos da região metropolitana de Natal/RN. COLÓQUIO – Revista do Desenvolvimento Regional, Taquara/RS, v. 22, n. 3, p. 61–84, jul./set. 2025.",
            "RAIS/MTE. Relação Anual de Informações Sociais, 2007 e 2017. Brasília: Ministério do Trabalho. IBGE. Contas Regionais e divisão territorial em mesorregiões."]
    for i, r in enumerate(refs):
        card(s, 0.9, 2.1 + i * 1.12, 11.55, 0.98)
        text(s, 1.2, 2.3 + i * 1.12, 10.95, 0.7, r, size=13, color=BODY)


if __name__ == "__main__":
    with zipfile.ZipFile(DOCX) as z:
        mapa = z.extract("word/media/image6.png", path=tempfile.mkdtemp())
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    capa(prs); territorio(prs, mapa); teoria(prs); metodo(prs); ql(prs); emprego(prs); setorial(prs)
    vocacoes(prs); perfis(prs); investir(prs); conclusao(prs); referencias(prs)
    prs.save(OUT)
    chk = Presentation(OUT)
    assert len(chk.slides) == 12
    txt = "\n".join(sh.text_frame.text for sl in chk.slides for sh in sl.shapes if sh.has_text_frame)
    assert "401.392" in txt and "2,986" in txt and "ALVES" in txt
    print(f"ok: {OUT} com {len(chk.slides)} slides")
