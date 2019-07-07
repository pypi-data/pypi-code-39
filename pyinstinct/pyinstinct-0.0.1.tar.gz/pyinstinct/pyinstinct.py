import sys
import argparse
import random
from pyinstinct import __title__, __description__, __version__

def main(args=[]):
	if '-v' in args or '--version' in args:
		print("%s v%s" % (__title__, __version__))
		return
	parser = argparse.ArgumentParser()
	parser.parse_args(args)
	
	# game starts
	right = 0
	print("")
	for i in range(1,11):
		a = random.randint(1,5)
		while(True):
			b = input("{x}. Guess the number (1-5): ".format(x=i))
			if not str.isdigit(b):
				print("number has to be an integer")
				continue
			b = int(b)
			if not (b>=1 and b<=5):
				print("number should be between 1 and 5")
				continue
			if a == b:
				print("Correct guess!")
				right += 1
			else:
				print("Incorrect guess")
			break
	print("\nYou got {x} guesses right out of 10.\nYour score is {z}".format(x=right, z=(right/10)))
			
				
if __name__ == "__main__":
	main(sys.argv[1:])