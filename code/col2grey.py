import numpy as np
from PIL import Image
import sys, getopt, os
from tqdm import tqdm


def greyscale(in_path, out_folder):
    image = np.array(Image.open(in_path), dtype='uint32')
    image = np.array((image[:, :, 0] + image[:, :, 1] + image[:, :, 2]) / 3, dtype='uint8')
    img = np.zeros((image.shape[0], image.shape[1], 3), dtype='uint8')
    img[:, :, 0] = image
    img[:, :, 1] = image
    img[:, :, 2] = image

    img = Image.fromarray(img)

    filename = in_path.split('/')[-1]
    out_path = out_folder + '/' + filename
    img.save(out_path)


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "", ["inFolder=", "outFolder=", "scale="])
    except getopt.GetoptError:
        print('zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--inFolder':
            in_folder = arg
        elif opt == '--outFolder':
            out_folder = arg
        else:
            print('zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder>')
            sys.exit()

    files = os.listdir(in_folder)
    files = [file for file in files if '.png' in file or '.jpg' in file or '.jpeg' in file]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for file in tqdm(files):
        greyscale(in_folder + '/' + file, out_folder)