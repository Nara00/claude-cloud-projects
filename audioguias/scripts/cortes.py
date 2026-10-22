"""Busca tramos de 8+ palabras seguidas que faltan en lo que se escuchó (posible corte de la voz). Uso: cortes.py BASE tour..."""
import json, sys
for t in sys.argv[2:]:
    r = json.load(open(f"{sys.argv[1]}/verificacion/{t}.json"))
    found = []
    for s in r["stops"]:
        for d in s.get("diffs", []):
            left, right = d.split(" -> ", 1) if " -> " in d else (d, "")
            nl, nr = len(left.split()), len(right.split())
            if nl >= 8 and nr < nl * 0.5 and not left.startswith("parada "):
                found.append(f"  {s['n']:02d} faltan {nl - nr} palabras: {left[:100]}")
    print(t, "sin cortes" if not found else "POSIBLES CORTES:\n" + "\n".join(found))
