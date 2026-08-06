#!/usr/bin/env python3
"""
Funde o dados.json de uma edição do boletim no banco.json acumulado do site.

Uso:
    python3 scripts/merge_edicao.py edicoes/ed-01

O banco.json é a fonte única lida pelo index.html (site público) e contém
TODAS as oportunidades já divulgadas em qualquer edição, deduplicadas por
título. Itens já existentes têm prazo/link/valor/publico/status atualizados,
mas preservam a dataCadastro original (usada para a badge "Novo" do site).

Se o "destaque" da edição for um texto institucional (boas-vindas, aviso,
etc.) em vez de uma oportunidade real, marque "institucional": true nele —
assim ele não é mesclado no banco.json como se fosse um edital.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BANCO_PATH = RAIZ / "banco.json"


def chave(titulo):
    return re.sub(r"\s+", " ", (titulo or "").strip().lower())


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
    for item in coletar_oportunidades(edicao):
        ch = chave(item.get("titulo"))
        if not ch:
            continue
        if ch in mapa:
            existente = mapa[ch]
            for campo in ("prazo", "link", "valor", "publico", "status", "resumo", "origem", "imagem", "local", "_cat"):
                if item.get(campo):
                    existente[campo] = item[campo]
            atualizados += 1
        else:
            item["dataCadastro"] = hoje
            banco["oportunidades"].append(item)
            mapa[ch] = item
            adicionados += 1

    banco["atualizadoEm"] = hoje
    with open(BANCO_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Edição: {dados_path}")
    print(f"Adicionados: {adicionados} | Atualizados: {atualizados}")
    print(f"Total no banco: {len(banco['oportunidades'])}")
    print(f"banco.json atualizado em {BANCO_PATH}")


if __name__ == "__main__":
    main()
