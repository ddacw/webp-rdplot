# webp-rdplot

## Prerequisites
- [libwebp](https://github.com/webmproject/libwebp)
- [matplotlib](https://matplotlib.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/)

## Usage

### Display the RD curve for a single image
```$ python psnr.py filename [{psnr/ssim}]```

### Display RD curves for a directory containing images
```$ python multi.py [-h] [-s] [-q QUALITY] [-mq] directory```

## Extras

* ### `get_frames.py`
  **Requirements**: numpy, pytube3, moviepy

  ```$ python get_frames.py [-h] [-r RES] [-s START] [-d DURATION] [-f FPS] url title```

  **Example:** 
  `$ python get_frames.py -r 720p -s 70 -d 8 -f 0.5 https://youtu.be/g4Hbz2jLxvQ sample`


## Example

### `psnr.py`
![psnr](examples/psnr.png)

### `multi.py`
![multi](examples/multi.png)
