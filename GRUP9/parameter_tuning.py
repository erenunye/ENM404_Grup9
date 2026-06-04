"""
parameter_tuning.py
-------------------
Tabu Search için sistematik parametre tuning.

Test edilen parametreler:
  - tenure:   [5, 10, 20, 30, 50]
  - max_iter: [500, 1000, 2000]

Her kombinasyon için 5 çalıştırma yapılır.
Tuning tai20x5 ve tai50x10 üzerinde yapılır.
"""

import time
import random
import csv
import os
from instance_loader import load_taillard
from tabu_search import tabu_search
from generate_taillard import TAILLARD_CATALOG

TUNING_INSTANCES = ['tai20x5', 'tai50x10']

TENURE_VALUES   = [5, 10, 20, 30, 50]
MAXITER_VALUES  = [500, 1000, 2000]
N_RUNS          = 5
RANDOM_SEED     = 42

BKS = {name: info['bks'] for name, info in TAILLARD_CATALOG.items()}


def run_tuning():
    random.seed(RANDOM_SEED)
    results = []

    total = len(TUNING_INSTANCES) * len(TENURE_VALUES) * len(MAXITER_VALUES)
    done = 0

    print("Parametre Tuning Başlıyor")
    print(f"Toplam kombinasyon: {total}  |  Her biri {N_RUNS} çalıştırma\n")

    for inst_name in TUNING_INSTANCES:
        info = TAILLARD_CATALOG[inst_name]
        pt, _, _, _ = load_taillard(f'instances/{inst_name}.txt')
        bks = BKS[inst_name]

        print(f"── {inst_name} (BKS={bks}) ──────────────────────────")
        print(f"  {'Tenure':>7} {'MaxIter':>8} {'Best':>7} {'Mean':>7} {'Std':>6} {'Gap%':>7} {'Süre(s)':>8}")
        print(f"  {'-'*7} {'-'*8} {'-'*7} {'-'*7} {'-'*6} {'-'*7} {'-'*8}")

        for tenure in TENURE_VALUES:
            for max_iter in MAXITER_VALUES:
                cmaxs = []
                times = []

                for _ in range(N_RUNS):
                    start = time.time()
                    _, cmax, _ = tabu_search(
                        pt,
                        tenure=tenure,
                        max_iter=max_iter,
                        no_improve_limit=max_iter // 5,
                        use_insert=True,
                        verbose=False
                    )
                    elapsed = time.time() - start
                    cmaxs.append(cmax)
                    times.append(elapsed)

                best  = min(cmaxs)
                mean  = sum(cmaxs) / len(cmaxs)
                std   = (sum((x - mean)**2 for x in cmaxs) / len(cmaxs)) ** 0.5
                gap   = (best - bks) / bks * 100
                avg_t = sum(times) / len(times)

                print(f"  {tenure:>7} {max_iter:>8} {best:>7} {mean:>7.1f} {std:>6.1f} {gap:>+7.2f}% {avg_t:>8.2f}")

                results.append({
                    'instance': inst_name,
                    'tenure': tenure,
                    'max_iter': max_iter,
                    'best': best,
                    'mean': round(mean, 1),
                    'std': round(std, 1),
                    'gap_pct': round(gap, 2),
                    'avg_time': round(avg_t, 2),
                })

                done += 1

        print()

    # CSV'ye kaydet
    os.makedirs('results', exist_ok=True)
    csv_path = 'results/tuning_results.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"Tuning sonuçları kaydedildi: {csv_path}")

    # En iyi kombinasyonu bul
    print("\n── En İyi Parametre Kombinasyonları ──────────────────")
    for inst_name in TUNING_INSTANCES:
        inst_results = [r for r in results if r['instance'] == inst_name]
        # gap'e göre, eşitlikteyse süreye göre sırala
        best = min(inst_results, key=lambda r: (r['gap_pct'], r['avg_time']))
        print(f"  {inst_name}: tenure={best['tenure']}, max_iter={best['max_iter']} "
              f"→ gap={best['gap_pct']:+.2f}%, süre={best['avg_time']:.2f}s")

    return results


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_tuning()
