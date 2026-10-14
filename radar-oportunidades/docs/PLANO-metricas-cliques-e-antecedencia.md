# Plano de implementação — Métricas de cliques e antecedência de divulgação

**✅ CONCLUÍDO E PUBLICADO em 14/10/2026** (commit `478b388`). Teste de ponta a ponta aprovado: 3 cliques reais no site público registrados na planilha com edital, categoria e canal. Este documento fica como registro das decisões; a referência atual de funcionamento é o `CLAUDE.md`.

Lições do teste que ficaram no código: o parâmetro `c` é reservado pelo Google (a categoria vai em `cat`); o Apps Script grava tudo como texto (senão "04" vira 4 e códigos como "1e5" viram número).

**Atualização (14/10/2026, tarde):** decidido e implementado — dashboard oficial passa a ser o do **site** (abertos + encerrados, valores e % nos gráficos, antecedência pública com CSV, boletins enviados); dashboard do sistema **removido**; Histórico lê `edicoes/indice.json`; verificação de títulos parecidos na curadoria (editor + botão "Revisar edição") e no merge; correção automática de maiúsculas; site lê prazos com várias datas (vale a última). Detalhes no `CLAUDE.md`.

**Status (14/10/2026):** código escrito e testado localmente; **falta** atualizar o Apps Script, commit/push e teste de ponta a ponta. Já feito: planilha criada, Apps Script de teste implantado e acessível por "Qualquer pessoa", Python 3.12 instalado, `ir.html`, links do site/boletim/WhatsApp, campos novos no merge, preenchimento retroativo do `banco.json` e seções novas do dashboard.
**Decidido por:** Juliana Cassaro (DPPGE) · **Elaborado em:** 07/10/2026

---

## 1. Problemas a resolver

1. **Medir o interesse em cada edital**, somando os três canais de divulgação (site, boletim e WhatsApp) e sabendo de qual canal veio cada clique.
2. **Medir com quanta antecedência divulgamos cada oportunidade**: os dias entre o primeiro anúncio e o fim das inscrições, para usar em relatórios.

**Restrições:**
- a solução deve ser gratuita;
- deve ser fácil de manter;
- não pode depender de outros setores, como a TI;
- ninguém deve precisar criar ou alterar links à mão a cada edição.

---

## 2. Decisão: sistema próprio (Google Planilhas + Apps Script)

Avaliamos duas propostas.

| | GoatCounter (externo) | **Planilha própria (escolhida)** |
|---|---|---|
| Custo | Gratuito | Gratuito |
| Configuração | 2 min | ~15 min, uma vez |
| Dono dos dados | Serviço externo | **DPPGE** (conta `julianacs@ifes.edu.br`) |
| Integrado ao Radar | Não | **Sim**, aparece no dashboard do sistema |
| Relatórios personalizados | Limitado | **Livre** |
| Manutenção | Nenhuma | Baixa |

Por que a planilha própria foi escolhida:
- os dados ficam com a instituição;
- o resultado aparece no dashboard do próprio Radar;
- a planilha permite montar relatórios livres.

O link curto `links.ifes.edu.br/radar` continua em uso para o acesso geral ao site.

---

## 3. Parte A — Rastreamento de cliques

### 3.1 Desenho

```
Merge + push → GitHub Pages publica o banco.json
        ↓
Site, boletim e WhatsApp exibem links rastreáveis (montados automaticamente)
        ↓
Pessoa clica → ir.html (página de passagem no site do Radar)
        ├── envia o registro ao Apps Script → Google Planilha (1 linha por clique)
        └── abre o edital original (ao mesmo tempo; não espera a planilha)
        ↓
Dashboard do radar_sistema_dppge.html lê a planilha e apresenta os dados
```

Se o Google estiver fora do ar, a pessoa chega ao edital normalmente. Só aquele clique deixa de ser contado.

### 3.2 Formato do link

```
https://julianacs-28.github.io/cerebro-dppge-colatina/radar-oportunidades/ir.html?e=k3f9a2&de=whatsapp&ed=04
```

| Parâmetro | Significado | Valores |
|---|---|---|
| `e` | Código curto do edital, calculado do título normalizado (mesma chave de deduplicação do merge: minúsculas, espaços colapsados) | ex.: `k3f9a2` |
| `de` | Canal | `site` · `boletim` · `whatsapp` |
| `ed` | Edição | ex.: `04`; não existe nos cliques vindos do site |

- **O código `e`** é um hash do título (FNV-1a 32 bits em base36). Ele precisa dar o mesmo resultado no JavaScript (site, sistema e `ir.html`). Ninguém digita esse código.
- **O `ir.html` procura o código no `banco.json` publicado** e redireciona para o `link` atual. Por isso, se um link de edital for corrigido depois, os boletins antigos passam a levar ao endereço novo.
- **Se o código não for encontrado**, por exemplo num boletim enviado antes do merge, o clique é registrado do mesmo jeito e a pessoa vai para a página inicial do Radar. Ela nunca vê uma página de erro.

### 3.3 Estrutura da planilha

| Data/hora | Código | Edital | Edição | Categoria | Canal |
|---|---|---|---|---|---|
| 07/10 14:21 | k3f9a2 | FAPES 12/2026 | — | Pesquisa | site |
| 07/10 14:25 | k3f9a2 | FAPES 12/2026 | 04 | Pesquisa | whatsapp |
| 07/10 15:03 | k3f9a2 | FAPES 12/2026 | 04 | Pesquisa | boletim |

- **Nenhum dado pessoal** é guardado: nem IP, nem e-mail, nem identificador de usuário. Isso deixa a solução tranquila em relação à LGPD.
- **Robôs não devem ser contados.** Os antivírus de e-mail costumam "clicar" nos links para verificá-los, mas não executam JavaScript. Por isso o registro só é feito por JavaScript, quando um navegador real abre a página.

### 3.4 Nomenclatura no dashboard

Usar **"cliques nos editais"**, **"acessos aos editais"** ou **"indicador de interesse"**. Nunca usar "pessoas interessadas": sem identificar o usuário, 100 cliques podem vir de menos de 100 pessoas. O dashboard deve trazer uma nota curta explicando isso.

### 3.5 Indicadores do dashboard

- Editais mais clicados
- Cliques por canal (site × boletim × WhatsApp)
- Cliques por categoria
- Cliques por edição (comparação entre boletins)

---

## 4. Parte B — Antecedência de divulgação

### 4.1 O que já existe e por que não basta

- O `banco.json` tem o `prazo` e a `dataCadastro`. Hoje a `dataCadastro` coincide com a data de envio de cada edição, mas isso acontece por acaso: ela registra o dia em que o merge rodou.
- Quando um prazo é prorrogado, o merge sobrescreve o campo `prazo` e o **prazo original se perde**.
- Não fica registrado **onde** o edital foi anunciado pela primeira vez.

### 4.2 Campos novos no banco.json

O merge grava estes campos **só na primeira vez** que o edital aparece, e nunca mais os altera:

| Campo | Exemplo | Origem |
|---|---|---|
| `primeiraDivulgacao` | `06/10/2026` | `dataEnvio` da edição, ou `data` da avulsa |
| `primeiraEdicao` | `04` ou `avulsa` | `numero` da edição |
| `prazoOriginal` | `30/10/2026` | `prazo` no momento do primeiro anúncio |

**Antecedência (dias)** = `prazoOriginal` − `primeiraDivulgacao`

### 4.3 Preenchimento retroativo

Todas as edições (ed-01 a ed-04) e as avulsas estão no repositório. Um script reprocessa a história em ordem cronológica e preenche os três campos para os 37 editais atuais, recuperando inclusive os prazos originais dos editais prorrogados.

### 4.4 Regra para prazos fora do padrão (**decidida em 14/10/2026**)

| Caso | Exemplo atual | Regra |
|---|---|---|
| Mais de um prazo | Prêmio Fapes 17/2026: "24/07/2026 (Jornalismo: 15/09/2026)" | Usar o **primeiro** prazo |
| Evento com inscrição | WorCAP, PAEP, Curso INPI (07/08 = fim das inscrições, confirmado) | Entra em **"até o fim das inscrições"**, como qualquer edital |
| Evento sem inscrição | (novo) `semInscricao: true` | Entra em **"até o evento"**, a partir do início de `dataEvento` |
| Intervalo de datas (itens antigos) | 78ª Reunião Anual da SBPC: "26/07 a 01/08/2026" | Tratado como data do evento → **"até o evento"** (16 dias) |
| Fluxo contínuo / prazo não definido | EPLI ("datas a definir pelo campus") | **Contagem à parte** no dashboard ("sem prazo de encerramento") |

Para isso, os cards de Eventos ganharam dois campos: `dataEvento` e `semInscricao` (ver `CLAUDE.md`, seção "Cards de Eventos"). Decisão da Juliana: o prazo nunca fica vazio sem explicação — ou tem o fim das inscrições, ou a caixa "Não é necessária inscrição" marcada.

### 4.5 Indicadores no dashboard

- Antecedência média de divulgação (dias)
- Editais divulgados com menos de 7 dias de antecedência (alerta)
- Lista exportável para relatório

---

## 5. Arquivos que serão alterados

| Arquivo | Mudança |
|---|---|
| `ir.html` (novo) | Página de passagem: busca o edital no `banco.json`, registra o clique e redireciona |
| `index.html` | Links dos cards passam por `ir.html?…&de=site` |
| `radar_sistema_dppge.html` | Boletim e WhatsApp com links rastreáveis (`de=boletim` / `de=whatsapp` + `ed`); novas seções no dashboard (cliques e antecedência) |
| `scripts/merge_edicao.py` | Grava `primeiraDivulgacao`, `primeiraEdicao` e `prazoOriginal` |
| `scripts/` (novo) | Script de preenchimento retroativo |
| `apps-script/Codigo.gs` (novo) | Código para colar no Apps Script da planilha |
| `CLAUDE.md` e `README.md` | Novo fluxo, novos campos e instruções |

---

## 6. Novo fluxo de publicação (afeta Juliana e Luisa)

```
1. Montar/revisar a edição no sistema (como hoje)
2. python3 scripts/merge_edicao.py edicoes/ed-XX
3. Commit + push
4. Aguardar ~1 minuto (GitHub Pages publicar)
5. SÓ ENTÃO: "Gerar para Outlook" e "Gerar para WhatsApp" → enviar
```

Antes, o boletim era enviado e o site era atualizado depois. Agora **o site é atualizado primeiro e o anúncio vem depois**. A Luisa precisa ser avisada dessa mudança.

---

## 7. Pré-requisitos e pendências

- [ ] **Confirmar a regra dos prazos fora do padrão** (seção 4.4).
- [ ] **Python neste computador:** não está instalado, e o merge e o script retroativo precisam dele. Duas saídas: instalar o Python aqui (python.org ou Microsoft Store) ou rodar na máquina da Luisa.
- [ ] **Publicação do Apps Script como "Qualquer pessoa":** a publicação do App da Web precisa permitir acesso de "Qualquer pessoa". Contas institucionais às vezes têm essa opção bloqueada pelo administrador. Testar logo no início. Se estiver bloqueada, avaliar uma alternativa antes de escrever o resto.
- [ ] **Avisar a Luisa** sobre o novo fluxo (seção 6).

Observação: no computador da DPPGE (usuário `3672522`), o `git` não está no PATH. Lá é preciso usar o Git do GitHub Desktop:
`C:\Users\3672522\AppData\Local\GitHubDesktop\app-3.6.6\resources\app\git\cmd\git.exe`
Em outro computador, conferir se o `git` e o Python estão disponíveis antes de começar.

**Antes de começar em qualquer computador:** atualizar a pasta com o GitHub (fetch/pull), porque a Luisa também publica no Radar.

---

## 8. Ordem de execução para amanhã

1. **Juliana:** criar a planilha na conta institucional e testar se a publicação como "Qualquer pessoa" é permitida. É o ponto que pode mudar o plano, então vem primeiro.
2. **Juliana:** decidir sobre o Python (instalar aqui ou usar a máquina da Luisa).
3. **Claude:** escrever o `apps-script/Codigo.gs` e o passo a passo de configuração.
4. **Claude:** criar o `ir.html` e a função de código do edital.
5. **Claude:** alterar os links no `index.html` (site).
6. **Claude:** alterar os links do boletim e do WhatsApp no `radar_sistema_dppge.html`.
7. **Claude:** alterar o `merge_edicao.py` e criar o script retroativo; rodar o retroativo.
8. **Claude:** criar as seções novas do dashboard (cliques e antecedência).
9. **Juntas:** testar de ponta a ponta. Clicar num edital pelo site, por um boletim de teste e por uma mensagem de teste, e conferir as linhas na planilha.
10. **Claude:** atualizar o `CLAUDE.md` e o `README.md`.
11. **Juliana:** commit, push e avisar a Luisa.
