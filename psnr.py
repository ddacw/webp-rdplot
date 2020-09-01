import os
import re
import subprocess
import sys

import matplotlib.pyplot as plt

from PIL import Image


def process_q(filename, q, m, estimator):
    """Returns the file size and PSNR value for compression factor q."""
    filename_webp = filename.split(".")[0] + ".webp"
    cmd_cwebp = "cwebp -q {} -m {} {} -o {}".format(
        q, m, filename, filename_webp)
    cmd_disto = "get_disto -{} {} {}".format(
        estimator, filename_webp, filename)
    subprocess.run(cmd_cwebp, shell=True, stderr=subprocess.DEVNULL)
    disto = subprocess.run(cmd_disto, shell=True, capture_output=True)
    sz, psnr = re.search(
        r"\d+ \d+.\d+", (disto.stdout).decode("utf-8")).group(0).split(" ")
    os.remove(filename_webp)
    return int(sz), float(psnr)


def process_m(filename, m, pixel_count, estimator):
    """Returns the list of file sizes and PSNR values for 
    compression method m.
    """
    bitrate, psnr = [], []
    for q in range(0, 101, 5):
        _size, _psnr = process_q(filename, q, m, estimator)
        bitrate.append(_size / pixel_count)
        psnr.append(_psnr)
    return bitrate, psnr


def main():
    filename = sys.argv[1]
    estimator = "psnr"
    if len(sys.argv) == 3:
        assert sys.argv[2] in ["psnr", "ssim"], "Invalid estimator."
        estimator = sys.argv[2]

    im = Image.open(filename)
    w, h = im.size
    methods = [0, 2, 4, 6]

    for m in methods:
        bitrate, psnr = process_m(filename, m, w * h, estimator)
        plt.plot(bitrate, psnr, label="m={}".format(m))

    plt.legend(loc="lower right")
    plt.xlabel("Bitrate")
    plt.ylabel(estimator.upper())
    plt.show()


if __name__ == "__main__":
    main()
