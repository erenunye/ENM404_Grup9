"""
results_logger.py
-----------------
Deney sonuçlarını kaydeder ve istatistiksel özet üretir.
"""

import csv
import os
import statistics


class ResultsLogger:
    def __init__(self, output_dir="results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.records = []  # (instance, run, cmax, time)

    def log(self, instance_name, run_id, cmax, elapsed_time):
        self.records.append({
            'instance': instance_name,
            'run': run_id,
            'cmax': cmax,
            'time': elapsed_time,
        })

    def summary(self, instance_name, bks=None):
        """Bir instance için istatistiksel özet döndürür."""
        runs = [r for r in self.records if r['instance'] == instance_name]
        if not runs:
            return None

        cmaxs = [r['cmax'] for r in runs]
        times = [r['time'] for r in runs]

        best = min(cmaxs)
        worst = max(cmaxs)
        mean = statistics.mean(cmaxs)
        std = statistics.stdev(cmaxs) if len(cmaxs) > 1 else 0.0
        avg_time = statistics.mean(times)

        result = {
            'instance': instance_name,
            'n_runs': len(runs),
            'best': best,
            'worst': worst,
            'mean': round(mean, 1),
            'std': round(std, 1),
            'avg_time': round(avg_time, 2),
        }

        if bks is not None:
            gap = (best - bks) / bks * 100
            result['bks'] = bks
            result['gap_pct'] = round(gap, 2)

        return result

    def print_summary_table(self, instances_bks=None):
        """Tüm instance'lar için özet tabloyu yazdırır."""
        if instances_bks is None:
            instances_bks = {}

        instance_names = list(dict.fromkeys(r['instance'] for r in self.records))

        print("\n" + "=" * 80)
        print(f"{'Instance':<15} {'BKS':>6} {'Best':>6} {'Mean':>7} {'Std':>6} {'Gap%':>6} {'Time(s)':>8}")
        print("=" * 80)

        for name in instance_names:
            bks = instances_bks.get(name)
            s = self.summary(name, bks)
            if s:
                bks_str = str(s.get('bks', '-'))
                gap_str = f"{s.get('gap_pct', '-')}%" if 'gap_pct' in s else '-'
                print(f"{name:<15} {bks_str:>6} {s['best']:>6} {s['mean']:>7} {s['std']:>6} {gap_str:>6} {s['avg_time']:>8}")

        print("=" * 80)

    def save_csv(self, filename="all_results.csv"):
        """Tüm çalıştırma sonuçlarını CSV'ye kaydeder."""
        filepath = os.path.join(self.output_dir, filename)
        if not self.records:
            return
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['instance', 'run', 'cmax', 'time'])
            writer.writeheader()
            writer.writerows(self.records)
        print(f"CSV kaydedildi: {filepath}")
