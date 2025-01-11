import parselmouth
from draw import draw_dots
from path_extractor import collect_paths
from loudness import loudness_calc
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt

def main():
    """
    This is a script that calculates possible correlations between mean
    values of signal features and sonority ranks.
    """


    # Словарь рангов. Ключи -- фонемы, содержимое -- 4 пустых списка для
    # среднего значения интенсивности, громкости, интенсивности в
    # фильтрованном сигнале, громкости в фильтрованном сигнале.
    sounds = {
        ("a", "ɒ", "ɑ", "ã", "æ", "ɐ")                : [],
        ("œ", "e", "o", "ɔ", "ɤ", "ε", "õ", "ø", "ʌ") : [],
        ("i", "ɪ", "u", "ʊ", "ɯ", "y", "ʏ")           : [],
        ("ə", "ɵ", "ɜ", "ɘ", "ɞ")                     : [],
        ("ɨ", "ʉ")                                    : [],
        ("j", "w")                                    : [],
        ("ɹ", "ɺ")                                    : [],
        ("ɾ")                                         : [],
        ("l", "ɫ", "ɮ")                               : [],
        ("r")                                         : [],
        ("m", "n", "ŋ")                               : [],
        ("v", "z", "ʒ", "ɦ", "ɣ", "ð")                : [],
        ("d͡ʒ", "d͡z")                                  : [],
        ("b", "d", "g")                               : [],
        ("f", "s", "ʃ", "h", "θ", "x")                : [],
        ("t͡ʃ", "t͡s")                                  : [],
        ("p", "t", "k")                               : []
    }

    # Глобальные переменные
    paths = collect_paths("text")
    filter_setting = ">2000"  # Частота фильтра, выше или ниже которой все частоты обрезаются

    for soundfile, gridfile in zip(paths[0], paths[1]):
        # Конвертация триграфов в юникод
        tg = parselmouth.read(gridfile)
        parselmouth.praat.call(tg, "Convert to Unicode")
        tgt_grid_uni = tg.to_tgt()

        # Извлечение всех значений время <-> интенсивность из TextGrid
        acoustic_tier = tgt_grid_uni.get_tier_by_name("acoustic")
        # Обработка звукового файла
        sound = parselmouth.Sound(soundfile)
        intensity = sound.to_intensity()
        time_points = intensity.xs()
        intensity_values = intensity.values.reshape(-1)
        data = sound.values.reshape(-1)
        samplerate = sound.sampling_frequency

        # Приминение фильтра
        filtered_sound = parselmouth.praat.call(sound, "Filter (formula)", f"if x{filter_setting} then 0 else self fi")
        filtered_intensity = filtered_sound.to_intensity()
        filtered_time_points = filtered_intensity.xs()
        filtered_intensity_values = filtered_intensity.values.reshape(-1)
        filtered_data = filtered_sound.values.reshape(-1)

        # Обработка каждого интервала в тире
        for interval in acoustic_tier:
            name, start, end = interval.text, interval.start_time, interval.end_time

            if name in ["pause", "pause_filled", "glot"]:  # Отброс нефонемных интервалов
                continue
            for symbol in ["~", "-", "'", ":", "°", "+", "", ".", "̚̚v"]:  # Отброс излишних фонетических символов
                name = name.replace(symbol, "")

            # Отбор значений из общего пула в рамках отрезков [start:end]
            framed_intensity = []
            for time, value in zip(time_points, intensity_values):
                if start <= time <= end:
                    framed_intensity.append(value)
            # Отбор значений для филтрованного сигнала
            filtered_framed_intensity = []
            for time, value in zip(filtered_time_points, filtered_intensity_values):
                if start <= time <= end:
                    filtered_framed_intensity.append(value)        

            # Определение средних значений
            if len(framed_intensity) > 0:
                intensity_mean = sum(framed_intensity) / len(framed_intensity)
                loundness_mean = loudness_calc(data, samplerate, start, end)

            # Определение средних значений в фильтрованном сигнале
            if len(filtered_framed_intensity) > 0:
                filtered_intensity_mean = sum(filtered_framed_intensity) / len(filtered_framed_intensity)
                filtered_loudness_mean = loudness_calc(filtered_data, samplerate, start, end)        

                # Внесение каждого среднего значения в словарь под соответствующий ранг
                for key in sounds:
                    if len(sounds[key]) == 0:
                        for _ in range(4):
                            sounds[key].append([])
                    if name in key:
                        sounds[key][0].append(intensity_mean)
                        sounds[key][1].append(loundness_mean)
                        sounds[key][2].append(filtered_intensity_mean)
                        sounds[key][3].append(filtered_loudness_mean)

    # Определение среднего значения интенсивности и громкости для каждого ранга
    for key in sounds:
        for list_index in range(4):
            sounds[key][list_index] = np.mean(sounds[key][list_index])

    # Образование списков значений рангов, интенсивности и громкости
    results = []
    for _ in range(4):
        results.append([])

    for key in sounds:
        counter = 0
        for item in sounds[key]:
            results[counter].append(item)
            counter += 1

    results.append(list(range(len(sounds),0,-1)))

    # Корреляция
    print("Корреляция с интенсивностью в оригинальном сигнале")
    print(pearsonr(results[4], results[0]))
    print("##############################")
    print("Корреляция с громкостью в оригинальном сигнале")
    print(pearsonr(results[4], results[1]))
    print("##############################")
    print("Корреляция с интенсивностью в фильтрованном сигнале")
    print(pearsonr(results[4], results[2]))
    print("##############################")
    print("Корреляция с громкостью в фильтрованном сигнале")
    print(pearsonr(results[4], results[3]))

    draw_dots(results[4], results[0], results[1], results[2], results[3])

if __name__ == "__main__":
    main()