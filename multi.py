import multiprocessing
import os
import sys

import matplotlib.pyplot as plt

from PIL import Image
from psnr import process_m, process_q


def get_data(directory, filename, estimator):
    """Returns the bitrate and psnr data for a single image."""
    filename = directory + "/" + filename
    im = Image.open(filename)
    w, h = im.size
    method = 4
    return process_m(filename, method, w * h, estimator)


def plot_multi(directory, estimator):
    """Plots RD-curves for all images inside directory."""
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    data = pool.starmap(get_data, [(directory, filename, estimator) for filename in os.listdir(
        directory) if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))])
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


def plot_q(directory, estimator, quality):
    """Plots bitrate-PSNR at fixed quality for all images in directory."""
    for filename in os.listdir(directory):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            continue

        # get id of img
        i = int(filename.split(".")[0].split("_")[1])
        method = 4
        filename = directory + "/" + filename
        sz, psnr = process_q(filename, quality[i], method, estimator)
        im = Image.open(filename)
        bitrate = sz / (im.size[0] * im.size[1])
        plt.plot(bitrate, psnr, ".", color="r")


def main():
    directory = sys.argv[1]
    estimator = "psnr"
    quality = []

    if len(sys.argv) == 3:
        assert sys.argv[2] in ["psnr", "ssim"], "Invalid estimator."
        estimator = sys.argv[2]

    print("Multi started.")
    plot_multi(directory, estimator)
    print("Multi completed.")

    if len(sys.argv) == 4:
        assert sys.argv[3] == "q"
        print("Enter quality for each frame:")
        quality = list(map(int, input().split()))
        plot_q(directory, estimator, quality)

    plt.title(directory)
    plt.xlabel("Bitrate")
    plt.ylabel(estimator.upper())
    plt.savefig("{}.png".format(directory))
    plt.show()


if __name__ == "__main__":
    main()
