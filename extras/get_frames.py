#!/usr/bin/env python

import argparse
import os
import shutil
import sys

import numpy as np

from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.fx.resize import resize


class Getter:
    def __init__(self, url, outfile, res, start_time, duration, fps, adj_timestamps):
        self.url = url
        self.outfile = outfile
        self.res = res

        # in seconds
        self.start_time = start_time
        self.duration = duration

        self.fps = fps
        self.adj_timestamps = adj_timestamps

    def get_video(self):
        """Downloads video from Youtube with given quality."""
        yt = YouTube(self.url)
        videos = yt.streams.filter(
            file_extension="mp4", resolution=self.res)
        assert len(videos) > 0, "Video unavailable."
        videos[0].download(filename=self.outfile)
        print("Download complete.")

    def get_extract(self):
        """Trims videos for specified duration (in seconds)."""
        ffmpeg_extract_subclip("{}.mp4".format(self.outfile), self.start_time,
                               self.start_time + self.duration,
                               targetname="{}-trimmed.mp4".format(self.outfile))

    def get_frames(self):
        """Creates list of frames with timestamps + directory of frames."""
        with open("{}-list.txt".format(self.outfile), "w") as frame_list:
            clip = VideoFileClip("{}-trimmed.mp4".format(self.outfile))
            clip = clip.fx(resize, height=180)
            for i, t in enumerate(np.arange(0, self.duration, 1/self.fps)):
                frame_filename = "{0}/{0}_{1}.png".format(self.outfile, i)
                clip.save_frame(frame_filename, t)
                # ending timestamp in millisecond
                timestamp = (t + 1 / self.fps) * 1000

                if self.adj_timestamps:
                    timestamp *= 3 / self.duration  # 3-second duration
                frame_list.write("{} {}\n".format(
                    frame_filename, int(timestamp)))

    def move_files(self):
        os.remove("{}.mp4".format(self.outfile))
        shutil.move("{}-trimmed.mp4".format(self.outfile), self.outfile)


def main():
    parser = argparse.ArgumentParser(description=""" 
        Extracts frames from Youtube videos.
    """)

    parser.add_argument("url", help="video URL")
    parser.add_argument("title", help="custom video title")

    parser.add_argument("-r", "--res", default="360p", help="video resolution")
    parser.add_argument("-s", "--start", type=float, default=0,
                        help="starting timestamp of the video extract")
    parser.add_argument("-d", "--duration", type=float, default=3,
                        help="duration of the video extract")
    parser.add_argument("-f", "--fps", type=float, default=8,
                        help="frames per second")
    parser.add_argument("-y", "--yt_duration", action='store_true',
                        help="enable adjusting timestamps to fit a 3-second duration")

    args = parser.parse_args()

    url = args.url
    outfile = args.title

    resolution = args.res
    assert resolution in ["1080p", "720p", "480p",
                          "360p", "240p", "144p"], "Invalid resolution."
    start_time = args.start
    assert start_time >= 0, "Invalid start time."
    duration = args.duration
    assert duration >= 0, "Invalid duration."
    fps = args.fps
    assert fps > 0, "Invalid frame rate."
    adj_timestamps = args.yt_duration

    try:
        shutil.rmtree(outfile)
        print("Existing directory removed.")
    except OSError:
        pass
    os.mkdir(outfile)

    getter = Getter(url, outfile, resolution, start_time,
                    duration, fps, adj_timestamps)

    getter.get_video()
    getter.get_extract()
    getter.get_frames()
    getter.move_files()


if __name__ == "__main__":
    main()
