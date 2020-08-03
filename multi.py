import os
import sys

import matplotlib.pyplot as plt

from PIL import Image
from psnr import process_m, process_q


def main():
    directory = sys.argv[1]
    estimator = "psnr"
    if len(sys.argv) == 3:
        assert sys.argv[2] in ["psnr", "ssim"], "Invalid estimator."
        estimator = sys.argv[2]

    for filename in os.listdir(directory):
        print(filename)
        filename = directory + "/" + filename
        im = Image.open(filename)
        w, h = im.size
        bitrate, psnr = process_m(filename, 4, w * h, estimator)
        plt.plot(bitrate, psnr, color="royalblue")

    plt.xlabel("Bitrate")
    plt.ylabel(estimator.upper())
    plt.show()


if __name__ == "__main__":
    main()
