"""
instance_loader.py
------------------
Taillard benchmark instance dosyalarını okur.

Taillard formatı:
    İlk satır: n_jobs n_machines seed upper_bound lower_bound
    Sonraki satırlar: processing_times matrisi (n_machines x n_jobs)

Kaynak: http://mistic.heig-vd.ch/taillard/problemes.dir/ordonnancement.dir/ordonnancement.html
"""

import os
import random


def load_taillard(filepath):
    """
    Taillard formatındaki dosyayı okur.

    Returns:
        processing_times: p[i][j] = j. işin i. makinedeki işlem süresi
        n_jobs (int)
        n_machines (int)
        meta (dict): seed, upper_bound, lower_bound (varsa)
    """
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    # İlk satır: header
    header = lines[0].split()
    n_jobs = int(header[0])
    n_machines = int(header[1])
    meta = {
        'n_jobs': n_jobs,
        'n_machines': n_machines,
        'seed': int(header[2]) if len(header) > 2 else None,
        'upper_bound': int(header[3]) if len(header) > 3 else None,
        'lower_bound': int(header[4]) if len(header) > 4 else None,
    }

    # Kalan satırlar: işlem süreleri
    processing_times = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        if row:
            processing_times.append(row)

    return processing_times, n_jobs, n_machines, meta


def generate_instance(n_jobs, n_machines, seed=42, p_min=1, p_max=99):
    """
    Rastgele Flow-Shop instance üretir (Taillard'ın yöntemiyle).

    Args:
        n_jobs: İş sayısı
        n_machines: Makine sayısı
        seed: Rastgele tohum
        p_min, p_max: İşlem süresi aralığı

    Returns:
        processing_times: p[i][j] matrisi
    """
    rng = random.Random(seed)
    processing_times = [
        [rng.randint(p_min, p_max) for _ in range(n_jobs)]
        for _ in range(n_machines)
    ]
    return processing_times


def save_instance(processing_times, n_jobs, n_machines, filepath, seed=0):
    """Instance'ı Taillard formatında kaydeder."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(f"{n_jobs} {n_machines} {seed} 0 0\n")
        for row in processing_times:
            f.write(' '.join(map(str, row)) + '\n')
    print(f"Kaydedildi: {filepath}")
