# print("For going to the virtualenv : source rcn/bin/activate")
# print("python evaluate.py --methods=f --suffix=warping_refine --dataset=inference --customDataFolder=example_images")
import cv2
import numpy as np
from PIL import Image
from scipy.signal import convolve2d


def gaussian_matrix(size, sigma = 3):
    matrix = np.zeros((size, size))
    origin_x = (size - 1) / 2
    origin_y = (size - 1) / 2
    for x in range(0, size):
        for y in range(0, size):
            u = x - origin_x
            v = y - origin_y
            h = 1 / (2 * np.pi * sigma * sigma) * np.exp(-(u*u + v*v)/(2 * sigma * sigma))
            matrix[x, y] = h
    return matrix
                    

def bilateral_filtering(img, kernel_size=3, sigma = 3):
    """
    The Bilateral Filtering.
    
    Inputs:
        img              The input image
        neigh            The neighborhoud of pixels
                         
    Outputs: 
        bilateral_img    A smoothed image
    """
    
    # Write the function here
    gaussian_kernel = gaussian_matrix(kernel_size, sigma=sigma)
    img_x, img_y = img.shape
    
    bilateral_img_size = (img_x + kernel_size - 1, img_y + kernel_size - 1)
    bilateral_filtered_img = np.zeros(bilateral_img_size)
    
    padded_img_x, padded_img_y = bilateral_img_size
    padded_img = np.zeros(bilateral_img_size)
    
    padded_img[0:img_x, 0:img_y] = img
                          
    for x in range(bilateral_img_size[0]):
        filtered_pixel = 0
        for y in range(bilateral_img_size[1]):
            
            # ex [ x-2, x - 1, x]
            img_cursor_x = np.array(
                range(x - kernel_size + 1, x + 1)
            ) % padded_img_x
            img_cursor_y = np.array(
                range(y - kernel_size + 1, y + 1)
            ) % padded_img_y

            img_cursor = padded_img[img_cursor_x, :][:, img_cursor_y]
            
            # substract center value to all the image, then inverse
            diff_img = padded_img[x, y] - img_cursor 
            G_sigma_R = 1 / np.sqrt(2 * np.pi * sigma ** 2) * np.exp(-1/2 * (diff_img /sigma) ** 2)
            
            bilateral_kernel = G_sigma_R * gaussian_kernel
            W_p = np.sum(bilateral_kernel)
            
            filtered_pixel = 1/W_p * np.sum(bilateral_kernel * np.flip(img_cursor))
            bilateral_filtered_img[x, y] = filtered_pixel
    
    # Return the result
    return bilateral_filtered_img