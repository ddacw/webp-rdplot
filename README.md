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

  ```$ python get_frames.py [-h] [-r RES] [-s START] [-d DURATION] [-f FPS] [-y] url title```

  **Example:** 
  `$ python get_frames.py -s 138 -d 6 -f 4 -y https://youtu.be/C6kn6nXMWF0 sample`


## Example

### `psnr.py`
![psnr](examples/psnr.png)

### `multi.py`
![multi](examples/multi.png)
