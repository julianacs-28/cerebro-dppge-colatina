# Radar de Oportunidades — DPPGE · Ifes Campus Colatina

## Sobre o projeto

O **Radar de Oportunidades** é um ecossistema de comunicação institucional da Diretoria de Pesquisa, Pós-Graduação e Extensão (DPPGE) do Ifes Campus Colatina. Seu objetivo é divulgar editais, bolsas, fomento e oportunidades acadêmicas para a comunidade do campus (docentes, técnicos, estudantes de graduação e pós-graduação).

**Responsável:** Juliana Cristina da Silva Cassaro — Assistente em Administração, DPPGE · Ifes Colatina  
**Contato institucional:** pesquisa.col@ifes.edu.br  
**Formação:** Design — todas as decisões visuais devem considerar estética, hierarquia e experiência do usuário.

---

## Arquivos e pastas do projeto

| Caminho | Função |
|---|---|
| `index.html` | Site público do portal de oportunidades (GitHub Pages) — lê `banco.json` |
| `banco.json` | Acumulado real de **todas** as oportunidades já divulgadas — fonte única do site, gerado pelo script de mesclagem (nunca editar à mão) |
| `radar_sistema_dppge.html` | Sistema interno de gestão — editor, preview, histórico, dashboard de uma edição |
| `edicoes/ed-XX/dados.json` | JSON de uma edição específica do boletim (o que foi/será importado no editor) |
| `edicoes/ed-XX/imagens/` | Imagens exclusivas daquela edição (referenciadas com caminho relativo à raiz de `radar-oportunidades/`, ex: `edicoes/ed-03/imagens/destaque.jpg`) |
| `scripts/merge_edicao.py` | Funde o `dados.json` de uma edição no `banco.json` acumulado |
| `scripts/preencher_historico.py` | Preenche retroativamente `primeiraDivulgacao`/`primeiraEdicao`/`prazoOriginal` (já rodado em 14/10/2026; só precisa de novo se algo for refeito) |
| `ir.html` | Página de passagem: registra o clique de um edital na planilha de métricas e redireciona para o edital (ver seção "Métricas de cliques") |
| `apps-script/Codigo.gs` | Código do Google Apps Script que recebe os cliques (copiar/colar no Apps Script da planilha — não roda a partir daqui) |
| `edicoes/indice.json` | Índice de todas as edições e avulsas publicadas — gerado pelo merge (nunca editar à mão); lido pelo Histórico do sistema e pelo dashboard do site ("Boletins enviados") |
| `metricas/` | Atalho da planilha Google "RADAR-cliques-nos-editais" (no `.gitignore`; os dados ficam na conta institucional) |
| `docs/` | Planos e documentação de apoio |
| `edicoes/avulsas/AAAA-MM-DD-slug/dados.json` | Inclusão avulsa no site, fora do ciclo de uma edição (ver seção própria abaixo) |
| `edicoes/avulsas/REGISTRO.md` | Log humano de todas as inclusões avulsas já feitas |

**Importante:** `banco.json` ≠ `edicoes/ed-XX/dados.json`. O primeiro é a base pública e cumulativa do site (nunca perde oportunidades antigas); o segundo é o conteúdo de uma edição isolada do boletim (o que foi enviado por e-mail naquela ocasião).

---

## Fluxo de trabalho

```
1. Pesquisar oportunidades relevantes na web
2. Fazer curadoria — decidir o que entra na edição
3. Criar o JSON da edição em edicoes/ed-XX/dados.json
   (imagens exclusivas da edição em edicoes/ed-XX/imagens/)
4. Abrir radar_sistema_dppge.html → Importar JSON → editar/revisar no editor
5. Clicar em "✔ Revisar edição" e resolver os itens "Corrigir" (resumo sem título exato,
   link vazio, título parecido com um já divulgado etc.)
   Salvar/ajustar → Exportar JSON → sobrescrever edicoes/ed-XX/dados.json
6. Atualizar o site: python scripts/merge_edicao.py edicoes/ed-XX
   (funde a edição no banco.json acumulado, preservando tudo que já foi publicado)
7. Commitar e fazer push → aguardar ~1 minuto até o GitHub Pages publicar
8. SÓ ENTÃO: "Gerar para Outlook" → nova aba abre → Ctrl+A → Ctrl+C → colar no Outlook → enviar e-mail
   e "Gerar para WhatsApp" → enviar
   Se aparecer a faixa amarela "Este gerador está diferente da versão publicada no site":
   salvar a edição, recarregar a página (F5) e abrir a edição de novo antes de gerar.
```

**⚠️ Aba antiga = boletim sem contagem de cliques (aconteceu na ed-05):** o Pull no GitHub Desktop atualiza o arquivo no computador, mas uma aba do gerador que já estava aberta continua rodando o código antigo até ser recarregada. Por isso o gerador compara o próprio código (o `<script id="codigo-gerador">`) com o publicado no site — ao abrir, ao voltar para a aba e antes de gerar — e mostra a faixa amarela/pergunta se forem diferentes. Logo depois de um push, a faixa pode aparecer por ~1 minuto até o GitHub Pages publicar; é esperado.

**⚠️ A ordem importa (mudou em out/2026):** os links dos editais no boletim e no WhatsApp passam por `ir.html`, que procura o edital no `banco.json` **publicado**. Se o boletim for enviado antes do merge + push, o clique é registrado, mas a pessoa cai na página inicial do Radar em vez do edital.

---

## Inclusões avulsas (fora de uma edição)

Quando surge uma oportunidade urgente **depois** de uma edição já ter sido enviada — e não vale a pena esperar a próxima —, ela pode ser publicada direto no site sem esperar o próximo boletim. Critério: prazo apertado (não sobreviveria até a próxima edição) ou item de alto impacto. Fora isso, esperar e incluir normalmente na próxima edição.

```
1. Criar edicoes/avulsas/AAAA-MM-DD-slug-curto/dados.json
   contendo só "categorias": { ... } com o(s) card(s) novo(s)
   (mesma estrutura de card usada em edicoes/ed-XX — ver abaixo).
   Campos "data" (DD/MM/AAAA) e "motivo" no topo do JSON. A "data" é lida
   pelo merge: vira a primeiraDivulgacao dos itens novos (antecedência).
   O "motivo" é só documentação.
2. Atualizar o site: python3 scripts/merge_edicao.py edicoes/avulsas/AAAA-MM-DD-slug-curto
3. Registrar a inclusão em edicoes/avulsas/REGISTRO.md (uma linha na tabela)
4. Commitar e fazer push
5. Se o prazo for curto, considerar um aviso avulso (e-mail simples ou
   WhatsApp) além do site — não precisa ser um boletim completo.
   O item entra normalmente na próxima edição numerada de qualquer forma.
```

**Não é uma "edição"** — não tem `numero`, `mes`, `dataEnvio` nem `destaque` institucional, e não é importado no `radar_sistema_dppge.html` para gerar um boletim. Serve só para alimentar o `banco.json` (site) antes do tempo.

---

## Estrutura de dados (edicoes/ed-XX/dados.json)

```json
{
  "numero": "01",
  "mes": "Julho 2026",
  "dataEnvio": "01/07/2026",
  "destaque": {
    "status": "NOVO",
    "categoria": "pesquisa",
    "origem": "Coord. de Pesquisa",
    "titulo": "Nome do Edital",
    "link": "https://...",
    "resumo": "O Nome do Edital visa/oferece/apoia [ação], destinado a [público]. [Detalhe operacional].",
    "prazo": "DD/MM/AAAA",
    "valor": "R$ 0.000",
    "publico": "Público-alvo",
    "imagem": "https://github.com/...?raw=true",
    "ctaTexto": "Acessar Edital → (opcional — sobrescreve o texto padrão do botão)",
    "institucional": "false (opcional — true quando o destaque é boas-vindas/aviso, não uma oportunidade real; nesse caso não é mesclado no banco.json e normalmente vem com status e categoria vazios, ver abaixo)"
  },
  "categorias": {
    "pesquisa": [...],
    "internac": [...],
    "bolsas": [...],
    "evento": [...],
    "premiacoes": [...],
    "extensao": [...]
  },
  "informes": [
    {
      "titulo": "Título",
      "texto": "Texto do informe.",
      "email": "pesquisa.col@ifes.edu.br"
    }
  ]
}
```

### Campos de cada card de categoria
```json
{
  "status": "NOVO | PRAZO PRÓXIMO | ÚLTIMOS DIAS | FLUXO CONTÍNUO | \"\" (sem status)",
  "origem": "Ver lista de origens abaixo",
  "titulo": "Nome completo do edital",
  "link": "https://...",
  "resumo": "Texto seguindo a fórmula padrão",
  "prazo": "DD/MM/AAAA",
  "valor": "R$ ...",
  "publico": "...",
  "imagem": "https://github.com/...?raw=true (opcional)",
  "local": "... (só para categoria evento)",
  "dataEvento": "DD/MM/AAAA ou \"23 a 25/09/2026\" (só para categoria evento)",
  "semInscricao": "false | true (só para categoria evento)"
}
```

### Cards de Eventos (categoria `evento`)

- **`prazo` é sempre o fim das inscrições**, nunca a data do evento. No boletim, no site e no WhatsApp aparece como "Inscrições até DD/MM/AAAA".
- **`dataEvento`** = quando o evento acontece: `DD/MM/AAAA`, `23 a 25/09/2026` ou `28/09 a 02/10/2026`. Aparece como "Realização: ...". O editor avisa se o formato não for reconhecido.
- **`semInscricao: true`** só quando o evento é de acesso livre, sem nenhuma inscrição. O prazo fica vazio e o boletim/site mostram "Não é necessária inscrição". **Gratuito ≠ sem inscrição** — o mais comum é evento gratuito com inscrição.
- Um card de evento nunca deve ficar com prazo vazio sem `semInscricao` marcado — o editor mostra um aviso em vermelho.
- No site, evento sem inscrição não tem pílula de urgência; vira "Encerrado" quando a última data de `dataEvento` passa.
- Itens antigos (antes de out/2026) não têm `dataEvento`; se o `prazo` deles for um intervalo ("26/07 a 01/08/2026"), o dashboard trata como data do evento.

### Status e categoria vazios ("sem vínculo")

`status` (em qualquer card ou no destaque) e `categoria` (só no destaque) aceitam `""` — o editor mostra a opção **"— Sem status —"** / **"— Sem categoria —"** nos selects. Quando vazio:
- Nenhuma badge de status é renderizada no boletim (fica só a origem, sem a barra separadora).
- Nenhum rótulo de categoria é renderizado acima do destaque.

Uso típico: destaque **institucional** (boas-vindas, aviso), que não é uma oportunidade real e não deve carregar um selo "NOVO" nem ser associado a uma categoria de conteúdo — ver `edicoes/ed-01/dados.json` para um exemplo real.

---

## Estrutura de dados (banco.json)

Gerado automaticamente por `scripts/merge_edicao.py` — nunca editar à mão. É uma lista plana (sem separação por edição), com `_cat` indicando a categoria e `dataCadastro` preservada entre mesclagens:

```json
{
  "atualizadoEm": "07/07/2026",
  "oportunidades": [
    {
      "_cat": "pesquisa",
      "status": "NOVO",
      "origem": "Coord. de Pesquisa",
      "titulo": "Nome do Edital",
      "link": "https://...",
      "resumo": "...",
      "prazo": "DD/MM/AAAA",
      "valor": "R$ 0.000",
      "publico": "Público-alvo",
      "imagem": "",
      "dataCadastro": "07/07/2026",
      "primeiraDivulgacao": "07/07/2026",
      "primeiraEdicao": "01",
      "prazoOriginal": "DD/MM/AAAA"
    }
  ]
}
```

`primeiraDivulgacao` (data de envio da edição, ou `data` da avulsa), `primeiraEdicao` (número ou `"avulsa"`) e `prazoOriginal` (prazo no momento do primeiro anúncio) são gravados pelo merge **só na primeira vez** que o edital aparece e nunca mais mudam — mesmo que o prazo seja prorrogado depois. Servem para medir a antecedência de divulgação (dashboard).

---

## Métricas de cliques nos editais

Os links de cada edital no **site**, no **boletim** e no **WhatsApp** passam por `ir.html`:

```
.../radar-oportunidades/ir.html?e=CODIGO&de=CANAL&ed=NUMERO_EDICAO
```

- `e` = código curto do título (função `codigoEdital`, FNV-1a 32 bits em base36 sobre o título normalizado). **A mesma função existe em `index.html`, `ir.html` e `radar_sistema_dppge.html` — se mudar uma, mude as três.**
- `de` = `site` | `boletim` | `whatsapp`. `ed` = número da edição (não existe nos cliques vindos do site).
- `ir.html` procura o edital no `banco.json`, envia o registro ao App da Web do Apps Script (em paralelo, sem bloquear) e redireciona para o `link` atual. Se o código não for encontrado, vai para a página inicial do Radar.
- O destaque **institucional** e cards sem título/link mantêm o link original (não são rastreados).
- A planilha guarda só data/hora, código, título, edição, categoria e canal — **nenhum dado pessoal**. O dashboard do **site** lê a planilha (`?acao=dados`) e mostra "cliques nos editais" / "indicador de interesse". **Nunca chamar de "pessoas interessadas":** sem identificar o usuário, 100 cliques podem ser menos de 100 pessoas.
- Antecedência (dashboard do site, pública com tabela e CSV), em dias a partir de `primeiraDivulgacao`, em três blocos:
  1. **Até o fim das inscrições** — `prazoOriginal` começa por `DD/MM/AAAA` (qualquer categoria, inclusive eventos com inscrição; com dois prazos vale o primeiro). Mostra média e quantos tiveram menos de 7 dias (alerta).
  2. **Até o evento** — eventos com `semInscricao` (início de `dataEvento`) e itens antigos com prazo em intervalo.
  3. **Sem prazo de encerramento** — contagem à parte: fluxo contínuo + prazo não definido (ex.: EPLI).
- A URL do App da Web está em `ir.html` (`REGISTRO_URL`) e em `index.html` (`METRICAS_URL`). Ao mudar o `apps-script/Codigo.gs`, colar na planilha e usar **Implantar → Gerenciar implantações → editar → Nova versão** (assim a URL não muda).

---

## Design System

### Paleta institucional
| Uso | Cor |
|---|---|
| Verde escuro (cabeçalho/rodapé boletim) | `#0c420b` |
| Verde médio (faixas secundárias) | `#196d1e` |
| Fundo externo do boletim | `#ededed` |
| Fundo do site | `#f9f9f7` |
| Branco | `#ffffff` |
| Borda | `#e8e8e4` |

### Paleta por categoria
| Categoria | Chave JSON | Fundo | Cor texto |
|---|---|---|---|
| Pesquisa & Fomento | `pesquisa` | `#EBE9F4` | `#4A368F` |
| Internacionalização | `internac` | `#DDE8FA` | `#0149AF` |
| Bolsas & Auxílios | `bolsas` | `#F4CEDD` | `#C2195A` |
| Eventos & Capacitações | `evento` | `#FCE5D5` | `#A03B11` |
| Premiações | `premiacoes` | `#F5EFD7` | `#7A5B00` |
| Extensão & Comunidade | `extensao` | `#D7F6F1` | `#006A5C` |

### Paleta de status (semáforo)
| Status | Cor borda/texto | Fundo | Ícone GitHub |
|---|---|---|---|
| NOVO | `#1B5E20` | `#e8f5e8` | `novo.png` |
| PRAZO PRÓXIMO | `#F57F17` | `#fff8e1` | `circulo-laranja.png` |
| ÚLTIMOS DIAS | `#C41E3A` | `#ffebee` | `ultimos-dias.png` |
| FLUXO CONTÍNUO | `#9E9E9E` | `#f5f5f5` | `fluxo-continuo.png` |

### Tipografia
- Fonte principal: `'Segoe UI', Arial, sans-serif`
- Segoe UI é nativa do Windows/Outlook — usar sempre como primeira opção

---

## Ícones — Repositório GitHub

Base URL: `https://github.com/julianacs-28/radar-oportunidades-imagens/blob/main/`  
Sufixo obrigatório: `?raw=true`

| Ícone | Arquivo |
|---|---|
| Logo Radar | `radar-oportunidades.png` |
| Estrela (Destaque) | `estrela.png` |
| Pesquisa & Fomento | `pesquisa-fomento.png` |
| Internacionalização | `internacionalizacao.png` |
| Bolsas & Auxílios | `bolsas-auxilio.png` |
| Eventos & Capacitações | `evento-capacitacao.png` |
| Premiações | `premiacoes.png` |
| Extensão & Comunidade | `comunidade_extensao.png` |
| Informes | `informes.png` |
| Status NOVO | `novo.png` |
| Status PRAZO PRÓXIMO | `circulo-laranja.png` |
| Status ÚLTIMOS DIAS | `ultimos-dias.png` |
| Status FLUXO CONTÍNUO | `fluxo-continuo.png` |
| Calendário | `calendario.png` |
| Dinheiro | `dinheiro.png` |
| Público-alvo | `publico-alvo.png` |
| E-mail | `email.png` |
| Localização | `localizacao.png` |

---

## Origens disponíveis (campo "origem" no JSON)

- Coord. de Pesquisa
- Coord. de Pós-Graduação
- Coord. de Extensão
- Coord. de Laboratórios
- Coord. de Rel. Institucionais
- Núcleo de Rel. Internacionais
- Núcleo de Arte e Cultura
- Núcleo de Ed. Ambiental
- Núcleo de Incubação
- DPPGE

---

## Regras de escrita do resumo

**Fórmula padrão:**
> [Nome do edital/programa, linkado] visa/oferece/apoia [ação principal], destinado a [público-alvo]. [Detalhe operacional relevante].

**Título:**
- Nunca em MAIÚSCULAS — maiúscula só no início das palavras principais e nas siglas (o editor corrige sozinho)
- Padrão recomendado (não obrigatório — a ordem é livre): `[Nome do programa] — [Instituição] (Edital NN/AAAA[, Nª chamada])`, com travessão " — " como separador
- Republicação: repetir o título **exatamente** como na primeira divulgação

**Regras:**
- Máximo 3 frases
- O nome do edital aparece linkado dentro do resumo (não apenas no CTA)
- O CTA final deve ser descritivo: "Acessar Edital PRPPG 10/2024 →" (nunca "Ver edital →")
- Linguagem clara, objetiva e institucional

**Exemplo correto:**
> O [Edital PRPPG 10/2024 — Prociência](link) apoia projetos de pesquisa institucionais no âmbito do Ifes. As propostas devem ser submetidas pelo sistema SIGPESq, com análise por comitê gestor que avalia currículo Lattes e produção técnico-científica recente.

**⚠️ Regra crítica — o `resumo` deve conter o `titulo` EXATO (caractere a caractere):**

O link dentro do resumo não é markdown — é gerado automaticamente. Tanto o boletim (`radar_sistema_dppge.html`, via `resumo.replace(titulo, ...)`) quanto o site (`index.html`, que linka o `.oport-titulo` inteiro com `o.link`) dependem do texto do `resumo` **conter a string do `titulo` de forma idêntica**, incluindo sufixos como "— Fapes", "(Edital 18/2026)", "— Programa X". Se o resumo usar uma versão abreviada, parafraseada ou reordenada do título, o `.replace()` não encontra a ocorrência e **falha silenciosamente** — sem erro, mas também sem link no meio do texto.

Checklist antes de salvar um card:
- [ ] Copiar o `titulo` literalmente (copiar/colar, não reescrever) para dentro da primeira frase do `resumo`
- [ ] Não abreviar, não reordenar, não remover sufixos do título ao mencioná-lo no resumo
- [ ] Conferir com `titulo in resumo` (Python) ou busca de texto simples antes de publicar

Isso já causou o problema real na ed-01, onde vários resumos mencionavam apenas uma versão curta do título (ex.: título "Parcerias entre Startups — Fapes (Edital 18/2026)" mas resumo começando com "O Edital Fapes Nº 18/2026...") — o link nunca aparecia no meio do texto, nem no boletim nem no site.

---

## Lógica de status

### No boletim (decisão editorial)
- **NOVO** = primeira vez que a oportunidade é divulgada
- **PRAZO PRÓXIMO** = mais de 20 dias para encerrar
- **ÚLTIMOS DIAS** = menos de 20 dias para encerrar
- **FLUXO CONTÍNUO** = sem prazo fixo de inscrição

### No site público (automático — dois eixos independentes)
**Eixo 1 — Novidade** (baseado em `dataCadastro`):
- NOVO = inserido no `banco.json` há ≤ 20 dias
- `dataCadastro` é adicionado por `scripts/merge_edicao.py` na primeira vez que a oportunidade aparece em alguma edição

**Eixo 2 — Urgência** (baseado no prazo):
- ÚLTIMOS DIAS = prazo em ≤ 20 dias
- PRAZO PRÓXIMO = prazo em > 20 dias
- FLUXO CONTÍNUO = sem prazo fixo
- ENCERRADO = prazo já passou
- Com mais de uma data no prazo, vale a **última** data completa: "24/07/2026 (Jornalismo: 15/09/2026)" encerra em 15/09; "26/07 a 01/08/2026" encerra em 01/08. (A antecedência usa a **primeira**.)
- Evento com `semInscricao`: sem pílula de urgência; vira ENCERRADO quando a última data de `dataEvento` passa.

Os dois status aparecem como pílulas lado a lado em cada oportunidade.

**Deduplicação:** ao rodar `scripts/merge_edicao.py`, o título normalizado (minúsculas, espaços colapsados) é usado como chave. Se a oportunidade já existe no `banco.json`, atualiza título/prazo/link/valor/status/resumo mas preserva `dataCadastro`, `primeiraDivulgacao`, `primeiraEdicao` e `prazoOriginal` (a badge "Novo" não reaparece e a antecedência não muda). O título também é atualizado porque a chave ignora maiúsculas: "EDITAL FAPES…" corrigido para "Edital Fapes…" é o mesmo item, e o resumo novo precisa continuar contendo o título exato.

**Títulos parecidos:** a verificação principal é no editor (curadoria). O merge repete o aviso no terminal como rede de segurança, sem bloquear. Regra (igual em `merge_edicao.py → titulos_parecidos` e no editor → `titulosParecidos`; mudar nos dois): mesmo número de edital `NN/AAAA` do mesmo órgão, **ou** maioria das palavras de conteúdo em comum (ignorando órgãos, anos e termos genéricos como "edital", "chamada", "pesquisa"). Calibrada em out/2026: 2 pares sinalizados entre 666 do banco (Fapes 28 3ª×4ª chamada; PAEP×PAEP-EB) — ambos legítimos. Chamadas diferentes de um mesmo edital (3ª e 4ª chamada) são itens **distintos** e corretos.

---

## Compatibilidade Outlook Desktop (boletim)

O boletim HTML é enviado via Outlook Desktop clássico (motor Word). Regras críticas:

- ✅ Todo layout em `<table>` — nunca CSS flexbox ou grid
- ✅ Cores apenas hexadecimais sólidas — nunca `rgba()`
- ✅ `line-height` sempre em `px` com `mso-line-height-rule:exactly`
- ✅ Todos os ícones como PNG externos (GitHub) — nunca SVG base64 ou emoji
- ✅ `mso-padding-alt` em botões
- ✅ Conditional comments `<!--[if mso]>` para largura fixa 620px
- ✅ `text-align:left` explícito em células de conteúdo
- ❌ Nunca `rgba()`, SVG base64, emoji unicode
- ❌ `border-radius` em botões grandes não funciona no Outlook — usar retângulo

**Fluxo correto de envio:**
1. Clicar "Gerar para Outlook" no sistema
2. Boletim abre em nova aba do navegador
3. Ctrl+A → Ctrl+C na nova aba
4. Colar no corpo do e-mail no Outlook (nunca colar o código-fonte)

---

## Estrutura do boletim HTML gerado

```
Cabeçalho faixa 1 (verde médio #196d1e): instituição
Cabeçalho faixa 2 (verde escuro #0c420b): logo + título
Cabeçalho faixa 3 (verde médio): badge de edição + data

Destaque da Edição (fundo #f8fcf8, borda esquerda verde)
  └── badge status + origem + título + imagem + resumo + dados + botão

[Para cada categoria com cards:]
Cabeçalho de categoria (fundo colorido da categoria)
  └── Card: badge status + origem + título + resumo + dados + CTA

Informes da DPPGE
  └── Card com borda esquerda verde + e-mail

Rodapé (verde escuro #0c420b)
```

---

## Sistema de gestão (radar_sistema_dppge.html)

Aplicação HTML standalone com:
- **Editor** com 4 abas: Edição, Destaque, Categorias, Informes
- **Preview em tempo real** ao lado do editor
- **Verificação de títulos** (curadoria) — abaixo de cada título, compara com o `banco.json` publicado: "ℹ Já divulgado" (republicação) ou "⚠ Parecido com…" (possível mesmo edital escrito de outro jeito). Título em MAIÚSCULAS é corrigido sozinho ao sair do campo (siglas preservadas, mesmo trecho corrigido no resumo, com "Desfazer"); também ao importar um JSON.
- **✔ Revisar edição** (botão no topo) — checklist de todos os cards antes de fechar o boletim: resumo sem o título exato, link vazio, títulos parecidos/já divulgados, maiúsculas, eventos sem prazo/sem caixa, data de envio. Nunca bloqueia.
- **Histórico** — "Edições publicadas" (lidas de `edicoes/indice.json`, iguais para todos; botões Abrir no editor e HTML), "Inclusões avulsas" e, à parte, "Rascunhos salvos neste navegador" (localStorage, só naquele computador)
- **Aviso de versão** — faixa amarela no topo quando o código da aba é diferente do `radar_sistema_dppge.html` publicado; "Gerar para Outlook/WhatsApp" pergunta antes de gerar. Sem internet: só uma linha cinza discreta. Nunca bloqueia. O `id="codigo-gerador"` do `<script>` principal é o que a comparação usa — não remover.
- **Exportar JSON** → baixa o arquivo para subir no GitHub
- **Importar JSON** → carrega edição anterior
- **Modelo + Prompt IA** → prompt completo para gerar JSON via Claude
- **Não tem mais dashboard** (removido em out/2026) — o dashboard oficial é o do site.
- O Histórico publicado e a verificação de títulos leem arquivos do site: só funcionam com o sistema aberto pelo endereço do GitHub Pages (ou por um servidor local), não como arquivo `file://`.

---

## Site público (index.html)

Portal web com GitHub Pages:
- **Header fixo** verde com logo branco
- **Hero** verde com título e botões de ação
- **Barra de stats**: total de oportunidades, novas (≤20 dias), encerram em breve
- **Categorias** em grid 3 colunas com cards coloridos
- **Busca** por palavra-chave + filtro de instituição + filtro de categoria
- **Oportunidades recentes** com filtros de status (design igual ao semáforo)
- **Página de categoria** (tela inteira) com busca, filtro de status e origem
- **Dashboard** (oficial, público) — conta abertas **e** encerradas, filtrado pela data do primeiro anúncio (`primeiraDivulgacao`):
  - Indicadores: Divulgadas · Abertas agora · Encerradas · Novas · Encerram em breve · Boletins enviados (de `edicoes/indice.json`)
  - Gráficos de barras com **quantidade e %** escritos: por categoria, por coordenadoria/núcleo (8+ viram "Outras origens"), evolução mensal (só quantidade)
  - **Cliques nos editais** (planilha via Apps Script): mais clicados, por canal, por categoria, por edição
  - **Antecedência de divulgação**: 4 indicadores + tabela completa pública + "Baixar tabela (CSV)"
  - Categorias em **barras com o nome escrito**, não rosca: as cores oficiais Premiações × Eventos e Pesquisa × Internacionalização não se distinguem para daltônicos (validado). Cores dos canais (site/boletim/WhatsApp = verde/azul/magenta) validadas.
- **Sobre DPPGE** com informações institucionais e contato
- **Rodapé** verde com links de navegação

**URL pública:** `https://julianacs-28.github.io/cerebro-dppge-colatina/radar-oportunidades/`  
**Sistema interno:** `https://julianacs-28.github.io/cerebro-dppge-colatina/radar-oportunidades/radar_sistema_dppge.html`  
**URL curta (com métricas de acesso) — usar sempre no boletim e na mensagem de WhatsApp:** `https://links.ifes.edu.br/radar` (redireciona para a URL pública acima; constante `SITE_URL` em `radar_sistema_dppge.html`)

---

## Prompt para geração de conteúdo via IA

Quando receber dados de um edital (link, PDF ou texto), gerar JSON seguindo:

```
FONTES A CONSULTAR (quando o pedido for "buscar oportunidades novas", não
apenas transformar um edital específico já enviado):
- https://fapes.es.gov.br/
- https://www.gov.br/cnpq/pt-br
- https://www.gov.br/capes/pt-br
- http://portal.sbpcnet.org.br/
- https://www.ifes.edu.br/
- https://www.gov.br/inpe/pt-br
- https://www.gov.br/mcti/pt-br
- https://www.frm.org.br/
- https://www.fundacaopetermuranyi.org.br/main.asp?pag=premioatual
- https://fapesp.br/
- https://fapemig.br/
- https://www.gov.br/inpi/pt-br

ATENÇÃO — oportunidades interestaduais: mesmo em fontes regionais de outros
estados (ex.: Fapesp/SP, Fapemig/MG), verificar se o edital permite
participação de pesquisadores/instituições de outros estados, incluindo o
Espírito Santo — é comum haver chamadas nacionais publicadas por uma
fundação estadual. Só descartar se o edital for explicitamente restrito a
instituições daquele estado.

STATUS disponíveis: "NOVO" | "PRAZO PRÓXIMO" | "ÚLTIMOS DIAS" | "FLUXO CONTÍNUO"
CATEGORIAS: "pesquisa" | "internac" | "bolsas" | "evento" | "premiacoes" | "extensao"
ORIGENS: [lista acima]

FÓRMULA DO RESUMO:
[Nome do edital, que será linkado] visa/oferece/apoia [ação], destinado a [público]. [Detalhe operacional].

LINK: no campo "link", sempre o endereço ORIGINAL do edital. Nunca link
encurtado nem link do Radar (ir.html, links.ifes.edu.br) — o sistema gera
sozinho o link rastreável de cada edital no site, no boletim e no WhatsApp.

REGRA CRÍTICA: o texto de "resumo" deve conter o valor de "titulo" REPRODUZIDO
EXATAMENTE (mesmos caracteres, incluindo sufixos como "— Fapes" ou
"(Edital X/2026)"), pois o link dentro do resumo é inserido por substituição
de string exata (resumo.replace(titulo, ...)) tanto no boletim quanto no
site. Título abreviado, parafraseado ou reordenado = link não aparece.
Copie o título literalmente para dentro da primeira frase do resumo, não o
reescreva.

Retornar APENAS o JSON, sem texto adicional.
```

---

## Decisões de design importantes

- **Sem caixas excessivas** — design limpo com espaço em branco generoso
- **Hierarquia clara** — títulos grandes, labels em uppercase espaçado
- **Links sempre descritivos** — nunca "Ver mais" ou "Saiba mais" genérico
- **Acessibilidade** — links com contexto completo para leitores de tela
- **Consistência visual** — boletim e site usam o mesmo design system e ícones
