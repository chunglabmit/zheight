import argparse
import glob
import matplotlib
from matplotlib import pyplot
import matplotlib.figure
import os
import numpy as np
from skimage.filters import threshold_otsu
import scipy.ndimage as ndi
import tifffile

pyplot.ioff()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack",
                        help="Glob expression for the stack of images to be "
                        "loaded. Example: \"/path/to/img*.tif\"",
                        required=True)
    parser.add_argument("--output",
                        help="The output image file to be generated.",
                        required=True)
    parser.add_argument("--sigma",
                        help="The smoothing sigma for blurring the image",
                        default=20,
                        type=float)
    parser.add_argument("--multiplier",
                        help="Multiply the automatic threshold by this "
                        "number to get the actual threshold used",
                        default=.8,
                        type=float)
    parser.add_argument("--min-threshold",
                        help="The minimum allowed threshold (in case the "
                             "image is all black).",
                        default=15,
                        type=int)
    parser.add_argument("--output-array", 
                        help="Path to the output numpy array of the contour map.",
                        default=None,
                        type=str)
    return parser.parse_args()


def zmask(stack, z, sigma, tmult, min_threshold):
    fimg = stack[z].astype(np.float32)
    fimg = fimg
    simg = ndi.gaussian_filter(fimg, sigma)
    thresh = max(threshold_otsu(stack) * tmult, min_threshold)
    return simg > thresh

def calculate_rms(carray):
    return np.sqrt(np.sum(np.square(carray - np.mean(carray)))/np.prod(carray.shape))

def main():
    args = parse_arguments()
    stack = np.array([tifffile.imread(_) for _ in glob.glob(args.stack)])
    # if RGB, pick the brightest channel per pixel
    if stack.ndim == 4:
        stack = np.max(stack, 3)
    first_z = np.zeros((stack.shape[1], stack.shape[2]), np.uint8)
    for z in range(stack.shape[0]):
        zm = zmask(stack, z, args.sigma, args.multiplier, args.min_threshold)
        first_z[(first_z == 0) & zm] = z + 1
    if args.output_array is not None:
        np.save(args.output_array, first_z)
    rms = calculate_rms(first_z)
    print('RMS:', rms) 
    figure = pyplot.figure(figsize=(10, 8))
    ax = figure.gca()
    ax.set_ylim(stack.shape[1], 0)
    ax.axis("off")
    mimg = ax.imshow(first_z, cmap='jet')
    figure.colorbar(mimg)
    contour = ax.contour(first_z, levels=np.unique(first_z)[1:])
    ax.clabel(contour, inline=1, fontsize=10, fmt="%d")
    pyplot.savefig(args.output)
    pyplot.close()


if __name__=="__main__":
    main()
