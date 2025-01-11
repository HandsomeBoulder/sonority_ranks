import os.path

def collect_paths(dir_name: str) -> list:
    paths = [[],[]]
    # Пути к аудиофайлам
    for address, _, files in os.walk(dir_name):
        for name in files:
            if ".wav" in name:
                paths[0].append(os.path.join(address, name))

    # Нахождение пар путей
    for soundfile in paths[0]:
        paths[1].append(soundfile[:-3] + "TextGrid")

    return paths

# print(collect_paths("text"))