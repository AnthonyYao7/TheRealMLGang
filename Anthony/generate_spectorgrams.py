import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display
from PIL import Image


import os
import copy
import shutil
from subprocess import Popen, PIPE

n_processes = 6


def main():
    folder = 'temp_files/'

    filelist = os.listdir(folder)
    for f in filelist:
        os.remove(os.path.join(folder, f))

    audios = [os.path.join('audios', x) for x in os.listdir('audios')]

    done = [x.split('.')[0] for x in os.listdir('spectrograms')]

    audios = set(audios) - set(done)

    audios = sorted(list(audios))

    worker_audios = []

    for i in range(n_processes):
        worker_audios.append(copy.deepcopy(audios[i * (len(audios) // n_processes + n_processes): (i + 1) * (len(audios) // n_processes + n_processes)]))

        with open(os.path.join("work_lists", "{}.txt".format(i)), "w") as f:
            f.write("\n".join(worker_audios[i]) + "\n")

    processes = []

    for i in range(n_processes):
        processes.append(
            Popen(['python', 'generate_spectrograms_child.py', str(i)])
        )

    for p in processes:
        p.wait()


if __name__ == "__main__":
    main()
