import numpy as np
import cv2
import wx
import Interface.rollCallStart

class Class:

    name = None
    professor = None
    students = []

    def __init__(self, name, professor):
        self.name = name
        self.professor = professor

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getProfessor(self):
        return self.professor

    def setProfessor(self, professor):
        self.professor = professor

    def getStudents(self):
        return self.students

    def addStudent(self, student):
        return self.students.append(student)
        
    def removeStudent(self, student):

        for i in range(len(self.students)):
            if (student.getName() == self.students[i].getName()):
                return self.students.pop(i)
                
    def printSummary(self):
        print("You are currently reading the summary for " + self.name + " taught by " + self.professor + ".")
        print("There are " + str(len(self.students)) + " student(s) in this class.")
        print("\nHere are the students in this class:")
        print("_______________\n")

        for i in range(len(self.students)):
            print(str(i+1) + ". " + self.students[i].getName())

        print("\n_______________")
        print("\nEnd of class summary.")

        

class Student:

    name = None
    absent = True
    sample = []
 
    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def isAbsent(self):
        return self.absent

    def set_present(self):
        self.absent = False

    def set_absent(self):
        self.absent = True

class RollCallSystem:
    
    class_obj = None

    def __init__(self, classObject):
        self.class_obj = classObject
        Interface.rollCallStart.MyFrame1.__init__(self, None)
        

def main():

    class_1 = Class(name="Biology", professor="Mr. Smith")
    student_1 = Student(name="Elisabeth Petit - Bois")
    class_1.addStudent(student_1)

    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height
    while True:
        ret, img = cap.read()
        #img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]  
        cv2.imshow('video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            class_1.printSummary()
            break
    cap.release()
    cv2.destroyAllWindows()


main()
