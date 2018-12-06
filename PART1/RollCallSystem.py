import numpy as np
import cv2
import wx
from PIL import Image
import os
import copy

#import Interface.rollCallStart

class RollCallSystem:
    
    class_obj = None
    path = 'dataset'
    detector = None
    recognizer = None

    def __init__(self, classObject):
        self.class_obj = classObject

        #Interface.rollCallStart.MyFrame1.__init__(self, None)
        self.detector = cv2.CascadeClassifier('cascades/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        faces,ids = self.getImagesAndLabels(self.path)
        self.recognizer.train(faces, np.array(ids))
        # Save the model into trainer/trainer.yml
        #self.recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
        self.recognizer.save('trainer/trainer.yml')
        # Print the numer of faces trained and end program
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))


        self.recognizer.read('trainer/trainer.yml')
        font = cv2.FONT_HERSHEY_SIMPLEX
        #iniciate id counter
        id = 0
        # names related to ids: example ==> Marcelo: id=1,  etc
        names = copy.deepcopy(classObject.students)
        names.insert(0, "None")
        #print(len(names))

        cap = cv2.VideoCapture(0)
        cap.set(3,640) # set Width
        cap.set(4,480) # set Height
        # Define min window size to be recognized as a face
        minW = 0.1*cap.get(3)
        minH = 0.1*cap.get(4)
        while True:
            ret, img = cap.read()
            #img = cv2.flip(img, -1)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(
                gray,     
                scaleFactor=1.2,
                minNeighbors=5,     
                minSize = (int(minW), int(minH)),
            )
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                id, confidence = self.recognizer.predict(gray[y:y+h,x:x+w])

                # Check if confidence is less them 100 ==> "0" is perfect match 
                if (confidence < 100):

                    if classObject.students[id-1].isAbsent(): #None value skews the order
                        classObject.students[id-1].set_present()
                        print(classObject.students[id-1].getName() + " is present.")

                    id = names[id].getName()
                    confidence = "  {0}%".format(round(100 - confidence))
                else:
                    id = "unknown"
                    confidence = "  {0}%".format(round(100 - confidence))
                
                cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
                cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 

            cv2.imshow('camera',img)
            k = cv2.waitKey(30) & 0xff
            if k == 27: # press 'ESC' to quit
                self.class_obj.printSummary()
                break
        cap.release()
        cv2.destroyAllWindows()
    
    def getImagesAndLabels(self, path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            if imagePath == "dataset/.DS_Store":
                continue
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids

