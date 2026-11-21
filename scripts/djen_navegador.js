// Coletor de números-alvo pela API pública do DJEN, para rodar DENTRO de uma aba
// aberta em https://comunica.pje.jus.br/ (console do navegador ou ferramenta de
// JavaScript do navegador embutido). É o equivalente, no TJPA, do cjpg_navegador.js
// do TJSP: o TJPA não tem consulta de sentenças de 1º grau, e o seu Banco de
// Jurisprudência indexa só acórdãos e decisões monocráticas. Foi a via da sondagem
// de 21/11/2026 (docs/RUNBOOK_TJPA.md). Mesmas regras de scripts/djen_alvos.py.
//
// A API (a mesma que alimenta o comunica.pje.jus.br):
//   GET https://comunicaapi.pje.jus.br/api/v1/comunicacao?texto=...&siglaTribunal=TJPA
//       &dataDisponibilizacaoInicio=AAAA-MM-DD&dataDisponibilizacaoFim=AAAA-MM-DD
//       &pagina=N&itensPorPagina=100
//   Resposta: {status, message, count, items[]}; cada item traz id, numero_processo,
//   numeroprocessocommascara, codigoClasse, nomeClasse, tipoDocumento, nomeOrgao,
//   data_disponibilizacao, texto (inteiro teor), destinatarios, destinatarioadvogados.
// Semântica medida em 21/11/2026: cada consulta é UMA frase (aspas indiferentes;
// "fraude eletrônica estelionato" devolve a frase, não a interseção); não há OU nem
// E, por isso cada variante é uma consulta e a união se faz pelo id; não há filtro
// de classe, que se aplica aqui pelo codigoClasse. Do workspace da sessão a API
// devolve 403; do navegador do usuário responde sem captcha.
//
// Uso (cada chamada deve voltar em menos de 45 s; a coleta roda em segundo plano):
//   1. Colar este arquivo inteiro na aba do comunica.pje.jus.br.
//   2. djen.iniciar({tribunal: 'TJPA', inicio: '2020-01-01', fim: '2026-11-20'})
//      (opcional: so: ['FE','INV'], texto: true para guardar o inteiro teor na memória)
//   3. djen.estado()                 // acompanha: frase, página, publicações
//   4. djen.totais()                 // totais por frase, por rótulo e por classe
//   5. djen.csv()                    // uma linha por processo, sem nomes de pessoas
//   6. djen.controle('estelionato', ['2022','2023','2024','2025','2026'])  // cobertura
// Com o painel do navegador oculto os temporizadores desaceleram; é só esperar.

window.djen = (() => {
  const API = 'https://comunicaapi.pje.jus.br/api/v1/comunicacao';
  const CONSULTAS = {
    FE: ['fraude eletrônica'],
    FE_amp: ['171, § 2º-A', 'art. 171, § 2º-A'],
    INV: ['invasão de dispositivo informático'],
    CL: ['conta laranja', 'contas laranja', 'contas laranjas', 'cessão de conta', 'cessão de contas'],
    EE: ['estelionato eletrônico'],
  };
  // Classes que entram na lista de alvos. O HC (307) fica fora: tem número próprio
  // de 2º grau. No TJPA a apelação (417) mantém o número de origem.
  const CLASSES = {'283': 'AP', '10943': 'AP', '10944': 'AP', '417': 'APEL', '279': 'IP', '280': 'APF'};
  const PAUSA = 1500, POR_PAGINA = 100;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const norm = s => (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const st = {status: 'parado', erro: null, frase: null, pagina: 0, par: null,
              totais: {}, itens: new Map(), textos: new Map()};

  const indicadores = (texto, tipoDoc) => {
    const t = norm(texto), fim = t.slice(-4000);
    return {
      m_fraude_eletronica: /fraude eletronica/.test(t),
      m_171_2A: /171[^.;]{0,40}2[ºo°]?\s*-\s*a\b/.test(t),
      m_154A: /154\s*-\s*a\b/.test(t),
      m_laranja: /laranja|cessao de conta/.test(t),
      sentenca: tipoDoc === 'Sentença' ||
        (/(condeno|absolvo|julgo (parcialmente )?procedente|julgo improcedente)/.test(t) &&
         /dispositivo|ante o exposto|isto posto|diante do exposto/.test(t)),
      condena: /\bcondeno\b|julgo (parcialmente )?procedente/.test(fim),
      absolve: /\babsolvo\b|julgo improcedente/.test(fim),
    };
  };

  const url = (frase, p) => API + '?texto=' + encodeURIComponent(frase) +
    '&siglaTribunal=' + st.par.tribunal + '&dataDisponibilizacaoInicio=' + st.par.inicio +
    '&dataDisponibilizacaoFim=' + st.par.fim + '&pagina=' + p + '&itensPorPagina=' + POR_PAGINA;

  async function pagina(frase, p) {
    for (let k = 0; k < 3; k++) {
      const r = await fetch(url(frase, p));
      if (r.status === 200) return r.json();
      if (r.status === 429 || r.status >= 500) { await sleep(30000 * (k + 1)); continue; }
      throw new Error('HTTP ' + r.status + ' em "' + frase + '", página ' + p);
    }
    throw new Error('falha repetida em "' + frase + '", página ' + p);
  }

  // Guarda só metadados e indicadores; nomes de partes e advogados não entram.
  function registra(it, rotulo, frase) {
    let x = st.itens.get(it.id);
    if (!x) {
      x = {id: it.id, numero: it.numeroprocessocommascara || it.numero_processo,
           data: it.data_disponibilizacao, codigoClasse: String(it.codigoClasse),
           nomeClasse: it.nomeClasse, tipoDocumento: it.tipoDocumento,
           tipoComunicacao: it.tipoComunicacao, orgao: it.nomeOrgao,
           n_advogados: (it.destinatarioadvogados || []).length, chars: (it.texto || '').length,
           ...indicadores(it.texto, it.tipoDocumento), rotulos: [], frases: []};
      st.itens.set(it.id, x);
      if (st.par.texto) st.textos.set(it.id, it.texto);
    }
    if (!x.rotulos.includes(rotulo)) x.rotulos.push(rotulo);
    if (!x.frases.includes(frase)) x.frases.push(frase);
  }

  async function rodar() {
    for (const [rotulo, frases] of Object.entries(CONSULTAS)) {
      if (st.par.so && !st.par.so.includes(rotulo)) continue;
      for (const frase of frases) {
        st.frase = frase;
        let p = 1, n = 0;
        while (true) {
          const j = await pagina(frase, p);
          if (p === 1) st.totais[frase] = {rotulo, publicacoes: j.count};
          const its = j.items || [];
          its.forEach(it => registra(it, rotulo, frase));
          n += its.length; st.pagina = p;
          await sleep(PAUSA);
          if (its.length < POR_PAGINA || n >= j.count) break;
          p++;
        }
      }
    }
    st.status = 'ok';
  }

  function porProcesso() {
    const P = new Map();
    for (const x of st.itens.values()) {
      const tipo = CLASSES[x.codigoClasse];
      if (!tipo) continue;
      if (!P.has(x.numero)) P.set(x.numero, {numero: x.numero, AP: 0, APEL: 0, IP: 0, APF: 0,
        data_sentenca: '', primeira_pub: x.data, ultima_pub: x.data, consultas: new Set(),
        m_fraude_eletronica: 0, m_171_2A: 0, m_154A: 0, m_laranja: 0,
        n_pubs: 0, n_pubs_sem_advogado: 0, orgao_1g: ''});
      const p = P.get(x.numero);
      p[tipo] = 1; p.n_pubs++;
      if (!x.n_advogados) p.n_pubs_sem_advogado++;
      x.rotulos.forEach(r => p.consultas.add(r));
      if (x.data < p.primeira_pub) p.primeira_pub = x.data;
      if (x.data > p.ultima_pub) p.ultima_pub = x.data;
      for (const m of ['m_fraude_eletronica', 'm_171_2A', 'm_154A', 'm_laranja']) if (x[m]) p[m] = 1;
      if (tipo !== 'APEL' && !p.orgao_1g) p.orgao_1g = x.orgao;
      if (tipo === 'AP' && x.sentenca && x.data > p.data_sentenca) p.data_sentenca = x.data;
    }
    return [...P.values()].sort((a, b) => a.numero.localeCompare(b.numero));
  }

  function csv() {
    const cab = ['numero', 'acao_penal', 'apelacao', 'inquerito', 'flagrante', 'data_sentenca_djen',
      'primeira_pub', 'ultima_pub', 'consultas', 'm_fraude_eletronica', 'm_171_2A', 'm_154A',
      'm_laranja', 'n_pubs', 'n_pubs_sem_advogado', 'orgao_1g'];
    const q = s => /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
    return [cab.join(',')].concat(porProcesso().map(p => [p.numero, p.AP, p.APEL, p.IP, p.APF,
      p.data_sentenca, p.primeira_pub, p.ultima_pub, [...p.consultas].sort().join('+'),
      p.m_fraude_eletronica, p.m_171_2A, p.m_154A, p.m_laranja, p.n_pubs,
      p.n_pubs_sem_advogado, q(p.orgao_1g || '')].join(','))).join('\n') + '\n';
  }

  function totais() {
    const ps = porProcesso();
    const porRotulo = {};
    for (const x of st.itens.values()) for (const r of x.rotulos) {
      porRotulo[r] = porRotulo[r] || {publicacoes: 0, AP: new Set(), sentenca: new Set(), APEL: new Set()};
      const o = porRotulo[r]; o.publicacoes++;
      const tipo = CLASSES[x.codigoClasse];
      if (tipo === 'AP') { o.AP.add(x.numero); if (x.sentenca) o.sentenca.add(x.numero); }
      if (tipo === 'APEL') o.APEL.add(x.numero);
    }
    const rot = {};
    for (const [r, o] of Object.entries(porRotulo)) rot[r] = {publicacoes: o.publicacoes,
      acoes_penais: o.AP.size, com_sentenca: o.sentenca.size, apelacoes: o.APEL.size};
    const porClasse = {};
    for (const x of st.itens.values()) {
      const k = x.codigoClasse + ' ' + x.nomeClasse;
      porClasse[k] = porClasse[k] || new Set(); porClasse[k].add(x.numero);
    }
    return {parametros: st.par, frases: st.totais, por_rotulo: rot,
      publicacoes_distintas: st.itens.size,
      processos_por_classe: Object.fromEntries(Object.entries(porClasse).map(([k, s]) => [k, s.size])),
      alvos: {processos: ps.length, acao_penal: ps.filter(p => p.AP).length,
        apelacao: ps.filter(p => p.APEL).length,
        acao_penal_ou_apelacao: ps.filter(p => p.AP || p.APEL).length,
        so_apelacao: ps.filter(p => p.APEL && !p.AP).length,
        com_sentenca_djen: ps.filter(p => p.data_sentenca).length,
        sentenca_ou_apelacao: ps.filter(p => p.data_sentenca || p.APEL).length,
        inquerito: ps.filter(p => p.IP).length, flagrante: ps.filter(p => p.APF).length}};
  }

  // Série de controle: contagem de um termo comum por ano, para separar a cobertura
  // do DJEN do crescimento do fenômeno.
  async function controle(termo = 'estelionato', anos = ['2022', '2023', '2024', '2025', '2026']) {
    const out = {};
    for (const a of anos) {
      const fim = a === st.par?.fim?.slice(0, 4) ? st.par.fim : a + '-12-31';
      const u = API + '?texto=' + encodeURIComponent(termo) + '&siglaTribunal=' +
        (st.par?.tribunal || 'TJPA') + '&dataDisponibilizacaoInicio=' + a + '-01-01' +
        '&dataDisponibilizacaoFim=' + fim + '&pagina=1&itensPorPagina=1';
      out[a] = (await (await fetch(u)).json()).count;
      await sleep(PAUSA);
    }
    return out;
  }

  return {
    CONSULTAS, CLASSES,
    iniciar: (par = {}) => {
      st.par = {tribunal: 'TJPA', inicio: '2020-01-01',
                fim: new Date().toISOString().slice(0, 10), texto: false, so: null, ...par};
      Object.assign(st, {status: 'rodando', erro: null, totais: {}, itens: new Map(), textos: new Map()});
      rodar().catch(e => { st.status = 'erro'; st.erro = String(e); });
      return 'iniciado ' + st.par.tribunal + ' ' + st.par.inicio + ' a ' + st.par.fim;
    },
    estado: () => ({status: st.status, erro: st.erro, frase: st.frase, pagina: st.pagina,
                    publicacoes: st.itens.size}),
    totais, csv, controle, porProcesso,
    itens: (de, ate) => [...st.itens.values()].slice(de, ate),
    texto: id => st.textos.get(id),
  };
})();
