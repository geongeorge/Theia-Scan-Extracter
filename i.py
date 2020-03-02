import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-s", "--sample", required = False, action='store_true',
	help = "Get a sample image before exporting")


ap.add_argument("-t", '--threshold', type=int, action='store',required = True,
	help = "Set threshold value [0-255]")

args = vars(ap.parse_args())

# args['sample'] and args['threshold']