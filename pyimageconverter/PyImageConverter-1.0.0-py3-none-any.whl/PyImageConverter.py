import cv2
def convert(filename,frmt):
    string=filename.split('.')
    img_read=cv2.imread(filename)
    if(string[1]==frmt):
        return "Already in Prescribed Format"
    else:
        return cv2.imwrite(string[0]+"."+frmt,img_read)
        
    
