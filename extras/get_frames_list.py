#!/usr/bin/env python

import os
import shutil
import sys

from get_frames import Getter


def main():
    filename = sys.argv[1]
    with open(filename, "r") as url_list:
        for i, url in enumerate(url_list):
            outfile = "vid" + str(i)
            print(outfile)
            try:
                shutil.rmtree(outfile)
                print("Existing directory removed.")
            except OSError:
                pass
            # Getter(url, outfile, resolution, start_time,
            #        duration, fps, adj_timestamps)
            getter = Getter(url, outfile, "360p", 1,
                            6, 4, True)
            try:
                os.mkdir(outfile)
                getter.get_video()
                getter.get_extract()
                getter.get_frames()
                getter.move_files()
            except KeyError:
                os.rmdir(outfile)


if __name__ == "__main__":
    main()
