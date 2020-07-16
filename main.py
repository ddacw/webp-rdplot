import subprocess
import sys
import matplotlib.pyplot as plt

from PIL import Image


def process(filename, q):
    """Returns the file size and PSNR value for compression factor q."""
    cmd = 'cwebp -q {0} -print_psnr -short -mt {1} -o {1}.webp'.format(
        q, filename)
    completed = subprocess.run(cmd, shell=True, capture_output=True)
    output = str(completed.stderr)
    info = output[2:-3].strip().split(' ')
    return int(info[0]), float(info[1])


def main():
    filename = sys.argv[1]
    im = Image.open(filename)
    w, h = im.size
    bitrate, psnr = [], []

    for q in range(0, 101, 5):
        _size, _psnr = process(filename, q)
        bitrate.append(_size / (w * h))
        psnr.append(_psnr)
    
    plt.plot(bitrate, psnr)
    plt.xlabel('Bitrate')
    plt.ylabel('PSNR')
    plt.show()


if __name__ == "__main__":
    main()
