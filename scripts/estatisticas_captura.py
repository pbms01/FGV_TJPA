"""Captura a página inteira e só a figura (#fig) de uma página de estatística, em 2x, para conferir o
render e para slide. Requer playwright e Chrome. Uso, da raiz do repo:
  python3 scripts/estatisticas_captura.py docs/estatisticas/paginas/X.html /tmp/X_inteira.png docs/estatisticas/graficos/X.png light
"""
import os
import sys, asyncio
from playwright.async_api import async_playwright
async def main(src, out_full, out_fig, scheme):
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await b.new_page(viewport={"width": 960, "height": 900}, device_scale_factor=2, color_scheme=scheme)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        await pg.goto("file://" + os.path.abspath(src))
        await pg.wait_for_timeout(300)
        await pg.screenshot(path=out_full, full_page=True)
        await pg.locator("#fig").screenshot(path=out_fig)
        print("erros JS:", errs)
        await b.close()
asyncio.run(main(*sys.argv[1:5]))
