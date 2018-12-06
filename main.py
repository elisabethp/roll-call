import RollCallSystem as r

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
        print("\n_______________\n")
        print("You are currently reading the summary for " + self.name + " taught by " + self.professor + ".")
        print("There are " + str(len(self.students)) + " student(s) in this class.")
        print("\nHere are the students in this class:")
        print("_______________\n")

        for i in range(len(self.students)):
            print(str(i+1) + ". " + self.students[i].getName() + " - " + str(self.students[i].isAbsent()))

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


def main():

    class_1 = Class(name="Biology", professor="Mr. Smith")
    class_1.printSummary()

    student_1 = Student(name="Elisabeth Petit - Bois")
    class_1.addStudent(student_1)
    class_1.printSummary()

    class_1.setName("Mathematics")
    class_1.setProfessor("Mr. Walker")
    class_1.printSummary()

    student_1.setName("Student Number 1")
    class_1.printSummary()

    student_2 = Student(name="Elisabeth Petit - Bois")
    class_1.addStudent(student_2)
    class_1.printSummary()

    class_1.removeStudent(student_1)
    class_1.printSummary()


    rcs = r.RollCallSystem(class_1)

main()