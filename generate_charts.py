import matplotlib.pyplot as plt
import numpy as np

# Set style for academic paper
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['font.size'] = 9

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.6), dpi=300)

# Chart 1: MTTD & MTTR Comparison
metrics = ['Detection (MTTD)', 'Remediation (MTTR)']
traditional = [65.0, 600.0]  # in seconds (65s, 10 mins = 600s)
proposed = [20.0, 0.32]     # 20s pre-failure lead, 320ms = 0.32s

x = np.arange(len(metrics))
width = 0.32

rects1 = ax1.bar(x - width/2, traditional, width, label='Traditional SNMP NMS', color='#475569')
rects2 = ax1.bar(x + width/2, proposed, width, label='Proposed AI Digital Twin', color='#2563eb')

ax1.set_ylabel('Time (Seconds, Log Scale)')
ax1.set_yscale('log')
ax1.set_title('(a) Latency Benchmark (MTTD & MTTR)', fontsize=9.5, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(metrics)
ax1.legend(fontsize=8, loc='upper right')
ax1.grid(axis='y', linestyle='--', alpha=0.5)

# Chart 2: Rare Fault Classification F1-Score
fault_classes = ['Nominal', 'Congestion', 'Degradation', 'Loop/Storm']
ce_f1 = [0.99, 0.72, 0.61, 0.35]
focal_f1 = [0.99, 0.94, 0.92, 0.91]

x2 = np.arange(len(fault_classes))
rects3 = ax2.bar(x2 - width/2, ce_f1, width, label='Cross-Entropy (Baseline)', color='#94a3b8')
rects4 = ax2.bar(x2 + width/2, focal_f1, width, label='Focal Loss (gamma=2.0)', color='#10b981')

ax2.set_ylabel('F1-Score')
ax2.set_ylim(0, 1.15)
ax2.set_title('(b) Multi-Class F1-Score under 98:2 Imbalance', fontsize=9.5, fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(fault_classes, rotation=15)
ax2.legend(fontsize=8, loc='lower right')
ax2.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('fig_ieee_results.png', bbox_inches='tight')
print("IEEE benchmark figure generated: fig_ieee_results.png")
