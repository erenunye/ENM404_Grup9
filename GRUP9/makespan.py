"""
makespan.py
-----------
Flow-Shop Scheduling için Cmax (makespan) hesaplama modülü.
"""


def calculate_makespan(permutation, processing_times):
    """
    Verilen iş sırası için makespan hesaplar.

    Args:
        permutation: İş sırası listesi, örn. [2, 0, 4, 1, 3]
        processing_times: p[i][j] matrisi, Boyut: (n_machines x n_jobs)

    Returns:
        Cmax (int)
    """
    n_machines = len(processing_times)
    n_jobs = len(permutation)

    C = [0] * n_jobs  # Sadece önceki satırı tut (bellek tasarrufu)
    prev = [0] * n_jobs

    for i in range(n_machines):
        row = processing_times[i]
        c_ik_prev = 0  # C[i][k-1]
        for k in range(n_jobs):
            job = permutation[k]
            c_ik_prev = max(c_ik_prev, prev[k]) + row[job]
            C[k] = c_ik_prev
        prev = C[:]

    return C[n_jobs - 1]
