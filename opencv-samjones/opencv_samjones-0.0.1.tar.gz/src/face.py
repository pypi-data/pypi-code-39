def faces():
    import numpy as np
    import cv2
    import pickle
    cascade  = input('Cascade File:')
    #src/cascades/data/haarcascade_frontalface_alt2.xml
    face_cascade=cv2.CascadeClassifier(cascade)
    #eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    #smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #recognizer.read("./recognizers/mtx.yml")

    #labels = {"person_name": 1}
    #with open("pickles/face-labels.pickle", 'rb') as f:
        #og_labels = pickle.load(f)
        #labels = {v:k for k,v in og_labels.items()}

    cap=cv2.VideoCapture(0)
    while(True):
        ret,frame = cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,scaleFactor=1.5,minNeighbors=5)
        for (x,y,w,h) in faces:
            print(x,y,w,h)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            #id_, conf = recognizer.predict(roi_gray)
            '''if conf>=45 and conf <= 85:
                #print(id_)
                print(labels[id_])
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 255, 255)
                stroke = 2'''
                #cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)
            img_item = "7.png"
            cv2.imwrite(img_item, roi_color)
            img_item = "my-image.png"
            cv2.imwrite(img_item,roi_gray)
            color=(255, 0, 0) #BGR 0-255 
            stroke=2
            end_cord_x=x + w
            end_cord_y=y + h
            cv2.rectangle(frame,(x, y),(end_cord_x, end_cord_y),color,stroke)
            sub_face = frame[y:y+h, x:x+w]
            sub_face = cv2.GaussianBlur(sub_face,(23, 23), 30)
            frame[y:y+sub_face.shape[0], x:x+sub_face.shape[1]] = sub_face
            face_file_name ="samjones.jpg"
            cv2.imwrite(face_file_name, frame)
            '''subitems = smile_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in subitems:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)'''
        cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()