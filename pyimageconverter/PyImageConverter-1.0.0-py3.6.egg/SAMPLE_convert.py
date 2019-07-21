import PyImageConverter
import cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
filename = askopenfilename() 

frmt=input("Enter the format (bmp/jpg/png):")
converted_image=PyImageConverter.convert(filename,frmt)
cv2.imshow('Converted Image',converted_image)
cv2.destroyAllWindows()
