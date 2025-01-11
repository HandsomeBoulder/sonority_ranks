import matplotlib.pyplot as plt

def draw_dots(ranks, intensity_means, loudness_means, filtered_intensity_means, filtered_loudness_means):
    # Построение графика корреляции признаков
    plt.scatter(ranks, intensity_means, color='blue', label='Средние значения интенсивности')
    plt.title("Корреляция между рангами сонорности и акустическими признаками")
    plt.xlabel("Ранги сонорности")
    plt.ylabel("Средние значения признаков")
    plt.legend()
    plt.grid()
    plt.savefig("Интенсивность1.png")
    plt.close()

    plt.scatter(ranks, loudness_means, color='red', label='Средние значения громкости')
    plt.title("Корреляция между рангами сонорности и акустическими признаками")
    plt.xlabel("Ранги сонорности")
    plt.ylabel("Средние значения признаков")
    plt.legend()
    plt.grid()
    plt.savefig("Громкость1.png")
    plt.close()

    plt.scatter(ranks, filtered_intensity_means, color='green', label='Интенсивность в фильтрованном сигнале')
    plt.title("Корреляция между рангами сонорности и акустическими признаками")
    plt.xlabel("Ранги сонорности")
    plt.ylabel("Средние значения признаков")
    plt.legend()
    plt.grid()
    plt.savefig("Интенсивность2.png")
    plt.close()

    plt.scatter(ranks, filtered_loudness_means, color='black', label='Громкость в фильтрованном сигнале')
    plt.title("Корреляция между рангами сонорности и акустическими признаками")
    plt.xlabel("Ранги сонорности")
    plt.ylabel("Средние значения признаков")
    plt.legend()
    plt.grid()
    plt.savefig("Громкость2.png")
    plt.close()