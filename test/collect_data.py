# import tkinter as tk
# from tkinter import Message, Text
# import cv2, os
# import csv
# import numpy as np
# from PIL import Image, ImageTk
# import tkinter.font as font
# from tkinter import messagebox, ttk
# import pymysql
# from tkinter import *
# import re


# window = tk.Tk()
# window.title("Collecting Dataset")
# window.configure(bg="#ccd9de")
# window.geometry('1350x700+0+0')

# # try:
# #     conn = mysql.connector.connect(
# #         user='root',
# #         password='',
# #         host='localhost',
# #         database='face_recognition'
# #     )
# #     cursor = conn.cursor()
# # except mysql.connector.OperationalError as e:
# #         messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
# # except Exception as e:
# #         print(e)
# #         messagebox.showerror("Error","Close all the windows and restart your program")
    
# root_dir = os.getcwd()
# st_code = StringVar()
# st_fullName = StringVar()
# st_birthDay = StringVar()
# st_phone = StringVar()
# st_email = StringVar()
# cl_className = StringVar()
# mydata = []
# dataset_dir = os.path.join(root_dir,'face-db/')

# def add_student():
#     conn = pymysql.connect(
#         user='root',
#         password='',
#         host='localhost',
#         database='face_recognition'
#     )
#     if st_code.get()=="" or st_fullName=="" or st_birthDay=="" or st_phone=="" or st_email=="" or cl_className=="":
#         messagebox.showerror("Error","All fields are Required")
#     else:
#         if(re.search('[a-zA-Z]+', st_fullName.get()) and re.search('^B\d{7}$', st_code.get())):
#             if len(st_phone.get()) != 10:
#                 messagebox.showerror('Error', 'Contact Number must be 10 digits')
#             else:
#                 if (re.search('^[9]\d{9}$', st_phone.get())):
#                     regex = '^[a-zA-Z]+b\d{7}@student\.ctu\.edu\.vn$'
#                     if(re.search(regex, st_email.get())):
#                         class_id = cl_className.get()
#                         code = st_code.get()
#                         input_directory = os.path.join(dataset_dir,f'{class_id}/{code}')
#                         if not os.path.exists(input_directory):
#                             os.makedirs(input_directory)
#                             count = 1
#                             print("[INFO] starting video stream...")
#                             video_capture = cv2.VideoCapture(0)
#                             face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#                             while count <= 50:
#                                 try:
#                                     check, frame = video_capture.read()
#                                     gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#                                     faces = face_cascade.detectMultiScale(gray,1.3,5)
#                                     for (x,y,w,h) in faces:  
#                                         face = frame[y-5:y+h+5,x-5:x+w+5]
#                                         resized_face = cv2.resize(face,(160,160))
#                                         cv2.imwrite(os.path.join(input_directory,code + str(count) + '.jpg'),resized_face)
#                                         cv2.rectangle(frame, (x,y), (x+w, y+h),(0,0,255), 2)
#                                         count += 1
#                                         # show the output frame
#                                         cv2.imshow("Frame",frame)
#                                         key = cv2.waitKey(1)
#                                         if key == ord('q'):
#                                             break
#                                 except Exception as e:
#                                     pass
#                                 video_capture.release()
#                                 cv2.destroyAllWindows()
#                                 cur1 = conn.cursor()
#                                 cur1.execute("INSERT INTO students(st_code, st_fullName, st_birthDay, st_phone, st_email, cl_className) VALUES (%s,%s, %s, %s, %s,%s)", (st_code.get(), st_fullName.get(), st_birthDay.get(), st_phone.get(),st_email.get(), cl_className.get()))
#                                 conn.commit()
#                                 messagebox.showinfo("Success", "All photos are collected") 
#                                 conn.close()

# ############################################################################
# id = Label(window, text = "Student ID", bg = "gray", font = ("italic",13, "bold")).place(x = 35, y = 100 )
# E1 = Entry(window, width = 20, textvariable = st_code,  font = ("italic",13, "bold") ).place(x = 180  , y = 100)
# post = Label(window, text = "Full Name", bg = "gray",  font = ("italic",13, "bold")).place(x = 35, y = 150 )
# E2 = Entry(window, width = 20, textvariable = st_fullName,  font = ("italic",13, "bold")).place(x =180, y = 150)
# bd = Label(window, text = "Birthday", bg = "gray", font = ("italic",13, "bold")).place(x =35, y = 200)
# E3 = Entry(window, width = 20, textvariable = st_birthDay , font = ("italic",12, "bold")).place(x = 180, y = 200)
# no = Label(window, text = "Contact.No", bg = "gray", font = ("italic",12, "bold")  ).place(x = 35, y = 250)
# E4 = Entry(window, width = 20, textvariable = st_phone , font = ("italic",12, "bold") ).place(x = 180, y = 250 )
# mail = Label(window, text = " Email Address", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y = 300)
# E5 = Entry(window, width = 20, textvariable = st_email , font = ("italic",12, "bold") ).place(x = 180, y = 300)
# classId = Label(window, text = "Class ID", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y= 350)
# E6 = ttk.Combobox(window, textvariable = cl_className , values = ['DI17V7F1','DI17V7F2','DI17V7F3','DI17V7F4'], state = "readonly",  font = ("italic",11, "bold")).place(x = 180, y = 350)

# # gender = Label(window, text = "Class ID", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y= 250)
# # E7 = ttk.Combobox(window, textvariable = cl_className , values = ['DI17V7F1','DI17V7F2','DI17V7F3','DI17V7F4'], state = "readonly",  font = ("italic",11, "bold")).place(x = 180, y = 250)
# # no = Label(window, text = "Contact.No", bg = "gray", font = ("italic",12, "bold")  ).place(x = 35, y = 250)
# # E4 = Entry(window, width = 20, textvariable = st_phone , font = ("italic",12, "bold") ).place(x = 180, y = 300 ) 
# # address = Label(window, text = " Email Address", bg = "gray", font = ("italic",12, "bold")).place(x = 35, y = 350)
# # E5 = Entry(window, width = 20, textvariable = st_email , font = ("italic",12, "bold") ).place(x = 180, y = 350)
                                                
# btn1 = Button(window, text = "Add", bg = "green", height = "1", width = "7",command = add_student, font = ("Times new Roman", 14 , "bold")).place(x = 10, y = 10)
# btn2 = Button(window, text = "Update", bg = "green", height = "1", width = "7", font = ("Times new Roman", 14 , "bold")).place(x = 105, y = 10)
# btn3 = Button(window, text = "Delete", bg = "green",  height = "1", width = "7", font = ("Times new Roman", 14 , "bold")).place(x = 205, y = 10)
# btn4 = Button(window, text = "Clear", bg = "green", height = "1", width = "7", font = ("Times new Roman", 14 , "bold")).place(x = 305, y = 10)
                        
# ############################################################################
# # lbl = tk.Label(window, text="Face Recognition Based Attendance System", bg="#ccd9de" , fg="#3289a8" , width=50 , height=3, font=('times', 30, 'italic bold')) 
# # lbl.place(x=100, y=20)

# # lbl1 = tk.Label(window, text="Enter ID", width=20 , height=2 , fg="#3289a8" , bg="white", font=('times', 15, ' bold ') ) 
# # lbl1.place(x=200, y=200)

# # txt1 = tk.Entry(window, width=20, bg="white", fg="#3289a8", font=('times', 15, ' bold '))
# # txt1.place(x=550, y=215)

# # lbl2 = tk.Label(window, text="Class ID", width=20 , fg="#3289a8", bg="white", height=2, font=('times', 15, ' bold ')) 
# # lbl2.place(x=200, y=300)

# # classID=['DI21V7F1', 'DI21V7F2','DI21V7F3','DI21V7F4']

# # txt2=ttk.Combobox(window, values=classID,font=("Consolas", 15), width=13)
# # # txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 15, ' bold ')  )
# # txt2.place(x=550, y=315)
# # txt2.set('Select...')

# # lbl3 = tk.Label(window, text="Notification →", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
# # lbl3.place(x=200, y=400)

# # message = tk.Label(window, text="", bg="white", fg="black", width=30, height=2, font=('times', 15, ' bold ')) 
# # message.place(x=550, y=400)
 
# # def clearSId():
# #     txt1.delete(0, 'end')

# # def clearCId():
# #     txt2.delete(0, 'end')
# #     txt2.set('Select...')

# # def takeImages():        
    
# #     if(txt1.get()=="" or txt2.get()=="Select..." or txt2.get()==""):
# #         res = "Please fill all information!"
# #         lbl3 = tk.Label(window, text="Notification →", width=20 , fg="red", bg="white", height=2, font=('times', 15, ' bold ')) 
# #         lbl3.place(x=200, y=400)
# #         message.configure(text= res, fg="black", bg="red")
# #         # messagebox.showinfo('Result', 'Please fill all information!')
# #     else:
# #         SId=(txt1.get())
# #         CId=(txt2.get())
# #         lbl3 = tk.Label(window, text="Notification →", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
# #         lbl3.place(x=200, y=400)
# #         message.configure(text="",fg="black", bg="white")
# #         folder_name = f"./face-db/{CId}/{SId}"
# #         if not os.path.exists(folder_name):
# #             os.makedirs(folder_name)

# #         cam = cv2.VideoCapture("http://192.168.117.120/video")
# #         harcascadePath = "haarcascade_frontalface_default.xml"
# #         detector = cv2.CascadeClassifier(harcascadePath)
# #         sampleNum = 0
        
# #         while (True):
# #             ret, img = cam.read()
# #             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #             faces = detector.detectMultiScale(gray, 1.3, 5)
            
# #             for (x,y,w,h) in faces:
# #                 cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
# #                 sampleNum=sampleNum+1
# #                 cv2.putText(img, str(sampleNum), (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 3)
# #                 file_name_path = f"{folder_name}/img{sampleNum}.jpg"
# #                 cv2.imwrite(file_name_path, gray[y:y+h,x:x+w])
# #                 resized = cv2.resize(img, (600,400))
# #                 cv2.imshow('Face Detecting',resized)
# #             if cv2.waitKey(100) & 0xFF == ord('q'):
# #                 break
# #             elif sampleNum>50:
# #                 break
# #         cam.release()
# #         cv2.destroyAllWindows() 



# # clearButton1 = tk.Button(window, text="Clear", command=clearSId, fg="white", bg="gray", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
# # clearButton1.place(x=850, y=200)

# # clearButton2 = tk.Button(window, text="Clear", command=clearCId, fg="white", bg="gray", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
# # clearButton2.place(x=850, y=300)  

# # takeImg = tk.Button(window, text="Take Images", command=takeImages, fg="white", bg="#3289a8", width=20, height=3, activebackground = "Green", font=('times', 15, ' bold '))
# # takeImg.place(x=400, y=500)

# # quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="white", bg="gray", width=20, height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
# # quitWindow.place(x=700, y=500)

# window.mainloop()
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pymysql
import unicodedata
import re

def remove_accents(input_str):
    nfkd_str = unicodedata.normalize('NFKD', input_str)
    no_accents_str = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
    return re.sub(r'[^a-zA-Z0-9\s]', '', no_accents_str)

def import_excel(file_paths):
    if not file_paths:
        print("No files selected for import.")
        return
    
    conn = pymysql.connect(
        user='root',
        password='',
        host='localhost',
        database='face_recognition'
    )
    cur = conn.cursor()
    
    try:
        with cur:
            for file_path in file_paths:
                df = pd.read_excel(file_path, sheet_name='Worksheet')

                cols = ['STT', 'Điểm 10', 'Vi phạm quy chế', 'Phái', 'Khóa nhập điểm']
                df.drop(cols, inplace=True, axis=1)

                df.rename(columns={
                    'Mã sinh viên': 'st_code',
                    'Họ và Tên': 'st_fullName',
                    'cl_ID': 'cl_className'
                }, inplace=True)

                df = df[['st_code', 'st_fullName', 'cl_className']]

                def create_email(full_name, st_code):
                    full_name_no_accents = remove_accents(full_name)
                    last_name = full_name_no_accents.split()[-1].lower()
                    email = f"{last_name}{st_code.lower()}@student.ctu.edu.vn"
                    return email

                df['st_email'] = df.apply(lambda row: create_email(row['st_fullName'], row['st_code']), axis=1)

                insert_query = """
                INSERT INTO students (st_code, st_fullName, st_email, cl_className)
                VALUES (%s, %s, %s, %s)
                """
                for index, row in df.iterrows():
                    cur.execute(insert_query, (row['st_code'], row['st_fullName'], row['st_email'], row['cl_className']))
            conn.commit()
            print("Data imported successfully into the 'students' table.")
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    finally:
        conn.close()

def choose_files():
    file_paths = filedialog.askopenfilenames(
        filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
    )
    if file_paths:
        entry_var.set(", ".join(file_paths))

window = tk.Tk()
window.title("Load file")
window.configure(bg="#ccd9de")
window.geometry('1350x700+0+0')

title = tk.Label(window, text="Import Excel", font=("times new roman", 25, "bold"), bg="#134B70", fg="#FDFFE2", bd=7, relief=tk.GROOVE)
title.place(x=0, y=0, relwidth=1)

frame = tk.Frame(window, bg="#EEEEEE")
frame.place(x=50, y=200, width=1200, height=50)

label = tk.Label(frame, text="Choose Files:", bg="#EEEEEE", compound=tk.LEFT, font=("times new roman", 15, "bold"))
label.grid(row=0, column=0, padx=10, pady=5)

entry_var = tk.StringVar()
entry = tk.Entry(frame, font=("times new roman", 15, "bold"), relief=tk.GROOVE, bg="lightgray", width=100, textvariable=entry_var)
entry.grid(row=0, column=1, padx=10, pady=5)

choose_button = tk.Button(window, text="Choose Excel Files", font=("times new roman", 15, "bold"), command=choose_files, bg="#134B70", fg="#FDFFE2")
choose_button.place(x=50, y=300)

import_button = tk.Button(window, text="Import Excel Files", font=("times new roman", 15, "bold"), command=lambda: import_excel(entry_var.get().split(", ")), bg="#134B70", fg="#FDFFE2")
import_button.place(x=250, y=300)

window.mainloop()
