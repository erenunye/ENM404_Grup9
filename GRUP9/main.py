"""
main.py
-------
ENM404 – Grup 9: Flow-Shop Scheduling + Tabu Search
Ana deney dosyası.

Kullanım:
    python main.py

Çıktılar:
    results/all_results.csv    → ham çalıştırma sonuçları
    plots/convergence_*.png    → yakınsama grafikleri
"""

import time
import os
import sys

from instance_loader import generate_instance, load_taillard, save_instance
from tabu_search import tabu_search
from results_logger import ResultsLogger
from plotter import plot_convergence, plot_all_convergence

# ─── Bilinen En İyi Çözümler (BKS) ─────────────────────────────────────────
# Kaynak: Taillard (1993), http://mistic.heig-vd.ch/taillard
BKS = {
    'tai20x5':  1278,
    'tai50x10': 2724,
    'tai100x10':5770,
    'tai100x20':6286,
    'tai200x20':11294,
}

# ─── Parametreler ────────────────────────────────────────────────────────────
PARAMS = {
    'tenure':          50,   # Tuning sonucu: en düşük gap + en düşük std
    'max_iter':        600,  # Tuning sonucu: kalite/süre dengesi
    'no_improve_limit':120,  # max_iter / 5
    'use_insert':      True,
    'n_runs':          10,
}

# ─── Instance Tanımları ──────────────────────────────────────────────────────
# (isim, n_jobs, n_machines, seed, zorluk)
INSTANCES = [
    ('tai20x5',   20,  5,  873654221, 'Kolay'),
    ('tai50x10',  50,  10, 379008056, 'Orta'),
    ('tai100x10', 100, 10, 878272350, 'Zor'),
    ('tai100x20', 100, 20, 715671442, 'Zor'),
    ('tai200x20', 200, 20, 760290334, 'Çok Zor'),
]


def run_experiments():
    logger = ResultsLogger(output_dir='results')
    all_histories = {}  # instance -> liste of history listleri

    print("=" * 60)
    print("ENM404 Grup 9 | Flow-Shop + Tabu Search")
    print("=" * 60)

    for inst_name, n_jobs, n_machines, seed, difficulty in INSTANCES:
        print(f"\n[{difficulty}] {inst_name} ({n_jobs}x{n_machines})")
        print(f"  BKS: {BKS.get(inst_name, '?')}")

        # Instance oluştur (ya da dosyadan yükle)
        inst_file = f"instances/{inst_name}.txt"
        if os.path.exists(inst_file):
            pt, _, _, _ = load_taillard(inst_file)
        else:
            pt = generate_instance(n_jobs, n_machines, seed=seed)
            save_instance(pt, n_jobs, n_machines, inst_file, seed=seed)

        run_histories = []

        for run in range(1, PARAMS['n_runs'] + 1):
            start = time.time()
            best_perm, best_cmax, history = tabu_search(
                pt,
                tenure=PARAMS['tenure'],
                max_iter=PARAMS['max_iter'],
                no_improve_limit=PARAMS['no_improve_limit'],
                use_insert=PARAMS['use_insert'],
                verbose=False,
            )
            elapsed = round(time.time() - start, 2)

            logger.log(inst_name, run, best_cmax, elapsed)
            run_histories.append(history)
            print(f"  Çalıştırma {run:2d}: Cmax={best_cmax}  Süre={elapsed}s")

        all_histories[inst_name] = run_histories

        # Tek instance yakınsama grafiği (1. çalıştırma)
        plot_convergence(
            run_histories[0], inst_name,
            bks=BKS.get(inst_name),
            output_dir='plots'
        )

    # ─── Özet Tablo ──────────────────────────────────────────────────────────
    logger.print_summary_table(instances_bks=BKS)
    logger.save_csv()

    # ─── Tüm instance yakınsama grafikleri ───────────────────────────────────
    all_first_histories = {name: hists[0] for name, hists in all_histories.items()}
    plot_all_convergence(all_first_histories, BKS, output_dir='plots')

    print("\nTamamlandı! Sonuçlar: results/ ve plots/ klasörlerinde.")


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_experiments()
