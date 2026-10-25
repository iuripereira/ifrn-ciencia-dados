#!/usr/bin/env bash
# Publica uma disciplina encerrada no portfólio público: copia só o que está versionado aqui,
# menos o .publicignore, e faz 1 commit no clone do portfólio em .public/. Uso: ./publicar.sh POS.NNNN
set -euo pipefail

cd "$(dirname "$0")"
codigo="${1:?uso: ./publicar.sh POS.NNNN}"
portfolio="${PORTFOLIO:-.public}"
pasta=$(ls -d "$codigo"-*/ 2>/dev/null | head -1) || true
[[ -n "$pasta" ]] || { echo "pasta $codigo-* não encontrada" >&2; exit 1; }
[[ -d "$portfolio/.git" ]] || { echo "clone do portfólio não encontrado em $portfolio (git clone git@github.com:iuripereira/ifrn-ciencia-dados-portfolio.git .public)" >&2; exit 1; }
pasta="${pasta%/}"

# Só arquivos rastreados pelo git: .gitignore já filtrou pdf/zip/checkpoints.
lista=$(mktemp); trap 'rm -f "$lista"' EXIT
git ls-files -- "$pasta" > "$lista"
[[ -s "$lista" ]] || { echo "$pasta não tem arquivos versionados" >&2; exit 1; }

echo "== simulação =="; rsync -an --files-from="$lista" --exclude-from=.publicignore --out-format='%n' ./ "$portfolio/"
read -rp "Publicar $pasta em $portfolio? [s/N] " ok
[[ "$ok" == [sS] ]] || exit 0

# Limpa o destino antes: rsync com --files-from não apaga o que saiu da origem.
rm -rf "${portfolio:?}/$pasta"
rsync -a --files-from="$lista" --exclude-from=.publicignore ./ "$portfolio/"
git -C "$portfolio" add -- "$pasta" environment.yml
git -C "$portfolio" commit -m "feat: publica $codigo ($(date +%Y).$(( $(date +%-m) > 6 ? 2 : 1 )))"
echo "commit feito em $portfolio — revise e dê git push."
