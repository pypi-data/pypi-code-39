from G6_iris_recognition.locate2 import *
from G6_iris_recognition.circle_iris_operation import *
from math import sin, cos, radians

def rectangle(fname):
    try:  
      # img1 = bnw(fname)
      # img = img1[22:,22:]
      # img_out = circle_iris_operation(fname)
      rgb = cv2.imread(fname)
      img_out = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)
      params = locate(img_out)


      Ri = params[0] # Inner (pupil) radius
      Ro = params[1] # Outer (iris) radius
      y,x = params[2] # center coordinates
      x -= 10
      y -= 10

      H = int(Ro - Ri)
      W = 360
      newmap = zeros([H,W])
      # print("+++++++++++++++++++++++++++++++++++++++++++++++++",Ro,Ri,H,W)
      for r in range(H):
        for c in range(W):
                # print("@@@@@111111111111111",int(x + (Ri + r) * cos(radians(c))),int(y + (Ri + r) * sin(radians(c))))
                mapped_point_col = int(x + (Ri + r) * cos(radians(c)))
                mapped_point_row = int(y + (Ri + r) * sin(radians(c)))
                dot = img_out[min([img_out.shape[0]-1,mapped_point_row]), min([img_out.shape[1]-1,mapped_point_col])]
                newmap[r,c] = dot
      # print("newmap[5:44,:]",len(newmap[5:44,:]))
      if len(newmap[5:44,:]) !=0:
          return newmap[5:44,:]  
      else:
          print("rectangle expression1")  
          return "invalid image"
    except Exception as e:
      print("rectangle expression2",e)        
      return "invalid image"