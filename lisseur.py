import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
from cv2 import bilateralFilter
from help import bilateral_filtering
import sys, getopt, os
from tqdm import tqdm


def lissage(in_path, out_folder, type, sigma = 3, sigmaColor= 20):
    image = np.array(Image.open(in_path))
    x, y, z = image.shape if (len(image.shape) == 3) else (image.shape + (0,))

    if type == "bilateral":
        filtered = bilateralFilter(image, d=20, sigmaColor=sigmaColor, sigmaSpace= 10)
    else:
        filtered = gaussian_filter(image, sigma=sigma)

    img = Image.fromarray(filtered)

    filename = in_path.split("/")[-1]
    out_path = out_folder + "/" + filename
    img.save(out_path)


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "", ["inFolder=", "outFolder=", "type=", "sigma=", "sigmaColor="])
    except getopt.GetoptError:
        print(
            "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --type=<type>"
        )
        sys.exit(2)

    out_folder = None
    type = None
    sigma = None
    sigmaColor = None
    
    for opt, arg in opts:
        if opt == "--inFolder":
            in_folder = arg
        elif opt == "--outFolder":
            out_folder = arg
        elif opt == "--type":
            type = arg
        elif opt == "--sigma":
            sigma = float(arg)
        elif opt == "--sigmaColor":
            sigmaColor = float(arg)
        else:
            print(
                "zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --type=<type>"
            )
            sys.exit()

    type = type or "gaussian"
    sigma = sigma or 3
    sigmaColor = sigmaColor or 20
    out_folder = out_folder or (in_folder + "_lisse_" + type)

    # if type == "gaussian":
    #     out_folder += str(sigma)

    files = os.listdir(in_folder)
    files = [
        file for file in files if ".png" in file or ".jpg" in file or ".jpeg" in file
    ]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for file in tqdm(files):
        lissage(in_folder + "/" + file, out_folder, type, sigma=sigma, sigmaColor=sigmaColor)
