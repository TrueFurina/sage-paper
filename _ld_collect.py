"""Collect the parallel leak_durable scan outputs into one table."""
import glob
import json

rows = []
for path in sorted(glob.glob("data/leak_durable_sensitivity_*.json")):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    for r in d["results"]:
        rows.append(r)
rows.sort(key=lambda r: r["leak_durable"])

lines = []
lines.append(f"{'ld':>6} | {'theta':>7} | {'lam*':>5} | {'gain*':>7} | "
             f"{'left':>8} | {'right':>8} | {'ctrl_left':>9} | {'share':>6} | "
             f"verdict")
lines.append("-" * 92)
for r in rows:
    lines.append(f"{r['leak_durable']:>6.3f} | {r['theta']:>7.4f} | "
                 f"{r['lambda_star']:>5.2f} | {r['gain_star']:>7.4f} | "
                 f"{r['left_effect']:>+8.4f} | {r['right_effect']:>+8.4f} | "
                 f"{r['control_left_effect']:>+9.4f} | "
                 f"{r['attributable_share']:>5.0%} | {r['verdict']}")

lines.append("")
lines.append(f"n values = {len(rows)}")
base = rows[0]
lines.append(f"BASELINE ld={base['leak_durable']}: share={base['attributable_share']:.0%} "
             f"lam*={base['lambda_star']} gain*={base['gain_star']} "
             f"left={base['left_effect']:+.4f} ctrl={base['control_left_effect']:+.4f}")
below = [r for r in rows if r["attributable_share"] < 0.5]
if below:
    lines.append(f"first below 50%: ld={below[0]['leak_durable']} "
                 f"share={below[0]['attributable_share']:.0%}")
else:
    lines.append("no value drops below 50% in this scan")
shares = [r["attributable_share"] for r in rows]
lines.append(f"share range over scan: {min(shares):.0%} .. {max(shares):.0%}")

with open("logs/_ld_summary.out", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
