#!/usr/bin/env python3
"""
Preenche, de forma retroativa, primeiraDivulgacao / primeiraEdicao / prazoOriginal
no banco.json, reprocessando todas as edições e inclusões avulsas em ordem
cronológica. Só preenche o que está faltando — nunca sobrescreve um valor já gravado.

Uso (a partir da pasta radar-oportunidades):
    python scripts/preencher_historico.py            # grava no banco.json
    python scripts/preencher_historico.py --simular  # só mostra o que faria

Roda uma única vez para recuperar o histórico; daí em diante o merge_edicao.py
grava esses campos sozinho a cada oportunidade nova.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

from merge_edicao import (
    BANCO_PATH,
    RAIZ,
    chave,
    coletar_oportunidades,
    data_da_edicao,
    numero_da_edicao,
)

CAMPOS = ("primeiraDivulgacao", "primeiraEdicao", "prazoOriginal")


def parse_data(texto):
    try:
        return datetime.strptime(texto, "%d/%m/%Y")
    except (ValueError, TypeError):
        return datetime.max


def listar_edicoes():
    """Todas as edições e avulsas, da mais antiga para a mais recente."""
    arquivos = sorted((RAIZ / "edicoes").rglob("dados.json"))
    edicoes = []
    for arq in arquivos:
        with open(arq, encoding="utf-8") as f:
            edicoes.append((arq, json.load(f)))
    edicoes.sort(key=lambda par: (parse_data(data_da_edicao(par[1])), str(par[0])))
    return edicoes


def main():
    simular = "--simular" in sys.argv

    with open(BANCO_PATH, encoding="utf-8") as f:
        banco = json.load(f)
    mapa = {chave(o.get("titulo")): o for o in banco["oportunidades"]}

    vistos = set()
    preenchidos = 0
    for arq, edicao in listar_edicoes():
        data = data_da_edicao(edicao)
        numero = numero_da_edicao(edicao)
        if not data:
            print(f"AVISO: {arq.parent.name} sem data de envio — ignorada")
            continue
        for item in coletar_oportunidades(edicao):
            ch = chave(item.get("titulo"))
            if not ch or ch in vistos:
                continue
            vistos.add(ch)
            op = mapa.get(ch)
            if op is None:
                continue
            novos = {
                "primeiraDivulgacao": data,
                "primeiraEdicao": numero,
                "prazoOriginal": item.get("prazo", ""),
            }
            faltando = {k: v for k, v in novos.items() if k not in op}
            if faltando:
                op.update(faltando)
                preenchidos += 1
                print(f"{numero:>6} | {data} | prazo {item.get('prazo', '—') or '—'} | {op['titulo'][:60]}")

    sem_origem = [o["titulo"] for o in banco["oportunidades"] if "primeiraDivulgacao" not in o]
    print(f"\nOportunidades preenchidas: {preenchidos} de {len(banco['oportunidades'])}")
    if sem_origem:
        print("Sem edição de origem encontrada (campos não preenchidos):")
        for t in sem_origem:
            print(f"  - {t}")

    if simular:
        print("\n[--simular] Nada foi gravado.")
        return
    with open(BANCO_PATH, "w", encoding="utf-8") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"banco.json atualizado em {BANCO_PATH}")


if __name__ == "__main__":
    main()
