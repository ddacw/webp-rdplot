#!/usr/bin/env python

import multiprocessing
import os
import sys
import subprocess

import matplotlib.pyplot as plt


def run_compare(list_filename):
    print(list_filename)
    cmd = "./thumbnailer_compare {}".format(list_filename)
    comparison = subprocess.run(cmd, shell=True, capture_output=True)
    lines = (comparison.stdout).decode("utf-8").strip().split("\n")
    data = []
    for line in lines:
        data.append([float(x) for x in line.split(" ")])
    return [method_stat for method_stat in data]  # mean


def main():
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    data = pool.map(
        run_compare, [filename for filename in os.listdir()
                      if filename.lower().endswith("list.txt")])
    pool.close()

    I = len(data)
    J = len(data[0])
    K = len(data[0][0])
    methods_stat = [[[None for _ in range(I)]
                     for _ in range(J)]
                    for _ in range(K)]

    for i in range(I):
        for j in range(J):
            for k in range(K):
                methods_stat[k][j][i] = data[i][j][k]

    fig, axs = plt.subplots(2, 2, sharey=True)
    titles = ("max_dec", "max_inc", "mean", "median")
    colors = ("r", "g", "black", "black")
    fig.suptitle("thumbnail_compare")
    for i, title in enumerate(titles):
        x = (i >> 1) & 1
        y = i & 1
        axs[x, y].axhline(y=0, color="lightgray", linestyle="-")
        axs[x, y].boxplot(methods_stat[i], showfliers=False)
        axs[x, y].set_title(title, color=colors[i])

    plt.savefig("Stat.png")
    plt.show()


if __name__ == "__main__":
    main()
