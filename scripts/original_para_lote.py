#!/usr/bin/env python3
"""Converte o PDF original de uma peça (baixado pelo link do pdpj_get_documento_url) no formato
de lote do pdpj_read_documentos_batch, para que `pipe_tjpa.py grava ARQUIVO` o trate como
qualquer leitura do Codex. Só o texto vai ao repositório; o PDF fica fora dele.

Uso: original_para_lote.py SAIDA NUMERO:ID:NOME:PDF [NUMERO:ID:NOME:PDF ...]
(PDF pode ser também o .txt de uma peça já gravada, para reentrar no lote.)

Decisões:
- Camada de texto primeiro (pdftotext -layout). Se tiver menos de 200 caracteres úteis por
  página, o PDF é imagem e passa por OCR (pdftoppm a 300 dpi + tesseract -l por).
- O marcador de procedência diz de onde veio o texto ("parser pdftotext do original" ou
  "OCR tesseract do original"), porque o codex_denuncias.procedencia() o registra no manifesto
  e a extração precisa saber que o texto do OCR é ruidoso.
- A linha "Original:" leva só /doc/<numero>/<id>, sem o token ?t=, que o separa_lote usa para
  achar o ID e que o grava proíbe no corpo.
"""
import os
import subprocess
import sys
import tempfile


def texto_html(arq):
    import html
    import re
    s = open(arq, encoding="utf-8", errors="replace").read()
    s = re.sub(r"(?is)<(script|style).*?</\1>", "", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</tr>|</h\d>", "\n", s)
    return "parser HTML do original", html.unescape(re.sub(r"<[^>]+>", "", s))


def texto_pdf(pdf):
    if pdf.lower().endswith((".html", ".htm")):
        return texto_html(pdf)
    paginas = int(next((l.split()[-1] for l in subprocess.run(
        ["pdfinfo", pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith("Pages:")), "1"))
    camada = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True).stdout
    if len("".join(camada.split())) >= 200 * paginas:
        return "parser pdftotext do original", camada
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "300", "-png", pdf, os.path.join(d, "p")], check=True)
        partes = []
        for img in sorted(os.listdir(d)):
            partes.append(subprocess.run(["tesseract", os.path.join(d, img), "-", "-l", "por"],
                                         capture_output=True, text=True).stdout)
    return "OCR tesseract do original", "\n".join(partes)


def main():
    saida, specs = sys.argv[1], sys.argv[2:]
    blocos = []
    for spec in specs:
        numero, uid, nome, pdf = spec.split(":", 3)
        if pdf.endswith(".txt"):
            # peça já gravada na primeira passada (textos/<trib>/...): entra de novo no lote
            # com o marcador original, para o grava não rebaixar a contagem do status
            txt = open(pdf, encoding="utf-8").read()
            blocos.append("--- %s ---\nOriginal: https://mcp.tecjustica.com/doc/%s/%s\n%s"
                          % (nome, numero, uid, txt))
            print(numero, uid, "texto já gravado", len(txt), "chars", file=sys.stderr)
            continue
        fonte, txt = texto_pdf(pdf)
        blocos.append("--- %s ---\nOriginal: https://mcp.tecjustica.com/doc/%s/%s\n[%s]\n\n%s\n"
                      % (nome, numero, uid, fonte, txt))
        print(numero, uid, fonte, len(txt), "chars", file=sys.stderr)
    open(saida, "w", encoding="utf-8").write("\n".join(blocos))


if __name__ == "__main__":
    main()
