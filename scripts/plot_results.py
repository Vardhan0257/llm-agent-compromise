"""Plot detection-rate comparisons and save figures used by the notebook.
"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path('results').mkdir(parents=True, exist_ok=True)

def detection_rate_from_df(df):
    total = df.groupby(['mode', 'family']).size().rename('total')
    blocked = df[df['status']=='blocked'].groupby(['mode','family']).size().rename('blocked')
    merged = pd.concat([total, blocked], axis=1).fillna(0)
    merged['detection_rate'] = merged['blocked'] / merged['total']
    return merged.reset_index()

# load files
bypass_path = Path('results/bypass_metrics.csv')
controlled_path = Path('results/controlled_metrics.csv')

if controlled_path.exists():
    df_ctrl = pd.read_csv(controlled_path)
    summary_ctrl = detection_rate_from_df(df_ctrl)
    pivot = summary_ctrl.pivot(index='family', columns='mode', values='detection_rate')
    ax = pivot.plot(kind='bar', rot=0, figsize=(8,5))
    ax.set_ylim(0,1)
    ax.set_ylabel('Detection rate')
    plt.title('Detection Rate by Payload Family (controlled)')
    plt.tight_layout()
    plt.savefig('results/fig_detection_rates_controlled.png')
    print('Wrote results/fig_detection_rates_controlled.png')
else:
    print('Missing', controlled_path)

if bypass_path.exists():
    df_b = pd.read_csv(bypass_path)
    summary_b = detection_rate_from_df(df_b)
    pivot = summary_b.pivot(index='family', columns='mode', values='detection_rate')
    ax = pivot.plot(kind='bar', rot=0, figsize=(8,5))
    ax.set_ylim(0,1)
    ax.set_ylabel('Detection rate')
    plt.title('Detection Rate by Payload Family (bypass set)')
    plt.tight_layout()
    plt.savefig('results/fig_detection_rates_bypass.png')
    print('Wrote results/fig_detection_rates_bypass.png')
else:
    print('Missing', bypass_path)
