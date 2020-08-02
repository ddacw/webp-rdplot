import re
import subprocess
import sys

import matplotlib.pyplot as plt

from PIL import Image


def process_q(filename, q, m, estimator):
    """Returns the file size and PSNR value for compression factor q."""
    cmd = 'cwebp -q {0} -m {1} -print_{2} -short -mt {3}'.format(
        q, m, estimator, filename)
    completed = subprocess.run(cmd, shell=True, capture_output=True)
    info = re.search(r'\d+ \d+.\d+', str(completed.stderr)).group(0).split(' ')
    return int(info[0]), float(info[1])


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
    estimator = 'psnr'
    if len(sys.argv) == 3:
        assert sys.argv[2] in ['psnr', 'ssim'], "Invalid estimator."
        estimator = sys.argv[2]

    im = Image.open(filename)
    w, h = im.size
    methods = [0, 2, 4, 6]

    for m in methods:
        bitrate, psnr = process_m(filename, m, w * h, estimator)
        plt.plot(bitrate, psnr, label='m={}'.format(m))

    plt.legend(loc='lower right')
    plt.xlabel('Bitrate')
    plt.ylabel(estimator.upper())
    plt.show()


if __name__ == "__main__":
    main()
