
from Cerebro.interface import process_video as pi
import cv2 
import Cerebro as c

def main():
	c.set_cwd("C:/Users/manar/Desktop/Cerebro/Cerebro")
	pi.detect_video_emotions_with_tracking("c.mp4","c_out_tracking.mp4",50, verbose=True)
	
	
if __name__== "__main__":
  main()