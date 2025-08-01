
#Classes (OOP)
import json
import os

 
class Person:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id

 

class Student(Person):
    def __init__(self, name, student_id):
        super().__init__(name, student_id)
        self.courses = {}  # {course_code: grade}

 

    def enroll(self, course):
        if course.course_code not in self.courses:
            self.courses[course.course_code] = None

 

    def assign_grade(self, course_code, grade):
        if course_code in self.courses:
            self.courses[course_code] = grade

 

    def to_dict(self):
        return {
            'name': self.name,
            'student_id': self.student_id,
            'courses': self.courses
        }

 

    @staticmethod
    def from_dict(data):
        student = Student(data['name'], data['student_id'])
        student.courses = data['courses']
        return student

 

class Course:
    def __init__(self, course_name, course_code):
        self.course_name = course_name
        self.course_code = course_code

 

    def to_dict(self):
        return {
            'course_name': self.course_name,
            'course_code': self.course_code
        }

 

    @staticmethod

    def from_dict(data):
        return Course(data['course_name'], data['course_code'])

 

class GradeBook:
    def __init__(self):
        self.students = {}
        self.courses = {}

 

    def add_student(self, student):
        if student.student_id not in self.students:
            self.students[student.student_id] = student

 

    def add_course(self, course):
        if course.course_code not in self.courses:
            self.courses[course.course_code] = course

 

    def enroll_student(self, student_id, course_code):
        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            student.enroll(course)

 

    def assign_grade(self, student_id, course_code, grade):
        if student_id in self.students:
            student = self.students[student_id]
            student.assign_grade(course_code, grade)

 

    def get_student_info(self, student_id):
        if student_id in self.students:
            student = self.students[student_id]
            info = f"Name: {student.name}\nID: {student.student_id}\nCourses:\n"
            for code, grade in student.courses.items():
                course_name = self.courses[code].course_name if code in self.courses else code
                grade_str = grade if grade is not None else "Not Assigned"
                info += f"- {course_name} ({code}): {grade_str}\n"

            return info

        return "Student not found."

 

    def save_to_file(self, filename='students.json'):

        data = {

            'students': [student.to_dict() for student in self.students.values()],

            'courses': [course.to_dict() for course in self.courses.values()]

        }

        with open(filename, 'w') as f:

            json.dump(data, f, indent=4)

 

    def load_from_file(self, filename='students.json'):

        if not os.path.exists(filename):

            return

        with open(filename, 'r') as f:

            data = json.load(f)

        for student_data in data.get('students', []):

            student = Student.from_dict(student_data)

            self.students[student.student_id] = student

        for course_data in data.get('courses', []):

            course = Course.from_dict(course_data)

            self.courses[course.course_code] = course

 

#GUI using Tkinter

import tkinter as tk

from tkinter import messagebox, ttk

 

gradebook = GradeBook()

gradebook.load_from_file()

 

class StudentApp:

    def __init__(self, master):

        self.master = master

        master.title("Student Management System")

 

        #Entry Fields

        self.name_entry = self.make_entry("Student Name:", 0)

        self.id_entry = self.make_entry("Student ID:", 1)

        self.course_name_entry = self.make_entry("Course Name:", 2)

        self.course_code_entry = self.make_entry("Course Code:", 3)

        self.grade_entry = self.make_entry("Grade:", 4)

 

        #Buttons

        self.make_button("Add Student", self.add_student, 5)

        self.make_button("Add Course", self.add_course, 6)

        self.make_button("Enroll Student", self.enroll_student, 7)

        self.make_button("Assign Grade", self.assign_grade, 8)

        self.make_button("View Record", self.view_record, 9)

 

        #Output

        self.output = tk.Text(master, height=10, width=50)

        self.output.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

 

    def make_entry(self, label, row):

        tk.Label(self.master, text=label).grid(row=row, column=0, sticky=tk.W)

        entry = tk.Entry(self.master)

        entry.grid(row=row, column=1)

        return entry

 

    def make_button(self, text, command, row):

        tk.Button(self.master, text=text, command=command).grid(row=row, column=0, columnspan=2, pady=2)

 

    def add_student(self):

        name = self.name_entry.get()

        sid = self.id_entry.get()

        if name and sid:

            student = Student(name, sid)

            gradebook.add_student(student)

            gradebook.save_to_file()

            messagebox.showinfo("Success", "Student added.")

        else:

            messagebox.showerror("Error", "Enter name and ID.")

 

    def add_course(self):

        cname = self.course_name_entry.get()

        ccode = self.course_code_entry.get()

        if cname and ccode:

            course = Course(cname, ccode)

            gradebook.add_course(course)

            gradebook.save_to_file()

            messagebox.showinfo("Success", "Course added.")

        else:

            messagebox.showerror("Error", "Enter course name and code.")

 

    def enroll_student(self):

        sid = self.id_entry.get()

        ccode = self.course_code_entry.get()

        gradebook.enroll_student(sid, ccode)

        gradebook.save_to_file()

        messagebox.showinfo("Success", "Student enrolled.")

 

    def assign_grade(self):

        sid = self.id_entry.get()

        ccode = self.course_code_entry.get()

        try:

            grade = int(self.grade_entry.get())

            gradebook.assign_grade(sid, ccode, grade)

            gradebook.save_to_file()

            messagebox.showinfo("Success", "Grade assigned.")

        except ValueError:

            messagebox.showerror("Error", "Grade must be a number.")

 

    def view_record(self):

        sid = self.id_entry.get()

        info = gradebook.get_student_info(sid)

        self.output.delete(1.0, tk.END)

        self.output.insert(tk.END, info)

 

if __name__ == '__main__':

    root = tk.Tk()

    app = StudentApp(root)

    root.mainloop()

    gradebook.save_to_file()