# Utilitário da coleta na conversa. Rodar de dentro de fgv_tjpa.
#   python ../pipe.py next                 -> próximo número (metas: INV censo, CL 50, FE até 200)
#   python ../pipe.py ids MAPA             -> IDs (repetidos) das partes da peça inicial; guarda em /tmp/cur.json
#   python ../pipe.py grava LOTE           -> grava texto, manifesto e status do processo corrente
#   python ../pipe.py status NUM STATUS "detalhe"
import sys, os, json, math, re, csv, hashlib
from datetime import datetime, timezone
sys.path.insert(0, 'scripts'); import codex_denuncias as c

CUR = '/tmp/cur.json'
agora = lambda: datetime.now(timezone.utc).isoformat(timespec='seconds')

def ler(f):
    s = open(f, encoding='utf-8').read()
    if s.lstrip().startswith('['):
        v, _ = json.JSONDecoder().raw_decode(s.lstrip()); s = '\n'.join(b.get('text', '') for b in v)
    return s

def estrato(num):
    for a in c.ler_csv(c.AMOSTRA):
        if a['numero'] == num: return a['estrato']

def status(num, st, docs=0, custo=1, det=''):
    linha = dict(numero=num, estrato=estrato(num), status=st, docs=docs, chamadas_estimadas=custo, quando=agora(), detalhe=det)
    c.anexar(c.STATUS, list(linha), linha)

cmd = sys.argv[1]
if cmd == 'next':
    amostra = c.ler_csv(c.AMOSTRA); feitos = {s['numero']: s for s in c.ler_csv(c.STATUS)}
    por, ok = c.plano(amostra, feitos)
    for e in ('INV', 'CL', 'FE'):
        cota = None if e == 'INV' else c.COTA_CL if e == 'CL' else c.TOTAL_ALVO - ok['INV'] - ok['CL']
        if cota is not None and ok[e] >= cota: continue
        pend = [a for a in por[e] if a['numero'] not in feitos]
        if pend:
            print(pend[0]['numero'], e, 'ordem', pend[0]['ordem_no_estrato'], '| obtidos', ok); break
    else:
        print('FIM', ok)
elif cmd == 'ids':
    s = ler(sys.argv[2]); num = re.search(r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}', s).group(0)
    ps = c.pecas_iniciais(s); pul = []
    # categoria "Peça Inicial" às vezes traz folhas do inquérito junto: havendo denúncia nomeada, fica só ela (e aditamentos),
    # antes do descarte de partes sem texto, para não trocar a denúncia escaneada por folha nativa do inquérito
    den = [p for p in ps if re.search(r'Den\w*ncia|Aditamento', p['nome'], re.I)]
    if den and len(den) < len(ps):
        pul += [p for p in ps if p not in den]; ps = den
    if any(not p['sem_texto'] for p in ps):
        # parte sem texto do mesmo protocolo de uma parte nativa é página da própria peça (vai por OCR); de outro protocolo, descarta
        nat = {p['pje'].rpartition('_')[0] for p in ps if not p['sem_texto']}
        pul += [p for p in ps if p['sem_texto'] and p['pje'].rpartition('_')[0] not in nat]; ps = [p for p in ps if p not in pul]
    vis = set(); ded = []
    # a mesma parte às vezes aparece repetida no acervo (mesmo código PJe, IDs e até ordinais distintos):
    # fica uma por código PJe, preferindo a de texto nativo à cópia sem texto
    for p in sorted(ps, key=lambda p: p['sem_texto']):
        (pul if p['pje'] in vis else ded).append(p); vis.add(p['pje'])
    ps = sorted(ded, key=lambda p: (p['protocolo'], p['parte']))
    cand = False
    if not ps:
        # denúncia nomeada como tal mas classificada fora da categoria Peça Inicial (ex.: "Outros")
        ent = [m.groups() for m in re.finditer(r'\[(\d+)\] (\S+) \| (Den\w*ncia[^|\n]*) \| ([^\n]*)\n\s+ID: (\S+) \| PJe: (\S+)', s)]
        vis2 = set(); ent = [e for e in ent if not (e[4] in vis2 or vis2.add(e[4]))]
        if ent:
            ps = [{'ordinal': int(x[0]), 'data': x[1], 'nome': x[2], 'id': x[4], 'pje': x[5], 'protocolo': x[5].rpartition('_')[0],
                   'parte': int(x[5].rpartition('_')[2] or 0) if x[5].rpartition('_')[2].isdigit() else 0,
                   'sem_texto': 'sem texto' in x[3]} for x in ent]
            if any(not p['sem_texto'] for p in ps): ps = [p for p in ps if not p['sem_texto']]
            vis = set(); ps = [p for p in ps if not (p['pje'] in vis or vis.add(p['pje']))]
            ps.sort(key=lambda p: (p['protocolo'], p['parte']))
    if not ps:
        # reserva: peça do MP mais próxima antes da decisão de recebimento da denúncia
        ent = [m.groups() for m in re.finditer(r'\[(\d+)\] (\S+) \| ([^|\n]+) \| ([^\n]*)\n\s+ID: (\S+) \| PJe: (\S+)(?:\n\s+Mov: ([^\n]*))?', s)]
        rec = [e for e in ent if e[6] and 'Recebida a den' in e[6]]
        if rec:
            o = min(int(e[0]) for e in rec)
            cs = [e for e in ent if o - 60 <= int(e[0]) < o and e[5].startswith('PG') and re.search(r'Manifesta[^|]*MP|Manifesta[^|]*Minist|Cota|Peti', e[2])
                  and int((re.search(r'(\d+) chars', e[3]) or [0, 0])[1]) >= 1000]
            if cs:
                e = max(cs, key=lambda e: int(e[0])); cand = True; proto = e[5].rpartition('_')[0]; vis = set()
                grupo = [x for x in ent if x[5].rpartition('_')[0] == proto and not (x[4] in vis or vis.add(x[4]))]
                ps = sorted([{'ordinal': int(x[0]), 'data': x[1], 'nome': x[2], 'id': x[4], 'pje': x[5], 'protocolo': proto,
                       'parte': int(x[5].rpartition('_')[2] or 0), 'sem_texto': 'sem texto' in x[3]} for x in grupo], key=lambda p: p['parte'])
    if not ps:
        status(num, 'sem_peca_inicial', 0, 1); print('SEM PECA INICIAL', num); sys.exit()
    json.dump({'numero': num, 'partes': ps, 'puladas': [p['id'] for p in pul], 'candidata': cand}, open(CUR, 'w'))
    tot = 0
    for p in ps:
        m = re.search(r'\[%d\] %s \| [^\n]*?(\d+) chars' % (p['ordinal'], p['data']), s); tot += int(m.group(1)) if m and int(m.group(1)) else 2000
    if cand: print('CANDIDATA (sem peça inicial no mapa):', ps[0]['ordinal'], ps[0]['nome'], file=sys.stderr)
    # peça sem texto indexado (OCR) tem tamanho desconhecido: repete o máximo para garantir a persistência do resultado
    rep = 50 // len(ps) if any(p['sem_texto'] for p in ps) else max(1, min(50 // len(ps), math.ceil(75000 / max(tot, 1))))
    print(num, len(ps), 'partes', tot, 'chars, rep', rep, file=sys.stderr)
    print(json.dumps([p['id'] for p in ps] * rep))
elif cmd == 'grava':
    cur = json.load(open(CUR)); num = cur['numero']; textos = c.separa_lote(ler(sys.argv[2])); n = 0
    if cur.get('candidata'):
        t0 = ' '.join(textos.get(p['id'], '') for p in cur['partes'])
        if not re.search(r'denuncio|ofere[cç]\w* (a presente )?den[úu]ncia|incurs[oa]s? n|como incurs', t0, re.I):
            status(num, 'sem_peca_inicial', 0, 2, 'candidata lida não era denúncia: ' + cur['partes'][0]['nome']); print('candidata não é denúncia', num); sys.exit()
    for k, p in enumerate(cur['partes'], 1):
        corpo = textos.get(p['id'])
        if not corpo or len(corpo.strip()) < 40: continue
        assert '?t=' not in corpo
        d = os.path.join(c.DIR_TEXTOS, num); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, '%02d_%s.txt' % (k, p['id'])), 'w', encoding='utf-8').write(corpo)
        c.anexar(c.MANIFESTO, ['numero','estrato','documento_id','parte','nome','pje','data','procedencia','chars','sha256','lido_em'],
          dict(numero=num, estrato=estrato(num), documento_id=p['id'], parte=k, nome=p['nome'], pje=p['pje'], data=p['data'],
               procedencia=c.procedencia(corpo), chars=len(corpo), sha256=hashlib.sha256(corpo.encode()).hexdigest(), lido_em=agora()))
        n += 1
    det = ('sem texto, não lidas: ' + ' '.join(cur['puladas'])) if cur['puladas'] else ''
    if cur.get('candidata'): det = ('denúncia juntada como ' + cur['partes'][0]['nome'] + '; ' + det).strip('; ')
    status(num, 'ok' if n else 'sem_texto', n, 2, det)
    # capitulação da denúncia, para conferir o estrato
    t = ' '.join(open(os.path.join(c.DIR_TEXTOS, num, f), encoding='utf-8').read() for f in sorted(os.listdir(os.path.join(c.DIR_TEXTOS, num)))) if n else ''
    cap = re.findall(r'(?:incurs[oa]s?|denuncio)[^.]{0,200}', t.replace('\n', ' '), re.I)
    print('gravado', num, n, 'partes', len(t), 'chars |', (cap[-1][:160] if cap else 'capitulação não localizada'))
elif cmd == 'status':
    status(sys.argv[2], sys.argv[3], 0, 1, sys.argv[4] if len(sys.argv) > 4 else ''); print('status', sys.argv[2], sys.argv[3])
