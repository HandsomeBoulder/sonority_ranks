import librosa
import numpy as np

def loudness_calc(data: np.array, samplerate: float, start: float, end: float) -> float:
    """
    This is a function that calculates mean loudness of a soundfile frame
    """
    frame = 200
    hop = 100
    n_mels = 26
    loudness = 0
    # Перевод в отсчеты
    start *= samplerate
    end *= samplerate
    # Обрезка окна
    data = data[int(start):int(end)]
    # Быстрое преобразование Фурье
    spectrum = librosa.stft(data, n_fft=frame, hop_length=hop)
    spectrum = spectrum ** 2  # Спектр мощности
    # Мел-банк
    mel_bank = librosa.filters.mel(sr=samplerate, n_fft=frame, n_mels=n_mels, fmin=20, fmax=8000)
    # Получение центральных частот треугольников
    mel_frequencies = librosa.mel_frequencies(n_mels=n_mels, fmin=20, fmax=8000)
    # Вычисление мел-спектра
    mel_spectrum = np.dot(mel_bank, spectrum)
    # Перевод данных в вещественные числа
    mel_spectrum = np.abs(mel_spectrum)
    # Вычисление кривых
    for frequency, mel in zip(mel_frequencies, mel_spectrum):
        curve = (frequency**2 + 56.8e6) * frequency**4 / ((frequency**2 + 6.3e6)**2 * (frequency**2 + 0.38e9) * (frequency**6 + 9.58e26))
        # Извлечение кубического корня
        section = (mel * curve) ** (1/3)
        # Получение итоговой громкости сложением
        loudness += section
    # Среднее значение громкости для отрезка
    loudness_mean = np.mean(loudness)
    # loudness_mean = loudness_mean.astype('float64')

    return loudness_mean