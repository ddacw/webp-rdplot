# webp-rdplot

## Prerequisites
- [libwebp](https://github.com/webmproject/libwebp)
- [matplotlib](https://matplotlib.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)

## Usage

### Display the RD curve for a single image
```$ python psnr.py filename [psnr/ssim]```

### Display RD curves for a directory containing images
```$ python multi.py directory [psnr/ssim]```

## Extras

* ### `get_frames.py`
  **Requirements**: numpy, pytube3, moviepy

  ```$ python get_frames.py {url} {outfile} [{resolution} {start} {end} {fps}]```

  **Example:** 
  `$ python get_frames.py https://youtu.be/g4Hbz2jLxvQ spi1 480p 79 89 6`


## Example

### `psnr.py`
![psnr](example/psnr.png)

### `multi.py`
![multi](example/multi.png)
