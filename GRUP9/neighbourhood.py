"""
neighbourhood.py
----------------
Tabu Search için komşuluk yapısı.

İki hamle tipi:
- SWAP:   permutation içinde i ve j. pozisyonları yer değiştirir
- INSERT: i. pozisyondaki işi j. pozisyona taşır

Her hamle (i, j, move_type) tuple'ı ile temsil edilir.
Bu tuple aynı zamanda tabu listesine eklenir.
"""

import random
from makespan import calculate_makespan

# Büyük instance'larda tam tarama yerine rastgele örnekleme
# n <= FULL_SEARCH_THRESHOLD → tam komşuluk
# n > FULL_SEARCH_THRESHOLD  → MAX_NEIGHBOURS rastgele komşu
FULL_SEARCH_THRESHOLD = 30
MAX_NEIGHBOURS = 80   # büyük instance'lar için örnekleme boyutu


def apply_swap(permutation, i, j):
    """i ve j. pozisyonları swap eder, yeni permütasyon döndürür."""
    p = permutation[:]
    p[i], p[j] = p[j], p[i]
    return p


def apply_insert(permutation, i, j):
    """i. pozisyondaki işi çıkarıp j. pozisyona ekler."""
    p = permutation[:]
    job = p.pop(i)
    p.insert(j, job)
    return p


def get_best_neighbour(permutation, processing_times, tabu_list,
                       best_known_cmax, use_insert=True):
    """
    Tabu listesini dikkate alarak en iyi komşuyu bulur.

    Küçük instance'larda tam tarama, büyüklerde rastgele örnekleme.
    Aspirasyon kriteri: Tabu olsa bile BKS'yi geçen çözüm kabul edilir.

    Returns:
        best_neighbour (list): En iyi komşu permütasyon
        best_cmax (int): O komşunun makespan değeri
        best_move (tuple): Yapılan hamle (tabu listesine eklenecek)
    """
    n = len(permutation)
    best_cmax = float('inf')
    best_neighbour = None
    best_move = None

    # Tüm olası swap çiftleri
    all_pairs = [(i, j) for i in range(n - 1) for j in range(i + 1, n)]

    # Büyük instance'larda örnekleme
    if n > FULL_SEARCH_THRESHOLD:
        pairs = random.sample(all_pairs, min(MAX_NEIGHBOURS, len(all_pairs)))
    else:
        pairs = all_pairs

    for i, j in pairs:
        move = (permutation[i], permutation[j], 'swap')
        neighbour = apply_swap(permutation, i, j)
        cmax = calculate_makespan(neighbour, processing_times)

        is_tabu = move in tabu_list
        aspiration = cmax < best_known_cmax

        if (not is_tabu or aspiration) and cmax < best_cmax:
            best_cmax = cmax
            best_neighbour = neighbour
            best_move = move

    # Insert komşuları (küçük instance'larda ek çeşitlilik)
    if use_insert and n <= FULL_SEARCH_THRESHOLD:
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                move = (permutation[i], j, 'insert')
                neighbour = apply_insert(permutation, i, j)
                cmax = calculate_makespan(neighbour, processing_times)

                is_tabu = move in tabu_list
                aspiration = cmax < best_known_cmax

                if (not is_tabu or aspiration) and cmax < best_cmax:
                    best_cmax = cmax
                    best_neighbour = neighbour
                    best_move = move

    return best_neighbour, best_cmax, best_move
