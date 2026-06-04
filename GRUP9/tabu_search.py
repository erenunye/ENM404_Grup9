"""
tabu_search.py
--------------
Flow-Shop Scheduling için Tabu Search algoritması.

Bileşenler:
- Başlangıç çözümü: NEH sezgiseli
- Komşuluk: Swap + Insert
- Tabu listesi: Son `tenure` hamleyi yasaklar
- Aspirasyon: BKS'yi geçen tabu hamle kabul edilir
- Durdurma: max_iter veya no_improve_limit iterasyon iyileşme yoksa dur
"""

from collections import deque
from makespan import calculate_makespan
from neh import neh
from neighbourhood import get_best_neighbour


def tabu_search(processing_times,
                tenure=20,
                max_iter=1000,
                no_improve_limit=200,
                use_insert=True,
                verbose=False):
    """
    Tabu Search ile Flow-Shop Scheduling çözer.

    Args:
        processing_times: p[i][j] = j. işin i. makinedeki işlem süresi
        tenure (int): Tabu listesi uzunluğu
        max_iter (int): Maksimum iterasyon sayısı
        no_improve_limit (int): Bu kadar iterasyon iyileşme olmazsa dur
        use_insert (bool): Insert komşuluğunu da kullan
        verbose (bool): Her iterasyonu yazdır

    Returns:
        best_perm (list): En iyi bulunan iş sırası
        best_cmax (int): En iyi makespan
        history (list): Her iterasyondaki mevcut Cmax (yakınsama grafiği için)
    """

    # --- Başlangıç çözümü (NEH) ---
    current_perm, current_cmax = neh(processing_times)
    best_perm = current_perm[:]
    best_cmax = current_cmax

    # Tabu listesi (deque ile otomatik tenure yönetimi)
    tabu_list = deque(maxlen=tenure)

    history = [current_cmax]
    no_improve = 0

    for iteration in range(1, max_iter + 1):

        # En iyi komşuyu bul
        neighbour, neighbour_cmax, move = get_best_neighbour(
            current_perm, processing_times, tabu_list,
            best_cmax, use_insert=use_insert
        )

        if neighbour is None:
            # Hiç komşu bulunamadı (çok nadir)
            break

        # Hamleyi uygula
        current_perm = neighbour
        current_cmax = neighbour_cmax

        # Tabu listesine ekle
        if move:
            tabu_list.append(move)

        # Global en iyi güncelle
        if current_cmax < best_cmax:
            best_cmax = current_cmax
            best_perm = current_perm[:]
            no_improve = 0
        else:
            no_improve += 1

        history.append(current_cmax)

        if verbose and iteration % 100 == 0:
            print(f"  İter {iteration:4d} | Mevcut: {current_cmax} | En İyi: {best_cmax}")

        # Erken durdurma
        if no_improve >= no_improve_limit:
            if verbose:
                print(f"  → {no_improve_limit} iterasyon iyileşme yok, durduruluyor.")
            break

    return best_perm, best_cmax, history
