"""Ordena candidatos da fila por família de modo de execução (usado na quarta rodada).

Lê o corpus local e a fila, descarta processos já usados ou rejeitados e fatos anteriores
a 28/05/2021, conta as ocorrências da expressão de cada família nos 4.500 caracteres
seguintes a "Vistos" e lista primeiro os casos com solução divergente da denúncia.
Uso: candidatos_familia.py F01,F02 <quantos> <caracteres do trecho> [processos a pular]
"""
import json, re, sys, csv, unicodedata
sys.path.insert(0,'/home/claude/coleta/scripts')
from extrato import limpa
def norm(s): return unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
FAM={
"F01": r"falsa central|central de (?:atendimento|seguranca|relacionamento)|funcionari[oa]s? do banco|se passando por (?:funcionari|atendente|gerente|preposto)|motoboy|setor de (?:seguranca|fraude)|falso (?:funcionario|gerente|atendente)",
"F02": r"(?:se passando por|fingindo ser|passando-se por|como se fosse) (?:o |a |seu |sua )?(?:filh|sobrinh|net|irma|irmao|pai|mae|marido|espos|parente|amig|genro|nora|cunhad)",
"F03": r"e-?mail (?:falso|fraudulento)|site falso|pagina falsa|link|sms|boleto falso|comprovante (?:falso|de pagamento falso|de pix falso)|falso comprovante",
"F04": r"acesso remoto|anydesk|teamviewer|programa malicioso|instalar (?:um )?aplicativo|instalou (?:um )?aplicativo|espelhamento|controle remoto",
"F05": r"chip|portabilidade|linha telefonica|perfil hackeado|conta (?:do|de) (?:instagram|whatsapp|facebook) (?:foi )?(?:invadida|hackeada|clonada)|whatsapp (?:foi )?clonado|clonagem",
"F06": r"companheir|namorad|ex-?(?:mulher|marido|namorad|companheir)|violencia domestica|cuidador|empregada domestica|enteado|padrasto|madrasta|(?:seu|sua) (?:filh|net|sobrinh|irma|irmao|genro|nora|tio|tia)",
"F07": r"biometria|selfie|reconhecimento facial|prova de vida|abertura de conta|conta (?:aberta )?em nome d|emprestimo (?:em nome|consignado|pessoal)|cartao em nome",
"F08": r"anuncio|marketplace|olx|venda de (?:veiculo|carro|moto|celular)|intermediari|aluguel|cedeu (?:a |sua )?conta|conta (?:laranja|de passagem)|emprestou (?:a |sua )?conta",
"F09": r"(?:funcionari|empregad|operador|vendedor|estagiari|caixa)[oa]?s? (?:da|do|de) (?:empresa|banco|loja|agencia|cooperativa|supermercado|instituicao)|acesso (?:privilegiado|ao sistema)|sistema interno|credenciais|login e senha",
"F10": r"maquininha|maquina de cartao|caixa eletronico|terminal (?:bancario|de autoatendimento)|aproximacao|autoatendimento",
}
RXF={k:re.compile(v) for k,v in FAM.items()}
u=json.load(open('/home/claude/coleta/base/usados.json')); used=set(u['base'])|set(u['rej'])
tri={r['processo']:r for r in csv.DictReader(open('/home/claude/coleta/triagem/triagem.csv',encoding='utf-8'))}
fila={r['processo']:r for r in csv.DictReader(open('/home/claude/coleta/triagem/fila.csv',encoding='utf-8'))}
MAP = {"154A": "154-A", "155B": "155§4B", "171A": "171§2A"}
def diverge(r):
    s=r["sol"]
    if any(x in s for x in ("absolvo","desclassifica","extincao","improcedente")): return True
    for t in r["tipos_ab"].split("+"):
        if t in MAP and MAP[t] not in r["arts_disp"]: return True
    return False
RXN = re.compile(r"Consta|Segundo (?:a denúncia|apurado|se apurou)|Narra|Apurou-se|porque|Conforme (?:apurado|narra)", re.I)
fams=sys.argv[1].split(','); n=int(sys.argv[2]); nn=int(sys.argv[3]); skip=set(sys.argv[4].split(',')) if len(sys.argv)>4 else set()
res={f:[] for f in fams}
for line in open('/home/claude/coleta/triagem/corpus.jsonl',encoding='utf-8'):
    r=json.loads(line); p=r['processo']
    if p in used or p in skip or p not in fila or fila[p]['fato']<'2021-05-28': continue
    fr=fila[p]
    if not any(x in fr['tipos_ab'] for x in ('154A','155B','171A','171')): continue
    t=r['texto']; i=max(t.lower().find('vistos'),0); narr=norm(t[i:i+4500])
    for f in fams:
        h=len(RXF[f].findall(narr))
        if h:
            m=RXN.search(t,i+100); k=m.start() if m else i
            res[f].append((diverge(fr), h, int(fr['chars']), p, (r.get('Comarca') or '')[:12], fr['tipos_ab'], fr['sol'][:22], limpa(t[k:k+nn]).replace('\n',' ')))
for f in fams:
    L=sorted(res[f], key=lambda x:(-x[0], -x[1], -x[2]))[:n]
    print('########',f,len(res[f]))
    for x in L: print(('D' if x[0] else 'C'), x[1], x[3], x[4], x[5], x[6], '|', x[7]); 
