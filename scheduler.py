import numpy as np
import json, operator, csv
import random

from test import*

MAX_SCHEDULE_DAYS = 14
TIME_SLOTS = 3
time = ['930','1400','1830']
exam_day = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]

class exam:
   def __init__(self, course_code, course_name, course_instructor, duration,priority, student_class,day,exam_time=None, location= None):
      self.course_code = course_code
      self.course_name = course_name
      self.course_instructor = course_instructor
      self.location = location
      self.duration = duration
      self.student_class = student_class
      self.priority = priority
      self.exam_time = exam_time
      self.day = day

   def __str__(self):
      return (self.course_name)
      
class day:
   def __init__(self, exam, name_day, number_day):
      self.exam = exam
      self.name_day = name_day
      self.number_day = number_day
      

class scheduler:
   def __init__ (self,file_name):
      locations = []
      exam_dict = {}
      exam_names = []
      student_dict={}
      with open(file_name,'r') as exam_info:
         exam_info = exam_info.readlines()[1:]
         
         for row in exam_info:
            row = row.split(',')
            if row[0] != None:
               new_exam = exam(row[0],row[1],row[2],row[4],row[5],row[6],row[8],row[7],row[3])
               exam_names.append(new_exam)
               
               exam_dict.update({row[0]:new_exam})
                  
               if row[6] not in student_dict.keys():
                  student_dict[row[6]] = []
                  student_dict[row[6]].append(new_exam)
               else:
                  student_dict[row[6]].append(new_exam)
                  
               if new_exam.location not in locations:
                  locations.append(new_exam.location)
               
                      
      self.schedule = exam_dict
      self.exam_names = exam_names
      self.locations = locations
      self.student_dict = student_dict
      
   def remove(self,course_code):
      self.schedule.pop(course_code)

   def add_exam(self):
      course_code = input("Enter course code:")
      course_name = input("Enter course name:")
      course_instructor = input("Enter course instructor:")
      location = input("Enter location:")
      duration = input("Enter duration:")
      priority = input("Enter priority:")
      student_class = input("Enter Student Class:")
      exam_time = input("Enter Exam Time:")
      day = input("Enter exam day:")
      new_exam = exam(course_code, course_name, course_instructor, location, duration,priority, student_class,exam_time,day)
      bruh = str(student_class)
      
      self.schedule.update({course_code:new_exam})
         
      if bruh not in self.student_dict.keys():
         self.student_dict[bruh] = []
         self.student_dict[bruh].append(new_exam)
      else:
         self.student_dict[bruh].append(new_exam)      
         
      if new_exam.location not in self.locations:
         self.locations.append(new_exam.location)      
      
      self.exam_names.append(new_exam)
      
   def conflict_check(self):
      conflict = False
      for i,j in self.schedule.items():
         for a,b in self.schedule.items():
            if i != a:
               if j.exam_time == b.exam_time and j.student_class ==b.student_class:
                  conflict = True
               if j.location == b.location and j.exam_time == b.exam_time:
                  conflict = True
      return conflict
   
   def suggestion(self):
      for i,j in self.schedule.items():
         if j.location == '':
            j.location = random.choice(self.locations)
         if j.exam_time == '':
            j.exam_time = random.choice(time)
         if type(j.day) != int or j.day =='':
            j.day = random.choice(exam_day)
                                
   def prioritize(self):
         list1=[]
         list2=[]
         list3=[]
         count1 = 0
         count2 = 0
         count3 = 0
         
         for i in self.exam_names:
            if i.priority == '1':
               list1.append(i)
               count1 += 1
            elif i.priority == '2':
               list2.append(i)
               count2 += 1
            else:
               list3.append(i)
               count3 += 1
               
         last_day1 = -(count1//-3)
         last_day2= -(count2//-3)+last_day1
         last_day3= -(count3//-3)+last_day2
         
         for i in list1:
            if last_day1 == 1:
               i.day = 1
            elif i.day > last_day1:
               temp = range(1,last_day1)
               i.day = random.choice(temp)
         for i in list2:
            if last_day2 == last_day1:
               i.day = last_day2
            elif i.day > last_day2:
               i.day = random.choice(range(last_day1,last_day2))
         for i in list3:
            if last_day2 == last_day3:
               pass
            elif i.day > last_day3:
               i.day = random.choice(range(last_day2,14))
      
   def overload_check(self):
      overload = False
      big = {}
      for i in self.student_dict.keys():
         time = {}
         temp_exam_list = self.student_dict[i]
         for a in temp_exam_list:
            if a.day not in time.keys():
               time[a.day] = []
               time[a.day].append(a.exam_time)
            else:
               time[a.day].append(a.exam_time)
               if len(time[a.day])>2:
                  overload = True
            big.update({i:time})

      for i,j in big.items():
         for a,b in j.items():
            if '1400' and '1830' in b:
               num = int(a)
               new = num +1
               if new > 9:
                  if str(new) in j.keys():
                     if '930' in j[new]:
                        overload = True
               else:
                  haha = str(new)+'\r\n'
                  if haha in j.keys():
                     if '930' in j[haha]:
                        overload = True
                        
      return overload
   
   def display(self):
      for a in self.schedule.keys():
         i = self.schedule[a]
         print("Course Code:",i.course_code,"Course Name:",i.course_name,"Course Instructor:", i.course_instructor,"Exam Location:",i.location,"Exam Duration:",i.duration,"Student Class:",i.student_class,"Priority:",i.priority,"Exam Time:",i.exam_time,"Exam Day:",i.day)
         

   def student_class_scheduler(self,student_class):
      a = str(student_class)
      for i in self.student_dict[a]:
         print("Course Code:",i.course_code,"Course Name:",i.course_name,"Course Instructor:", i.course_instructor,"Exam Location:",i.location,"Exam Duration:",i.duration,"Student Class:",i.student_class,"Priority:",i.priority,"Exam Time:",i.exam_time,"Exam Day:",i.day)
         
   def output(self,file_name):
      with open(file_name,mode = 'w') as output_file:
         fieldnames = ['Course Code','Course Name','Course Instructor','Location','Duration','Priority','Student Class','Time','Day']
         writer = csv.DictWriter(output_file, fieldnames=fieldnames)
         
         writer.writeheader()
         for i in self.exam_names:
            writer.writerow({"Course Code":i.course_code,"Course Name":i.course_name,"Course Instructor":i.course_instructor,"Location":i.location,"Duration":i.duration,"Priority":i.priority,"Student Class":i.student_class,"Time":i.exam_time,"Day":i.day})
            
