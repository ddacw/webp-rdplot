#!/usr/bin/env python

import os
import shutil
import sys

import numpy as np

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


class Getter:
    def __init__(self, url, outfile, res, start_time, end_time, fps):
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
            file_extension="mp4", resolution=self.res)
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
        with open("{}-list.txt".format(self.outfile), "w") as frame_list:
            clip = VideoFileClip("{}-trimmed.mp4".format(self.outfile))
            for i, t in enumerate(np.arange(0, self.end_time-self.start_time, 1/self.fps)):
                frame_filename = "{0}/{0}_{1}.jpeg".format(self.outfile, i)
                clip.save_frame(frame_filename, t)
                frame_list.write("{} {}\n".format(frame_filename, int(t*1000)))

    def move_files(self):
        shutil.move("{}.mp4".format(self.outfile), self.outfile)
        shutil.move("{}-trimmed.mp4".format(self.outfile), self.outfile)


def main():
    assert len(sys.argv) >= 3, "Insufficient arguments."

    url = sys.argv[1].strip()
    outfile = sys.argv[2].strip()

    resolution = "360p"
    start_time = 0
    end_time = 3
    fps = 8

    if len(sys.argv) >= 4:
        resolution = sys.argv[3].strip()
        assert resolution in ["1080p", "720p", "480p",
                              "360p", "240p", "144p"], "Invalid resolution."
    if len(sys.argv) >= 6:
        start_time = float(sys.argv[4])
        end_time = float(sys.argv[5])
        assert start_time <= end_time, "Invalid timestamps."
    if len(sys.argv) >= 7:
        fps = int(sys.argv[6])

    try:
        shutil.rmtree(outfile)
    except OSError:
        pass
    os.mkdir(outfile)

    getter = Getter(url, outfile, resolution, start_time, end_time, fps)
    getter.get_video()
    getter.get_extract()
    getter.get_frames()
    getter.move_files()


if __name__ == "__main__":
    main()
