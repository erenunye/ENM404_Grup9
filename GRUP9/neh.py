"""
neh.py
------
NEH (Nawaz-Enscore-Ham, 1983) sezgiseli ile başlangıç çözümü üretir.
Flow-Shop için literatürde en iyi başlangıç yöntemi olarak kabul edilir.

Algoritma:
1. İşleri toplam işlem sürelerine göre azalan sırada sırala
2. İlk iki işi en iyi sırada yerleştir
3. Her yeni işi mevcut dizinin en iyi pozisyonuna ekle
"""

from makespan import calculate_makespan


def neh(processing_times):
    """
    NEH sezgiseli ile Flow-Shop başlangıç çözümü üretir.

    Args:
        processing_times: p[i][j] = j. işin i. makinedeki işlem süresi

    Returns:
        permutation (list): İş sırası
        cmax (int): Bu sıranın makespan değeri
    """
    n_machines = len(processing_times)
    n_jobs = len(processing_times[0])

    # Adım 1: Her işin toplam işlem süresini hesapla
    total_times = []
    for j in range(n_jobs):
        total = sum(processing_times[i][j] for i in range(n_machines))
        total_times.append((total, j))

    # Azalan sırada sırala
    total_times.sort(reverse=True)
    sorted_jobs = [job for _, job in total_times]

    # Adım 2-3: Sırayla en iyi pozisyona ekle
    permutation = [sorted_jobs[0]]

    for idx in range(1, n_jobs):
        job = sorted_jobs[idx]
        best_cmax = float('inf')
        best_pos = 0

        # Bu işi her pozisyona ekleyip en iyiyi bul
        for pos in range(len(permutation) + 1):
            candidate = permutation[:pos] + [job] + permutation[pos:]
            cmax = calculate_makespan(candidate, processing_times)
            if cmax < best_cmax:
                best_cmax = cmax
                best_pos = pos

        permutation = permutation[:best_pos] + [job] + permutation[best_pos:]

    return permutation, calculate_makespan(permutation, processing_times)
