import os
from G6_iris_recognition.feature_vec import *
# from sqlalchemy import exc
import  pickle, numpy as np, re
# from datetime import datetime, timedelta, date
# import scipy.misc
# import imutils  # helper functions from pyimagesearch.com\
import threading
# import pyttsx3
# import json
# import time as t
# import hashlib
from scipy.spatial import distance
# from hexhamming import hamming_distance
# from builtins import map as imap
try:
    import itertools.imap as map
except ImportError:
    pass
# from itertools import  imap
import operator


# image = str(input('Insert the image path: '))
def iris_recg(test_db_model_path,image):
        # image = str(input('Insert the image path: '))
        # print("InputValues____",image)
        # print("InputValues____",os.path.exists(image))
        # if os.path.exists(image):
            # print("InputValues____",image)
            data = pickle.loads(open(test_db_model_path, "rb").read())
            # print("[INFO] loading encodings...")
            process_this_frame = True
            iris_encodings = data["encodings"]
            names = data["names"]
            print("+++++++++++++++++")
            threading.Thread(target=match_thread(iris_encodings,names,image)).start()
# print("InputValues____",image)



def match_thread(iris_encodings,names,iris_image):
        iris_encodings_in_image = engroup(iris_image)
        if iris_encodings_in_image !="invalid image":
            match = find_match(iris_encodings, names, iris_encodings_in_image)
            return match
        else:
            print("main3 invalid image") 
            return "unmatch" 



def hamming_check_string(str1,str2):
        hamming_distance_value = 0
        # print("111111",str1,str2)
        # print("111111",map(int, str1),map(int, str2))
        hamming_distance_value=np.sum((np.array(map(int, str1))) != (np.array(map(int, str2))))
        return hamming_distance_value
    # for i in range(5):
        #     # print("__________________",str1,str2)
	# 	hamming_distance_value += int(str1[i] != str2[i])
        # val = (np.linalg.norm(known_faces - face, axis=1))  # <= tolerance)
        # finalVal=0

# def dataaa(str1,str2):
#      print("######",str1,str2)
# def hamming_check_string(str1,str2):
#         hamming_distance_value = 0
#         # hamming_distance_value=np.sum((np.array(map(int, str1))) != (np.array(map(int, str2))))
#      	print("@@@@@@@@@@@",len(str1),len(str2))
#         for i in range(len(str1)):  
#             # print(+_+_+_,i)  
#             #  print("______________",str1[i],str2[i])     
#             # print("######",str1[i],str2[i])
#             # dataaa(int(str1[i]),int(str2[i]))
# 	    	hamming_distance_value += int(str1[i] != str2[i])
#             #  print("__________________",hamming_distance_value)    
#     	return hamming_distance_value



# def compare_iris_encodings(known_iris, iris_encodings_in_image,names):
#     finalVal = 0
#     print("+++++++++++++++++++++++++++++++++",names)
#     for iriss in known_iris:
#         hamming_distance_value=0
#         hamming_distance_value=	hamming_check_string(iriss,iris_encodings_in_image)
#         print("++++++++hamming_distance+++++++++",hamming_distance_value)
#         if hamming_distance_value and hamming_distance_value < 1500:
#             finalVal +=0
#             # print("++++++++hamming_distance1+++++++++",hamming_distance,finalVal)
#         else:
#             finalVal +=100  
#             # print("++++++++hamming_distance2+++++++++",hamming_distance,finalVal)  
        
#         # val = (np.linalg.norm(known_faces - face, axis=1))  # <= tolerance)
#         # finalVal=0
#     return finalVal
def compare_iris_encodings(known_iris, iris_encodings_in_image,name):
    finalVal = 0
    # print("+++++++++++++++++++++++++++++++++")
    hamming_distance_value=0
    hamming_distance=0
    finalVal=0
    finalVal2=0
    for iriss in known_iris:
        hgroup1, vgroup1 = iriss
        
        hgroup2, vgroup2 = iris_encodings_in_image
        # valuation(hgroup1, hgroup2,vgroup1, vgroup2)

        hamming_distance_value = distance_loop1(hgroup1, hgroup2)
        hamming_distance_value += distance_loop2(vgroup1, vgroup2, hamming_distance_value)	
        # hamming_distance = distance_loop(hgroup1, hgroup2)
        # hamming_distance += distance_loop(vgroup1, vgroup2)
        # print("hamming_distance",hamming_distance_value,hamming_distance)
        # hamming_distance += distance_loop2(vgroup1, vgroup2, hamming_distance_value)
	    
        # if hamming_distance_value and hamming_distance_value < 600:
            # finalVal +=0
        # print("----------hamming_distance1------------",name,hamming_distance_value)    
        finalVal2=finalVal2+hamming_distance_value
        finalVal=finalVal+hamming_distance
        # print("----------hamming_distance1------------",hamming_distance_value,finalVal2)
        # else:
        #     finalVal +=100  
        #     print("++++++++hamming_distance2+++++++++",hamming_distance_value,finalVal)  
        
        # val = (np.linalg.norm(known_faces - face, axis=1))  # <= tolerance)
        # finalVal=0
    print("++++++++hamming_distance1+++++++++",name,finalVal2,finalVal)    
    return finalVal2



def valuation(hgroup1, hgroup2,vgroup1, vgroup2):
    distnc1=distance.cdist(hgroup1, hgroup2,'hamming') 
    distnc2=distance.cdist(vgroup1, vgroup2,'hamming')
    value1=np.average(distnc1)
    value2=np.average(distnc2)
    # print("hamming_H",(value1+value2)) 
    # print("hamming_v",value2) 

def distance_loop(str1, str2):
    assert len(str1) == len(str2)
    #ne = str.__ne__  ## this is surprisingly slow
    ne = operator.ne
    return sum(imap(ne, str1, str2))

def distance_loop1(hgroup1, hgroup2):
    

    hamming_distance_value = 0
    for row in range(13):
        # hgroup1[row] is a list of 32 members
        for col in range(32):      
            hamming_distance_value += hamming_check_string(hgroup1[row][col],hgroup2[row][col])

    return hamming_distance_value

def distance_loop2(vgroup1, vgroup2, hamming_distance_value):
    for row in range(36):
        for col in range(9):

            hamming_distance_value += hamming_check_string(vgroup1[row][col],vgroup2[row][col])	
    return hamming_distance_value

def find_match(known_iris, names, iris_encodings_in_image):
        namevalue=""
        matchlist=[]
        for index,iriss in enumerate(known_iris):
            # print("hamming_dist_iriss",index,len(iriss))
            matches = compare_iris_encodings(iriss, iris_encodings_in_image,names[index])
            
            if matches !=0:
                matchlist.append(matches)
            else:
                matchlist.append(2000)    
        # print("totallist",matchlist,names,(matchlist.index(min(matchlist))),matchlist[(matchlist.index(min(matchlist)))])  
        if matchlist[(matchlist.index(min(matchlist)))]<4500:
            namevalue = names[(matchlist.index(min(matchlist)))] 
            print("match",namevalue,matchlist[(matchlist.index(min(matchlist)))]) 
            return namevalue   
        # if namevalue !="":
        #     print("match",namevalue)
        #     return namevalue
        else:
            print("match","unmatch")
            return "unmatch"

# "Test_Images/00r9/01_L.bmp" 
# "Test_Images/00a3/01_L.bmp"
# "Test_Images/00v1/01_L.bmp"
# image="Test_Images/00v1/01_L.bmp"
# if os.path.exists(image):
#     test_list=["Test_Images/00v1/01_L.bmp","Test_Images/00v1/04_L.bmp",
#                "Test_Images/00a3/03_L.bmp","Test_Images/00a3/02_L.bmp",
#                "Test_Images/00r9/02_L.bmp","Test_Images/00r9/06_L.bmp"]
#     data = pickle.loads(open("encodingModel/irisEncodings.pickle", "rb").read())
#     # print("[INFO] loading encodings...")
#     process_this_frame = True
#     iris_encodings = data["encodings"]
#     names = data["names"]
#     for i in test_list:   
#          print("+++++++++++++++++")
#          threading.Thread(target=match_thread(iris_encodings,names,i)).start()
















# from imutils import paths
# import pickle
# import os
# import scipy.misc
# # import numpy as np
# from feature_vec import *



# directory_list = list()
# for root, dirs, files in os.walk(
#         "Test_Image",
#         topdown=False):
#     for name in dirs:
#         directory_list.append(os.path.join(root, name))
        
# print ("directory_list", directory_list)
# iris_names=[]
# iris_name_encodings=[]
# invalid_image=False
# for directory in directory_list:
#     # grab the paths to the input images in our dataset
#     paths_to_images = list(paths.list_files(os.path.join(directory)))
#     # initialize the list of iris_name_encodings and iris_names
#     iris_encodings = []
#     name = directory.split(os.path.sep)[-1]
    
#     print ("++++++++++++++++++++++++++++++++++++++++++++name",name)
#     # Encode the images located in the folder to thier respective numpy arrays
#     invalid_image=False
#     for path_to_image in paths_to_images:
#         data = pickle.loads(open("encodingModel/irisEncodings.pickle", "rb").read())
#         # print("[INFO] loading encodings...")
#         process_this_frame = True
#         iris_encodings = data["encodings"]
#         names = data["names"]
#         # print("+++++++++++++++++")
#         threading.Thread(target=match_thread(iris_encodings,names,path_to_image)).start()
        
# print("finish")       