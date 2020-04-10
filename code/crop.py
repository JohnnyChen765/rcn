import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
import sys, getopt, os
from tqdm import tqdm


def image_crop(in_path, out_folder, n_crop=4):
    
    image = np.array(Image.open(in_path))
    x, y, z = image.shape if (len(image.shape) == 3) else (image.shape + (0,))

    n_crop_x = int(np.sqrt(n_crop))

    ws_x = int(round(x / n_crop_x))
    ws_y = int(round(y / n_crop_x))

    for i in range(0, x, ws_x):
        for j in range(0, y, ws_y):
            if z > 0:
                img_crop = image[i : i + ws_x, j : j + ws_y, :]

            else:
                img_crop = image[i : i + ws_x, j : j + ws_y]

            img = Image.fromarray(img_crop)
            filename = in_path.split("/")[-1]

            name, extension = filename.split(".")
            out_path = (
                out_folder
                + "/"
                + name
                + "_"
                + str(int(i / ws_x))
                + "_"
                + str(int(j / ws_y))
                + "."
                + extension
            )

            img.save(out_path)


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "", ["inFolder=", "outFolder=", "crop="])
    except getopt.GetoptError:
        print(
            "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --crop=<crop>"
        )
        sys.exit(2)

    out_folder = None

    for opt, arg in opts:
        if opt == "--inFolder":
            in_folder = arg
        elif opt == "--outFolder":
            out_folder = arg
        elif opt == "--crop":
            n_crop = int(arg)
        else:
            print(
                "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --crop=<crop>"
            )
            sys.exit()

    out_folder = out_folder or (in_folder + "_cropped_" + str(n_crop))

    files = os.listdir(in_folder)
    files = [
        file for file in files if ".png" in file or ".jpg" in file or ".jpeg" in file
    ]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for file in tqdm(files):
        image_crop(in_folder + "/" + file, out_folder, n_crop)
