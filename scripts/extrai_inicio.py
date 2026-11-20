# Extrai as primeiras páginas de PDFs baixados (procedimento policial, denúncia) e devolve
# texto com CPF/CNPJ trocados por hash com sal. OCR só nas páginas com menos de 500
# caracteres, o corte que separou documento-imagem de textual na amostra da skill de teses.
# O texto bruto vai para dados/bruto/, que é apagado ao fim da coleta; o que persiste é a
# planilha de codificação, sem nomes.
import argparse, hashlib, os, re, secrets, subprocess, sys

SAL_F = "/home/claude/dados/.sal"
if not os.path.exists(SAL_F):
    open(SAL_F, "w").write(secrets.token_hex(16)); os.chmod(SAL_F, 0o600)
SAL = open(SAL_F).read().strip()
def h(x):
    return "ID_" + hashlib.sha256((SAL + re.sub(r"\D", "", x)).encode()).hexdigest()[:12]
DOC = re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b|\b\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}\b")

def pagina(pdf, n, lang):
    t = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), "-layout", pdf, "-"],
                       capture_output=True, text=True).stdout
    if len(t.strip()) >= 500:
        return t, "texto"
    base = f"/tmp/ocr_{os.getpid()}_{n}"
    subprocess.run(["pdftoppm", "-f", str(n), "-l", str(n), "-r", "200", "-png", pdf, base], capture_output=True)
    png = next((f"/tmp/{f}" for f in os.listdir("/tmp") if f.startswith(os.path.basename(base))), None)
    if not png:
        return t, "vazio"
    o = subprocess.run(["tesseract", png, "-", "-l", lang], capture_output=True, text=True).stdout
    os.remove(png)
    return o, "ocr"

p = argparse.ArgumentParser()
p.add_argument("pdf"); p.add_argument("--paginas", type=int, default=4)
p.add_argument("--max-chars", type=int, default=6000); p.add_argument("--lang", default="por")
a = p.parse_args()
total = subprocess.run(["pdfinfo", a.pdf], capture_output=True, text=True).stdout
npag = int(re.search(r"Pages:\s+(\d+)", total).group(1)) if "Pages:" in total else a.paginas
saida, modos = [], []
for n in range(1, min(a.paginas, npag) + 1):
    t, m = pagina(a.pdf, n, a.lang); saida.append(t); modos.append(m)
txt = DOC.sub(lambda m: h(m.group()), "\n".join(saida))
print(f"[paginas_pdf={npag} lidas={len(modos)} modos={','.join(modos)}]")
print(txt[:a.max_chars])
