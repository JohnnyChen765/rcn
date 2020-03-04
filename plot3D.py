import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_real_plane_parameters(params):
    A, B, C = params
    # if (a,b,c) is a unit verctor plane params, and d plane offset,
    # and (A,B,C) = (a,b,c) * d
    # we can extract (a,b,c,d)

    d = np.sqrt(A ** 2 + B ** 2 + C ** 2)
    return (A / d, B / d, C / d, d)


def plot_plane_params(params, ax):
    a, b, c, d = params
    x = np.linspace(-3, 3, 20)
    y = np.linspace(-3, 3, 20)
    X, Y = np.meshgrid(x, y)
    Z = (d - a * X - b * Y) / c

    ax.plot_surface(X, Z, Y)


def pipeline(list_params):
    list_real_params = [get_real_plane_parameters(params) for params in list_params]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    plt.xlabel("x")
    plt.ylabel("y")
    for params in list_real_params:
        plot_plane_params(params, ax)
    # ax.view_init(elev=1)
    plt.show()


def pipeline_compare(list_params1, list_params2):
    list_real_params1 = [get_real_plane_parameters(params) for params in list_params1]
    list_real_params2 = [get_real_plane_parameters(params) for params in list_params2]
    fig = plt.figure()
    ax = fig.add_subplot(121, projection="3d")
    ax2 = fig.add_subplot(122, projection="3d")
    for params in list_real_params1:
        plot_plane_params(params, ax)
    for params in list_real_params2:
        plot_plane_params(params, ax2)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


def print_info(arr1, arr2):
    if arr1 is not None:
        print(f"path1 plane params is {arr1}")
        print(f"path1 plane offset is {[np.sqrt(np.sum(arr ** 2)) for arr in arr1]}")
    if arr2 is not None:
        print(f"path2 plane params is {arr2}")
        print(f"path2 plane offset is {[np.sqrt(np.sum(arr ** 2)) for arr in arr2]}")


import sys, getopt, os
from tqdm import tqdm

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "", ["path=", "path2=", "print"])
    except getopt.GetoptError:
        print("zoom.py --path=<path> --path2=<path2>")
        sys.exit(2)

    arr1 = None
    arr2 = None
    print_arg = False
    for opt, arg in opts:
        if opt == "--path":
            arr1 = np.load(arg)
        elif opt == "--path2":
            arr2 = np.load(arg)
        elif opt == "--print":
            print_arg = True
        else:
            print("zoom.py --path=<path> --path2=<path2>")

            sys.exit()

    if print_arg:
        print_info(arr1, arr2)

    if arr2 is not None:
        pipeline_compare(arr1, arr2)
    else:
        pipeline(arr1)

