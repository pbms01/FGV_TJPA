# Sorteio complementar FE: páginas intercaladas (ponto médio entre páginas originais), embaralhadas com a
# semente 20261120; as 7 primeiras foram lidas no CJPG em 2026-11-20 (total da lista: 1702, antes 1704).
# Em cada página, 2 elegíveis por embaralhamento com a mesma semente, excluídos os já sorteados.
import csv, json, random
L = {  # pagina: [numero, classe, comarca, data, cd_doc, chars, m_fe, cond, abs, assunto, foro, vara]
 36:[["1528251-61.2024.8.26.0050","SÃO PAULO","01/09/2026","1E002F2PR0000-50--78117964",11891,1,1,0,"Estelionato Majorado","Foro Central Criminal Barra Funda","24ª Vara Criminal"],
     ["1500417-67.2024.8.26.0411","Pacaembu","01/09/2026","BF0002JNP0000-411--110583368",12919,1,1,0,"Estelionato","Foro de Pacaembu","2º Vara"],
     ["1500372-17.2024.8.26.0491","Rancharia","01/09/2026","DN0002RIM0000-491--173151668",23268,1,0,0,"Estelionato","Foro de Rancharia","2ª Vara"],
     ["1504678-78.2022.8.26.0562","Santos","01/09/2026","FM000VMDQ0000-562--100182172",23930,1,1,0,"Estelionato","Foro de Santos","5ª Vara Criminal"]],
 77:[["1507261-35.2024.8.26.0281","Itatiba","08/04/2026","7T00064450000-281--117763946",13263,1,1,0,"Estelionato","Foro de Itatiba","Vara Criminal"],
     ["0000207-97.2026.8.26.0483","Presidente Venceslau","08/04/2026","DF0003E670000-483--106225599",19552,1,1,0,"Estelionato","Foro de Presidente Venceslau","2ª Vara"],
     ["1501971-59.2022.8.26.0297","Jales","07/04/2026","8900042LG0000-297--144959771",35057,1,0,0,"Estelionato","Foro de Jales","1ª Vara Criminal"]],
 99:[["1501027-59.2022.8.26.0361","Mogi das Cruzes","28/11/2025","A1000FOCK0000-361--59766148",11603,1,1,0,"Estelionato","Foro de Mogi das Cruzes","1ª Vara Criminal"],
     ["1509002-62.2020.8.26.0019","Americana","28/11/2025","0J0006AYS0000-19--145676082",24996,1,1,0,"Furto Qualificado","Foro de Americana","2ª Vara Criminal"],
     ["1502545-18.2024.8.26.0037","Araraquara","28/11/2025","11000HRFO0000-37--55906568",20316,1,1,0,"Furto","Foro de Araraquara","3ª Vara Criminal"],
     ["1500362-65.2023.8.26.0407","Osvaldo Cruz","27/11/2025","BB00023LY0000-407--103374067",17879,1,1,0,"Estelionato","Foro de Osvaldo Cruz","2ª Vara"],
     ["1500872-29.2022.8.26.0176","Embu das Artes","27/11/2025","4W0005QEL0000-176--123013967",15910,1,1,0,"Estelionato","Foro de Embu das Artes","1ª Vara Cível"],
     ["0006187-73.2024.8.26.0037","Araraquara","26/11/2025","11000HRBO0000-37--55759689",25091,1,1,0,"Receptação","Foro de Araraquara","1ª Vara Criminal"]],
 108:[["1507731-91.2022.8.26.0554","Santo André","14/10/2025","FE000HKJY0000-554--159618370",11750,1,1,0,"Estelionato","Foro de Santo André","3ª Vara Criminal"],
     ["1501858-32.2024.8.26.0040","Araraquara","13/10/2025","140001VMD0000-37--55190121",21807,1,1,0,"Estelionato","Foro de Araraquara","3ª Vara Criminal"],
     ["1538470-70.2023.8.26.0050","SÃO PAULO","10/10/2025","1E002CTMU0000-50--69230442",29762,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","1ª Vara Criminal"],
     ["1500721-73.2025.8.26.0559","São José do Rio Preto","09/10/2025","FJ0007FWT0000-576--97838420",12601,1,1,0,"Estelionato","Foro de São José do Rio Preto","4ª Vara Criminal"],
     ["1500179-30.2022.8.26.0084","Campinas","09/10/2025","2C0003B3A0000-114--143535876",7494,1,1,0,"Estelionato","Foro de Campinas","1ª Vara Criminal"],
     ["1535484-46.2023.8.26.0050","SÃO PAULO","09/10/2025","1E002CO3P0000-50--69234652",13285,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","5ª Vara Criminal"],
     ["1035419-84.2024.8.26.0564","São Bernardo do Campo","08/10/2025","FO000NT030000-564--159055047",24106,1,1,0,"Estelionato","Foro de São Bernardo do Campo","2ª Vara Criminal"]],
 140:[["1515211-17.2021.8.26.0050","SÃO PAULO","28/11/2024","1E0026W4D0000-50--62314424",15484,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","18ª Vara Criminal"],
     ["1507403-04.2024.8.26.0228","SÃO PAULO","27/11/2024","6C0004DEI0000-50--59354256",15531,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","14ª Vara Criminal"],
     ["1502912-87.2022.8.26.0562","Santos","26/11/2024","FM000TY610000-562--83557267",8184,1,1,0,"Estelionato","Foro de Santos","3ª Vara Criminal"],
     ["1506637-51.2021.8.26.0358","Mirassol","25/11/2024","9Y00034G10000-358--89122191",39001,1,1,0,"Estelionato","Foro de Mirassol","1ª Vara"],
     ["1501202-71.2022.8.26.0161","Diadema","20/11/2024","4H0008SKF0000-161--102714644",49821,1,0,0,"Estelionato","Foro de Diadema","1ª Vara Criminal"],
     ["1500003-28.2022.8.26.0027","Iacanga","17/11/2024","0R0000OCO0000-27--50002798",12737,1,1,0,"Estelionato","Foro de Iacanga","Vara Única"]],
 144:[["1520090-13.2024.8.26.0228","SÃO PAULO","02/10/2024","6C0004SDH0000-50--61063253",13239,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","18ª Vara Criminal"],
     ["1523962-56.2022.8.26.0050","SÃO PAULO","30/09/2024","1E0029P9C0000-50--54159927",15216,1,1,0,"Estelionato","Foro Central Criminal Barra Funda","9ª Vara Criminal"],
     ["1510860-11.2021.8.26.0564","São Bernardo do Campo","27/09/2024","FO000HPGY0000-564--140474483",40612,1,1,0,"Fato Atípico","Foro de São Bernardo do Campo","5ª Vara Criminal"],
     ["1501175-19.2022.8.26.0572","São Joaquim da Barra","25/09/2024","FW0002NW80000-572--102238876",33117,1,0,0,"Estelionato","Foro de São Joaquim da Barra","2ª Vara"],
     ["1501575-51.2022.8.26.0081","Adamantina","23/09/2024","290001MSD0000-81--90126003",17168,1,1,0,"Estelionato","Foro de Adamantina","3ª Vara"]],
 171:[]}
ORDEM_PAGINAS = [171, 99, 108, 144, 77, 36, 140]
A = 'dados/cjpg/amostra_tjsp.csv'
rows = list(csv.DictReader(open(A, encoding='utf-8'))); campos = list(rows[0].keys())
ja = {r['numero'] for r in rows}
meta = json.load(open('dados/cjpg/sorteio_listas.json'))['listas']['FE']
P = meta['paginas_lista']; frac = (len(meta['paginas_sorteadas']) + len(ORDEM_PAGINAS)) / P
rnd = random.Random(20261120); novos = []
for pg in ORDEM_PAGINAS:
    el = [x for x in L[pg] if x[0] not in ja]
    rnd.shuffle(el); toma = el[:2]
    for x in toma:
        ja.add(x[0])
        novos.append(dict(estrato='FE', numero=x[0], lista='FE_compl', pagina=pg, elegiveis_na_pagina=len(el),
            peso=round(1 / (frac * (len(toma) / len(el))), 3), classe='Ação Penal - Procedimento Ordinário',
            assunto=x[8], comarca=x[1], foro=x[9], vara=x[10], data_disponibilizacao=x[2], cd_doc_cjpg=x[3],
            chars_sentenca=x[4], m_171_2A=True, m_fraude_eletronica=bool(x[5]), m_154A=False, m_conta_laranja=False,
            m_imputacao=True, condena=bool(x[6]), absolve=bool(x[7]), imputacao='', dv_ok=True))
rnd.shuffle(novos)
o = max(int(r['ordem_no_estrato']) for r in rows if r['estrato'] == 'FE')
for n in novos:
    o += 1; n['ordem_no_estrato'] = o; rows.append({k: n.get(k, '') for k in campos})
with open(A, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(rows)
for n in novos: print(n['ordem_no_estrato'], n['numero'], n['pagina'], n['peso'])
