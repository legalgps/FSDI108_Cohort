class Student:

    def __init__(self, name, age):
        # class constructor - the init method on Python
        self.name = name
        self.age = age

    def say_hello(self):
        print("Hi there! My name is " + self.name)


print("***************Test2*********")

student1 = Student("Chris Daming", 36)
# Don't need the "new" in python
# Never send hte self - python will put it in

student1.say_hello()

#student 1 and 2 are objects
student2 = Student("Sergio Inzunza", 35)
student2.say_hello()


print(student1.name)
student1.name = "Name changed"
print(student1.name)





#get data from dictionary - return me["email"]        object: print(student1.name)