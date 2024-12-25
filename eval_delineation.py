import numpy as np
from jsonFile import Point

class Pair:
    def __init__(self, docPoint, predPoint):
        self.docPoint = docPoint
        self.predPoint = predPoint


def processing_signal(result, start, threshold):
    maximum_x = []
    maximum_y = []
    indexes = []

    for i in range(len(result)-1):
        if result[i] > threshold:
            maximum_y.append(result[i])
            maximum_x.append(i)

            # plt.plot(i, result[i], 'ob', markersize = 4)

            if result[i + 1] < threshold or (i+1 == len(result)-1):
                if result[i+1] > threshold:
                    maximum_y.append(result[i])
                    maximum_x.append(i)

                max_point_y = max(maximum_y)
                max_point_x = maximum_x[maximum_y.index(max_point_y)]
                point = Point(max_point_x + start, max_point_y)
                indexes.append(point)
                maximum_x.clear()
                maximum_y.clear()

    return indexes

def eval_delineation(true_signal, our_signal, threshold):
    radius = 50
    # threshold = 0.8

    if len(true_signal) == 0:
        return -1, -1

    our_signal = np.array(our_signal)
    indices = np.where(our_signal >= threshold)[0]  # Индексы, где сигнал >= threshold
    not_pair = true_signal[:] # создаем копию списка

    matches = []
    used_indices = set()

    for point in true_signal:
        start = max(0, point.x - radius // 2)
        end = min(len(our_signal), point.x + radius // 2)

        # Используем NumPy для фильтрации индексов в диапазоне
        # valid_indices = indices[(indices >= start) & (indices < end)]
        pairs = processing_signal(our_signal[start:end], start, threshold)
        # pairs = [Point(i.x, our_signal[i.x]) for i in valid_points]

        if pairs:
            # Убираем уже использованные индексы
            pairs = [p for p in pairs if p.x not in used_indices]

            if pairs:
                # Находим ближайший с помощью NumPy
                closest = find_close(point, pairs)
                used_indices.add(closest.x)  # Отмечаем индекс как использованный
                del_pair(point, not_pair)
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

def del_pair(point, not_pair):
    for i, p in enumerate(not_pair):
        if p.x == point.x and p.y == point.y:
            del not_pair[i]
    return not_pair


