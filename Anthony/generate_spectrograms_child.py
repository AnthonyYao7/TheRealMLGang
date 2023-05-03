import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from PIL import Image

import os
import sys
import time
import copy



n_processes = 6


def read_mp3(f, save_index):
    command = "ffmpeg -i {} -acodec pcm_s16le -ac 1 -ar 16000 temp_files/output{}.wav".format(f, save_index)
    os.system(command)
    x, sr = librosa.load('temp_files/output{}.wav'.format(save_index), sr=16000)
    return x, sr


def make_spectrogram(filename, save_index):
    signal, sampling_rate = read_mp3(filename, save_index)

    S = librosa.feature.melspectrogram(y=signal, sr=sampling_rate, n_mels=256, fmax=2048, hop_length=256)
    S_db = librosa.power_to_db(S, ref=np.max)
    fig, ax = plt.subplots()
    ax.set_axis_off()
    img = librosa.display.specshow(S_db, x_axis='time', y_axis='mel', sr=sampling_rate, fmax=2048, ax=ax)
    plt.savefig("temp_files/out{}.png".format(save_index), bbox_inches="tight", pad_inches=0.0)
    plt.close()

    im = Image.open("temp_files/out{}.png".format(save_index))
    res = im.resize((im.width//16, im.height//16), Image.LANCZOS)
    res.save(os.path.join("spectrograms", os.path.basename(filename).split(".")[0] + ".png"))

    os.remove("temp_files/output{}.wav".format(save_index))
    os.remove("temp_files/out{}.png".format(save_index))


def make_spectrograms_multiprocessing(process_index):
    audio_files = []
    with open(os.path.join("work_lists", "{}.txt".format(process_index)), "r") as f:
        for line in f.readlines():
            audio_files.append(line.strip())

    for audio_file in audio_files:
        print("doing {}".format(audio_file))
        make_spectrogram(audio_file, process_index)

    with open("temp_files/time_finished{}".format(process_index), "a") as f:
        f.write(str(time.ctime()) + "\n")


def main():
    make_spectrograms_multiprocessing(int(sys.argv[1]))


if __name__ == "__main__":
    main()
