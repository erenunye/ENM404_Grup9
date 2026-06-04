"""
generate_taillard.py
--------------------
Taillard (1993) makalesindeki orijinal rastgele sayı üreticisi ile
benchmark instance'larını birebir üretir.

Kaynak: Taillard, E. (1993). Benchmarks for basic scheduling problems.
        European Journal of Operational Research, 64(2), 278-285.

Taillard'ın C kodundaki seed tabanlı LCG (Linear Congruential Generator)
Python'a çevrilmiştir. Bu sayede literatürdeki BKS değerleriyle
karşılaştırma yapılabilir.
"""

import os


def taillard_rng(seed):
    """
    Taillard'ın orijinal rastgele sayı üreticisi (LCG).
    Her çağrıda seed güncellenir, [0,1] arasında float döner.
    """
    seed = (seed * 536870923 + 1) % (2**31 - 1)
    return seed, seed / (2**31 - 1)


def generate_taillard_instance(n_jobs, n_machines, seed_init, p_min=1, p_max=99):
    """
    Taillard'ın orijinal yöntemiyle işlem süresi matrisi üretir.

    Returns:
        processing_times[i][j]: j. işin i. makinedeki işlem süresi
        seed_final: son seed değeri
    """
    seed = seed_init
    processing_times = []

    for i in range(n_machines):
        row = []
        for j in range(n_jobs):
            seed, r = taillard_rng(seed)
            p = int(r * (p_max - p_min + 1)) + p_min
            row.append(p)
        processing_times.append(row)

    return processing_times, seed


# ─── Taillard Benchmark Kataloğu ─────────────────────────────────────────────
# Her grup için: (n_jobs, n_machines, seed, BKS_upper_bound)
# Kaynak: Taillard (1993), Tablo 1 — ilk instance her gruptan
TAILLARD_CATALOG = {
    'tai20x5':  {'n_jobs': 20,  'n_machines': 5,  'seed': 873654221, 'bks': 1278},
    'tai50x10': {'n_jobs': 50,  'n_machines': 10, 'seed': 379008056, 'bks': 2724},
    'tai100x10':{'n_jobs': 100, 'n_machines': 10, 'seed': 878272350, 'bks': 5770},
    'tai100x20':{'n_jobs': 100, 'n_machines': 20, 'seed': 715671442, 'bks': 6286},
    'tai200x20':{'n_jobs': 200, 'n_machines': 20, 'seed': 760290334, 'bks': 11294},
}


def save_taillard_txt(name, processing_times, n_jobs, n_machines, seed, bks, output_dir):
    """Instance'ı standart Taillard formatında kaydeder."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{name}.txt")
    with open(filepath, 'w') as f:
        # Header: n_jobs n_machines seed upper_bound lower_bound
        f.write(f"{n_jobs} {n_machines} {seed} {bks} 0\n")
        for row in processing_times:
            f.write(' '.join(map(str, row)) + '\n')
    return filepath


def generate_all(output_dir='instances'):
    """Tüm 5 benchmark instance'ını üret ve kaydet."""
    print("Taillard Benchmark Instance Üretici")
    print("=" * 50)

    generated = {}

    for name, info in TAILLARD_CATALOG.items():
        pt, _ = generate_taillard_instance(
            info['n_jobs'], info['n_machines'], info['seed']
        )
        filepath = save_taillard_txt(
            name, pt,
            info['n_jobs'], info['n_machines'],
            info['seed'], info['bks'],
            output_dir
        )
        generated[name] = pt

        # Doğrulama: makine/iş boyutları
        assert len(pt) == info['n_machines'], "Makine sayısı hatalı!"
        assert len(pt[0]) == info['n_jobs'], "İş sayısı hatalı!"

        print(f"  ✓ {name:12s} | {info['n_jobs']:3d} iş x {info['n_machines']:2d} makine "
              f"| BKS={info['bks']:6d} | Kaydedildi: {filepath}")

    print(f"\nToplam {len(generated)} instance üretildi → {output_dir}/")
    return generated


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    generate_all()
