import os
import subprocess
import sys

import matplotlib.pyplot as plt

from PIL import Image


def process_q(filename, q, m):
    """Returns the file size and PSNR value for compression factor q."""
    cmd = 'cwebp -q {0} -m {1} -print_psnr -short -mt {2} -o {2}.webp'.format(
        q, m, filename)
    completed = subprocess.run(cmd, shell=True, capture_output=True)
    subprocess.call(['rm', '{}.webp'.format(filename)])
    output = str(completed.stderr)
    info = output[2:-3].strip().split(' ')
    return int(info[0]), float(info[1])


def process_m(filename, m, pixel_count):
    """Returns the list of file sizes and PSNR values for 
    compression method m.
    """
    bitrate, psnr = [], []
    for q in range(0, 101, 5):
        _size, _psnr = process_q(filename, q, m)
        bitrate.append(_size / pixel_count)
        psnr.append(_psnr)
    return bitrate, psnr


def main():
    filename = sys.argv[1]
    im = Image.open(filename)
    w, h = im.size
    methods = [0, 2, 4, 6]

    for m in methods:
        bitrate, psnr = process_m(filename, m, w * h)
        plt.plot(bitrate, psnr, label='m={}'.format(m))

    plt.legend(loc='lower right')
    plt.xlabel('Bitrate')
    plt.ylabel('PSNR')
    plt.show()


if __name__ == "__main__":
    main()
