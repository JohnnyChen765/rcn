import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from scipy.ndimage.interpolation import zoom

folder = "./custom_images"
zoom_int = 4
# Read Images 
img = mpimg.imread(folder + '/' + 'test2.jpg') 
zoomed = zoom(img, zoom_int, output=None, order=3, mode='constant', cval=0.0, prefilter=True)
import ipdb; ipdb.set_trace()
# Output Images 
plt.imshow(img) 