import numpy as np
from PIL import Image
from scipy.ndimage.interpolation import zoom
import sys, getopt, os
from tqdm import tqdm

def image_zoom(in_path, out_folder, zoom_scale, order = 3):
    image = np.array(Image.open(in_path))
    x, y, z = image.shape if (len(image.shape) == 3) else (image.shape + (0,))
    x = int(round(x * zoom_scale))
    y = int(round(y * zoom_scale))

    if z > 0:
        img_rgb = np.zeros((x, y, z), dtype='uint8')

        for i in range(0, z):
            img_rgb[:, :, i] = zoom(np.array(image)[:, :, i], zoom=zoom_scale, order=order)
    else:
        img_rgb = np.zeros((x, y), dtype='uint8')
        img_rgb[:, :] = zoom(np.array(image)[:, :], zoom=zoom_scale, order=order)

    img = Image.fromarray(img_rgb)

    filename = in_path.split('/')[-1]
    out_path = out_folder + '/' + filename
    img.save(out_path)


if __name__ == '__main__':
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "" ,["inFolder=", "outFolder=", "scale=", "order="])
    except getopt.GetoptError:
        print('zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --scale=<zoomScale>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--inFolder':
            in_folder = arg
        elif opt == '--outFolder':
            out_folder = arg
        elif opt == '--scale':
            zoom_scale = float(arg)
        elif opt == '--order':
            order = int(arg)
        else:
            print('zoom.py --inFolder=<inputFolder> --outFolder=<outputFolder> --scale=<zoomScale>')
            sys.exit()
    
    files = os.listdir(in_folder)
    files = [file for file in files if '.png' in file or '.jpg' in file or '.jpeg' in file]
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for file in tqdm(files):
        image_zoom(in_folder + '/' + file, out_folder, zoom_scale, order)