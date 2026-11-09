# Microdados — Dicionário de Dados (ENEM 2025 RN)

### Dicionário dos Microdados — ENEM 2025 / RN

#### RESULTADOS_2025_RN.csv (~16 MB, separador ;, codificação latin1)

Um registro por participante que concluiu o ensino médio em escola do RN. ~30.450 linhas. Principais colunas:

   Coluna |  Descrição |
    `CO_ESCOLA` |  Código da escola (chave para junção com o catálogo) |
  `NO_MUNICIPIO_ESC` |  Município da escola |
  `TP_DEPENDENCIA_ADM_ESC` |  Dependência administrativa: 1=Federal, 2=Estadual, 3=Municipal, 4=Privada |
  `TP_PRESENCA_CN/CH/LC/MT` |  Presença em cada prova (0=falta, 1=presença, 2=eliminado) |
  `NU_NOTA_CN` |  Nota em Ciências da Natureza |
  `NU_NOTA_CH` |  Nota em Ciências Humanas |
  `NU_NOTA_LC` |  Nota em Linguagens e Códigos |
  `NU_NOTA_MT` |  Nota em Matemática |
  `NU_NOTA_REDACAO` |  Nota da redação (0–1000) e notas por competência (COMP1–COMP5) |

Notas vazias indicam ausência do participante na prova.

#### catalogo_escolas_rn.csv (~220 KB, separador vírgula, codificação utf-8)

Catálogo com ~4.938 escolas do RN:

   Coluna |  Descrição |
    `CO_ESCOLA` |  Código da escola |
  `NO_ESCOLA` |  Nome da escola |

#### Origem e licença

Recorte derivado dos Microdados do ENEM, publicados pelo INEP como dados abertos (gov.br/inep — dados abertos). Uso educacional. Os dados são anonimizados pelo INEP; ainda assim, discutiremos na Unidade 5 os cuidados éticos ao publicar rankings de escolas.

⬇️ Os dois arquivos CSV estão anexados nesta seção da Unidade 1.

Última atualização: quinta-feira, 6 ago. 2026, 20:29