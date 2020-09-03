import argparse
import multiprocessing
import os
import sys

import matplotlib.pyplot as plt

from PIL import Image
from psnr import process_m, process_q


def get_data(directory, filename, estimator):
    """Returns the filesize and psnr data for a single image."""
    filename = directory + "/" + filename
    method = 4
    return process_m(filename, method, estimator)


def plot_multi(directory, estimator):
    """Plots RD-curves for all images inside directory."""
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    data = pool.starmap(get_data, [(directory, filename, estimator) for filename in os.listdir(
        directory) if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))])
    pool.close()

    for filesize, psnr in data:
        sz = len(filesize)
        p25 = sz // 4
        p50 = sz // 2
        p75 = 3 * sz // 4

        plt.plot(filesize[:p25+1], psnr[:p25+1], color="midnightblue")
        plt.plot(filesize[p25:p50+1], psnr[p25:p50+1], color="mediumblue")
        plt.plot(filesize[p50:p75+1], psnr[p50:p75+1], color="dodgerblue")
        plt.plot(filesize[p75:], psnr[p75:], color="skyblue")

    plt.axvline(x=150/len(data))


def plot_q(directory, estimator, quality, point_color="r"):
    """Plots filesize-PSNR at fixed quality for all images in directory."""
    for filename in os.listdir(directory):
        if not filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
            continue

        # get id of img
        i = int(filename.split(".")[0].split("_")[1])
        method = 4
        filename = directory + "/" + filename

        q = None

        if type(quality) is int:
            q = quality
        elif type(quality) is list:
            q = quality[i]

        sz, psnr = process_q(filename, q, method, estimator)
        filesize = sz / 1024  # in kilobyte(s)
        plt.plot(filesize, psnr, ".", color=point_color)


def main():
    parser = argparse.ArgumentParser(description="""
        Display RD curves for all images in a directory.
    """)
    parser.add_argument("directory", help="directory containing images")
    parser.add_argument(
        "-s", "--ssim", action='store_true', help="use SSIM instead of PSNR")
    parser.add_argument("-q", "--quality", type=int,
                        default=None, help="plot points of fixed quality")
    parser.add_argument("-mq", "--multi_quality", action='store_true',
                        help="enable plotting points of varied quality values")

    args = parser.parse_args()
    directory = args.directory
    estimator = "ssim" if args.ssim else "psnr"
    quality = args.quality

    print("Multi started.")
    plot_multi(directory, estimator)
    print("Multi completed.")

    if quality is not None:
        plot_q(directory, estimator, quality, "r")

    if args.multi_quality:
        print("List of quality values:")
        multi_quality = list(map(int, input().split()))
        plot_q(directory, estimator, multi_quality, "orange")

    plt.title(directory)
    plt.xlabel("filesize (kB)")
    plt.ylabel(estimator.upper())
    plt.savefig("{}.png".format(directory))
    plt.show()


if __name__ == "__main__":
    main()
