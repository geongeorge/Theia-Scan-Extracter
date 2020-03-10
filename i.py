import argparse
import os
from extracter.extract import processImage, saveImage,showImage

__author__ = "Geon George"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    """ Main entry point of the app """

    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-s", "--sample", required=False, action='store_true',
                    help="Get a sample image before exporting")

    ap.add_argument("-t", '--threshold', type=int, action='store', required=True,
                    help="Set threshold value [0-255]")

    ap.add_argument("-i", '--image', action='store', required=True,
                    help="Set image file")

    args = vars(ap.parse_args())

    # args['sample'], args['image'] and args['threshold']

    # Image file name (and location)
    thresh = args['threshold']
    image = args['image']
    showSample = args['sample']

    # Check if file exist
    if(not os.path.isfile(image)):
        print("Cannot locate image: "+image)
        return

    # Proceed to process the image
    img = processImage(image,thresh)

    if showSample:
        showImage(img)
    else:
        saveImage(img)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
