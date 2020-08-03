#!/usr/bin/env python

import os
import sys

import numpy as np

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *


def get_video(url, outfile, res):
    """Downloads video from Youtube with given quality."""
    yt = YouTube(url)

    videos = yt.streams.filter(
        file_extension="mp4", progressive=True, resolution=res)
    assert len(videos) > 0, "Invalid resolution."

    if not os.path.exists("{}.mp4".format(outfile)):
        videos[0].download(filename=outfile)
        print("Downloaded.")
    else:
        print("File already existed.")


def get_extract(outfile, start_time, end_time):
    """Trims videos for specified duration (in seconds)."""
    ffmpeg_extract_subclip("{}.mp4".format(
        outfile), start_time, end_time, targetname="{}-trimmed.mp4".format(outfile))


def get_frames(outfile, fps):
    try:
        os.mkdir(outfile)
    except OSError:
        "Creating directory failed."

    with open("{}-list.txt".format(outfile), "w") as frame_list:
        clip = VideoFileClip("{}-trimmed.mp4".format(outfile))
        for t in enumerate(np.arange(0, clip.duration, 1/fps)):
            frame_filename = "{0}/{0}_{1}.jpeg".format(outfile, t[0])
            clip.save_frame(frame_filename, t[1])
            frame_list.write("{} {}\n".format(frame_filename, int(t[1]*1000)))


def main():
    # python get_frames.py {url} {outfile} {resolution} {start} {end} {fps}
    url = sys.argv[1]
    outfile = sys.argv[2]
    resolution = "360p"
    start_time = 0
    end_time = 5
    fps = 5

    if len(sys.argv) >= 4:
        resolution = sys.argv[3].strip()
    if len(sys.argv) >= 6:
        start_time = float(sys.argv[4])
        end_time = float(sys.argv[5])
    if len(sys.argv) >= 7:
        fps = int(sys.argv[6])

    print(url, resolution, start_time, end_time, fps)

    get_video(url, outfile, resolution)
    get_extract(outfile, start_time, end_time)
    get_frames(outfile, fps)


if __name__ == "__main__":
    main()
