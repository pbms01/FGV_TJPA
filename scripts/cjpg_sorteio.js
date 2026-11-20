// Sorteio da amostra de 200 denúncias do TJSP sobre a listagem do cjpg.
// Rodar numa aba aberta em https://esaj.tjsp.jus.br/cjpg/ (colar o arquivo).
//   sorteio.iniciar()   // roda em segundo plano
//   sorteio.estado()    // acompanha
//   JSON.stringify(sorteio.resultado())
//
// Desenho (RUNBOOK_TJSP, 20/11/2026):
//  - Quatro listas do cjpg, todas com filtro de ação penal (TPU 283, 10943, 10944).
//  - Páginas sorteadas por amostragem sistemática com início aleatório sobre a
//    lista ordenada por data de disponibilização (espalha no tempo e nas comarcas).
//  - Em cada página sorteada, até 2 julgados elegíveis, escolhidos ao acaso
//    entre os elegíveis da página; a invasão é censo (todas as páginas, todos).
//  - Estratos excludentes por precedência: INV > CL > FE (lista FE ou acréscimo FE_amp).
//  - Peso = 1 / (fração de páginas sorteadas x fração dos elegíveis tomados na página).
//  - Ordem de processamento aleatória (chave sorteada), para que parar na cota
//    dê subamostra aleatória, e não só os julgados mais recentes.
// Semente fixa: 20261120 (gerador mulberry32).

window.sorteio = (() => {
  const SEMENTE = 20261120;
  const CLASSES = '8657,8803,8804';
  const PAUSA = 3000;
  const POR_PAGINA = 2;
  const LISTAS = [
    // rotulo, pesquisa livre, páginas a sortear (0 = todas, censo)
    ['INV', '"invasão de dispositivo informático"', 0],
    ['CL', '"conta laranja" OU "contas laranja" OU "contas laranjas" OU "cessão de conta" OU "cessão de contas"', 34],
    ['FE', '"fraude eletrônica"', 38],
    ['FE_amp', '"2º-A" E estelionato', 28],
  ];

  function mulberry32(a) {
    return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  const rnd = mulberry32(SEMENTE);
  const sleep = ms => new Promise(r => setTimeout(r, ms));

  const RX = {
    a2: /171[^.;]{0,25}(§|par\.?|parágrafo)\s*2º?\s*-?\s*A\b/i,
    fe: /fraude eletr[ôo]nica/i,
    a154: /154\s*-\s*A/i,
    cl: /contas? laranjas?|cess[ãa]o de contas?/i,
    imp: /foi denunciad|foram denunciad|ofereceu den[úu]ncia|denunciou|incurs[oa]s? n/i,
    cond: /\bcondeno\b|julgo procedente/i,
    abs: /\babsolvo\b|julgo improcedente/i,
  };

  const parse = html => {
    const d = new DOMParser().parseFromString(html, 'text/html');
    const tot = (d.body.innerText.match(/Resultados\s+\d+\s+a\s+\d+\s+de\s+(\d+)/) || [])[1];
    const barreira = /captcha|acesso negado/i.test(d.body.innerText) && !d.querySelector('tr.fundocinza1');
    const linhas = [...d.querySelectorAll('tr.fundocinza1')].map(tr => {
      const f = {};
      tr.querySelectorAll('tr.fonte td').forEach(td => {
        const m = td.innerText.match(/^\s*([^:\n]+):\s*([\s\S]*)$/);
        if (m && m[1].length < 30) f[m[1].trim()] = m[2].trim();
      });
      const ds = [...tr.querySelectorAll('div[align=justify]')];
      const t = (ds.sort((a, b) => b.textContent.length - a.textContent.length)[0]?.textContent || '').replace(/\s+/g, ' ').trim();
      const i = t.search(RX.imp);
      return {
        numero: tr.querySelector('span.fonteNegrito')?.textContent.trim(),
        classe: f['Classe'], assunto: f['Assunto'], comarca: f['Comarca'], foro: f['Foro'], vara: f['Vara'],
        data_disponibilizacao: f['Data de Disponibilização'],
        cd_doc_cjpg: tr.querySelector('a[title="Visualizar Inteiro Teor"]')?.getAttribute('name'),
        chars_sentenca: t.length, m_171_2A: RX.a2.test(t), m_fraude_eletronica: RX.fe.test(t),
        m_154A: RX.a154.test(t), m_conta_laranja: RX.cl.test(t), m_imputacao: i >= 0,
        condena: RX.cond.test(t.slice(-4000)), absolve: RX.abs.test(t.slice(-4000)),
        imputacao: i >= 0 ? t.slice(i, i + 420) : '',
      };
    });
    return {total: tot ? +tot : 0, linhas, barreira};
  };

  // Estrato do julgado conforme a lista de origem (precedência INV > CL > FE).
  function estrato(x, lista) {
    if (!x.m_imputacao) return null;
    if (lista === 'INV') return x.m_154A ? 'INV' : null;
    if (x.m_154A) return null;                         // pertence à invasão
    if (lista === 'CL') return x.m_conta_laranja ? 'CL' : null;
    if (x.m_conta_laranja) return null;                // pertence à conta laranja
    if (lista === 'FE') return x.m_171_2A ? 'FE' : null;
    if (lista === 'FE_amp') return (x.m_171_2A && !x.m_fraude_eletronica) ? 'FE' : null; // só o acréscimo
    return null;
  }

  const st = {status: 'parado', lista: null, pagina: null, feitas: 0, previstas: 0, erro: null, listas: {}, amostra: [], vistos: new Set()};

  async function rodar() {
    st.status = 'rodando'; st.inicio = new Date().toISOString();
    for (const [rot, livre, nPag] of LISTAS) {
      st.lista = rot;
      const p = new URLSearchParams({'dadosConsulta.pesquisaLivre': livre, tipoNumero: 'UNIFICADO',
        'classeTreeSelection.values': CLASSES, 'assuntoTreeSelection.values': '', 'dadosConsulta.ordenacao': 'DESC'});
      const r1 = parse(await fetch('/cjpg/pesquisar.do?' + p).then(r => r.text()));
      const N = r1.total, P = Math.ceil(N / 10);
      let paginas;
      if (!nPag || nPag >= P) paginas = [...Array(P).keys()].map(k => k + 1);
      else {
        const passo = P / nPag, ini = rnd() * passo;
        paginas = [...new Set([...Array(nPag).keys()].map(k => Math.floor(ini + k * passo) + 1))];
      }
      const fracPag = paginas.length / P;
      st.listas[rot] = {pesquisa_livre: livre, total: N, paginas_lista: P, paginas_sorteadas: paginas, fracao_paginas: fracPag, elegiveis_vistos: 0, tomados: 0};
      st.previstas += paginas.length;
      for (const pg of paginas) {
        let r = pg === 1 ? r1 : null;
        if (!r) {
          await sleep(PAUSA);
          r = parse(await fetch('/cjpg/trocarDePagina.do?pagina=' + pg).then(x => x.text()));
          if (!r.linhas.length && !r.barreira) { await sleep(PAUSA); await fetch('/cjpg/pesquisar.do?' + p); await sleep(PAUSA); r = parse(await fetch('/cjpg/trocarDePagina.do?pagina=' + pg).then(x => x.text())); }
        }
        if (r.barreira) { st.status = 'parado'; st.erro = 'barreira em ' + rot + ' p. ' + pg; return; }
        st.pagina = pg; st.feitas++;
        const eleg = r.linhas.map(x => ({x, e: estrato(x, rot)})).filter(o => o.e && !st.vistos.has(o.x.numero));
        st.listas[rot].elegiveis_vistos += eleg.length;
        for (let k = eleg.length - 1; k > 0; k--) { const j = Math.floor(rnd() * (k + 1)); [eleg[k], eleg[j]] = [eleg[j], eleg[k]]; }
        const toma = rot === 'INV' ? eleg : eleg.slice(0, POR_PAGINA);
        const fracNaPag = eleg.length ? toma.length / eleg.length : 0;
        for (const o of toma) {
          st.vistos.add(o.x.numero);
          st.amostra.push({...o.x, estrato: o.e, lista: rot, pagina: pg, elegiveis_na_pagina: eleg.length,
            peso: +(1 / (fracPag * fracNaPag)).toFixed(3), chave: rnd()});
        }
        st.listas[rot].tomados += toma.length;
      }
      await sleep(PAUSA);
    }
    // ordem de processamento: aleatória dentro de cada estrato
    st.amostra.sort((a, b) => a.chave - b.chave);
    const cont = {};
    st.amostra.forEach(a => { cont[a.estrato] = (cont[a.estrato] || 0) + 1; a.ordem_no_estrato = cont[a.estrato]; });
    st.fim = new Date().toISOString(); st.status = 'ok';
  }

  return {
    iniciar: () => { rodar().catch(e => { st.status = 'erro'; st.erro = String(e); }); return 'iniciado'; },
    estado: () => ({status: st.status, lista: st.lista, pagina: st.pagina, feitas: st.feitas, previstas: st.previstas, amostra: st.amostra.length, erro: st.erro}),
    resultado: () => ({semente: SEMENTE, por_pagina: POR_PAGINA, inicio: st.inicio, fim: st.fim, listas: st.listas, amostra: st.amostra}),
  };
})();
