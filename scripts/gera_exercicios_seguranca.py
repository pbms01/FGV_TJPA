"""Gera os exercícios da aula de segurança (INV 2 e AP 2428) sobre o layout de identidade-fe114.html.

Uso: python3 scripts/gera_exercicios_seguranca.py [URL_DA_ANCORA] [URL_DO_CONTRASTE]
(as URLs, depois da publicação, entram como links cruzados entre os dois exercícios)."""
import os, re, sys, html
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../docs/aula/exercicios/")
modelo = open(BASE + "identidade-fe114.html", encoding="utf-8").read()
head = modelo[:modelo.index("<body>")]
script = modelo[modelo.index("<script>"):]

def q_html(n, total, pergunta, gab, base, pontos):
    gp = "\n".join(f"        <p>{p}</p>" for p in gab)
    pts = "\n".join(f'          <label class="ponto"><input type="checkbox" data-q="{n}"> {p}</label>' for p in pontos)
    return f'''    <article class="q" id="q{n}" aria-labelledby="t-q{n}">
      <div class="qhead"><span class="qnum">{n} de {total}</span><h3 id="t-q{n}">{pergunta}</h3></div>
      <label class="sr" for="r{n}">Sua resposta à questão {n}</label>
      <textarea id="r{n}" placeholder="Escreva sua resposta aqui."></textarea>
      <div class="actions">
        <span class="count" id="c{n}">0 caracteres · mínimo de 40</span>
        <button type="button" id="b{n}" disabled>Responder e ver o gabarito</button>
      </div>
      <div class="gabarito" id="g{n}" hidden aria-live="polite">
        <h3>Gabarito</h3>
{gp}

        <p class="base">{base}</p>
        <fieldset>
          <legend>Sua resposta cobriu estes pontos?</legend>
{pts}
        </fieldset>
        <span class="placar" id="s{n}">0 de {len(pontos)} pontos marcados</span>
      </div>
    </article>'''

def pagina(titulo, eyebrow, caso_ps, dl, questoes, sintese, rodape, link=None):
    h = head.replace("<title>O investidor do perfil clonado</title>", f"<title>{titulo}</title>")
    ps = "\n".join(f"    <p>{p}</p>" for p in caso_ps)
    dls = "\n".join(f"      <div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in dl)
    qs = "\n".join(q_html(i + 1, len(questoes), *q) for i, q in enumerate(questoes))
    si = "\n".join(f"      <li>{s}</li>" for s in sintese)
    rp = "\n".join(f"    <p>{r}</p>" for r in rodape)
    lk = f'\n    <p class="lead">{link}</p>' if link else ""
    corpo = f'''<body>
<main class="wrap">
  <header>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{titulo}</h1>
    <p class="lead">Leia o caso e responda às três questões. O gabarito de cada uma aparece quando você envia a sua resposta. Depois, marque os pontos que a sua resposta cobriu.</p>{lk}
    <div class="status">
      <span class="chip" id="progresso" aria-live="polite">0 de 3 respondidas</span>
      <button type="button" class="ghost" id="recomecar">Recomeçar</button>
    </div>
  </header>

  <section class="caso" aria-labelledby="t-caso">
    <h2 id="t-caso">O caso</h2>
{ps}
    <dl>
{dls}
    </dl>
  </section>

  <div class="questoes">
{qs}
  </div>

  <section class="sintese" id="sintese" aria-labelledby="t-sintese" aria-live="polite">
    <h2 id="t-sintese">O que o caso acrescenta à decisão</h2>
    <p id="sintese-espera">A síntese aparece quando as três questões estiverem respondidas.</p>
    <ul id="sintese-lista" hidden>
{si}
    </ul>
  </section>

  <footer>
{rp}
    <p>As respostas ficam só nesta página e se perdem ao recarregá-la.</p>
  </footer>
</main>

'''
    return h + corpo + script

link_ancora = sys.argv[1] if len(sys.argv) > 1 else ""
link_contraste = sys.argv[2] if len(sys.argv) > 2 else ""

ancora = pagina(
  "O chip que mudou de mão às 21h57",
  "Segurança da informação · Par único · Caso âncora (TJSP)",
  ["Em janeiro de 2021, vítimas de Presidente Prudente perderam de repente o sinal do celular e acharam que era pane. A linha tinha passado a outro aparelho, que recebeu os códigos de verificação dos bancos e entrou nas contas: transferências, pagamentos de boletos, um Pix de R$ 190,00 a um desconhecido.",
   "A investigação chegou a um grupo com quatro funções: quem obtinha as senhas bancárias, quem distribuía, quem cedia contas para receber e quem trocava as linhas. Uma das denunciadas trabalhava numa loja terceirizada da operadora e tinha login, senha e token do sistema de atendimento. Pelo sistema, trocava o ICCID do chip da vítima pelo de um chip do grupo. Em juízo, disse que os gerentes mandavam os funcionários emprestar as senhas aos colegas novos."],
  [("Datas", "Fatos de 20 a 22/01/2021, antes da Lei 14.155/2021; denúncia em outubro de 2023; sentença em setembro de 2025 (3ª Vara Criminal de Presidente Prudente, TJSP)."),
   ("Denúncia", "Art. 171, §2º-A, e art. 154-A do CP, duas vezes cada; organização criminosa (Lei 12.850/2013) e lavagem (Lei 9.613/1998)."),
   ("Prova", "Registros do sistema da operadora sobre as trocas de chip, informações de operadoras, do Google e da Apple sobre os aparelhos que receberam as linhas, extratos da conta de destino."),
   ("Sentença", "Nova definição para o furto mediante fraude (art. 155, §4º, II e IV). A funcionária foi condenada por uma das duas invasões, pelo furto e pela organização criminosa, a 5 anos e 4 meses de reclusão e 3 meses de detenção em regime semiaberto, e absolvida da outra invasão e da lavagem.")],
  [("Onde estava a barreira que o grupo precisava vencer para entrar nas contas, e por onde ela foi vencida?",
    ["A barreira era a autenticação da linha telefônica, que os bancos usam como segundo fator: quem tem o número recebe o código. O grupo não quebrou essa autenticação. Ela foi operada por dentro, por uma funcionária que tinha credencial legítima para trocar chips e a usou fora da finalidade.",
     "O SIM swap aparece, para a vítima, como ataque técnico sofisticado; nos autos, é o uso de um acesso funcional. É o padrão que Ross Anderson descreveu em 1993 para os caixas eletrônicos: as fraudes vinham de erros de implementação e de gestão, não da criptoanálise."],
    "Na base (68 denúncias do TJSP com barreira entre o agente e o sistema), a técnica é a via em 5 das 41 denúncias que narram a passagem; em 24 a credencial saiu da própria vítima, e em 7 a porta foi aberta por quem tinha acesso legítimo.",
    ["Identificou a autenticação da linha como segundo fator dos bancos.", "Distinguiu o uso de credencial legítima da quebra técnica da barreira.", "Localizou a vulnerabilidade no serviço da operadora, e não na vítima.", "Relacionou o caso ao acesso interno."]),
   ("O fato é de janeiro de 2021, e a redação do art. 154-A então vigente exigia a invasão \"mediante violação indevida de mecanismo de segurança\". Onde a sentença encontrou essa violação, e o que muda para um fato posterior a 28/05/2021?",
    ["A sentença a encontrou no próprio uso da credencial: \"mediante uso indevido de senha e token, funcionários de lojas terceirizadas da Tim acessaram o sistema da empresa\", e \"a violação do mecanismo de segurança deu-se por meio do aliciamento de funcionários com acesso ao sistema\". A leitura é defensável, mas mostra o problema da elementar: a barreira estava íntegra, e quem a abriu estava autorizado a abri-la para outro fim.",
     "A Lei 14.155/2021 suprimiu a exigência. Para fato posterior a 28/05/2021, invadir basta; a violação deixa de ser questão de tipicidade e passa, quando muito, à dosimetria."],
    "Na base, entre as sentenças com fato posterior à lei que se pronunciam sobre a questão, cinco ainda tratam a barreira como exigência (três absolvem por falta dela e duas a encontram), contra quatro que a dispensam.",
    ["Apontou a redação de 2012 do art. 154-A como aplicável ao fato.", "Identificou o uso de senha e token legítimos como a \"violação\" achada.", "Notou a tensão entre barreira íntegra e acesso autorizado desviado.", "Concluiu que, depois da Lei 14.155, a barreira não é mais elementar."]),
   ("A ré disse que as senhas eram emprestadas entre colegas. Que prova responde a essa versão? E a posição dela dentro do serviço pesou na pena do 154-A?",
    ["O próprio registro do sistema da operadora: o token mudava a cada 30 segundos, as trocas foram feitas fora do horário de trabalho dela (uma às 21h57) e em linhas de DDDs que ela dizia não conseguir atender, e ao menos 25 trocas dela em um mês correspondem a linhas de vítimas com boletim de ocorrência. O controle de segurança que ela usou para abrir a porta foi o que provou quem abriu.",
     "Na pena, não pesou: para o 154-A, a sentença não viu \"elementos de culpabilidade desfavoráveis\" e fixou o mínimo (3 meses de detenção). Em outro caso de acesso interno da base (INV 8), a culpabilidade foi acentuada porque os réus \"se aproveitaram da relação profissional e da confiança depositada neles\". A posição de confiança é fundamento possível do art. 59, e aqui não foi pedido nem examinado."],
    "Na base, nos 7 acessos internos, todos com condenação ao menos parcial, a sentença atribuiu o acesso pelo registro do próprio sistema em 5; a posição de confiança pesou na pena em 2 sentenças.",
    ["Usou o registro do sistema (login, token, horário, DDD) contra a versão de senha compartilhada.", "Notou que o controle de segurança virou prova da autoria.", "Constatou a pena mínima do 154-A, sem valoração da posição funcional.", "Discutiu a posição de confiança como circunstância do art. 59."])],
  ["Na tipicidade, desde 28/05/2021 o art. 154-A não exige barreira vencida; quem ainda a procura absolve casos que a lei quis alcançar.",
   "Na investigação, o registro de acesso do próprio sistema (login, token, horário, terminal) é a primeira diligência quando a porta foi aberta por dentro.",
   "Na prova, a credencial própria se atribui pelo registro; a versão de senha compartilhada se testa contra o token, o horário e a região.",
   "Na pena, a posição de confiança dentro do serviço é circunstância a examinar no art. 59, e não foi examinada neste caso."],
  ["Caso de uma ação penal do TJSP, com denúncia e sentença lidas por inteiro, sem os nomes dos réus. Os números vêm da base de pesquisa de 198 denúncias e suas sentenças, com codificação conferida por segundo leitor."],
  link=(f'Contraste: <a href="{link_contraste}">Esqueceu a senha?</a> (STF, AP 2428).' if link_contraste else None))

contraste = pagina(
  "Esqueceu a senha?",
  "Segurança da informação · Par único · Caso de contraste (STF)",
  ["Entre agosto de 2022 e janeiro de 2023, os sistemas do Conselho Nacional de Justiça foram invadidos ao menos 13 vezes. Dentro deles, o invasor inseriu documentos falsos: alvarás de soltura, ordens de bloqueio e um mandado de prisão contra um ministro do Supremo Tribunal Federal. Agia, segundo a acusação, a mando de uma parlamentar.",
   "O controle de acesso aos sistemas do CNJ (BNMP, Renajud e outros) passa por um sistema corporativo de login. Os registros de acesso apontavam usuários legítimos: servidores e uma magistrada, que não tinham feito as inserções."],
  [("Datas", "Fatos de agosto de 2022 a janeiro de 2023, depois da Lei 14.155/2021; denúncia da PGR recebida em maio de 2024; julgamento pela Primeira Turma do STF em maio de 2025 (AP 2428)."),
   ("Denúncia", "Art. 154-A, §2º, do CP (invasão com prejuízo econômico), 13 vezes, e art. 299 do CP (falsidade ideológica), 16 vezes. A denúncia narra que o executor \"teria violado indevidamente mecanismos de segurança\"."),
   ("Prova", "Registros dos sistemas do CNJ, confissão do executor, material por ele entregue e investigação da Polícia Federal."),
   ("Defesa", "Entre outras teses, a falta de acesso integral aos dados armazenados em nuvem do executor.")],
  [("O invasor não quebrou cifra nenhuma. Por onde ele passou pela barreira do CNJ?",
    ["Segundo o voto do relator, pela funcionalidade \"Esqueceu a senha?\" da tela de login do sistema de controle de acesso, por credenciais violadas de um funcionário e dados de outro usuário, por credenciais forjadas e pelas credenciais de uma magistrada no Renajud; e entrou no repositório de código do CNJ a partir de uma vulnerabilidade encontrada no GitHub, que expôs segredos e tokens.",
     "A habilidade do agente estava em achar e encadear falhas de gestão de credenciais, não em vencer a criptografia. Na base do TJSP há o mesmo caminho: um escrevente entrou duas vezes na conta gov.br de um juiz, mesmo depois da troca de senha e da verificação em duas etapas, e confessou ter usado a opção \"esqueci a senha\" (INV 4)."],
    "Na base, a técnica (falha explorada, programa malicioso, força bruta) é a via em 5 das 41 denúncias que narram a passagem; nas demais, a porta foi aberta por credenciais, da vítima, de quem tinha acesso ou recuperadas.",
    ["Identificou a recuperação de senha como via.", "Apontou o uso de credenciais legítimas de terceiros.", "Mencionou o segredo exposto em repositório de código.", "Distinguiu falha de gestão de credenciais de quebra de criptografia."]),
   ("Os fatos são posteriores à Lei 14.155/2021, mas a denúncia narra a violação de mecanismos de segurança. Isso importa à tipicidade? E à pena?",
    ["À tipicidade, não: desde 28/05/2021 o art. 154-A pune invadir, sem exigir barreira vencida, e o voto aplica a pena da redação nova sem analisar a elementar. À pena, sim: o voto conta quatro circunstâncias judiciais negativas e põe na culpabilidade o \"reconhecido conhecimento técnico em matéria de invasão de sistemas informatizados\", e nas circunstâncias o planejamento detalhado e as medidas para dificultar a descoberta. A pena do executor chegou a 8 anos e 3 meses, em regime fechado, com danos materiais e morais coletivos de R$ 2 milhões.",
     "A violação da barreira migrou do tipo para a dosimetria, e lá precisa de fundamento concreto, como o voto deu."],
    "Na base do TJSP, a técnica do agente pesa na pena em uma sentença (INV 4, \"expertise e habilidade incomuns\"), e cinco sentenças com fato posterior à lei ainda tratam a barreira como exigência do tipo.",
    ["Negou que a violação seja elementar depois de 28/05/2021.", "Identificou a técnica como matéria de culpabilidade e circunstâncias.", "Exigiu fundamento concreto para a valoração na pena.", "Comparou com sentenças da base que ainda exigem a barreira."]),
   ("Os registros do CNJ apontavam as credenciais de servidores e de uma magistrada. Por que eles não bastavam para a autoria, e o que a completou?",
    ["Porque o registro identifica a credencial, e não a pessoa: com credencial de terceiro, o log aponta quem não agiu. A autoria se provou cruzando o registro com outra trilha, a confissão do executor, o material que ele entregou e a investigação.",
     "É o oposto do caso âncora (INV 2), em que a credencial era da própria agente e o registro bastou para atribuir as trocas de chip a ela. A pergunta prática, diante de um log, é de quem era a credencial que ele registra."],
    "Na base, nos 7 acessos internos, o registro do sistema atribuiu o acesso em 5; nos dois restantes (credencial cedida por servidoras e senhas compradas que não funcionaram), a autoria veio da confissão e do aparelho apreendido.",
    ["Distinguiu a identificação da credencial da identificação da pessoa.", "Indicou a necessidade de outra trilha de prova.", "Comparou com a credencial própria do caso âncora.", "Formulou a pergunta de quem era a credencial registrada."])],
  ["Na tipicidade, a violação de mecanismo de segurança deixou de ser elementar do art. 154-A em 28/05/2021; narrada na denúncia, ela informa a pena, não o tipo.",
   "Na dosimetria, o conhecimento técnico pode pesar na culpabilidade, com fundamento concreto, como o voto deu.",
   "Na prova, o log identifica a credencial; com credencial alheia, a autoria depende de cruzar o registro com outra trilha.",
   "No fenômeno, o caso de maior repercussão do período confirma o padrão da base: a porta é aberta por credenciais, não pela quebra da criptografia."],
  ["Caso de ação penal originária do STF (AP 2428), lido no voto do relator em reprodução publicada; os nomes das partes foram omitidos. Os números da base vêm de 198 denúncias do TJSP e suas sentenças, com codificação conferida por segundo leitor."],
  link=(f'Âncora: <a href="{link_ancora}">O chip que mudou de mão às 21h57</a> (TJSP).' if link_ancora else None))

open(BASE + "seguranca-inv2.html", "w", encoding="utf-8").write(ancora)
open(BASE + "seguranca-ap2428.html", "w", encoding="utf-8").write(contraste)
print("ok", len(ancora), len(contraste))
