import cv2

def as_cv2_bgr(img_path):
    '''
    Loads Imge as CV2 BGR format
    '''
    img = cv2.imread(img_path)
    return img