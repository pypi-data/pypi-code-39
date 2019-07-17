import csv
import time
from PIL import Image
from skimage import measure
import numpy as np
import argparse
import logging
import os
from os import path

# In order to avoid for test cases to generate multiple loggers,
# maintaining a dict
loggers = {}

def log_setup(fileName):
	"""
	Set up logging configuration
	"""
	global loggers
	if loggers.get(os.path.basename(fileName)):
		return loggers.get(os.path.basename(fileName))
	else :
		logger = logging.getLogger(os.path.basename(fileName))
		logger.setLevel(logging.INFO)
		sh = logging.StreamHandler()
		sh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
		logger.addHandler(sh)
		loggers[os.path.basename(fileName)] = logger
		return logger

def parse_args():
    """Parses and returns the script arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', '-f', required=True, help='Absolute path to input containing images file names in csv format')
    parser.add_argument('--dir', '-d', required=True, help='Absolute path to image directory contaning all images')
    args = parser.parse_args()

    return args


def compare_images(imageA, imageB):
	# structural similarity index for the images
	s = measure.compare_ssim(imageA, imageB) 
	return '%.2f'%((1-s))
	

def row_writer(row1, row2, similarity, elapsed, writer):
	if writer is None:
		raise IOError("Found output csv writer empty")
	fields = [row1, row2, similarity, elapsed]
	try:
		writer.writerow(fields)
	except Exception as ex:
		raise Exception(ex)

def drcompare_main(inputCsvFile, dirPath):

	logger = log_setup(os.path.basename(__file__))
	
	absOutputFilePath = dirPath + "/output.csv"
	logger.info("Absolute output path: "+ absOutputFilePath)

	logger.info("Input path: "+ inputCsvFile)

	# Open input file reader
	try:
		inputFile = open(inputCsvFile,mode='rt')
	except Exception as err:
		logger.error("Failed to open input file: " + str(err))
		return
	freader = csv.reader(inputFile)

	# Remove the output file if it already exists		
	if path.exists(absOutputFilePath):
		os.remove(absOutputFilePath)
		logger.debug("Removed output.csv at " + absOutputFilePath)

	# Open output file writer
	try:		
		outputFile = open(absOutputFilePath,'a', newline='')
	except Exception as err:
		logger.error("Failed to open output file: " + str(err))
		return
	writer = csv.writer(outputFile)

	# Write down the header row in the output file
	try:	
		row_writer("image1","image2","similar","elapsed", writer)
	except Exception as err:
		logger.warning("Failed to write row in output file: " + str(err))

	# Traverse through all input rows and process them		
	for row in freader:
		logger.debug(row)
				
		# Ignore the first row in imput csv
		if row[0] == "image1" and row[1] == "image2":
			continue

		# Ignore if any one of the image path is missing input file
		if row[0] == "" or row[1] == "":
			try:
				row_writer(str(row[0]), str(row[1]),str(-1),str(-1), writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))
			logger.warning("Found missing data in input csv row :" + str(row))
			continue

		# Build the image paths using given directory paths
		imagefile1 = dirPath + "/"+row[0]
		imagefile2 = dirPath + "/"+row[1]

		# Skip the row if anyone of the given image doesn't exist
		if (not os.path.exists(imagefile1)) or (not os.path.exists(imagefile2)):
			try:
				row_writer(str(row[0]), str(row[1]),str(-1),str(-1),writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))
			logger.warning("Found invalid file path(s) in input csv row :" + str(row))
			continue
				
		# If two paths point to the same file, set the value to represent same
		if imagefile1 == imagefile2:
			try:
				row_writer(str(row[0]), str(row[1]),str(0),str(0),writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))
			logger.warning("The images pair appears to be pointing to the same file : (1) " + imagefile1 + "; (2) " + imagefile2 )
			continue

		# Read the image pair		
		image1 = []
		image2 = []
		try:
			image1 = np.array(Image.open(imagefile1).convert('L'))
			image2 = np.array(Image.open(imagefile2).convert('L'))
		except Exception as err:
			logger.warning("Failed to open path as image: " + str(err))
			try:
				row_writer(str(row[0]), str(row[1]),str(-1),str(-1),writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))
			continue

		# Process them only if they are of same size
		if image1.size == image2.size:
			# Record the start time
			start = time.time()
			s = compare_images(image1, image2)
			logger.debug("SSIM : "+str(s))
			# Record the end time
			end = time.time()
			time_elapsed = '%.3f'%(end - start)
			logger.debug("Elapsed : "+str(time_elapsed))

			# Build the row and write to the output file
			try:
				row_writer(str(row[0]), str(row[1]),str(s),str(time_elapsed),writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))
		else:
			# Since the image sizes are different, consider them different images
			d = 1 
			time_elapsed =0 
			try:
				row_writer(str(row[0]), str(row[1]),str(d),str(time_elapsed),writer)
			except Exception as err:
				logger.warning("Failed to write row in output file: " + str(err))	
	# Close output and input files
	outputFile.close()
	inputFile.close()
	logger.debug("Closed output file descriptor")
	return absOutputFilePath

if __name__ == '__main__':
    args = parse_args()
    drcompare_main(args.file, args.dir)
