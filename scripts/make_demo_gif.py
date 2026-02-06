"""Create a simple GIF demonstrating a bypass under baseline and block under validator.

The script picks a payload that bypassed the baseline but was blocked by the validator
from `results/bypass_metrics.csv` and renders two frames with matplotlib, then
assembles them into `results/demo.gif`.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import imageio

Path('results').mkdir(parents=True, exist_ok=True)

bypass = Path('results/bypass_metrics.csv')
if not bypass.exists():
    print('Missing', bypass)
    raise SystemExit(1)

df = pd.read_csv(bypass)
# find a payload text that was safe under baseline and blocked under validator
baseline_safe = df[(df['mode']=='baseline') & (df['status']!='blocked')]['payload']
validator_blocked = df[(df['mode']=='validator') & (df['status']=='blocked')]['payload']

candidates = [p for p in baseline_safe.unique() if p in validator_blocked.unique()]
if not candidates:
    # fallback: pick any obfuscated example
    candidates = ['E X F I L T R A T E _ D A T A']

payload = candidates[0]
print('Selected payload for demo:', payload)

frames = []
fig, ax = plt.subplots(figsize=(10,4))
ax.axis('off')
# frame 1: baseline (bypassed)
ax.text(0.5, 0.7, 'Baseline: Bypassed', ha='center', va='center', fontsize=20, color='red')
ax.text(0.5, 0.35, payload, ha='center', va='center', fontsize=14)
plt.tight_layout()
frame1_path = 'results/frame1.png'
plt.savefig(frame1_path)
frames.append(imageio.imread(frame1_path))
plt.clf()

# frame 2: validator (blocked)
fig, ax = plt.subplots(figsize=(10,4))
ax.axis('off')
ax.text(0.5, 0.7, 'Validator: Blocked', ha='center', va='center', fontsize=20, color='green')
ax.text(0.5, 0.35, payload, ha='center', va='center', fontsize=14)
plt.tight_layout()
frame2_path = 'results/frame2.png'
plt.savefig(frame2_path)
frames.append(imageio.imread(frame2_path))
plt.close('all')

out_gif = 'results/demo.gif'
imageio.mimsave(out_gif, frames, duration=1.5)
print('Wrote', out_gif)
