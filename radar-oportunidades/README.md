# Radar de Oportunidades — DPPGE · Ifes Campus Colatina

O Radar de Oportunidades é o canal da Diretoria de Pesquisa, Pós-Graduação e Extensão (DPPGE) do Ifes Campus Colatina para divulgar editais, bolsas, fomento, eventos e premiações à comunidade do campus. Ele reúne um **boletim** (e-mail e WhatsApp), um **site público** com todas as oportunidades já divulgadas e **métricas** de interesse e de antecedência de divulgação.

Este LEIAME descreve o que o Radar faz e o fluxo de trabalho de cada edição. Os detalhes técnicos (design system, estrutura dos JSON, compatibilidade com o Outlook) estão no [CLAUDE.md](CLAUDE.md).

*Atualizado em 14/10/2026.*

| | Endereço |
|---|---|
| **Site público** (usar sempre no boletim e no WhatsApp) | https://links.ifes.edu.br/radar |
| Site público (endereço direto) | https://julianacs-28.github.io/cerebro-dppge-colatina/radar-oportunidades/ |
| **Sistema interno** (editor do boletim) | https://julianacs-28.github.io/cerebro-dppge-colatina/radar-oportunidades/radar_sistema_dppge.html |
| **Dashboard oficial** | Menu **Dashboard** do site público |

---

## Como o Radar está organizado

| Peça | O que é | Quem usa |
|---|---|---|
| **Boletim por e-mail** | Edição numerada, gerada pelo sistema e colada no Outlook | Comunidade do campus |
| **Mensagem de WhatsApp** | Versão resumida da mesma edição: imagem de cabeçalho + texto | Comunidade do campus |
| **Site público** (`index.html`) | Todas as oportunidades já divulgadas, com busca, filtros, status automáticos e dashboard | Comunidade e público em geral |
| **Sistema interno** (`radar_sistema_dppge.html`) | Editor das edições: monta, revisa e gera o boletim e o WhatsApp | Equipe da DPPGE |
| **Banco de oportunidades** (`banco.json`) | Lista acumulada de tudo o que já foi divulgado; é a fonte do site | Gerado pelo merge, nunca editado à mão |
| **Planilha de cliques** | Registro de cada clique em um edital (site, boletim, WhatsApp), sem dados pessoais | Lida pelo dashboard do site |

---

## Funcionalidades

### Site público

- **Página inicial:** barra de números (oportunidades com prazo vigente e com prazo encerrado), categorias, busca por palavra-chave e filtros por instituição e categoria, e a lista de oportunidades recentes com filtro de status.
- **Página de cada categoria**, com busca, filtro de status e de origem.
- **Status automáticos em dois eixos**, mostrados como pílulas lado a lado (ver "Status" abaixo).
- **Cards de eventos** com "Inscrições até …" ou "Não é necessária inscrição" e a data de realização.
- **Links dos editais rastreáveis:** cada clique passa pela página de passagem `ir.html`, que registra o clique e abre o edital (ver "Métricas").
- **Dashboard oficial** (menu Dashboard):
  - **painel de período** em destaque: Este ano (padrão), 3, 6, 9 ou 12 meses, com o intervalo por extenso;
  - **indicadores:** Divulgadas, Abertas agora, Encerradas, Novas, Encerram em breve e Boletins enviados;
  - **gráficos** por categoria, por coordenadoria/núcleo e evolução mensal, com quantidade e % escritos em cada barra;
  - **cliques nos editais:** os mais clicados, por canal, por categoria e por edição;
  - **antecedência de divulgação:** médias, alertas de menos de 7 dias, tabela completa e "Baixar tabela (CSV)".

  Todos os números contam as oportunidades **abertas e encerradas** divulgadas no período, pela data do primeiro anúncio.
- **Sobre a DPPGE** e contato.

### Sistema interno (editor)

- **Editor com 4 abas** (Edição, Destaque, Categorias, Informes) e **prévia em tempo real** do boletim.
- **Cards de Eventos** com "Fim das inscrições", a caixa **"Não é necessária inscrição"**, "Data do evento" e "Local", e aviso quando falta informação.
- **Verificação de títulos na curadoria:** embaixo de cada título, o editor compara com o que já foi publicado:
  - **ℹ Já divulgado:** republicação; o item será atualizado e manterá a data original;
  - **⚠ Parecido com …:** possível mesmo edital escrito de outro jeito.
- **Correção automática de maiúsculas:** título em CAIXA ALTA é corrigido ao sair do campo e ao importar um JSON. As siglas são preservadas, o mesmo trecho é corrigido no resumo e há a opção "Desfazer".
- **✔ Revisar edição:** checklist de todos os cards antes de fechar o boletim, em três níveis (Corrigir, Atenção, Informação). Nunca bloqueia.
- **🚀 Gerar para Outlook:** abre o boletim pronto numa nova aba, para copiar e colar no Outlook.
- **📱 Gerar para WhatsApp:** imagem de cabeçalho e texto formatado, enviados em mensagens separadas.
- **📚 Histórico:**
  - edições publicadas, iguais para todos, com "Abrir no editor" e "HTML";
  - inclusões avulsas;
  - rascunhos salvos neste navegador.
- **📥 Importar JSON / ⬇ Exportar JSON** e **🆕 Nova Edição**, que sugere o próximo número.
- **📄 Modelo + Prompt IA:** prompt completo para gerar o JSON de uma edição com o Claude, já com todas as regras.

O sistema **não tem mais dashboard próprio**: o oficial é o do site. O Histórico de edições publicadas e a verificação de títulos leem arquivos do site, então funcionam com o sistema aberto pelo endereço do GitHub Pages, e não pelo arquivo no computador.

### Métricas

**Cliques nos editais.** Os links de cada edital, no site, no boletim e no WhatsApp, passam pela página `ir.html`. Ela registra o clique na planilha "RADAR-cliques-nos-editais" (Google Planilhas + Apps Script, na conta institucional) e abre o edital na hora.
- O link carrega o código do edital, o canal (`site`, `boletim`, `whatsapp`) e, no boletim e no WhatsApp, o número da edição. Exemplo: `ir.html?e=k1ntaw&de=boletim&ed=05`.
- **Ninguém cria esses links à mão:** o site e o sistema os montam sozinhos.
- **Nenhum dado pessoal** é guardado. O número é um *indicador de interesse*, não uma contagem de pessoas: a mesma pessoa pode clicar mais de uma vez.
- O link curto `links.ifes.edu.br/radar`, da Comunicação, continua medindo as entradas no site. As duas medições se completam.

**Antecedência de divulgação.** O merge grava em cada oportunidade, só na primeira vez que ela aparece:
- `primeiraDivulgacao`: a data de envio da edição;
- `primeiraEdicao`: o número da edição, ou "avulsa";
- `prazoOriginal`: o prazo que valia naquele momento.

A antecedência é a quantidade de dias entre o anúncio e o fim das inscrições, ou, nos eventos sem inscrição, entre o anúncio e o início do evento. Itens de fluxo contínuo e de prazo ainda não definido são contados à parte.

---

## Mapa de pastas

```
radar-oportunidades/
├── index.html                   # site público — lê banco.json
├── ir.html                      # página de passagem: registra o clique e abre o edital
├── banco.json                   # TODAS as oportunidades já publicadas (nunca editar à mão)
├── radar_sistema_dppge.html     # sistema interno (editor do boletim)
├── edicoes/
│   ├── indice.json              # lista de edições e avulsas publicadas (gerado pelo merge)
│   ├── ed-01/
│   │   ├── dados.json           # conteúdo desta edição
│   │   └── imagens/             # imagens exclusivas da edição
│   ├── ed-02/  ...
│   └── avulsas/
│       ├── AAAA-MM-DD-slug/dados.json   # inclusão avulsa no site
│       └── REGISTRO.md          # log das inclusões avulsas
├── scripts/
│   ├── merge_edicao.py          # funde uma edição/avulsa no banco.json e gera o índice
│   └── preencher_historico.py   # preenchimento retroativo da antecedência (já rodado)
├── apps-script/
│   └── Codigo.gs                # código do Apps Script da planilha de cliques
├── docs/                        # planos e documentos de apoio
├── CLAUDE.md                    # referência técnica completa
└── README.md                    # este arquivo
```

`banco.json` ≠ `edicoes/ed-XX/dados.json`. O primeiro é o acumulado público do site; o segundo é o conteúdo isolado de uma edição do boletim (o que foi enviado naquela ocasião).

A pasta `metricas/` (atalho da planilha no Drive) e o cache do Python ficam fora do repositório, pelo `.gitignore`.

---

## Fluxo de trabalho de uma edição

| # | Passo | Onde |
|---|---|---|
| 1 | Atualizar a pasta com o GitHub | GitHub Desktop → Fetch / Pull |
| 2 | Pesquisar oportunidades na web | Fapes · CNPq · CAPES · Ifes · INPE · SBPC · MCTI · Fapesp · Fapemig · INPI… |
| 3 | Fazer a curadoria: o que entra e em qual categoria | Decisão editorial |
| 4 | Criar a pasta da edição e o JSON | `edicoes/ed-XX/dados.json` (+ `imagens/`, se houver) |
| 5 | Carregar no editor | Sistema → **Importar JSON** (ou **Nova Edição**) |
| 6 | Revisar | Avisos de título + **✔ Revisar edição** → resolver os itens "Corrigir" |
| 7 | Exportar | **⬇ Exportar JSON** → salvar em `edicoes/ed-XX/dados.json` |
| 8 | Atualizar o site | `python scripts/merge_edicao.py edicoes/ed-XX` |
| 9 | Publicar | Commit + push → o GitHub Pages atualiza em ~1 min |
| 10 | **Só então** enviar | **Gerar para Outlook** e **Gerar para WhatsApp** |

> ⚠️ **A ordem importa.** Os links dos editais no boletim e no WhatsApp passam por `ir.html`, que procura o edital no `banco.json` **publicado**. Se o boletim for enviado antes do merge e do push, o clique é registrado, mas a pessoa cai na página inicial do Radar em vez de chegar ao edital.

### Detalhes de cada passo

**1. Atualizar a pasta.** Mais de uma pessoa publica no Radar. Antes de começar, traga as mudanças do GitHub (Fetch e Pull no GitHub Desktop).

**2. Pesquisar.** Levantar editais, chamadas, bolsas e eventos abertos *na data de hoje*. Confira sempre o prazo real de inscrição, não a data de publicação do edital. Fontes regionais de outros estados (Fapesp, Fapemig) às vezes publicam chamadas nacionais: só descarte se o edital for explicitamente restrito àquele estado.

**3. Curadoria.** Filtrar pelo que é relevante para o campus e ainda está com prazo aberto (categorias abaixo).

**4. Criar a pasta e o JSON.** A pasta `edicoes/ed-XX/` é criada uma vez por edição, manualmente ou com apoio técnico. O `dados.json` pode ser gerado com o "📄 Modelo + Prompt IA" do sistema. Imagens exclusivas ficam em `edicoes/ed-XX/imagens/`, referenciadas a partir da raiz de `radar-oportunidades/` (ex.: `edicoes/ed-05/imagens/destaque.jpg`).

**5. Carregar no editor.** Há duas portas de entrada:
- **📥 Importar JSON:** quando já existe o `dados.json` da edição nova. Títulos em maiúsculas são corrigidos na importação.
- **🆕 Nova Edição:** para digitar direto no formulário. Limpa a tela e sugere o próximo número.

Para consultar ou reaproveitar uma edição anterior, use **📚 Histórico → Abrir no editor**.

⚠️ **Nunca importe o `banco.json`** para montar uma edição. Ele traria todas as oportunidades antigas para dentro da edição atual.

**6. Revisar.** Ajuste o Destaque, as Categorias e os Informes (a prévia atualiza em tempo real). Confira os avisos embaixo de cada título e clique em **✔ Revisar edição**. Resolva os itens **Corrigir**: resumo sem o título exato, link vazio ou encurtado, evento sem prazo e sem a caixa marcada, data de envio vazia.

**7. Exportar.** **⬇ Exportar JSON** baixa o arquivo para a pasta Downloads. **Nada é sobrescrito automaticamente:** salve o arquivo em `edicoes/ed-XX/dados.json`. O **💾 Salvar Edição** guarda só um rascunho neste navegador.

**8. Atualizar o site.** O merge funde a edição no acumulado. Ele **sempre soma, nunca substitui:** o que já foi publicado permanece, sem duplicar, e as datas originais são preservadas. Também gera o `edicoes/indice.json` e avisa no terminal se algum título novo for parecido com um já divulgado.
```bash
cd radar-oportunidades
python scripts/merge_edicao.py edicoes/ed-05     # no Mac/Linux: python3
```

**9. Publicar.** Commit e push (pelo GitHub Desktop). O GitHub Pages atualiza o site sozinho em cerca de 1 minuto.

**10. Enviar.**
- **🚀 Gerar para Outlook:** abre o boletim numa nova aba. Nessa aba, `Ctrl+A`, `Ctrl+C`, cole no corpo de um e-mail novo no Outlook (nunca o código-fonte) e envie.
- **📱 Gerar para WhatsApp:** envie primeiro a imagem e depois o texto, em mensagens separadas (a legenda de imagem corta textos longos).

---

## Inclusões avulsas (fora de uma edição)

Quando surge uma oportunidade urgente depois de uma edição já enviada, ela pode ir direto para o site, sem esperar o próximo boletim. Isso vale quando o prazo não sobreviveria até a próxima edição, ou quando o item é de alto impacto.

1. Criar `edicoes/avulsas/AAAA-MM-DD-slug-curto/dados.json` só com `"categorias": { … }`. Os campos `"data"` (data da publicação) e `"motivo"` vão no topo; a `data` vira a data de primeira divulgação.
2. `python scripts/merge_edicao.py edicoes/avulsas/AAAA-MM-DD-slug-curto`
3. Registrar em `edicoes/avulsas/REGISTRO.md`.
4. Commit e push.
5. Se o prazo for curto, considerar um aviso simples por e-mail ou WhatsApp. O item entra normalmente na próxima edição numerada.

---

## Regras de conteúdo

- **Título:** nunca em MAIÚSCULAS. Padrão recomendado (a ordem é livre): `[Nome do programa] — [Instituição] (Edital NN/AAAA, Nª chamada)`, com travessão " — ".
- **Republicação:** repetir o título **exatamente** como na primeira divulgação. O aviso "ℹ Já divulgado" confirma que deu certo. Chamadas diferentes de um mesmo edital (3ª e 4ª chamada) são oportunidades diferentes.
- **Resumo:** precisa conter o **título exato**, copiado e colado. É assim que o link aparece no meio do texto, no boletim e no site. Fórmula: *[Nome do edital] visa/oferece/apoia [ação], destinado a [público]. [Detalhe operacional].* Máximo de 3 frases.
- **Link:** sempre o endereço **original** do edital. Nunca um link encurtado nem um link do Radar: o sistema gera o link rastreável sozinho.
- **Eventos:** `prazo` = fim das inscrições; `dataEvento` = quando acontece; "Não é necessária inscrição" só se não houver inscrição nenhuma. **Gratuito não é o mesmo que sem inscrição.**
- **Data de envio:** a data real de envio da edição (DD/MM/AAAA). Ela vira a data de primeira divulgação das oportunidades novas.
- **CTA:** sempre descritivo ("Acessar Edital PRPPG 10/2024 →"), nunca "Ver mais".

---

## Categorias, coordenadorias e status

Cada oportunidade é classificada em três eixos independentes. Entender essa lógica ajuda na curadoria e na leitura do site e do dashboard.

### Categorias

A categoria descreve **o tipo de oportunidade**, não quem a divulga (isso é a origem).

| Categoria | Chave JSON | O que entra | Exemplos |
|---|---|---|---|
| Pesquisa & Fomento | `pesquisa` | Editais e chamadas de fomento a projetos de pesquisa | Chamada CNPq Universal · Editais Fapes de pesquisa |
| Internacionalização | `internac` | Mobilidade acadêmica, parcerias e cooperação com instituições estrangeiras | Chamadas CONFAP · Exames de proficiência |
| Bolsas & Auxílios | `bolsas` | Bolsas de iniciação científica, pós-graduação e auxílios a estudantes | PIBIC/PIBITI · Seleções de mestrado e doutorado |
| Eventos & Capacitações | `evento` | Congressos, seminários, workshops, cursos e semanas acadêmicas | Reunião Anual da SBPC · Cursos do INPI |
| Premiações | `premiacoes` | Prêmios, concursos e reconhecimentos acadêmicos | Prêmio Jovem Cientista · Prêmio Carolina Bori |
| Extensão & Comunidade | `extensao` | Projetos de extensão, ações comunitárias, cultura e responsabilidade social | Editais PROEX · Programas para a educação básica |

**Regra de curadoria:** quando uma oportunidade se encaixa em mais de uma categoria, escolha a que representa o **objetivo principal**. Um edital de bolsa para congresso no exterior entra em `bolsas` (o que se ganha), não em `evento` nem em `internac`.

### Coordenadorias (campo "origem")

A origem identifica **qual setor do Ifes Colatina é responsável** pela divulgação. É informativa e não muda a cor do card.

| Origem | O que costuma publicar |
|---|---|
| Coord. de Pesquisa | Editais e chamadas de projetos de pesquisa |
| Coord. de Pós-Graduação | Processos seletivos, bolsas e informes de pós-graduação |
| Coord. de Extensão | Editais e ações de extensão |
| Coord. de Laboratórios | Editais de uso, infraestrutura e equipamentos |
| Coord. de Rel. Institucionais | Parcerias e convênios institucionais |
| Núcleo de Rel. Internacionais | Mobilidade acadêmica e parcerias internacionais |
| Núcleo de Arte e Cultura | Eventos e editais culturais e artísticos |
| Núcleo de Ed. Ambiental | Ações e projetos de educação ambiental |
| Núcleo de Incubação | Empreendedorismo e apoio a negócios incubados |
| DPPGE | Informes institucionais e oportunidades sem setor específico |

### Status

Há **dois sistemas de status diferentes**. Não confundir.

**No boletim, o status é uma decisão editorial** de quem monta a edição:
- **NOVO:** primeira vez que a oportunidade é divulgada;
- **PRAZO PRÓXIMO:** faltam mais de 20 dias para o prazo;
- **ÚLTIMOS DIAS:** faltam menos de 20 dias;
- **FLUXO CONTÍNUO:** sem prazo fixo de inscrição.

**No site, o status é calculado automaticamente, em dois eixos** exibidos lado a lado:
- **Novidade** (pílula "Novo"): oportunidade inserida há até 20 dias. A data de cadastro original é preservada, então um item republicado não ganha "Novo" de novo.
- **Urgência:**
  - **Prazo próximo** (mais de 20 dias);
  - **Últimos dias** (até 20 dias);
  - **Fluxo contínuo** (sem prazo fixo);
  - **Encerrado** (o prazo já passou).

  Com mais de uma data no prazo, vale a **última**: "24/07/2026 (Jornalismo: 15/09/2026)" encerra em 15/09. Eventos sem inscrição não têm pílula de urgência e encerram quando o evento termina.

---

## Dois "históricos" diferentes — não confundir

| | Rascunhos do editor | Edições publicadas e site |
|---|---|---|
| Onde fica | No navegador (**💾 Salvar Edição**) | `edicoes/ed-XX/dados.json`, `edicoes/indice.json` e `banco.json`, versionados no Git |
| O que guarda | Rascunhos pessoais de edições | O que foi de fato publicado |
| Aparece em outros computadores? | Não, só naquele navegador | Sim, o mesmo para todo mundo |
| Onde ver no sistema | 📚 Histórico → "Rascunhos salvos neste navegador" | 📚 Histórico → "Edições publicadas" |
| É o registro oficial? | Não | **Sim** |

---

## Perguntas frequentes

**Exportar o JSON traz os dados de todas as edições anteriores?**
Não. Exporta só o que está no formulário, uma edição por vez.

**Importar um JSON por engano apaga alguma coisa?**
Não. Importar só preenche os campos na tela. Quem altera o `banco.json` é o merge, e ele só soma.

**Preciso criar a pasta `edicoes/ed-XX/` toda vez?**
Sim, uma vez por edição. Não há automação para isso.

**Por que a coluna "Edição" fica vazia em alguns cliques da planilha?**
Os cliques feitos no **site** não pertencem a uma edição. A edição é registrada quando o clique vem do boletim ou do WhatsApp.

**Os cliques das edições 01 a 04 são contados?**
Não. Elas foram enviadas antes da página de passagem, com os links diretos dos editais. A contagem por edição começa na ed-05.

**Preciso pedir um novo link curto à Comunicação?**
Não. O `links.ifes.edu.br/radar` aponta para a página inicial do site, que não mudou. Os links dos editais são gerados pelo próprio Radar.

**O aviso "Parecido com…" apareceu, mas é outra chamada do mesmo edital. E agora?**
Pode manter. Chamadas diferentes são oportunidades diferentes. O aviso existe para pegar o caso em que é o **mesmo** edital escrito de outro jeito.

**O dashboard mostra um número diferente do que eu esperava.**
Confira o **período** selecionado no painel do topo. Com "3 meses", por exemplo, edições mais antigas ficam de fora.

---

## Manutenção técnica (resumo)

- **Planilha de cliques:** o código do Apps Script está em `apps-script/Codigo.gs`. Para alterar, cole o código novo no Apps Script da planilha e use **Implantar → Gerenciar implantações → editar → Nova versão**, para a URL não mudar. A URL fica em `ir.html` (`REGISTRO_URL`) e em `index.html` (`METRICAS_URL`).
- **Não usar o parâmetro `c`** nos pedidos ao Apps Script: o Google o reserva e recusa o pedido. A categoria vai em `cat`.
- **Código do edital** (`codigoEdital`): a mesma função existe em `index.html`, `ir.html` e `radar_sistema_dppge.html`. Se mudar uma, mude as três.
- **Regra de títulos parecidos:** igual em `scripts/merge_edicao.py` (`titulos_parecidos`) e no sistema (`titulosParecidos`). Se mudar uma, mude a outra.
- Detalhes completos, design system e compatibilidade com o Outlook: [CLAUDE.md](CLAUDE.md).
