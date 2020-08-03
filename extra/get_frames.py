#!/usr/bin/env python

import os
import sys

import numpy as np

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import *


class Getter:
    def __init__(self, url, outfile, res="360p", start_time=0, end_time=10, fps=5):
        self.url = url
        self.outfile = outfile
        self.res = res

        # in seconds
        self.start_time = start_time
        self.end_time = end_time

        self.fps = fps

    def get_video(self):
        """Downloads video from Youtube with given quality."""
        yt = YouTube(self.url)
        videos = yt.streams.filter(
            file_extension="mp4", progressive=True, resolution=self.res)
        assert len(videos) > 0, "Video unavailable."

        if not os.path.exists("{}.mp4".format(self.outfile)):
            videos[0].download(filename=self.outfile)
            print("Downloaded.")
        else:
            print("File already existed.")

    def get_extract(self):
        """Trims videos for specified duration (in seconds)."""
        ffmpeg_extract_subclip("{}.mp4".format(self.outfile), self.start_time,
                               self.end_time, targetname="{}-trimmed.mp4".format(self.outfile))

    def get_frames(self):
        """Creates list of frames with timestamps + directory of frames."""
        try:
            os.mkdir(self.outfile)
        except OSError:
            print("Creating directory failed.")

        with open("{}-list.txt".format(self.outfile), "w") as frame_list:
            clip = VideoFileClip("{}-trimmed.mp4".format(self.outfile))
            for i, t in enumerate(np.arange(0, clip.duration, 1/self.fps)):
                frame_filename = "{0}/{0}_{1}.jpeg".format(self.outfile, i)
                clip.save_frame(frame_filename, t)
                frame_list.write("{} {}\n".format(frame_filename, int(t*1000)))


def main():
    assert len(sys.argv) >= 3, "Insufficient arguments."

    url = sys.argv[1].strip()
    outfile = sys.argv[2].strip()

    resolution = "360p"
    start_time = 0
    end_time = 5
    fps = 5

    if len(sys.argv) >= 4:
        resolution = sys.argv[3].strip()
        assert resolution in ["1080p", "720p", "480p",
                              "360p", "240p", "144p"], "Invalid resolution."
    if len(sys.argv) >= 6:
        start_time = float(sys.argv[4])
        end_time = float(sys.argv[5])
    if len(sys.argv) >= 7:
        fps = int(sys.argv[6])

    getter = Getter(url, outfile, resolution, start_time, end_time, fps)
    getter.get_video()
    getter.get_extract()
    getter.get_frames()


if __name__ == "__main__":
    main()
