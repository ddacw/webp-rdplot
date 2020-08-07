import multiprocessing
import os
import sys

import matplotlib.pyplot as plt

from PIL import Image
from psnr import process_m, process_q


def get_data(directory, filename, estimator):
    print(filename)
    filename = directory + "/" + filename
    im = Image.open(filename)
    w, h = im.size

    # bitrate, psnr
    return process_m(filename, 4, w * h, estimator)


def main():
    directory = sys.argv[1]
    estimator = "psnr"
    if len(sys.argv) == 3:
        assert sys.argv[2] in ["psnr", "ssim"], "Invalid estimator."
        estimator = sys.argv[2]

    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    data = pool.starmap(get_data, [(directory, filename, estimator) for filename in os.listdir(
        directory) if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))])
    pool.close()

    for bitrate, psnr in data:
        sz = len(bitrate)
        p25 = sz // 4
        p50 = sz // 2
        p75 = 3 * sz // 4

        plt.plot(bitrate[:p25+1], psnr[:p25+1], color="midnightblue")
        plt.plot(bitrate[p25:p50+1], psnr[p25:p50+1], color="mediumblue")
        plt.plot(bitrate[p50:p75+1], psnr[p50:p75+1], color="dodgerblue")
        plt.plot(bitrate[p75:], psnr[p75:], color="skyblue")

    plt.title(directory)
    plt.xlabel("Bitrate")
    plt.ylabel(estimator.upper())
    plt.show()


if __name__ == "__main__":
    main()
