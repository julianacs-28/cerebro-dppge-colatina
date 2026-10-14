/**
 * Radar de Oportunidades — registro de cliques nos editais
 *
 * Script vinculado à planilha "RADAR-cliques-nos-editais" (conta institucional).
 * Publicado como App da Web: executar como "Eu", acesso "Qualquer pessoa".
 *
 * Não guarda nenhum dado pessoal: só data/hora, edital, edição, categoria e canal.
 *
 * Rotas (todas GET):
 *   .../exec                                    → "ok" (teste de vida)
 *   .../exec?e=COD&t=...&de=...&ed=...&cat=...  → registra um clique (chamado por ir.html)
 *   .../exec?acao=dados                         → devolve os cliques em JSON (lido pelo dashboard do site)
 *
 * ATENÇÃO: não usar o parâmetro "c" — é reservado pelo Google e faz o pedido ser recusado
 * (HTTP 400, "Não foi possível abrir o arquivo"). Por isso a categoria vai em "cat".
 */

var ABA = 'Cliques';
var CABECALHO = ['Data/hora', 'Código', 'Edital', 'Edição', 'Categoria', 'Canal'];
var CANAIS = ['site', 'boletim', 'whatsapp'];
var FUSO = 'America/Sao_Paulo';

function doGet(e) {
  var p = (e && e.parameter) || {};
  try {
    if (p.acao === 'dados') return json_(lerDados_());
    if (p.e) return registrar_(p);
    return texto_('ok');
  } catch (err) {
    return texto_('erro');
  }
}

function registrar_(p) {
  var canal = String(p.de || '').toLowerCase();
  if (CANAIS.indexOf(canal) === -1) canal = 'site';

  var linha = [
    new Date(),
    limpar_(p.e, 20),
    limpar_(p.t, 300),
    limpar_(p.ed, 10),
    limpar_(p.cat, 30),
    canal
  ];

  var lock = LockService.getScriptLock();
  if (!lock.tryLock(8000)) return texto_('ocupado');
  try {
    var aba = abaCliques_();
    aba.appendRow(linha);
  } finally {
    lock.releaseLock();
  }
  return texto_('ok');
}

function abaCliques_() {
  var planilha = SpreadsheetApp.getActiveSpreadsheet();
  var aba = planilha.getSheetByName(ABA);
  if (!aba) {
    aba = planilha.insertSheet(ABA);
    aba.appendRow(CABECALHO);
    aba.setFrozenRows(1);
    aba.getRange(1, 1, 1, CABECALHO.length).setFontWeight('bold');
    aba.getRange('A:A').setNumberFormat('dd/MM/yyyy HH:mm');
  }
  return aba;
}

function lerDados_() {
  var aba = abaCliques_();
  var ultima = aba.getLastRow();
  if (ultima < 2) return { cliques: [] };
  var valores = aba.getRange(2, 1, ultima - 1, CABECALHO.length).getValues();
  var cliques = valores.map(function (r) {
    return {
      quando: r[0] instanceof Date ? Utilities.formatDate(r[0], FUSO, "yyyy-MM-dd'T'HH:mm:ss") : String(r[0]),
      codigo: String(r[1]),
      edital: String(r[2]),
      edicao: String(r[3]),
      categoria: String(r[4]),
      canal: String(r[5])
    };
  });
  return { cliques: cliques };
}

// Remove espaços extras, limita o tamanho e grava SEMPRE como texto: o apóstrofo inicial
// (invisível na planilha) impede que "04" vire 4, que um código como "1e5" vire 100000
// e que um texto começando com =, +, - ou @ seja interpretado como fórmula.
function limpar_(valor, max) {
  var s = String(valor == null ? '' : valor).replace(/\s+/g, ' ').trim().substring(0, max);
  return s ? "'" + s : '';
}

function texto_(s) {
  return ContentService.createTextOutput(s);
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
