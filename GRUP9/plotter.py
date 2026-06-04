"""
plotter.py
----------
Yakınsama grafikleri üretir.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def plot_convergence(history, instance_name, bks=None, output_dir='plots'):
    """Tek instance için yakınsama grafiği."""
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(history, color='#00A896', linewidth=1.8, label='Tabu Search')

    if bks is not None:
        ax.axhline(y=bks, color='#E74C3C', linewidth=1.2,
                   linestyle='--', label=f'BKS = {bks}')

    ax.set_title(f'Yakınsama Grafiği – {instance_name}', fontsize=13, fontweight='bold')
    ax.set_xlabel('İterasyon', fontsize=11)
    ax.set_ylabel('Makespan (Cmax)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#F8FAFB')
    fig.patch.set_facecolor('white')
    plt.tight_layout()

    filepath = os.path.join(output_dir, f'convergence_{instance_name}.png')
    plt.savefig(filepath, dpi=150)
    plt.close()
    print(f"  Grafik kaydedildi: {filepath}")


def plot_all_convergence(histories_dict, bks_dict=None, output_dir='plots'):
    """Tüm instance'ları tek grafikte gösterir."""
    os.makedirs(output_dir, exist_ok=True)
    if bks_dict is None:
        bks_dict = {}

    colors = ['#00A896', '#0D9488', '#F59E0B', '#EF4444', '#8B5CF6']
    n = len(histories_dict)
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4))
    if n == 1:
        axes = [axes]

    for ax, (name, history), color in zip(axes, histories_dict.items(), colors):
        # Normalize: BKS'ye göre gap% olarak göster
        bks = bks_dict.get(name)
        if bks:
            y = [(v - bks) / bks * 100 for v in history]
            ax.set_ylabel('Optimality Gap (%)', fontsize=9)
        else:
            y = history
            ax.set_ylabel('Cmax', fontsize=9)

        ax.plot(y, color=color, linewidth=1.5)
        if bks:
            ax.axhline(y=0, color='red', linewidth=0.8, linestyle='--', alpha=0.6)
        ax.set_title(name, fontsize=10, fontweight='bold')
        ax.set_xlabel('İterasyon', fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor('#F8FAFB')

    fig.suptitle('Tabu Search – Tüm Instance Yakınsama Grafikleri',
                 fontsize=12, fontweight='bold', y=1.02)
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'convergence_all.png')
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Genel grafik kaydedildi: {filepath}")
