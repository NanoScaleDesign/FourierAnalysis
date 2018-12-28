#!/usr/bin/env python3

from PIL import Image
import numpy as np

def main():
    # Read in image
    data = read_image('kyudai.png')

    # Calculate 2D FFT
    fft = calculate_fft(data)
    fft = shift_fft(fft)

    # Modify FFT
    fft = modify_fft(fft) # Your code here

    # Calculate absolute values and scale between 1 and 256 to fit in greyscale colour range
    fftabs = convert_abs(fft)

    # Save FFT image by placing data into an array with a suitable format for PIL
    save_image(data,fftabs,'kyudai.fft.png',logscale=True)

    # Calculate inverse 2D FFT
    ifftdata = ifft(fft)
    invfftabs = convert_abs(ifftdata)
    save_image(data,invfftabs,'kyudai.fft.ifft.png',logscale=False)

    return


def read_image(fname):
    """
    Read a greyscale image.
    Each pixel is a number between 1 and 255 where 255 is brightest.
    If generating images in GIMP, save the image under 8bpc GRAY format.
    You may also wish to re-size the canvas to 256x256 pixels.
    """

    data = np.array(Image.open(fname))

    return data


def shift_fft(fft):
    """
    Shift the zero-frequencies to the centre of the 2D fft
    """

    fft = np.fft.fftshift(fft)
    return fft


def modify_fft(fft):
    """
    Modify the image in frequency space

    Note: The FFT is displayed using a log scale due to the wide range of values.
    Thus, if you set any value to zero, this will raise an error.
    Instead then, use a very small number (eg: 1e-14) to avoid the error.
    """

    # Your code here
    
    return fft


def calculate_fft(data):
    """
    Calculates 2D FFT
    """
    fft = np.fft.fft2(data)

    return fft


def convert_abs(fft):
    """
    Convert a given complex 2D fft to absolute values only, and scale between 1 .. 256.
    Scaling is required because greyscale images require pixel values in this range.
    """

    fftabs = np.absolute(fft)
    fftabs = 256. * fftabs / fftabs.max()
    return fftabs


def save_image(data,fftabs,fname,logscale):
    """
    Saves fftabs using image_holder as a format specifier
    """

    # First prepare the Image format array
    image_holder = np.zeros_like(data)

    # Next, write brightness information
    if logscale:
        image_holder[...] = np.log(fftabs)
    else:
        image_holder[...] = fftabs

    fftimg = Image.fromarray(image_holder)
    fftimg.save(fname)

    return


def ifft(fft):
    """
    Calculate inverse 2D DFT 
    """

    fftinv = np.zeros_like(fft)
    fftinv[...] = np.fft.ifft2(fft)

    return fftinv


if __name__ == '__main__':
    main()
