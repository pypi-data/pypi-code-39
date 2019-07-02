import cv2
import numpy as np

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
 
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
 
    # return the edged image
    return edged


def adjust_gamma(image, gamma=1.90):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
 
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

def circle_iris_detect(gray):
    kernel = np.ones((3,3), np.uint8)
    # gray = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
    # gray = cv2.resize(gray1, (200, 240)) 
    # print("gray",gray.size,gray.shape)
    img_blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    vis = gray + img_blackhat
    # vis_resized = cv2.resize(vis, (280, 220)) 
    vis_resized = vis
    vis_median = cv2.medianBlur(vis_resized,3)
    vis_gaussian = cv2.GaussianBlur(vis_median,(3,3),0)

    vis_circles = cv2.HoughCircles(vis_gaussian, cv2.HOUGH_GRADIENT,2.3, 20,minRadius=40,maxRadius=100)
    # final1 = cv2.hconcat([gray,img_blackhat,vis])
    centerx=0
    centery=0
    if vis_circles is not None:
        # print("vis_circles",vis_circles,len(vis_circles))
        # convert the (x, y) coordinates and radius of the circles to integers
        vis_circles = np.round(vis_circles[0, :]).astype("int")
 
        # loop over the (x, y) coordinates and radius of the circles
    #     w0,h0 = gray.shape
        for (x, y, r) in vis_circles:
                mask = np.zeros((gray.shape[0],gray.shape[1]),dtype=np.uint8)   ##
                cv2.circle(mask,(x,y),r,(255,255,255),-1,0,0)                   ##
    #             out2=cv2.circle(gray,(x,y),r,(255,255,255),-1,8,0)
    #             cv2.circle(gray, (x, y), r, (0, 255, 0), 4)
                # cv2.imwrite("image.jpg",mask)
    ##             out = gray*mask
    ##             white = 255-out
                result = np.bitwise_and(gray,mask)                              ##
                output_result = result[y-r:y+r,x-r:x+r]   
        params = locate(output_result)
        return params
    else:
        print("vis_circles not found")


















    # kernel = np.ones((3,3), np.uint8)

    # # gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    # # gray = cv2.resize(gray1, (200, 240)) 
    # # print("gray",gray.size,gray.shape)
    # img_blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    # vis = gray + img_blackhat
    # # vis_resized = cv2.resize(vis, (280, 220)) 
    # vis_resized = vis
    # # vis_median = cv2.medianBlur(vis_resized,3)
    # vis_gaussian = cv2.GaussianBlur(vis_resized,(3,3),0)
    # # vis_canny = auto_canny(vis_gaussian)
    # # vis_gamma = adjust_gamma(vis_canny)
    # # detect circles in the image
    # # vis_circles = cv2.HoughCircles(vis_gamma, cv2.HOUGH_GRADIENT, 1.2, 100)
    # vis_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,2.3, 20,minRadius=20,maxRadius=100)
    # # final1 = cv2.hconcat([gray,img_blackhat,vis])
    # # final2 = cv2.hconcat([vis_resized,vis_median,vis_gaussian,vis_canny,vis_gamma])
    # # final = cv2.vconcat([final1,final2])
    # #--- Resizing the logo to the shape of room image ---
    # # img_blackhat_resize = cv2.resize(img_blackhat, (rgb.shape[1], rgb.shape[0]))
    # # vis = np.column_stack((gray, img_blackhat))

    # # cv2.imshow('rgb->gray->img_blackhat->vis->vis_resized->vis_median', final1)
    # # cv2.imshow('vis_resized->vis_median->vis_gaussian->vis_canny->vis_gamma',final2)

    # # ensure at least some circles were found
    # centerx=0
    # centery=0
    # if vis_circles is not None:
    #     print("vis_circles",vis_circles,len(vis_circles))
    # 	# convert the (x, y) coordinates and radius of the circles to integers
    # 	vis_circles = np.round(vis_circles[0, :]).astype("int")
 
    # 	# loop over the (x, y) coordinates and radius of the circles
    # #     w0,h0 = gray.shape
    # 	for (x, y, r) in vis_circles:
    #             mask = np.zeros((gray.shape[0],gray.shape[1]),dtype=np.uint8)   ##
    #             cv2.circle(mask,(x,y),r,(255,255,255),-1,0,0)                   ##

    # #             out2=cv2.circle(gray,(x,y),r,(255,255,255),-1,8,0)
    # #             cv2.circle(gray, (x, y), r, (0, 255, 0), 4)
    #             #cv2.imwrite(argv[2],mask)
    # ##             out = gray*mask
    # ##             white = 255-out

    #             result = np.bitwise_and(gray,mask)                              ##
    #             output_result = result[y-r:y+r,x-r:x+r]
 
    # 	# iris=np.where((output_result>50) & (output_result < 120),1.,0.)
    # # 	low_values_flags =  (output_result < 50)& (output_result < 120)  # Where values are low
    # # 	output_result[low_values_flags] = 0  # All low values set to 0    

    # 	# print("result=>shape",result.shape,output_result.shape)
    # 	# cv2.imshow("output_crop_cimg", gray)
    # 	# cv2.imshow("output_crop_cimg1", output_result)
    # 	# cv2.imshow("output_crop_cimg1", iris)
    # 	# cv2.waitKey(0)

    # 	params = locate(output_result)
    #     print("params",params)
    # 	return params
    # else:
    #     print("vis_circles not found")
