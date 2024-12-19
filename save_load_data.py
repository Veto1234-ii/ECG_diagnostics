import pickle


def save_data(preprocessed_data):
    # Сохранение
    with open("preprocessed_data.pkl", "wb") as f:
        pickle.dump(preprocessed_data, f)

def load_data():
    # Загрузка
    with open("preprocessed_data.pkl", "rb") as f:
        preprocessed_data = pickle.load(f)
    return preprocessed_data
