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

**Importante:** `banco.json` ≠ `edicoes/ed-XX/dados.json`. O primeiro é a base pública e cumulativa do site (nunca perde oportunidades antigas); o segundo é o conteúdo de uma edição isolada do boletim (o que foi enviado por e-mail naquela ocasião).

---

## Fluxo de trabalho

```
1. Pesquisar oportunidades relevantes na web
2. Fazer curadoria — decidir o que entra na edição
3. Criar o JSON da edição em edicoes/ed-XX/dados.json
   (imagens exclusivas da edição em edicoes/ed-XX/imagens/)
4. Abrir radar_sistema_dppge.html → Importar JSON → editar/revisar no editor
5. Salvar/ajustar → Exportar JSON → sobrescrever edicoes/ed-XX/dados.json
6. Clicar em "Gerar para Outlook" → nova aba abre → Ctrl+A → Ctrl+C → colar no Outlook → enviar e-mail
7. Atualizar o site: python3 scripts/merge_edicao.py edicoes/ed-XX
   (funde a edição no banco.json acumulado, preservando tudo que já foi publicado)
8. Commitar e fazer push → site público atualiza automaticamente
```

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
  "local": "... (só para categoria evento)"
}
```

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
      "dataCadastro": "07/07/2026"
    }
  ]
}
```

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

Os dois status aparecem como pílulas lado a lado em cada oportunidade.

**Deduplicação:** ao rodar `scripts/merge_edicao.py`, o título normalizado é usado como chave. Se a oportunidade já existe no `banco.json`, atualiza prazo/link/valor/status mas preserva a `dataCadastro` original (garante que a badge "Novo" não reapareça em itens antigos republicados).

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
- **Histórico** salvo em localStorage do navegador
- **Dashboard** com gráficos Chart.js e filtros de 3/6/9/12 meses
- **Exportar JSON** → baixa o arquivo para subir no GitHub
- **Importar JSON** → carrega edição anterior
- **Modelo + Prompt IA** → prompt completo para gerar JSON via Claude

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
- **Dashboard** no menu com KPIs e 4 gráficos
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
