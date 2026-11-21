// Coletor do cjpg para rodar DENTRO de uma aba aberta em https://esaj.tjsp.jus.br/cjpg/
// (console do navegador ou ferramenta de JavaScript do navegador embutido).
// Foi o caminho do piloto de 20/11/2026, porque o acesso automatizado a partir do
// workspace da sessão foi recusado. Mesmas regras de scripts/cjpg_alvos.py.
//
// Uso (cada chamada deve voltar em menos de 45 s; por isso a coleta longa roda
// em segundo plano e é consultada depois):
//   1. Colar este arquivo inteiro na aba.
//   2. cjpg.iniciar('FE', 0)          // 0 = todas as páginas; ou um limite
//   3. cjpg.estado()                  // acompanha: rotulo, pagina, total, linhas
//   4. JSON.stringify(cjpg.lote(0, 300))  // devolve linhas sem o inteiro teor
// Uma consulta por vez: a paginação depende da última consulta da sessão.
// Painel do navegador oculto desacelera os temporizadores (no piloto, cerca de
// 10 s por página em vez de 3 s).

window.cjpg = (() => {
  const CLASSES = '8657,8803,8804'; // TPU 283, 10943, 10944
  const CONSULTAS = {
    FE: '"fraude eletrônica"',
    FE_amp: '"2º-A" E estelionato',
    INV: '"invasão de dispositivo informático"',
    CL: '"conta laranja" OU "contas laranja" OU "contas laranjas" OU "cessão de conta" OU "cessão de contas"',
  };
  const PAUSA = 3000;
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const st = {rotulo: null, status: 'parado', pagina: 0, total: 0, linhas: [], erro: null};

  const inteiro = tr => {
    const ds = [...tr.querySelectorAll('div[align=justify]')];
    const d = ds.sort((a, b) => b.textContent.length - a.textContent.length)[0];
    return d ? d.textContent.replace(/\s+/g, ' ').trim() : '';
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
      const t = inteiro(tr);
      const i = t.search(/foi denunciad|foram denunciad|ofereceu den[úu]ncia|denunciou|incurs[oa]s? n/i);
      const fim = t.slice(-4000);
      return {
        numero: tr.querySelector('span.fonteNegrito')?.textContent.trim(),
        classe: f['Classe'], assunto: f['Assunto'], comarca: f['Comarca'], foro: f['Foro'],
        vara: f['Vara'], data_disponibilizacao: f['Data de Disponibilização'],
        cd_doc_cjpg: tr.querySelector('a[title="Visualizar Inteiro Teor"]')?.getAttribute('name'),
        chars_sentenca: t.length,
        m_171_2A: /171[^.;]{0,25}(§|par\.?|parágrafo)\s*2º?\s*-?\s*A\b/i.test(t),
        m_fraude_eletronica: /fraude eletr[ôo]nica/i.test(t),
        m_154A: /154\s*-\s*A/i.test(t),
        m_laranja: /laranja|cess[ãa]o de conta/i.test(t),
        m_imputacao: i >= 0,
        condena: /\bcondeno\b|julgo procedente/i.test(fim),
        absolve: /\babsolvo\b|julgo improcedente/i.test(fim),
        imputacao: i >= 0 ? t.slice(i, i + 420) : '',
      };
    });
    return {total: tot ? +tot : 0, linhas, barreira};
  };

  const pesquisar = livre => fetch('/cjpg/pesquisar.do?' + new URLSearchParams({
    'dadosConsulta.pesquisaLivre': livre, tipoNumero: 'UNIFICADO',
    'classeTreeSelection.values': CLASSES, 'assuntoTreeSelection.values': '',
    'dadosConsulta.ordenacao': 'DESC'})).then(r => r.text());
  const pagina = n => fetch('/cjpg/trocarDePagina.do?pagina=' + n).then(r => r.text());

  async function rodar(rotulo, maxPaginas) {
    const livre = CONSULTAS[rotulo];
    Object.assign(st, {rotulo, status: 'rodando', pagina: 1, linhas: [], erro: null});
    let r = parse(await pesquisar(livre));
    st.total = r.total;
    const ultima = Math.min(Math.ceil(r.total / 10), maxPaginas || Infinity);
    for (let n = 1; n <= ultima; n++) {
      if (n > 1) {
        await sleep(PAUSA);
        r = parse(await pagina(n));
        if (!r.linhas.length && !r.barreira) { // sessão perdida: refaz uma vez
          await sleep(PAUSA); await pesquisar(livre); await sleep(PAUSA); r = parse(await pagina(n));
        }
      }
      if (r.barreira) { st.status = 'parado'; st.erro = 'barreira na página ' + n; return; }
      st.linhas.push(...r.linhas.map(x => ({...x, consulta: rotulo, pagina: n})));
      st.pagina = n;
    }
    st.status = 'ok';
  }

  return {
    CONSULTAS,
    iniciar: (rotulo, maxPaginas = 0) => { rodar(rotulo, maxPaginas).catch(e => { st.status = 'erro'; st.erro = String(e); }); return 'iniciado ' + rotulo; },
    estado: () => ({rotulo: st.rotulo, status: st.status, pagina: st.pagina, total: st.total, linhas: st.linhas.length, erro: st.erro}),
    lote: (de, ate) => st.linhas.slice(de, ate),
  };
})();
