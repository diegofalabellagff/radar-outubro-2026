"""Gera index.html do radar do Dia 30.
Uso: python3 gen.py dados.json
dados.json = lista de linhas da consulta.sql (codigo_loja, venda, deliv, pct, ate_set, ate23, corte, atualizado)."""
import json, sys, os
base = os.path.dirname(os.path.abspath(__file__))
rows = {str(r["codigo_loja"]): r for r in json.load(open(sys.argv[1]))}
metas = json.load(open(os.path.join(base, "metas.json")))
def f(x):
    if x in (None, ""):
        return None
    return float(x)
lojas, faltando = [], []
for m in metas:
    r = rows.get(m["codigo_loja"])
    if r is None:
        faltando.append(m["nome"]); r = {}
    pct = f(r.get("pct"))
    if pct is not None and pct <= 0:
        pct = None
    lojas.append(dict(sup=m["sup"], nome=m["nome"], meta=m["meta"], venda=f(r.get("venda")) or 0.0,
        pct=pct, ate_set=f(r.get("ate_set")), ate23=f(r.get("ate23")), deliv=f(r.get("deliv")) or 0.0))
any_row = next(iter(rows.values()))
semdeliv = sum(1 for l in lojas if l["meta"] and not l["deliv"])
t = open(os.path.join(base, "template.html")).read()
t = (t.replace("__DATA__", json.dumps(lojas, ensure_ascii=False))
      .replace("__CORTE__", any_row.get("corte") or "?")
      .replace("__ATUALIZADO__", any_row.get("atualizado") or "?")
      .replace("__SEMDELIV__", str(semdeliv)))
open(os.path.join(base, "index.html"), "w").write(t)
tot = sum(l["venda"] for l in lojas if l["meta"]); meta = sum(l["meta"] for l in lojas if l["meta"])
proj = sum(l["venda"]/l["pct"] for l in lojas if l["meta"] and l["pct"])
ok = sum(1 for l in lojas if l["meta"] and l["pct"] and l["venda"]/l["pct"] >= l["meta"])
print(f"ok: vendido {tot:,.0f} de {meta:,.0f} ({tot/meta:.1%}), projeção {proj:,.0f} ({proj/meta:.0%}), {ok} lojas no ritmo, delivery zerado em {semdeliv} lojas")
if faltando:
    print("ATENÇÃO, lojas sem dado no Atlas:", ", ".join(faltando))
