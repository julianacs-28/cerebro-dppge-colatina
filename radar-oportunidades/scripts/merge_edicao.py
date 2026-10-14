#!/usr/bin/env python3
"""
Funde o dados.json de uma edição do boletim no banco.json acumulado do site.

Uso:
    python3 scripts/merge_edicao.py edicoes/ed-01

O banco.json é a fonte única lida pelo index.html (site público) e contém
TODAS as oportunidades já divulgadas em qualquer edição, deduplicadas por
título. Itens já existentes têm prazo/link/valor/publico/status atualizados,
mas preservam a dataCadastro original (usada para a badge "Novo" do site).

Na primeira vez que uma oportunidade aparece, também grava primeiraDivulgacao
(data de envio da edição), primeiraEdicao (número ou "avulsa") e prazoOriginal
(prazo naquele momento). Esses três campos nunca mais são alterados — servem
para medir a antecedência com que cada oportunidade foi divulgada.

Se o "destaque" da edição for um texto institucional (boas-vindas, aviso,
etc.) em vez de uma oportunidade real, marque "institucional": true nele —
assim ele não é mesclado no banco.json como se fosse um edital.
"""
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO_PATH = RAIZ / "banco.json"
INDICE_PATH = RAIZ / "edicoes" / "indice.json"


def chave(titulo):
    return re.sub(r"\s+", " ", (titulo or "").strip().lower())


# ── Semelhança de títulos ─────────────────────────────────────────────
# Mesma regra do editor (radar_sistema_dppge.html → titulosParecidos). Se mudar aqui, mude lá.
# Dois títulos são "parecidos" quando têm o mesmo número de edital (NN/AAAA) do mesmo órgão, ou
# quando compartilham a maior parte das palavras de conteúdo (ignorando órgãos, anos e termos genéricos).
PALAVRAS_GENERICAS = {
    "edital", "chamada", "chamadas", "publica", "programa", "apoio", "para", "com", "dos", "das", "nos",
    "nas", "por", "sobre", "entre", "edicao", "ciencia", "tecnologia", "inovacao", "pesquisa",
    "desenvolvimento", "premio", "nacional", "brasil",
}
ORGAOS = {
    "fapes", "cnpq", "capes", "mcti", "fndct", "confap", "inpe", "inpi", "finep", "sbpc", "ifes", "proex",
    "setec", "setad", "mec", "fapesp", "fapemig", "ompi", "minc", "mir", "mmulheres", "mpi", "anr", "cgaex",
    "paex", "erc",
}


def _analisar_titulo(titulo):
    s = unicodedata.normalize("NFD", (titulo or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    numeros = set(re.findall(r"\d{1,3}/\d{4}", s))
    s = re.sub(r"\d{1,3}/\d{4}", " ", s)
    palavras = set(re.findall(r"[a-z0-9]+", s))
    orgaos = palavras & ORGAOS
    conteudo = {
        w for w in palavras
        if len(w) >= 3 and w not in PALAVRAS_GENERICAS and w not in ORGAOS and not w.isdigit()
    }
    return conteudo, numeros, orgaos


def titulos_parecidos(a, b):
    ca, na, oa = _analisar_titulo(a)
    cb, nb, ob = _analisar_titulo(b)
    if (na & nb) and (oa & ob):
        return True
    comuns = ca & cb
    return bool(ca and cb and len(comuns) >= min(2, len(ca), len(cb))
                and len(comuns) / min(len(ca), len(cb)) >= 0.6)


# ── Índice das edições (lido pelo Histórico do sistema e pelo dashboard do site) ──
def gerar_indice():
    """Lista todas as edições e avulsas publicadas em edicoes/indice.json (mais recente primeiro)."""
    edicoes, avulsas = [], []
    for arq in sorted((RAIZ / "edicoes").rglob("dados.json")):
        with open(arq, encoding="utf-8") as f:
            d = json.load(f)
        itens = coletar_oportunidades(d)
        registro = {
            "pasta": arq.parent.relative_to(RAIZ).as_posix(),
            "data": data_da_edicao(d),
            "oportunidades": len(itens),
        }
        if d.get("numero"):
            registro.update({"numero": d["numero"], "mes": d.get("mes", "")})
            edicoes.append(registro)
        else:
            registro["titulos"] = [i.get("titulo", "") for i in itens]
            avulsas.append(registro)

    def ordem(r):
        try:
            return datetime.strptime(r["data"], "%d/%m/%Y")
        except ValueError:
            return datetime.min

    edicoes.sort(key=ordem, reverse=True)
    avulsas.sort(key=ordem, reverse=True)
    with open(INDICE_PATH, "w", encoding="utf-8") as f:
        json.dump({"edicoes": edicoes, "avulsas": avulsas}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return len(edicoes), len(avulsas)


def data_da_edicao(edicao_json):
    """Data de envio da edição ('dataEnvio') ou, nas avulsas, o campo livre 'data'."""
    return (edicao_json.get("dataEnvio") or edicao_json.get("data") or "").strip()


def numero_da_edicao(edicao_json):
    """Número da edição ('01', '04'...) ou 'avulsa' quando não há numero."""
    return (edicao_json.get("numero") or "").strip() or "avulsa"


def dados_primeira_divulgacao(edicao_json, item, hoje):
    """Campos gravados só na primeira vez que a oportunidade aparece e nunca mais alterados."""
    return {
        "primeiraDivulgacao": data_da_edicao(edicao_json) or hoje,
        "primeiraEdicao": numero_da_edicao(edicao_json),
        "prazoOriginal": item.get("prazo", ""),
    }


def carregar_banco():
    if BANCO_PATH.exists():
        with open(BANCO_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"atualizadoEm": "", "oportunidades": []}


def coletar_oportunidades(edicao_json):
    itens = []
    destaque = edicao_json.get("destaque")
    if destaque and destaque.get("titulo") and not destaque.get("institucional"):
        item = dict(destaque)
        item["_cat"] = destaque.get("categoria", "pesquisa")
        item.pop("categoria", None)
        item.pop("ctaTexto", None)
        item.pop("institucional", None)
        itens.append(item)
    for cat, lista in (edicao_json.get("categorias") or {}).items():
        for card in lista or []:
            item = dict(card)
            item["_cat"] = cat
            itens.append(item)
    return itens


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/merge_edicao.py edicoes/ed-XX")
        sys.exit(1)

    pasta_edicao = Path(sys.argv[1])
    dados_path = pasta_edicao / "dados.json"
    if not dados_path.exists():
        # Também aceita o caminho apontando direto para o arquivo .json
        if pasta_edicao.suffix == ".json" and pasta_edicao.exists():
            dados_path = pasta_edicao
        else:
            print(f"Não encontrei {dados_path}")
            sys.exit(1)

    with open(dados_path, encoding="utf-8") as f:
        edicao = json.load(f)

    banco = carregar_banco()
    mapa = {chave(o.get("titulo")): o for o in banco["oportunidades"]}
    hoje = datetime.now().strftime("%d/%m/%Y")

    adicionados, atualizados = 0, 0
    avisos = []
    for item in coletar_oportunidades(edicao):
        ch = chave(item.get("titulo"))
        if not ch:
            continue
        if ch in mapa:
            existente = mapa[ch]
            # "titulo" entra porque a chave ignora maiúsculas: um título corrigido ("EDITAL FAPES…" →
            # "Edital Fapes…") precisa substituir o antigo, senão o resumo novo deixa de contê-lo.
            for campo in ("titulo", "prazo", "link", "valor", "publico", "status", "resumo", "origem", "imagem", "local", "dataEvento", "_cat"):
                if item.get(campo):
                    existente[campo] = item[campo]
            # Booleano: precisa propagar também o False (ex.: evento que passou a exigir inscrição)
            if "semInscricao" in item:
                existente["semInscricao"] = bool(item["semInscricao"])
                if item["semInscricao"]:
                    existente["prazo"] = ""
            atualizados += 1
        else:
            # Rede de segurança: a verificação principal acontece no editor ("Revisar edição")
            semelhantes = [o for o in banco["oportunidades"] if titulos_parecidos(item.get("titulo"), o.get("titulo"))]
            for o in semelhantes:
                avisos.append(f"  NOVO:      {item.get('titulo')}\n"
                              f"  PARECIDO:  {o.get('titulo')}  (divulgado em {o.get('primeiraDivulgacao') or o.get('dataCadastro', '?')})")
            item["dataCadastro"] = hoje
            item.update(dados_primeira_divulgacao(edicao, item, hoje))
            banco["oportunidades"].append(item)
            mapa[ch] = item
            adicionados += 1

    banco["atualizadoEm"] = hoje
    with open(BANCO_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write("\n")

    n_edicoes, n_avulsas = gerar_indice()

    print(f"Edição: {dados_path}")
    print(f"Adicionados: {adicionados} | Atualizados: {atualizados}")
    print(f"Total no banco: {len(banco['oportunidades'])}")
    print(f"banco.json atualizado em {BANCO_PATH}")
    print(f"Índice: {n_edicoes} edição(ões) e {n_avulsas} avulsa(s) em {INDICE_PATH}")
    if avisos:
        print("\n⚠ ATENÇÃO — títulos novos parecidos com oportunidades já divulgadas:")
        print("\n\n".join(avisos))
        print("\nSe for o MESMO edital, corrija o título na edição para ficar idêntico ao já divulgado")
        print("e rode o merge de novo. Se for outra chamada/programa, está tudo certo.")


if __name__ == "__main__":
    main()
