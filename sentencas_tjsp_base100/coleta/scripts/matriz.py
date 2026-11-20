"""Roda a matriz de consultas da CJPG (famílias de conduta x janelas anuais).

Decisões:
- Classes criminais 8657 (ordinário) e 8803 (sumário): corta o cível bancário.
- Janelas por ano civil de 2022 a 2026; a data do fato é filtrada depois,
  no texto, porque a data de disponibilização não diz quando a conduta ocorreu.
- Consultas por conduta e por artigo convivem: as de conduta evitam que a
  amostra dependa da capitulação; as de artigo pegam o que os termos não pegam.
- Grava um JSONL por (consulta, ano); reexecutar pula o que já existe.
"""
import json, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from cjpg import consulta

CLASSES = "8657,8803"
ANOS = {
    "2022": ("01/01/2022", "31/12/2022"),
    "2023": ("01/01/2023", "31/12/2023"),
    "2024": ("01/01/2024", "31/12/2024"),
    "2025": ("01/01/2025", "31/12/2025"),
    "2026": ("01/01/2026", "20/11/2026"),
}
MATRIZ = [
    ("f01_falsa_central", '"falsa central" OU "central de atendimento" OU "central de segurança"', 2),
    ("f02_whatsapp", '"WhatsApp clonado" OU "whatsapp foi clonado" OU "clonagem do WhatsApp" OU "clonou o WhatsApp" OU "perfil falso"', 2),
    ("f03_link", '"phishing" OU "link falso" OU "página falsa" OU "site falso" OU "link malicioso"', 2),
    ("f04_remoto", '"acesso remoto" OU "AnyDesk" OU "TeamViewer" OU "programa malicioso" OU "malware"', 2),
    ("f05_chip", '"SIM swap" OU "troca de chip" OU "clonagem de chip" OU "chip clonado" OU "portabilidade numérica"', 2),
    ("f08_biometria", '"biometria facial" OU "reconhecimento facial" OU "prova de vida"', 2),
    ("f09_anuncio", '"anúncio falso" OU "falso anúncio" OU "Marketplace" OU "falsa corretora" OU "falso investimento"', 2),
    ("f10_insider", '"acesso privilegiado" OU "sistema interno" OU "credenciais de acesso"', 2),
    ("fia", '"inteligência artificial" OU "deepfake" OU "voz sintética" OU "clonagem de voz"', 2),
    ("f01b_motoboy", '"motoboy" E "cartão"', 2),
    ("f10b_aproximacao", '"aproximação" E "cartão" E "dispositivo eletrônico"', 2),
    ("f10c_caixa", '"caixa eletrônico" E "dispositivo eletrônico"', 2),
    ("f05b_conta", '"Instagram" E ("invadida" OU "hackeada" OU "invadiu")', 2),
    ("f06b_domestica", '"dispositivo informático" E "11.340"', 2),
    ("f08b_laranja", '"conta laranja" OU "cessão de conta" OU "cedeu sua conta" OU "§ 2º, inciso VII"', 2),
    ("f02c_parente", '"se passando por" E "WhatsApp" E "PIX"', 3),
    ("f05c_codigo", '"código de verificação" OU "conta do WhatsApp" OU "clonaram o WhatsApp"', 2),
    ("f06c_familia", '"aplicativo do banco" E ("neto" OU "filho" OU "cuidadora" OU "companheiro")', 2),
    ("f06d_celular", '"celular" E "invadiu" E ("companheira" OU "namorada" OU "ex-mulher")', 2),
    ("f07c_conta", '"abertura de conta" E ("documento falso" OU "selfie" OU "biometria")', 2),
    ("f09c_insider", '"ex-funcionário" E "sistema"', 2),
    ("f09d_funcionaria", '"funcionária" E "dispositivo eletrônico" E "empresa"', 2),
    ("a154", '"154-A"', 3),
    ("a154b", '"invasão de dispositivo" OU "dispositivo informático"', 3),
    ("a155", '"4º-B"', 3),
    ("a171", '"fraude eletrônica"', 3),
]

if __name__ == "__main__":
    raw = Path(__file__).resolve().parents[1] / "raw"
    raw.mkdir(exist_ok=True)
    resumo = []
    for tag, q, pags in MATRIZ:
        for ano, (ini, fim) in ANOS.items():
            fn = raw / f"{tag}_{ano}.jsonl"
            if fn.exists():
                continue
            for tent in range(3):
                try:
                    total, recs = consulta(q, ini, fim, CLASSES, pags)
                    break
                except Exception as e:
                    print("erro", tag, ano, e, flush=True)
                    time.sleep(10)
            else:
                continue
            with fn.open("w", encoding="utf-8") as f:
                for r in recs:
                    r["_consulta"] = {"tag": tag, "q": q, "ano": ano, "total": total}
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"{tag} {ano}: total={total} baixados={len(recs)}", flush=True)
            time.sleep(1.5)
    print("FIM", flush=True)
