import numpy as np
from jsonFile import Point

class Pair:
    def __init__(self, docPoint, predPoint):
        self.docPoint = docPoint
        self.predPoint = predPoint


def eval_delineation(true_signal, our_signal):
    radius = 50
    threshold = 0.8

    if len(true_signal) == 0:
        return -1, -1

    our_signal = np.array(our_signal)
    indices = np.where(our_signal >= threshold)[0]  # Индексы, где сигнал >= threshold
    not_pair = len(indices)

    matches = []
    used_indices = set()

    for point in true_signal:
        start = max(0, point.x - radius // 2)
        end = min(len(our_signal), point.x + radius // 2)

        # Используем NumPy для фильтрации индексов в диапазоне
        valid_indices = indices[(indices >= start) & (indices < end)]
        pairs = [Point(i, our_signal[i]) for i in valid_indices]

        if pairs:
            # Убираем уже использованные индексы
            pairs = [p for p in pairs if p.x not in used_indices]

            if pairs:
                # Находим ближайший с помощью NumPy
                closest = find_close(point, pairs)
                used_indices.add(closest.x)  # Отмечаем индекс как использованный
                not_pair -= 1
                matches.append(Pair(point, closest))
            else:
                matches.append(None)
        else:
            matches.append(None)

    return matches, not_pair


def find_close(p, pairs):
    # Векторизованный поиск ближайшей точки
    values = np.array([obj.x for obj in pairs])
    index = (np.abs(values - p.x)).argmin()
    return pairs[index]

