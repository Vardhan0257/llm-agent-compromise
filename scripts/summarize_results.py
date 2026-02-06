import csv
from collections import Counter, defaultdict

path = 'results/controlled_metrics.csv'
rows = []
with open(path, encoding='utf-8') as fh:
    reader = csv.DictReader(fh)
    for r in reader:
        rows.append(r)

counts_mode = defaultdict(Counter)
for r in rows:
    counts_mode[r['mode']][r['status']] += 1

print('Summary of controlled experiment results:')
for mode, counter in counts_mode.items():
    total = sum(counter.values())
    blocked = counter.get('blocked', 0)
    compromised = counter.get('compromised', 0)
    safe = counter.get('safe', 0)
    print(f"\nMode: {mode} — total={total}, blocked={blocked}, compromised={compromised}, safe={safe}")
    print(f"  Detection rate (blocked/total): {blocked/total*100:.1f}%")
    print(f"  Compromise rate (compromised/total): {compromised/total*100:.1f}%")

# breakdown by family
from collections import defaultdict
by_family = defaultdict(lambda: defaultdict(Counter))
for r in rows:
    by_family[r['mode']][r['family']][r['status']] += 1

print('\nPer-family breakdown:')
for mode, families in by_family.items():
    print(f"\nMode: {mode}")
    for fam, ctr in families.items():
        total = sum(ctr.values())
        blocked = ctr.get('blocked', 0)
        compromised = ctr.get('compromised', 0)
        print(f"  {fam}: total={total}, blocked={blocked}, compromised={compromised}, detection={blocked/total*100:.1f}%")
