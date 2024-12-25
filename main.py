import matplotlib.pyplot as plt
import numpy as np
import torch
import jsonFile as jsonFile
import save_load_data
from jsonFile import Point
from eval_delineation import eval_delineation


def prepare_data(file, leads, tops):
    data = {}

    for lead in leads:
        for top in tops:
            signals = []
            delDoc = []

            for patient in file:
                signal = file[patient]['Leads'][lead]['Signal']
                signals.append(signal)

                points = [
                    Point(
                        x=file[patient]['Leads'][lead]['DelineationDoc'][top][i][0],
                        y=signal[file[patient]['Leads'][lead]['DelineationDoc'][top][i][0]]
                    )
                    for i in range(len(file[patient]['Leads'][lead]['DelineationDoc'][top]))
                ]
                delDoc.append(points)

            data[(lead, top)] = (signals, delDoc)

    return data


def calculate_F1(error, withoutPair):
    F1_arr = []

    for m in range(len(error)):
        FP = withoutPair[m]
        FN = 0
        TP = 0
        print(f"FP = {FP} for i = {m}")
        for j in range(len(error[m])):
            if error[m][j] is None:
                FN += 1
            else:
                TP += 1

        precision = TP / (TP + FP) if TP + FP > 0 else 0
        recall = TP / (TP + FN) if TP + FN > 0 else 0

        F1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
        F1_arr.append(F1)
    return F1_arr


def calculate_mean(errors):
    mean_arr = []
    for error_list in errors:
        distances = [
            abs(e.docPoint.x - e.predPoint.x)
            for e in error_list if e is not None
        ]
        mean = np.mean(distances) if distances else 0
        mean_arr.append(mean)
    return mean_arr


if __name__ == '__main__':
    file = jsonFile.load("ecg_data_200.json")
    leads = ['i', 'ii', 'iii', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'avf', 'avl', 'avr']
    tops = ['p', 'qrs', 't']

    # preprocessed_data = prepare_data(file, leads, tops)

    preprocessed_data = save_load_data.load_data()

    errors_F1 = [[] for _ in tops]
    without_pair = [[] for _ in tops]

    for k in range(1):
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(24, 16))
        axes = [ax1, ax2, ax3]
        index = np.array([197])

        for i, top in enumerate(tops):
            avg = []
            docsPoints = []

            for lead in leads:
                signals, delDoc = preprocessed_data[(lead, top)]

                signals = torch.from_numpy(np.array(signals)).float()
                original_signal = signals[index].numpy()

                model = torch.load(f"model_{top}_{lead}.pth")
                model.eval()

                votes = np.zeros(original_signal.shape[1])
                for p in range(0, original_signal.shape[1] - 500):
                    binVote = model(signals[index][0][p:p + 500].unsqueeze(0))
                    binVote = binVote.squeeze(0).detach().numpy()
                    votes[p + 250 - 1] = binVote

                avg.append(votes)

                if lead == 'i':
                    docsPoints = delDoc[index[0]]

            result = np.mean(avg, axis=0)
            jsonFile.draw_signal(result, axes[i])
            jsonFile.drawXtop(docsPoints, axes[i])

            if len(docsPoints) == 0:
                break

            treshold = 0.6
            matches, not_pair = eval_delineation(docsPoints, result, treshold)
            if matches == -1 and not_pair == -1:
                break

            errors_F1[i].extend(matches)
            without_pair[i].append(not_pair)

    # Вычисление F1 и среднего
    F1_array = calculate_F1(errors_F1, without_pair)
    print(F1_array)
    mean_array = calculate_mean(errors_F1)
    print(mean_array)

    # Сохранение результата
    plt.savefig(f"Check_with_F1.png")
    plt.close()
