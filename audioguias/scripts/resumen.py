"""Resume la verificación de un tour y marca lo que hay que mirar. Uso: resumen.py BASE tour..."""
import json, sys
for t in sys.argv[2:]:
    r = json.load(open(f"{sys.argv[1]}/verificacion/{t}.json"))
    print(f"== {t}: {r['title']} ({len(r['stops'])} paradas, {sum(s['es_min'] for s in r['stops']):.0f} min)")
    for s in r["stops"]:
        flags = []
        if s["audio_match"] < 0.95: flags.append(f"match {s['audio_match']}")
        if not 0.85 <= s["word_ratio"] <= 1.4: flags.append(f"palabras {s['word_ratio']}")
        if s["missing_numbers"]: flags.append(f"números {s['missing_numbers']}")
        if flags:
            print(f"  {s['n']:02d} {s['name'][:40]}: {'; '.join(flags)}")
            if s["audio_match"] < 0.95:
                for d in s.get("diffs", [])[:12]: print("      ", d)
