import numpy as np
from PIL import Image
from scipy.stats import scoreatpercentile
import sys, getopt, os
from tqdm import tqdm


def contrast(in_path, out_folder, q1, q2):
    image = np.array(Image.open(in_path))
    x, y, z = image.shape if (len(image.shape) == 3) else (image.shape + (0,))

    min, max = scoreatpercentile(image, [q1 * 100, q2 * 100])
    image[image < min] = 0
    image[image > max] = 255

    img = Image.fromarray(image)

    filename = in_path.split("/")[-1]
    out_path = out_folder + "/" + filename
    img.save(out_path)


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "", ["inFolder=", "outFolder=", "q1=", "q2="])
    except getopt.GetoptError:
        print(
            "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --type=<type>"
        )
        sys.exit(2)

    out_folder = None
    q1 = None
    q2 = None
    
    for opt, arg in opts:
        if opt == "--inFolder":
            in_folder = arg
        elif opt == "--outFolder":
            out_folder = arg
        elif opt == "--q1":
            q1 = float(arg)
        elif opt == "--q2":
            q2 = float(arg)
        else:
            print(
                "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --type=<type>"
            )
            sys.exit()

    q1 = q1 or 0.05
    q2 = q2 or 0.95
    out_folder = out_folder or (in_folder + "_contrast")


    files = os.listdir(in_folder)
    files = [
        file for file in files if ".png" in file or ".jpg" in file or ".jpeg" in file
    ]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for file in tqdm(files):
        contrast(in_folder + "/" + file, out_folder, q1, q2)
