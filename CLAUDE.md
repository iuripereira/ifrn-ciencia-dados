# CLAUDE.md — Especialização em Ciência de Dados (IFRN)

Repo **privado** de trabalho do curso. Não é produto de software: sem ciclo deltaspec (specs, ADRs, debts). O TCC ganha repo próprio quando o tema fechar — só lá cabe `/deltaspec:projeto-init`.

## Convenções

- Uma pasta por disciplina: `POS.NNNN-slug/` (código do SUAP). Dentro, `aula-NN/` para material de aula e `atividade-NN/` para entregas.
- Código em Python; notebooks `.ipynb` rodam no Jupyter local (`conda env create -f environment.yml`, env `ifrn-cd`) ou no Google Colab. O cwd do notebook é a pasta dele: use caminhos relativos a ela.
- Dataset público entra junto da atividade, com a fonte citada no notebook ou num README da pasta.

## O que não entra no git

- Material do professor (`*.pdf`, slides) e pacotes de entrega (`*.zip`) — barrados pelo `.gitignore`.
- Transcrição de conteúdo do AVA/Moodle pode ficar no privado, mas precisa estar no `.publicignore` (ou usar o sufixo `.ava.md`) para não ir ao portfólio.

## Publicação

Repo público: `iuripereira/ifrn-ciencia-dados-portfolio`, clonado em `.public/` (ignorado pelo git daqui via `/.*`). Uma disciplina só é publicada **depois da nota final**, via `./publicar.sh POS.NNNN` — nunca antes do prazo (integridade acadêmica).
