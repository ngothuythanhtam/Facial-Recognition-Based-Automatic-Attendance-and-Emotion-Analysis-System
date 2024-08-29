import pickle
import os
from datetime import datetime
from statistics import mode
import sys
import webbrowser
import re
import shutil
import json
import tensorflow as tf
import tkinter as tk
import cv2
import numpy as np
import tkinter.font as font
from tkinter import ttk, filedialog, messagebox, Toplevel, Label, RIDGE, Button, Entry, Frame, Scrollbar, Canvas, Message, Text
from tkinter import *
import pymysql
from PIL import Image, ImageTk
import time
import pandas as pd
import unicodedata
import dlib
import face_analysis
import openpyxl
import json
from tkinter import messagebox, simpledialog

root_dir = os.getcwd()

try:
    detector = dlib.get_frontal_face_detector() # type: ignore
    predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat") # type: ignore
    angles = ['front', 'right', 'left', 'up', 'down']
    instructions = {
        'front': 'Please look straight ahead.',
        'right': 'Please turn your face to the right.',
        'left': 'Please turn your face to the left.',
        'up': 'Please tilt your face up.',
        'down': 'Please tilt your face down.'
    }
except cv2.error as e:
    print("Error: Provide correct path for face detection model.")
    sys.exit(1)
except Exception as e:
    print("{}".format(str(e)))
    sys.exit(1)
#############---------------------------------------------------------- ADMIN LOGIN PAGE ----------------------------------------------------------------#############
face = Tk()
face.title("Admin Login Page")
face.attributes("-fullscreen", True)
face.configure(bg = "#ccd9de")

password_db = "mysql"

## Variables for login ##
username_var = StringVar()
password_var = StringVar()
oldpass_var = StringVar()
user_var = StringVar()
newpass_var = StringVar()

def login():
    global password_db
    if username_var.get() == "" or password_var.get() == "":
        messagebox.showerror('Error','All the fields are required', parent = face)
    else:
        try:
            conn = pymysql.connect(host = 'localhost', user = 'root', password =password_db, database = 'face_recognition')
            curr = conn.cursor()
            curr.execute('select * from administrator where ad_code = %s and ad_pass = %s',(username_var.get(), password_var.get()))
            row = curr.fetchone()
            if row == None:
                messagebox.showerror('Error','Invalid Data')
            else:
                face.destroy()

######################################################### Function to import data from excel to MySQL ########################################################
                def import_data():
                    try:
                        conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                        cur = conn.cursor()
                        # All Required variables for database
                        entry_var = StringVar()
                        
                        ##### Choose the file path #####
                        def choose_files():
                            global file_paths
                            file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],parent=import_window)
                            if file_paths:
                                entry_var.set(", ".join(file_paths))

                        ##### Remove accents of the name #####
                        def remove_accents(input_str):
                            input_str = input_str.replace("Đ", "D").replace("đ", "d")
                            nfkd_str = unicodedata.normalize('NFKD', input_str)
                            no_accents_str = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
                            return re.sub(r'[^a-zA-Z0-9\s]', '', no_accents_str)
                        
                        ##### Import data to the 'students' table in MySQL #####
                        def import_students(file_paths):
                            if not file_paths:
                                messagebox.showerror("Error", "No files selected for import.", parent=import_window)
                                return
                            conn = pymysql.connect(user='root', password=password_db, host='localhost', database='face_recognition')
                            cur = conn.cursor()
                            try:
                                with cur:
                                    for file_path in file_paths:
                                        df = pd.read_excel(file_path, sheet_name='DSSV')
                                        
                                        # Rename the colums in Excel to match with the colums in database
                                        df.rename(columns={
                                            'Lớp': 'cl_className',
                                            'Mã sinh viên': 'st_code',
                                            'Họ và Tên': 'st_fullName'
                                        }, inplace=True)
                                        df = df[['st_code', 'st_fullName', 'cl_className']]
                                        
                                        # Create student's email by joining name+code+@student.ctu.edu.vn
                                        def create_email(full_name, st_code):
                                            full_name_no_accents = remove_accents(full_name)
                                            last_name = full_name_no_accents.split()[-1].lower()
                                            email = f"{last_name}{st_code.lower()}@student.ctu.edu.vn"
                                            return email
                                        df['st_email'] = df.apply(lambda row: create_email(row['st_fullName'], row['st_code']), axis=1)
                                        
                                        insert_query = """ INSERT INTO students (st_code, st_fullName, st_email, cl_className) VALUES (%s, %s, %s, %s)"""
                                        for index, row in df.iterrows():
                                            cur.execute(insert_query, (row['st_code'], row['st_fullName'], row['st_email'], row['cl_className']))
                                            
                                    conn.commit()
                                    messagebox.showinfo("Success", "Data imported successfully into the 'students' table.",parent=import_window)
                                        
                            except Exception as e:
                                messagebox.showerror("Error", f"An error occurred: {e}", parent=import_window)
                                conn.rollback()
                            finally:
                                conn.close()

                        ##### Import data to the 'courses' table in MySQL #####
                        def import_courses(file_paths):
                            if not file_paths:
                                messagebox.showerror("Error","No files selected for import.", parent=import_window)
                                return
                            conn = pymysql.connect(user='root', password=password_db, host='localhost', database='face_recognition')
                            cur = conn.cursor()
                            
                            try:
                                with cur:
                                    for file_path in file_paths:
                                        df = pd.read_excel(file_path, sheet_name='Sheet1')

                                        # Remove unnecessary columns
                                        cols = ['STT', 'Năm học', 'HK']
                                        df.drop(cols, inplace=True, axis=1)

                                        # Rename the colums in Excel to match with database
                                        df.rename(columns={
                                            'Mã HP': 'course_code',
                                            'Tên học phần': 'course_name',
                                            'Số TC': 'course_credits',
                                            'Mã ngành': 'maj_Code'
                                        }, inplace=True)

                                        if 'maj_Code' not in df.columns:
                                            raise ValueError("Required column 'maj_Code' is missing in the Excel file.")

                                        # convert type of courses_credits
                                        df['course_credits'] = df['course_credits'].astype(int)
                                        df = df[['course_code', 'course_name', 'course_credits', 'maj_Code']]

                                        insert_query = """
                                        INSERT INTO courses (course_code, course_name, course_credits, maj_Code)
                                        VALUES (%s, %s, %s, %s)
                                        """
                                        for index, row in df.iterrows():
                                            cur.execute(insert_query, (row['course_code'], row['course_name'], row['course_credits'], row['maj_Code']))
                                    conn.commit()
                                    messagebox.showinfo("Success", "Data imported successfully into the 'courses' table.", parent=import_window)
                                    
                            except Exception as e:
                                messagebox.showerror("Error", f"An error occurred: {e}", parent=import_window)
                                print(f"An error occurred: {e}")
                                conn.rollback()
                            finally:
                                conn.close()
                        
                        ##### Import data to the 'courseFollowAcaYear' table in MySQL #####
                        def import_courseFollowAcaYear(file_paths):
                            if not file_paths:
                                messagebox.showerror("Error","No files selected for import.", parent=import_window)
                                return
                            conn = pymysql.connect(user='root', password=password_db, host='localhost', database='face_recognition')
                            cur = conn.cursor()
                            try:
                                with cur:
                                    for file_path in file_paths:
                                        df = pd.read_excel(file_path, sheet_name='Sheet1')

                                        # Remove unnecessary columns
                                        cols = ['STT', 'Tên học phần', 'Số TC', 'Mã ngành']
                                        df.drop(cols, inplace=True, axis=1)

                                        # Rename the colums in Excel to match with database
                                        df.rename(columns={
                                            'Mã HP': 'course_code',
                                            'Năm học': 'ay_schoolYear',
                                            'HK': 'se_ID'
                                        }, inplace=True)

                                        df.replace("hè", "3", inplace=True)

                                        # Convert 'ay_schoolYear' to string and strip spaces
                                        df['ay_schoolYear'] = df['ay_schoolYear'].astype(str).str.strip()
                                        
                                        # Convert 'se_ID' to integer
                                        df['se_ID'] = df['se_ID'].astype(int)
                                        
                                        df = df[['course_code', 'ay_schoolYear', 'se_ID']]

                                        insert_query = """
                                        INSERT INTO courseFollowAcaYear (course_code, ay_schoolYear, se_ID)
                                        VALUES (%s, %s, %s)
                                        """
                                        for index, row in df.iterrows():
                                            cur.execute(insert_query, (row['course_code'], row['ay_schoolYear'], row['se_ID']))
                                    conn.commit()
                                    messagebox.showinfo("Success", "Data imported successfully into the 'courses' table.", parent=import_window)
                                    
                            except Exception as e:
                                messagebox.showerror("Error", f"An error occurred: {e}", parent=import_window)
                                print(f"An error occurred: {e}")
                                conn.rollback()
                            finally:
                                conn.close()
                            
                         ##### Import data to the 'studying' table in MySQL #####
                        
                        def import_studying():
                            try:
                                paths = StringVar()
                                import_frame = Toplevel()
                                import_frame.geometry('1000x400')
                                import_frame.configure(bg="#ccd9de")
                                import_frame.title("Import Studying")
                                
                                # Local variable to store file paths
                                local_file_paths = []

                                def choose_paths():
                                    nonlocal local_file_paths
                                    local_file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")], parent=import_frame)
                                    if local_file_paths:
                                        paths.set(", ".join(local_file_paths))
                                
                                
                                
                                def get_class(event=None):
                                    global cl_ID
                                    try:
                                        conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                                        cur = conn.cursor()
                                        class_options = search_class()
                                        cl_ID = class_options.get(class_combobox.get()) # type: ignore
                                        print(f"class_id_get_class: {cl_ID}")
                                    except Exception as e:
                                        print(f"Error in get_class: {e}")
                                    finally:
                                        cur.close()
                                        conn.close()
                                    
                                def execute(local_file_paths):
                                    
                                    global cl_ID
                                    if cl_ID is None:
                                        messagebox.showerror("Error", "Class ID not selected.", parent=import_frame)
                                        return
                                    print(f"class_id_excute: {cl_ID}")

                                    if not local_file_paths:
                                        messagebox.showerror("Error", "No files selected for import.", parent=import_frame)
                                        return
                                    conn = pymysql.connect(user='root', password=password_db, host='localhost', database='face_recognition')
                                    cur = conn.cursor()
                                    try:
                                        with cur:
                                            for file_path in local_file_paths:
                                                df = pd.read_excel(file_path, sheet_name='M01')
                                                
                                                cols = ['STT', 'Phái', 'Họ và Tên']
                                                df.drop(cols, inplace=True, axis=1)

                                                # Rename the colums in Excel to match with database
                                                df.rename(columns={'Mã sinh viên': 'st_code'}, inplace=True)

                                                df = df[['st_code']]

                                                insert_query = """
                                                INSERT INTO studying (st_code, clCourse_ID)
                                                VALUES (%s, %s)
                                                """
                                                for index, row in df.iterrows():
                                                    cur.execute(insert_query, (row['st_code'], cl_ID))
                                            conn.commit()
                                            messagebox.showinfo("Success", "Data imported successfully into the 'studying' table.", parent=import_frame)
                                    
                                    except Exception as e:
                                        messagebox.showerror("Error", f"An error occurred: {e}", parent=import_frame)
                                        print(f"An error occurred: {e}")
                                        conn.rollback()
                                    finally:
                                        cur.close()
                                        conn.close()

                                # Rest of the function code (UI elements) remains the same
                                # Hàm lấy dữ liệu về học phần - lớp
                                def search_course():
                                    conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                                    cur = conn.cursor()
                                    try:
                                        cur.execute("select cfa_ID, course_code from courseFollowAcaYear where course_code LIKE '%_H';;")
                                        cfa_data = cur.fetchall()
                                    finally:
                                        conn.close()
                                    course_options = {c_code: c_id for c_id, c_code in cfa_data}
                                    return course_options
                                
                                def search_class(event=None):
                                    conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                                    cur = conn.cursor()
                                    c_id = course_options.get(course_combobox.get())
                                    
                                    try:
                                        if c_id is not None:
                                            # Chuyển đổi c_id thành số nguyên
                                            cour_id = int(c_id)
                                        
                                        # In ra cour_id để kiểm tra giá trị trước khi thực hiện câu lệnh SQL
                                        print(f"cour_id: {cour_id}")
                                        print(type(cour_id))
                                        cur.execute('''SELECT clCourse_ID, cl.clCourse_code
                                                    FROM classCourse cl 
                                                    JOIN courseFollowAcaYear cfa ON cl.cfa_ID = cfa.cfa_ID
                                                    JOIN courses c ON cfa.course_code = c.course_code
                                                    WHERE cl.cfa_ID = "%s" ''', (cour_id,))
                                        class_data = cur.fetchall()
                                    except Exception as e:
                                        print(f"Error in search_class: {e}")
                                        print(f"Error type: {type(e)}")
                                        print(f"Error args: {e.args}")
                                        class_combobox.set("Lỗi khi tìm kiếm")
                                        return
                                    finally:
                                        cur.close()

                                    if class_data:
                                        class_options = {cl_code: cl_id for cl_id, cl_code in class_data}
                                        class_combobox.config(values=list(class_options.keys()))
                                    else:
                                        class_options = ["No class yet"]
                                        class_combobox.config(values=class_options)
                                    return class_options
                                
                                # GUI elements
                                course_label = Label(import_frame, text="Courses", bg="#EEEEEE", compound=LEFT, font=("times new roman", 15, "bold"))
                                course_label.grid(row=0, column=0, padx=30, pady=5)
                                
                                course_options = search_course()
                                course_combobox = ttk.Combobox(import_frame, values=list(course_options.keys()), font=("times new roman", 12), state="readonly")
                                course_combobox.set("Select Course")
                                course_combobox.grid(row=0, column=1, padx=10, pady=10)
                                course_combobox.bind('<<ComboboxSelected>>', search_class)

                                class_label = Label(import_frame, text="Classes", bg="#EEEEEE", compound=LEFT, font=("times new roman", 15, "bold"))
                                class_label.grid(row=1, column=0, padx=30, pady=5)
                                
                                class_combobox = ttk.Combobox(import_frame, font=("times new roman", 12), state="readonly")
                                class_combobox.set("Select Class")
                                class_combobox.grid(row=1, column=1, padx=20, pady=(10, 20))
                                class_combobox.bind('<<ComboboxSelected>>', get_class)

                                entry_path = tk.Entry(import_frame, font=("times new roman", 15, "bold"), relief=tk.GROOVE, bg="#ccd9de", width=50, textvariable=paths)
                                entry_path.grid(row=2, column=1, padx=50, pady=20)

                                browse_btn = tk.Button(import_frame, text="Browse", font=("times new roman", 15, "bold"), bg="#40679E", fg="#FDFFE2", command=choose_paths)
                                browse_btn.grid(row=2, column=2, padx=10, pady=20)

                                OK_btn = Button(import_frame, text="OK", font=("times new roman", 15, "bold"), bg="#40679E", fg="#FDFFE2", command=lambda: execute(local_file_paths))
                                OK_btn.grid(row=3, column=1, padx=10, pady=10)

                                import_frame.mainloop()
                            
                            except Exception as e:
                                messagebox.showerror("Error", f"An error occurred: {e}", parent=import_window)
                                conn.rollback()
                            finally:
                                conn.close()
                            
                        ######################################## Import data page ###################################
                        
                        import_window = Toplevel()
                        import_window.state('zoomed')
                        import_window.configure(bg="#ccd9de")
                        import_window.title("Import Excel")
                        title = Label(import_window, text="Import Data from Excel", bg="#134B70", fg="#FDFFE2", padx=15, pady=15, font=("Times New Roman", 20, "bold"), borderwidth=5, relief=RIDGE).place(x=600, y=80) 
                        
                        def back():
                            import_window.destroy()
                            
                        backbtn = Button(import_window, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, command=back)
                        backbtn.place(x=1380, y=20)
                        
                        frame = tk.Frame(import_window, bg="#DCF2F1")
                        frame.place(x=350, y=220, width=800, height=400)
                        
                        entry = tk.Entry(frame, font=("times new roman", 15, "bold"), relief=tk.GROOVE, bg="#ccd9de", width=60, textvariable=entry_var)
                        entry.grid(row=0, column=1, padx=50, pady=35)

                        choose_button = tk.Button(frame, text="Browse", font=("times new roman", 15, "bold"),  bg = "#40679E",fg="#FDFFE2", command=choose_files)
                        choose_button.place(x=670, y=25)

                        import_student_button = tk.Button(frame, text="Import students table", font=("times new roman", 15, "bold"),  bg = "#40679E",fg="#FDFFE2", command=lambda: import_students(entry_var.get().split(", ")))
                        import_student_button.place(x=50, y=100) 

                        import_courses_button = tk.Button(frame, text="Import courses table", font=("times new roman", 15, "bold"),  bg = "#40679E",fg="#FDFFE2",command=lambda: import_courses(entry_var.get().split(", ")),)
                        import_courses_button.place(x=300, y=100) 

                        import_studying_button = tk.Button(frame, text="Import studying table", font=("times new roman", 15, "bold"),  bg = "#40679E",fg="#FDFFE2", command=import_studying)
                        import_studying_button.place(x=550, y=100)
                        
                        import_courseFollowAcaYear_button = tk.Button(frame, text="Import courseFollowAcaYear table", font=("times new roman", 15, "bold"),  bg = "#40679E",fg="#FDFFE2",command=lambda: import_courseFollowAcaYear(entry_var.get().split(", ")),)
                        import_courseFollowAcaYear_button.place(x=50, y=180) 
                        
                         
                        
                        import_window.mainloop()

                    except pymysql.err.OperationalError as e:
                        messagebox.showerror("Error", "Sql Connection Error... Open Xamp Control Panel and then start MySql Server")
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Close all the windows and restart your program")

##############################################################################################################################################################

######################################################### Function to create class ###########################################################################
                def create_class():
                    # Create a new window
                    first = Toplevel()
                    # first.attributes("-fullscreen", True)
                    first.state('zoomed')
                    first.configure(bg="#ccd9de")
                    first.title("Create New Class")

                    #All Required variables for database
                    school_year = StringVar()
                    se = StringVar()
                    co_code = StringVar()
                    co_name = StringVar()

                    # Label for the title
                    Label(first, text="Create New Class", bg="#134B70", fg="#FDFFE2", padx=15, pady=15, 
                            font=("Times New Roman", 20, "bold"), borderwidth=5, relief=RIDGE).pack(side=TOP, pady=10)

                    # Function to go back
                    def back():
                        first.destroy()

                    # Back button
                    Button(first, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, 
                        command=back).place(x=1380, y=10)  
                    
                    # Update window to get accurate width and height
                    first.update_idletasks()
                    window_width = first.winfo_width()

                    # Frame to hold the Treeview
                    frame = Frame(first, bg = "#577B8D", borderwidth=5, relief=RIDGE)
                    window_width = first.winfo_width()
                    frame_width = window_width // 2
                    frame.place(x=50, y=125, width=frame_width - 75, height=700)

                    # Frame cho phần tìm kiếm
                    search_frame = Frame(frame, bg="#577B8D")
                    search_frame.pack(side=TOP, fill=X, padx=10, pady=10)

                    # Frame to hold a Create Class Widget
                    frame2 = Frame(first, bg = "#577B8D", borderwidth=5, relief=RIDGE)
                    frame2.place(x=775, y=125, width=frame_width - 75, height=700)

                    # Create a treeview for displaying the data
                    table_frame = Frame(frame, bg = "#577B8D")
                    table_frame.pack(fill=BOTH, expand=True, padx=10, pady= 10)

                    scrollbar_y = ttk.Scrollbar(table_frame, orient=VERTICAL)
                    columns = ("course_code", "course_name", "ay_schoolYear", "se_ID")
                    table1 = ttk.Treeview(table_frame,  yscrollcommand=scrollbar_y.set, columns=columns, show='headings')
                    scrollbar_y.config(command=table1.yview)
                    
                    # Sắp xếp các thành phần
                    scrollbar_y.pack(side=RIGHT, fill=Y)
                    table1.pack(side=LEFT, fill=BOTH, expand=True)

                    # Hàm lấy dữ liệu về học kỳ - năm học
                    def search_se_year():
                        conn = pymysql.connect(host = 'localhost', user = 'root', password=password_db, database = 'face_recognition')
                        cur = conn.cursor()
                        try:
                            # Lấy dữ liệu về học kỳ
                            cur.execute("SELECT se_ID, se_semesterName FROM semester")
                            se_data = cur.fetchall()

                            # Lấy dữ liệu về năm học
                            cur.execute("SELECT ay_schoolYear FROM years")
                            year_data = cur.fetchall()
                        finally:
                            conn.close()
                        
                        # Tạo danh sách các tùy chọn
                        se_options = {name: se_ID for se_ID, name in se_data}
                        year_options = [year[0] for year in year_data]

                        return se_options, year_options
                    
                    
                    # hàm search
                    def search_by_year_se():
                        conn = pymysql.connect(host='localhost', user='root', password=password_db, database='face_recognition')
                        cur = conn.cursor()
                        sem_id = se_options.get(search_sem.get())
                        year = search_year.get()
                        try:
                            if search_year.get() == "Chọn Năm Học" and search_sem.get() == "Chọn Học Kỳ":
                                messagebox.showwarning('Input Error', 'Please select either Year or Semester')
                                return
                            if search_year.get() == "Chọn Năm Học":
                                cur.execute("""SELECT cfa.course_code, c.course_name, cfa.ay_schoolYear, s.se_semesterName
                                            FROM coursefollowacayear cfa
                                            JOIN courses c ON cfa.course_code = c.course_code
                                            JOIN semester s ON cfa.se_ID = s.se_ID
                                            WHERE cfa.se_ID = %s""", (sem_id,))
                            elif search_sem.get() == "Chọn Học Kỳ":
                                cur.execute("""SELECT cfa.course_code, c.course_name, cfa.ay_schoolYear, s.se_semesterName
                                            FROM coursefollowacayear cfa
                                            JOIN courses c ON cfa.course_code = c.course_code
                                            JOIN semester s ON cfa.se_ID = s.se_ID
                                            WHERE cfa.ay_schoolYear = %s""", (year,))
                            else:
                                cur.execute("""SELECT cfa.course_code, c.course_name, cfa.ay_schoolYear, s.se_semesterName
                                            FROM coursefollowacayear cfa
                                            JOIN courses c ON cfa.course_code = c.course_code
                                            JOIN semester s ON cfa.se_ID = s.se_ID
                                            WHERE cfa.ay_schoolYear = %s AND cfa.se_ID = %s""", (year, sem_id))
                            
                            data = cur.fetchall()
                            
                            if data:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values=row)
                            else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent=first)
                        finally:
                            conn.close()
                            
                    # clear data
                    def clear():
                        search_year.set("Chọn Năm Học")
                        search_sem.set("Chọn Học Kỳ")   
                        display()
                        
                   # Clear 
                    def clear_data():
                        ipt5.set("Chọn Nhóm")
                        ipt6.delete(0, END)  
        
                    # Function to display data from the database
                    def display():
                        # Reconnect to the database inside the function
                        conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                        cur = conn.cursor()

                        # Execute the query
                        cur.execute("""
                            SELECT cfa.course_code, c.course_name, cfa.ay_schoolYear, s.se_semesterName
                            FROM coursefollowacayear cfa 
                            JOIN courses c ON cfa.course_code = c.course_code
                            JOIN semester s ON cfa.se_ID = s.se_ID
                        """)

                        # Fetch all data
                        data = cur.fetchall()

                        # If there's data, insert it into the table
                        if len(data) != 0:
                            table1.delete(*table1.get_children())
                            for row in data:
                                table1.insert('', END, values=row)
                            conn.commit()

                        # Close the connection
                        conn.close()

                    def focus_data(event):
                        global cfa_ID
                        cursor = table1.focus()
                        contents = table1.item(cursor)
                        row = contents['values']
                        if len(row) != 0:
                            co_code.set(row[0])
                            co_name.set(row[1])
                            school_year.set(row[2])
                            se.set(row[3])
                            
                            # Lấy cfa_ID cho mục được chọn
                            conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                            cur = conn.cursor()
                            try:
                                cur.execute("""
                                    SELECT cfa.cfa_ID
                                    FROM coursefollowacayear cfa 
                                    WHERE cfa.course_code = %s AND cfa.ay_schoolYear = %s AND cfa.se_ID = (SELECT se_ID FROM semester WHERE se_semesterName = %s)
                                """, (row[0], row[2], row[3]))
                                result = cur.fetchone()
                                if result:
                                    cfa_ID = result[0]
                                else:
                                    cfa_ID = None
                            finally:
                                conn.close()
                                
                    # Submit Data
                    def submit_data():
                        global cfa_ID
                        conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                        cur = conn.cursor()
                        
                        cl_code = ipt5.get()
                        cl_amount = ipt6.get()
                        
                        if cfa_ID is not None:
                            try:
                                # Execute the query
                                cur.execute("""
                                    INSERT INTO classcourse (clCourse_code, clCourse_amount, cfa_ID) 
                                    VALUES (%s, %s, %s)
                                """, (cl_code, cl_amount, cfa_ID))
                                
                                conn.commit()
                                messagebox.showinfo("Success", "Data submitted successfully", parent=first)
                            except pymysql.Error as e:
                                conn.rollback()
                                messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=first)
                        else:
                            messagebox.showerror("Error", "Please select a course first", parent=first)
                        
                        conn.close()

                    # Create a treeview for display the inputs
                    title1 = Label(search_frame, text = "Search By: " ,bg = "#577B8D", fg="#FDFFE2", font = ("Times New Roman", 20, "bold"))
                    title1.pack(side=LEFT, padx=10, pady=10, anchor=W)
                    # Tạo Combobox
                    se_options, year_options = search_se_year()
                    style = ttk.Style()
                    style.configure('Custom.TCombobox', padding=(5, 5, 5, 5))
                    # Năm Học
                    
                    search_year = ttk.Combobox(search_frame, values=year_options, state="readonly", width=20, style='Custom.TCombobox', height=25)
                    search_year.pack(side=LEFT, padx=10, pady=10)
                    # Học Kỳ
                    search_sem = ttk.Combobox(search_frame, values=list(se_options.keys()), state="readonly", width=20, style='Custom.TCombobox', height=25)
                    search_sem.pack(side=LEFT, padx=10, pady=10)
                    # Đặt giá trị mặc định cho Combobox (tùy chọn)
                    search_year.set("Chọn Năm Học")
                    search_sem.set("Chọn Học Kỳ")
                    #btn
                    button_frame = Frame(search_frame, bg="#577B8D")
                    button_frame.pack(side=LEFT)

                    search_button = Button(button_frame, text="Search", bg="#134B70", fg="#FDFFE2", font=("Times New Roman", 15), width= 5, command= search_by_year_se)
                    search_button.pack(side=LEFT, padx=(20, 5))
                    clear_btn = Button(button_frame , text="Clear", bg="#134B70", fg="#FDFFE2", font=("Times New Roman", 15), width= 5, command= clear)
                    clear_btn.pack(side=LEFT)

                    # Width of the frame and offsets to center the widgets
                    frame_width1 = 600
                    label_width = 130  # approximate width of the label in pixels
                    entry_width = 200  # approximate width of the entry in pixels
                    gap = 20  # gap between label and entry

                    # Calculating the x position to center the widgets
                    x_label = (frame_width1 - (label_width + entry_width + gap)) // 2
                    x_entry = x_label + label_width + gap

                    # Treeview for display create class widget
                    Label_Frame = Frame(frame2, bg="#134B70")
                    Label_Frame.pack(side=TOP, pady=(10, 10))

                    lb = Label(Label_Frame, text="Tạo Nhóm Học Phần", bg="#134B70", fg="#FDFFE2", font=("Times New Roman", 20, "bold"), padx=15, pady=15, borderwidth=5, relief=RIDGE)
                    lb.pack()

                    form_frame = Frame(frame2, bg = "#577B8D")
                    form_frame.pack(fill=BOTH, expand=True, padx=10, pady=(10, 50))  # Thêm padding phía dưới
                    lb1 = Label(form_frame, text="Mã Học Phần", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb1.place(x=x_label, y=50)
                    ipt1 = Entry(form_frame, state="disabled", textvariable = co_code, width=35, font=("italic", 13, "bold"))
                    ipt1.place(x=x_entry, y=50)

                    lb2 = Label(form_frame, text="Tên Học Phần", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb2.place(x=x_label, y=100)
                    ipt2 = Entry(form_frame, state="disabled", textvariable = co_name, width=35, font=("italic", 12, "bold"))
                    ipt2.place(x=x_entry, y=100)

                    lb3 = Label(form_frame, text="Năm Học", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb3.place(x=x_label, y=150)
                    ipt3 = Entry(form_frame, state="disabled",  textvariable = school_year, width=35, font=("italic", 12, "bold"))
                    ipt3.place(x=x_entry, y=150)

                    lb4 = Label(form_frame, text="Học Kỳ", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb4.place(x=x_label, y=200)
                    ipt4 = Entry(form_frame, state="disabled", textvariable = se, width=35, font=("italic", 12, "bold"))
                    ipt4.place(x=x_entry, y=200)
                    
                    lb5 = Label(form_frame, text="Chọn Nhóm", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb5.place(x=x_label, y=250)

                    class_options = ["M01", "M02", "M03", "M04"]
                    ipt5 = ttk.Combobox(form_frame, values=class_options, state="readonly", width=33, font=("italic", 13, "bold"))
                    ipt5.set("Chọn Nhóm")
                    ipt5.place(x=x_entry , y=250)  

                    lb6 = Label(form_frame, text="Nhập Số Lượng", bg="#577B8D", fg="#FDFFE2", font=("italic", 13, "bold"))
                    lb6.place(x=x_label, y=300)
                    ipt6 = Entry(form_frame, width=35, font=("italic", 13, "bold"))
                    ipt6.place(x=x_entry, y=300)


                    button_frame1 = Frame(frame2, bg="#577B8D")
                    button_frame1.pack(fill=X, side=BOTTOM, padx=10, pady=10)
                    clear_Class = Button(button_frame1, text="Clear", bg="#134B70", fg="#FDFFE2", font=("Times New Roman", 15), width=5, command=clear_data)
                    clear_Class.pack(side=RIGHT, padx=(0, 10))
                    # # Submit Btn
                    submit_btn = Button(button_frame1, text="Submit", bg="#134B70", fg="#FDFFE2", font=("Times New Roman", 15), width= 7, command= submit_data)
                    submit_btn.pack(side=RIGHT, padx=(0, 10))
                    
                    # Define the headings
                    for col in columns:
                        table1.heading(col, text=col)
                        table1.column(col, width=150)
                    
                    # Set specific headings and column widths
                    table1.heading("course_code", text="Mã Học Phần", anchor='w')
                    table1.heading('course_name', text="Tên Học Phần", anchor='w')
                    table1.heading("ay_schoolYear", text="Năm Học", anchor='w')
                    table1.heading("se_ID", text="Học Kỳ", anchor='w')

                    table1.column("course_code", width=100, anchor='w')
                    table1.column("course_name", width=250, anchor='w')
                    table1.column("ay_schoolYear", width=100, anchor='w')
                    table1.column("se_ID", width=100, anchor='w')

                    

                    # Focus Data
                    table1.bind("<<TreeviewSelect>>", focus_data)

                    
                    # Initial call to display to populate the table
                    display()

                    # Run the main loop
                    first.mainloop()
##############################################################################################################################################################

######################################################### Function to collect dataset ########################################################################
                def collect_dataset():
                    try:
                        conn = pymysql.connect(host = "localhost", user = "root", password =password_db, database = "face_recognition")
                        cur = conn.cursor()
                        collect_window = Toplevel()
                        collect_window.state('zoomed')
                        collect_window.configure(bg="#ccd9de")
                        collect_window.title("Manage Student Data")
                        print("Hi "+ str(username_var.get()))
                        face = Label(collect_window, text = "Management of Student" , bg = "#134B70" , fg="#FDFFE2", padx = 10, pady = 10, font = ("Times New Roman", 14, "bold") ,borderwidth = 5, relief = RIDGE).place(x = 180, y = 90)
                        cap = cv2.VideoCapture(0)
                        
                        #Back button
                        def back():
                            if cap:
                                cap.release()
                            collect_window.destroy()
                            
                        backbtn = Button(collect_window, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, command=back)
                        backbtn.place(x=1380, y=20)
                        
                        #All Required variables for database
                        scode_var = StringVar()
                        sname_var = StringVar()
                        smail_var = StringVar()
                        sclass_var = StringVar()
                        search_code = StringVar()
                        search_class = StringVar()
                        dataset_dir = os.path.join(root_dir,'face-db')

                        ##### Write the images collected to the created folder #####
                        def add_photos():
                            conn = pymysql.connect(host = "localhost", user = "root", password =password_db, database = "face_recognition")
                            cur1 = conn.cursor()
                            query = "SELECT st_code FROM students WHERE st_code = %s"
                            cur1.execute(query, (scode_var.get(),))
                            result = cur1.fetchone()
                            display()
                            if scode_var.get() == "":
                                messagebox.showerror("Error","Student Code is required!", parent = collect_window)
                            else:
                                # phone_url = 'http://192.168.1.3:8080/video'
                                cap = cv2.VideoCapture(0)
                                # Desired dimensions
                                width = 2568
                                height = 1926
                                query = "SELECT COUNT(*) FROM students WHERE st_code = %s"
                                cur.execute(query, (scode_var.get(),))
                                result = cur.fetchone()
                                if result and result[0] > 0:
                                    print("Student code exists. Proceed with adding photos.")
                                    code =scode_var.get()
                                    input_directory = os.path.join(dataset_dir,f'{code}')
                                    
                                    if not os.path.exists(input_directory):
                                        os.makedirs(input_directory, exist_ok = True)
                                        total_images_per_angle = 10
                                        count = 0
                                        print("[INFO] Starting collect data...")   

                                        for angle in angles:
                                            q = messagebox.askyesno("Instructions", instructions[angle], parent = collect_window)
                                            if not q:
                                                messagebox.showwarning("Close the window", "No data is collected!", parent = collect_window)
                                                shutil.rmtree(input_directory)
                                                break
                                            else:
                                                angle_count = 0
                                                while angle_count < total_images_per_angle:
                                                    ret, frame = cap.read() 
                                                    if not ret: 
                                                        break
                                                    # resized_frame = cv2.resize(frame, (width, height))
                                                    faces = detector(frame)
                                                    for face in faces:
                                                        file_name_path = f"{input_directory}/img{count}.jpg"
                                                        cv2.imwrite(file_name_path, frame)
                                                        x, y, w, h = face.left(), face.top(), face.width(), face.height()
                                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                        angle_count += 1
                                                        count += 1
                                                        cv2.putText(frame, str(count), (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 3)
                                                        print(f"Captured image {count} for {angle} angle.")
                                                        cv2.namedWindow('Face Detecting', cv2.WINDOW_NORMAL)
                                                        cv2.setWindowProperty('Face Detecting', cv2.WND_PROP_TOPMOST, 1)
                                                        cv2.imshow('Face Detecting',frame)
                                                        key = cv2.waitKey(1)
                                                        if key == ord('q') or count == 50:
                                                            messagebox.showinfo("Success", "All photos are collected", parent=collect_window)
                                                            break
                                        cap.release()
                                        cv2.destroyAllWindows()
                                        conn.close()
                                    else:
                                        if len(os.listdir(input_directory)) == 50:
                                            messagebox.showwarning("Error","Photo already added for this user. Click Update to update photo",parent = collect_window)
                                        else:
                                            ques = messagebox.askyesnocancel("Notification","Directory already exists with incomplete samples. Do you want to delete the directory", parent = collect_window)
                                            if (ques == True):
                                                shutil.rmtree(input_directory)
                                                messagebox.showinfo("Success", "Directory Deleted! Now you can add the photo samples", parent = collect_window) 
                                else:
                                    messagebox.showerror("Error", f"Student code {scode_var.get()} does not exist in the database.")

                        ##### Display the data of Student #####
                        def display():
                            conn = pymysql.connect(host = "localhost", user = "root", password =password_db, database = "face_recognition")
                            cur = conn.cursor()
                            cur.execute("select st_code, st_fullName, st_email, cl_className from students")
                            data = cur.fetchall()
                            if len(data)!= 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values = row)
                                conn.commit()
                            conn.close()
                            ########################################### To clear the data
                        
                        ##### Clear the data in text field area #####
                        def clear():
                            scode_var.set("")
                            sname_var.set("")
                            smail_var.set("")
                            sclass_var.set("")
                            search_class.set("")
                            search_code.set("")
                        
                        ##### Display the selected items in text field area #####
                        def focus_data(event):
                            cursor = table1.focus()
                            contents = table1.item(cursor)
                            row = contents['values']
                            if(len(row) != 0):
                                scode_var.set(row[0])
                                sname_var.set(row[1])
                                smail_var.set(row[2])
                                sclass_var.set(row[3])

                        
                        ##### Update the photos if the directory already exists with complete samples #####
                        def update_photos():
                            if scode_var.get() == "":
                                messagebox.showerror("Error","Ensure that Student Code are existed!", parent = collect_window)
                            else:
                                phone_url = 'http://192.168.1.3:8080/video'
                                cap = cv2.VideoCapture(phone_url)
                                # cap = cv2.VideoCapture(0)
                                code =scode_var.get()
                                input_directory = os.path.join(dataset_dir,f'{code}')
                                if os.path.exists(input_directory):
                                    q = messagebox.askyesno("Notification","Do you want to update the photo samples?", parent = collect_window)
                                    if (q == True):
                                        old_input_directory = os.path.join(dataset_dir,f'{code}')
                                        shutil.rmtree(old_input_directory) 
                                        new_input_directory = os.path.join(dataset_dir,f'{code}')
                                        os.mkdir(new_input_directory)
                                        total_images_per_angle = 10
                                        count = 0
                                        print("[INFO] Starting collect data...")   
                                        
                                        for angle in angles:
                                            q = messagebox.askyesno("Instructions", instructions[angle], parent = collect_window)
                                            if not q:
                                                messagebox.showwarning("Close the window", "No data is collected!", parent = collect_window)
                                                shutil.rmtree(input_directory)
                                                break
                                            else:
                                                angle_count = 0
                                                while angle_count < total_images_per_angle:
                                                    ret, frame = cap.read() 
                                                    if not ret: 
                                                        break
                                                    faces = detector(frame)
                                                    for face in faces:
                                                        file_name_path = f"{input_directory}/img{count}.jpg"
                                                        cv2.imwrite(file_name_path, frame)
                                                        x, y, w, h = face.left(), face.top(), face.width(), face.height()
                                                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                                        angle_count += 1
                                                        count += 1
                                                        cv2.putText(frame, str(count), (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 3)
                                                        print(f"Captured image {count} for {angle} angle.")
                                                        cv2.namedWindow('Face Detecting', cv2.WINDOW_NORMAL)
                                                        cv2.setWindowProperty('Face Detecting', cv2.WND_PROP_TOPMOST, 1)
                                                        cv2.imshow('Face Detecting',frame)
                                                        key = cv2.waitKey(1)
                                                        if key == ord('q') or count == 50:
                                                            messagebox.showinfo("Success", "All photos are collected", parent=collect_window)
                                                            break
                                        cv2.destroyAllWindows()
                                        conn.close()
                                        messagebox.showinfo("Success", "All photos are collected", parent=collect_window)
                                else:
                                    messagebox.showerror("Error","Photo samples for this student did not exist. Please click add to collect photos!", parent = collect_window)

                        ##### Delete directory already exists with incomplete samples #####
                        def delete_photos():
                            if scode_var.get() == "":
                                messagebox.showerror("Error","Student Code is required!", parent = collect_window)
                            else:
                                code = scode_var.get()
                                sclass = sclass_var.get()
                                folder = os.path.join(dataset_dir,f'{code}')
                                if not os.path.exists(folder):
                                    messagebox.showerror("Error",f'Folder {code} does not exist!', parent = collect_window)
                                else:
                                    shutil.rmtree(folder)
                                    messagebox.showinfo("Success",f"Folder {code} and all its photos have been deleted!", parent = collect_window)
                                display()

                        ##### Search student's information #####
                        def search_data():
                            conn = pymysql.connect(host = "localhost", user = "root", password =password_db, database = "face_recognition")
                            cur = conn.cursor()
                            if search_code.get()=="":
                                cur.execute("select st_code, st_fullName, st_email, cl_className from students where cl_className = %s", (search_class.get(),))
                            elif search_class.get()=="":
                                cur.execute("select st_code, st_fullName, st_email, cl_className from students where st_code = %s", (search_code.get(),))
                            else:
                                cur.execute("select st_code, st_fullName, st_email, cl_className from students where st_code = %s and cl_className=%s", (search_code.get(),search_class.get()))
                            data = cur.fetchall()
                            if len(data)!= 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values = row)
                                conn.commit()
                            else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent = collect_window)
                            conn.close()
                            clear()

                        ##### Show All Data #####
                        def show_data():
                            display()
                        
                        ##### Update 'students' table in MySQL #####
                        def update_db():
                            conn = pymysql.connect(host = "localhost", user = "root", password =password_db, database = "face_recognition")
                            cur = conn.cursor()
                            if sname_var.get()=="" or smail_var.get() =="" or sclass_var.get()=="":
                                messagebox.showerror("Error","All fields are Required", parent = collect_window)
                            else:
                                q = messagebox.askyesno("Update", "Do you want to save this?",parent = collect_window)
                                if q:
                                    if (re.search('[a-zA-Z]+', sname_var.get())):
                                        code = scode_var.get()
                                        mail = smail_var.get()
                                        name = sname_var.get()
                                        sclass = sclass_var.get()
                                        regex = '^[a-zA-Z]+[Bb]\d{7}@student\.ctu\.edu\.vn'
                                        if(re.search(regex, mail)):
                                            cur.execute("update students set st_fullName = %s, st_email = %s, cl_className = %s where st_code = %s",(name, mail, sclass,code))
                                            conn.commit()
                                            display()
                                            conn.close()
                                            messagebox.showinfo("Success", "Database updated successfully", parent = collect_window) 
                                        else:
                                            messagebox.showerror('Error','Please Enter the Valid Email Address', parent = collect_window)
                                    else:
                                        messagebox.showerror('Error', 'Full Name must be String Character', parent = collect_window)
                                else:
                                    messagebox.showinfo("Cancelled", "Update operation cancelled.", parent=collect_window)

                        ############################################# Student Management form ##############################################################
                        ##### Small Frame #####
                        small_frame = Frame(collect_window, bg = "#577B8D",borderwidth = "3", relief = SUNKEN, height = 620, width = 530)
                        small_frame.place(x = 25, y = 170)

                        code_label = Label(small_frame, text = "Student Code", bg = "#577B8D", fg="#FDFFE2", font = ("italic",13, "bold")).place(x = 69, y = 115 )
                        code_entry = Entry(small_frame,state="disabled", width = 23, textvariable = scode_var,  font = ("italic",13, "bold")).place(x =243, y = 115)

                        name_label = Label(small_frame, text = "Full Name", bg = "#577B8D",fg="#FDFFE2", font = ("italic",13, "bold")).place(x =69, y = 175)
                        name_entry = Entry(small_frame, width = 23, textvariable = sname_var , font = ("italic",12, "bold")).place(x = 243, y = 175)

                        class_label = Label(small_frame, text = "Class Name", bg = "#577B8D",fg="#FDFFE2", font = ("italic",12, "bold")).place(x = 69, y= 235)
                        class_entry = Entry(small_frame, width = 23, textvariable = sclass_var , font = ("italic",12, "bold")).place(x = 243, y = 235)
                        
                        email_label = Label(small_frame, text = " Email Address", bg = "#577B8D", fg="#FDFFE2", font = ("italic",12, "bold")).place(x = 69, y = 295)
                        email_entry = Entry(small_frame, width = 23, textvariable = smail_var , font = ("italic",12, "bold") ).place(x = 243, y = 295)

                        save_btn = Button(small_frame, text = "Change Info", bg = "#40679E",fg="#FDFFE2", height = "1", width = "16", command=update_db, font = ("Times new Roman", 14 , "bold")).place(x = 270, y = 375)
                        add_btn = Button(small_frame, text = "Add", bg = "#40679E",fg="#FDFFE2", height = "1", width = "7",command = add_photos, font = ("Times new Roman", 14 , "bold")).place(x = 69, y = 455)
                        update_btn = Button(small_frame, text = "Update", bg = "#40679E",fg="#FDFFE2", height = "1", width = "7",command=update_photos, font = ("Times new Roman", 14 , "bold")).place(x = 169, y = 455)
                        delete_btn = Button(small_frame, text = "Delete", bg = "#40679E",fg="#FDFFE2",  height = "1", width = "7", command=delete_photos, font = ("Times new Roman", 14 , "bold")).place(x = 269, y = 455)
                        clear_btn = Button(small_frame, text = "Clear", bg = "#40679E",fg="#FDFFE2", height = "1", width = "7",command = clear,  font = ("Times new Roman", 14 , "bold")).place(x = 369, y = 455)
                        
                        
                        ##### Large Frame #####
                        large_frame = Frame(collect_window, height = 700, width = 890, bg = "#577B8D", borderwidth = "3", relief = SUNKEN)
                        large_frame.place(x = 580, y = 90)
                        Label(collect_window, text = "Search By:",font = ("times new roman", 18 ,"bold"),bg = "#577B8D", fg="#FDFFE2").place(x = 605, y = 115 )
                        
                        classID = ttk.Combobox(collect_window, textvariable = search_class, values = ["DI21V7F1","DI21V7F2","DI21V7F3","DI21V7F4"], state = "readonly", width = 16, font = ("times new Roman",14))
                        classID.place(x = 750, y = 118)
                        classID.bind("<Return>", lambda event: search_data())
                        
                        search_field = Entry(collect_window, textvariable = search_code, width = 20, font = ("times new Roman",14) )
                        search_field.place(x = 950, y = 118)
                        search_field.bind("<Return>", lambda event: search_data())

                        search_btn = Button(collect_window,  text = "Search ",bg = "#40679E",fg="#FDFFE2", height = "1", width = "10",command = search_data, font = ("Times new Roman", 14 , "bold")).place(x = 1180, y = 110 ) 
                        show_btn = Button(collect_window, text = "Show All",bg = "#40679E",fg="#FDFFE2",  height = "1", width = "10",command = show_data ,font = ("Times new Roman", 14 , "bold")).place(x = 1322, y = 110)
                    
                        ##### Table frame #####
                        table_frame = Frame(large_frame, bg = "#577B8D", borderwidth = "2", relief = SUNKEN)
                        table_frame.place(x = 25, y = 75, height = 595, width = 835 )
                        style = ttk.Style()
                        # Configure the Treeview heading style
                        style.configure("Treeview.Heading", foreground="#201E43",font=('times new Roman', 14, 'bold'))
                        scroll_x =Scrollbar(table_frame, orient = HORIZONTAL)
                        scroll_y = Scrollbar(table_frame, orient = VERTICAL)
                        table1 = ttk.Treeview(table_frame, columns = ("st_code","st_fullName", "st_email","cl_className"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
                        scroll_x.pack(side = BOTTOM, fill = X )
                        scroll_y.pack(side = RIGHT, fill = Y)
                        scroll_x.config(command = table1.xview)
                        scroll_y.config(command = table1.yview)
                        table1.heading("st_code", text ="Student Code",anchor='w')
                        table1.heading('st_fullName', text = "Full Name",anchor='w')
                        table1.heading("st_email",text = "Email Address",anchor='w')
                        table1.heading("cl_className", text = "Class",anchor='w')
                        table1['show'] = 'headings'
                        table1.column("st_code", width = 50,anchor='w')
                        table1.column("st_fullName", width = 119, anchor='w')
                        table1.column("st_email", width = 150, anchor='w')
                        table1.column("cl_className", width = 50, anchor='w')
                        table1.pack(fill = BOTH, expand = True)
                        table1.bind("<ButtonRelease-1>", focus_data)
                        display()
                        collect_window.mainloop()
                        cv2.destroyAllWindows()
                    except pymysql.err.OperationalError as e:
                        messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error","Close all the windows and restart your program")
##############################################################################################################################################################

######################################################### Function to display photo samples ##################################################################
                def photo_samples():
                    try:
                        conn = pymysql.connect(host = "localhost", user = "root", password=password_db, database = "face_recognition")
                        cur = conn.cursor()
                        photo_window = Toplevel()
                        photo_window.state('zoomed')
                        photo_window.configure(bg="#ccd9de")
                        photo_window.title("Display Photo Samples")
                        face = Label(photo_window, text = "Photo Samples" , bg = "#134B70" , fg="#FDFFE2", padx = 10, pady = 10, font = ("Times New Roman", 14, "bold") ,borderwidth = 5, relief = RIDGE).place(x = 680, y = 13)
                        
                        def back():
                            photo_window.destroy()
                        backbtn = Button(photo_window, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, command=back)
                        backbtn.place(x=1380, y=20)
                        
                        #All Required variables for database
                        scode_var = StringVar()
                        sname_var = StringVar()
                        sclass_var = StringVar()
                        search_result = StringVar()
                        search_from = StringVar()
                        dataset_dir = os.path.join(root_dir,'face-db')

                        ##### Display the student's information #####
                        def display():
                            conn = pymysql.connect(host = "localhost", user = "root", password=password_db, database = "face_recognition")
                            cur = conn.cursor()
                            selected_class = search_from.get()
                            if selected_class == "Show All" or selected_class=="":
                                search_from.set("Show All")
                                cur.execute("select st_code, st_fullName, cl_className from students")
                                
                            else:
                                query = "SELECT st_code, st_fullName, cl_className FROM students WHERE cl_className = %s"
                                cur.execute(query, (selected_class,))
                            data = cur.fetchall()
                            if len(data)!= 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values = row)
                                conn.commit()
                            conn.close()

                        ##### Clear the data in text field area #####
                        def clear():
                            scode_var.set("")
                            sname_var.set("")
                            sclass_var.set("")
                            search_from.set("")
                            search_result.set("")
                            for widget in scrollable_frame.winfo_children():
                                widget.destroy()

                        ##### Display the selected items in text field area #####
                        def focus_data(event):
                            cursor = table1.focus()
                            contents = table1.item(cursor)
                            row = contents['values']
                            if(len(row) != 0):
                                scode_var.set(row[0])
                                sname_var.set(row[1])
                                sclass_var.set(row[2])

                        ##### Search student info #####
                        def search_data():
                            conn = pymysql.connect(host = "localhost", user = "root", password=password_db, database = "face_recognition")
                            cur = conn.cursor()
                            if search_from.get()=="" or search_from.get()=="Show All":
                                cur.execute("select st_code, st_fullName, cl_classname from students where st_code = %s", (search_result.get(),))
                            else:
                                cur.execute("select st_code, st_fullName, cl_className from students where st_code = %s and cl_className=%s", (search_result.get(),search_from.get()))
                            data = cur.fetchall()
                            if len(data)!= 0:
                                table1.delete(*table1.get_children())
                                for row in data:
                                    table1.insert('', END, values = row)
                                conn.commit()
                            else:
                                messagebox.showinfo('Sorry', 'No Data Found', parent = photo_window)
                            conn.close()
                            clear()

                        ##### Choose student code to display #####
                        def choose_student_code():
                            student_code = scode_var.get()
                            if student_code:
                                display_photos(student_code)
                            else:
                                messagebox.showerror("Error", "Please enter a student code", parent = photo_window)
                        
                        ##### Display photo samples by student code #####
                        def display_photos(student_code):
                            input_directory = os.path.join(dataset_dir, student_code)
                            if not os.path.exists(input_directory):
                                messagebox.showerror("Error", f"No data for {student_code}", parent = photo_window)
                                return
                            
                            # Clear any existing widgets in the scrollable frame
                            for widget in scrollable_frame.winfo_children():
                                widget.destroy()

                            img_list = os.listdir(input_directory)
                            row, col = 0, 0
                            image_references = []
                            
                            for idx, img_file in enumerate(img_list):
                                img_path = os.path.join(input_directory, img_file)
                                
                                # Open and resize the image
                                img = Image.open(img_path)
                                img = img.resize((256, 192), Image.LANCZOS)  # Adjust size to fit within the frame
                                img = ImageTk.PhotoImage(img)
                                
                                # Display the image in the frame
                                panel = Label(scrollable_frame, image=img)  # type: ignore
                                panel.image = img  # type: ignore # Keep a reference to avoid garbage collection
                                panel.grid(row=row, column=col, padx=5, pady=5)

                                # Rename the image for display purposes
                                display_name = f"Photo {idx+1}"  # Rename for display, e.g., Photo 1, Photo 2, etc.
                                label = Label(scrollable_frame, text=display_name)
                                label.grid(row=row+1, column=col, padx=5, pady=5)

                                col += 1
                                if col == 3:
                                    col = 0
                                    row += 2

                                image_references.append(img)

##################################################################### Student Management form ###############################
                        small_frame = Frame(photo_window, bg = "#577B8D",borderwidth = "3", relief = SUNKEN, height = 750, width = 530)
                        small_frame.place(x = 20, y = 80)
                        l1 = Label(small_frame, text = "Search By:",font = ("times new roman", 20 ,"bold"),bg = "#577B8D", fg="#FDFFE2").place(x = 25, y = 44 )
                        
                        c1 = ttk.Combobox(small_frame, textvariable = search_from, values = ["DI21V7F1","DI21V7F2","DI21V7F3","DI21V7F4", "Show All"], state = "readonly", width =16)
                        c1.place(x = 160, y = 54)
                        c1.bind("<Return>", lambda event: display())
                        
                        search_code = Entry(small_frame, textvariable = search_result, width = 21, font = ("times new Roman",14) )
                        search_code.place(x = 304, y = 50)
                        search_code.bind("<Return>", lambda event: search_data())
                        
                        ################################################################################## Table frame
                        table_frame = Frame(small_frame, bg = "#FDFFE2", borderwidth = "2", relief = SUNKEN)
                        table_frame.place(x = 25, y = 95, height = 620, width = 473 )
                        style = ttk.Style()
                        # Configure the Treeview heading style
                        style.configure("Treeview.Heading", 
                                        foreground="#201E43",  # Text color
                                        font=('times new Roman', 13, 'bold'))  # Font style
                        scroll_x =Scrollbar(table_frame, orient = HORIZONTAL)
                        scroll_y = Scrollbar(table_frame, orient = VERTICAL)
                        table1 = ttk.Treeview(table_frame, columns = ("st_code","st_fullName", "cl_className"), xscrollcommand = scroll_x.set, yscrollcommand = scroll_y.set)
                        scroll_x.pack(side = BOTTOM, fill = X )
                        scroll_y.pack(side = RIGHT, fill = Y)
                        scroll_x.config(command = table1.xview)
                        scroll_y.config(command = table1.yview)
                        table1.heading("st_code", text ="Student Code",anchor='w')
                        table1.heading('st_fullName', text = "Full Name",anchor='w')
                        table1.heading("cl_className", text = "Class",anchor='w')
                        table1['show'] = 'headings'
                        table1.column("st_code", width = 50,anchor='w')
                        table1.column("st_fullName", width = 119, anchor='w')
                        table1.column("cl_className", width = 50, anchor='w')

                        table1.pack(fill = BOTH, expand = True)
                        table1.bind("<ButtonRelease-1>", focus_data)
                        display()
                    ################################################################################### Large Frame
                        large_frame = Frame(photo_window, height = 750, width = 905, bg = "#577B8D", borderwidth = "3", relief = SUNKEN)
                        large_frame.place(x = 565, y = 80)
                        
                        stcode = Label(large_frame, text = "Student Code", bg = "#577B8D", fg="#FDFFE2", font = ("italic",14, "bold")).place(x = 25, y = 20 )
                        name = Label(large_frame, text = "Full Name", bg = "#577B8D",fg="#FDFFE2", font = ("italic",14, "bold")).place(x =225, y = 20)
                        classname = Label(large_frame, text = "Class Name", bg = "#577B8D",fg="#FDFFE2", font = ("italic",14, "bold")).place(x = 470, y= 20)
                        
                        E1 = Entry(large_frame,state="disabled", width = 18, textvariable = scode_var,  font = ("italic",12, "bold")).place(x =25, y = 50)
                        E2 = Entry(large_frame,state="disabled", width = 23, textvariable = sname_var , font = ("italic",12, "bold")).place(x = 225, y = 50)
                        E3 = Entry(large_frame, state="disabled",width = 18, textvariable = sclass_var , font = ("italic",12, "bold")).place(x = 470, y = 50)
                        
                        show_photo = Button(large_frame, text = "Display", bg = "#40679E",fg="#FDFFE2", height = "1", width = "7",command = choose_student_code,  font = ("Times new Roman", 14 , "bold")).place(x = 680, y = 40)
                        clear_btn = Button(large_frame, text = "Clear", fg='#E7F6F2', bg='#2C3333', height = "1", width = "7",command = clear,  font = ("Times new Roman", 14 , "bold")).place(x = 790, y = 40)
                        ##########################################################################Photo Frame
                        photo_frame = Frame(large_frame, bg = "white", borderwidth = "2", relief = SUNKEN)
                        photo_frame.place(x = 25, y = 95, height = 620, width = 850 )
                        # Create a vertical scrollbar
                        scroll_y = Scrollbar(photo_frame, orient=tk.VERTICAL)
                        
                        # Create a canvas and attach the scrollbar to it
                        canvas = tk.Canvas(photo_frame, yscrollcommand=scroll_y.set)
                        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                        
                        # Create a frame inside the canvas
                        scrollable_frame = Frame(canvas)
                        
                        # Bind the canvas configuration to update the scroll region
                        scrollable_frame.bind(
                            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
                        )
                        
                        # Add the frame to the canvas window
                        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

                        # Pack the scrollbar and configure its command
                        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
                        scroll_y.config(command=canvas.yview)
                        
                        def on_mouse_wheel(event):
                            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                            
                        # Bind mouse wheel event to canvas
                        def bind_mouse_wheel(event):
                            canvas.bind_all("<MouseWheel>", on_mouse_wheel)

                        def unbind_mouse_wheel(event):
                            canvas.unbind_all("<MouseWheel>")

                        # Bind mouse wheel event to canvas only when mouse is in photo_frame
                        photo_frame.bind("<Enter>", bind_mouse_wheel)
                        photo_frame.bind("<Leave>", unbind_mouse_wheel)
                        
                        photo_window.mainloop()
                    except pymysql.err.OperationalError as e:
                        messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error","Close all the windows and restart your program")
##############################################################################################################################################################

######################################################### Function to recognize faces and take attendance ####################################################
                def face_recognize():
                    try:
                        conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")

                        # Hàm lấy dữ liệu về học phần - lớp
                        def search_course():
                            conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                            cur = conn.cursor()
                            try:
                                cur.execute("select cfa_ID, course_code from courseFollowAcaYear where course_code LIKE '%_H';;")
                                cfa_data = cur.fetchall()
                            finally:
                                conn.close()
                            course_options = {c_code: c_id for c_id, c_code in cfa_data}
                            return course_options
                        
                        def search_class(event=None):
                            conn = pymysql.connect(host="localhost", user="root", password=password_db, database="face_recognition")
                            cur = conn.cursor()
                            
                            try:
                                c_id = course_options.get(course_combobox.get())
                                # Ensure c_id is not None and can be converted to an integer
                                if c_id is not None:
                                    cour_id = int(c_id)
                                    print(f"cour_id: {cour_id}")  # Debug: Check the value of cour_id
                                    print(type(cour_id))  # Debug: Ensure cour_id is an integer
                                
                                cur.execute('''SELECT clCourse_ID, cl.clCourse_code
                                            FROM classCourse cl 
                                            JOIN courseFollowAcaYear cfa ON cl.cfa_ID = cfa.cfa_ID
                                            JOIN courses c ON cfa.course_code = c.course_code
                                            WHERE cl.cfa_ID = "%s" ''', (cour_id,))
                                class_data = cur.fetchall()
                            except Exception as e:
                                print(f"Error in search_class: {e}")
                                print(f"Error type: {type(e)}")
                                print(f"Error args: {e.args}")
                                class_combobox.set("Lỗi khi tìm kiếm")
                                return
                            finally:
                                cur.close()

                            if class_data:
                                class_options = {cl_code: cl_id for cl_id, cl_code in class_data}
                                class_combobox.config(values=list(class_options.keys()))
                            else:
                                class_options = ["No class yet"]
                                class_combobox.config(values=class_options)
                            return class_options
                        
                        # Initialize camera capture object
                        cap = cv2.VideoCapture(0)  

                        def update_json_with_excel_path(course_code: str, group_code: str, json_path: str = 'attendance_info.json'):
                            """
                            Update the JSON file with a new Excel file path each time this function is called.
                            """
                            try:
                                # Create a directory to store the attendance files
                                directory = 'attendance_files'
                                if not os.path.exists(directory):
                                    os.makedirs(directory)

                                # Generate a timestamped filename
                                date_att = datetime.now().strftime('%d-%m-%Y')
                                file_name = f'{course_code}_{group_code}_{date_att}.xlsx'
                                file_path = os.path.join(directory, file_name)

                                # Create a new Excel file
                                workbook = openpyxl.Workbook()
                                sheet = workbook.active
                                if sheet is not None:
                                    sheet.title = "Sheet"
                                    sheet['A1'] = course_code
                                    sheet['B1'] = group_code
                                    sheet['C1'] = date_att
                                    sheet['A2'] = 'Student'
                                    sheet['B2'] = 'Time'
                                
                                workbook.save(file_path)
                                # Update JSON file with the new file path
                                data = {"attendance_file_path": file_path}
                                with open(json_path, 'w') as json_file:
                                    json.dump(data, json_file)

                                print(f"New Excel file created at {file_path} and JSON updated.")

                                return file_path

                            except Exception as e:
                                print(f"Error creating Excel file or updating JSON: {str(e)}")
                                messagebox.showerror("Error", f"Error creating Excel file or updating JSON: {str(e)}")

                        def mark_attendance():
                            """
                            This function handles the creation of a new Excel file with the course and group data
                            and updates the JSON file with the new Excel file path.
                            """
                            course_code = course_combobox.get()
                            group_code = class_combobox.get()

                            if course_code == "Choose Course" or course_code == "" or group_code == "Choose Group" or group_code == "":
                                messagebox.showerror("Error", "Please select both a course and a group!", parent = face_window)
                                return

                            # Update the Excel file path in JSON and save course and group data
                            excel_file_path = update_json_with_excel_path(course_code, group_code)

                            # Continue with face recognition stream (or any other action)
                            face_analysis.stream(
                                db_path="face-db",
                                enable_face_analysis=False,
                                model_name="ArcFace",
                                detector_backend="retinaface",
                                anti_spoofing=False,
                                source=0,
                            )

                        face_window = Toplevel()
                        face_window.title("Face Recognizer Page")
                        face_window.state('zoomed')
                        face_window.configure(bg="#ccd9de")

                        def back():
                            face_window.destroy()

                        backbtn = Button(face_window, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, command=back)
                        backbtn.place(x=1380, y=70)
                        
                        title_label = Label(face_window, text="Face Recognizer Page", font=("times new roman", 25, "bold"), bg="#134B70", fg="#FDFFE2", bd=7, relief=GROOVE)
                        title_label.place(x=0, y=0, relwidth=1)

                        main_frame = Frame(face_window, bg="#EEEEEE")
                        main_frame.place(x=550, y=240)
                        
                        logo_icon = Image.open('./img/face-scanner.png').resize((100, 100), Image.Resampling.LANCZOS)
                        logo_img = ImageTk.PhotoImage(logo_icon, master=main_frame) # type: ignore
                        logo_label = Label(main_frame, image=logo_img, bd=0)
                        logo_label.grid(row=0, columnspan=3, pady=40, padx=40)

                        course_label = Label(main_frame, text="Courses", bg="#EEEEEE", compound=LEFT, font=("times new roman", 15, "bold"))
                        course_label.grid(row=1, column=0, padx=30, pady=5)
                        class_label = Label(main_frame, text="Classes", bg="#EEEEEE", compound=LEFT, font=("times new roman", 15, "bold"))
                        class_label.grid(row=2, column=0, padx=30, pady=5)
                        
                        course_options = search_course()
                        course_combobox = ttk.Combobox(main_frame, values=list(course_options.keys()), font=("times new roman", 12), state="readonly")
                        course_combobox.set("Choose Course")
                        course_combobox.grid(row=1, column=1, padx=10, pady=10)
                        course_combobox.bind('<<ComboboxSelected>>', search_class)

                        class_combobox = ttk.Combobox(main_frame, font=("times new roman", 12), state="readonly")
                        class_combobox.set("Choose Group")
                        class_combobox.grid(row=2, column=1, padx=20, pady=(20, 30))
                        
                        button_frame = Frame(main_frame)
                        button_frame.grid(row=3, column=1, padx=10, pady=(20, 10))

                        start_btn = Button(button_frame, text="Start", width=5, activebackground="#008DDA", activeforeground="white", font=("times new roman", 20, "bold"), relief=GROOVE, bg="#22577E", fg="#FDFFE2", command=mark_attendance)
                        start_btn.grid(row=3, column=1, padx=10)

                        Label(face_window, text="Press q to stop camera !", fg='red',bg="#ccd9de", font=("times new roman", 18, "bold")).place(x=1200, y=800)

                        def exit_window(event=None):
                            face_window.destroy()
                        
                        face_window.bind("<Escape>", exit_window)
                        face_window.mainloop()
                                        
                        cv2.destroyAllWindows()
                        # display()       
                    except pymysql.err.OperationalError as e:
                        messagebox.showerror("Error", "SQL Connection Error... Open XAMPP Control Panel and then start MySQL Server")
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Close all the windows and restart your program")
##############################################################################################################################################################

                ##### GUI for the main page #####
                window = tk.Tk()
                window.title("Attendance and Emotion Analysis System")
                window.configure(bg="#ccd9de")
                window.state("zoomed")

                lbl = tk.Label(window, text="Facial Recognition Based Automatic Attendance and Emotion Analysis System ", bg="#ccd9de" , fg="#134B70" , width=70 , height=2, font=('times', 25, 'italic bold')) 
                lbl.place(x=85, y=40)

                excel_img = ImageTk.PhotoImage(Image.open('./img/excel.png').resize((170, 170), Image.LANCZOS))
                import_btn = Button(window, image = excel_img, text = "Import Data",font = ("Times New Roman" , 16), fg = "#344C64", height =230, width = 255, compound = BOTTOM,command=import_data)
                import_btn.place(x = 105, y = 200)
                
                database_img = ImageTk.PhotoImage(Image.open('./img/add-database.png').resize((180, 170), Image.LANCZOS))
                create_btn = Button(window, image = database_img, text = "Create Class",font = ("Times New Roman" , 16), fg = "#344C64", height =230, width = 255, compound = BOTTOM, command=create_class)
                create_btn.place(x = 445, y = 200)
                
                collect_img = ImageTk.PhotoImage(Image.open('./img/collect.png').resize((180, 170), Image.LANCZOS))
                collect_btn = Button(window, image = collect_img, text = "Collect Dataset",font = ("Times New Roman" , 16), fg = "#344C64", height =230, width = 255, compound = BOTTOM, command=collect_dataset) 
                collect_btn.place(x = 785, y = 200)

                gallery_img = ImageTk.PhotoImage(Image.open('./img/gallery.png').resize((180, 170), Image.LANCZOS))
                gallery_btn = Button(window, image = gallery_img, text = "Photo Samples",font = ("Times New Roman" , 16), fg = "#344C64", height =230, width = 255, compound = BOTTOM, command=photo_samples) 
                gallery_btn.place(x = 1125, y = 200)

                attendance_img = ImageTk.PhotoImage((Image.open('./img/attendance.png')).resize((170, 160), Image.LANCZOS))
                recognize_btn = Button(window , image = attendance_img , text = "Face Recognition" , font = ("Times new roman", 16), fg = "#344C64" , height = 230, width= 235 , compound = BOTTOM, command=face_recognize) 
                recognize_btn.place(x = 105, y = 520)

                emotion_img = ImageTk.PhotoImage(Image.open('./img/emo.png').resize((170, 160), Image.LANCZOS))
                emotion_btn = Button(window, image = emotion_img , text = "Emotion Analysis", font = ("Times new roman", 16), fg = "#344C64", height = 230, width= 255, compound = BOTTOM )
                emotion_btn.place(x = 445, y = 520)

                report_img = ImageTk.PhotoImage(Image.open('./img/report.png').resize((170, 160), Image.LANCZOS))
                report_btn = Button(window, image = report_img , text = "Attendance Report", font = ("Times new roman", 16), fg = "#344C64", height = 230, width= 255, compound = BOTTOM ) 
                report_btn.place(x = 785, y = 520)

                admin_img = ImageTk.PhotoImage(Image.open('./img/admin.png').resize((170, 160), Image.LANCZOS))
                account_btn = Button(window, image = admin_img , text = "Admin Account", font = ("Times new roman", 16), fg = "#344C64", height = 230, width= 255, compound = BOTTOM ) 
                account_btn.place(x = 1125, y = 520)

                def exit(event=None):
                    window.destroy()
                window.bind("<Escape>", exit)
                window.mainloop()
                
        except pymysql.err.OperationalError as e:
            messagebox.showerror( "Error","Sql Connection Error... Open Xamp Control Panel and then start MySql Server ")
        except Exception as e:
            print(e)
            messagebox.showerror("Error","Close all the windows and restart your program")
            
def login_GUI():
    title = Label(face, text = "Admin Login Page" , font = ("times new roman", 25, "bold"), bg = "#134B70", fg="#FDFFE2", bd = 7, relief = GROOVE) 
    title.place(x = 0, y = 0, relwidth = 1)

    login_frame = Frame(face, bg="#EEEEEE")
    login_frame.place(x=550, y=240)
    logo_img = ImageTk.PhotoImage(Image.open('./img/admin.png').resize((100, 100), Image.LANCZOS))  
    logo_image = Label(login_frame, image=logo_img, bd=0).grid(row=0, columnspan=3, pady=40, padx=40)
    image_references = {}
    image_references['logo'] = logo_img

    user_img = ImageTk.PhotoImage(Image.open('./img/profile.png').resize((40, 40), Image.LANCZOS)) 
    image_references['user'] = user_img

    password_img = ImageTk.PhotoImage(Image.open('./img/locked.png').resize((40, 40), Image.LANCZOS))
    image_references['password'] = password_img
 
    user_label = Label(login_frame , text = "Username", image = user_img, bg= "#EEEEEE", compound = LEFT, font = ("times new roman", 15, "bold")).grid( row  = 1 , column = 0, padx = 30, pady = 5) 
    user_entry = Entry(login_frame, font = ("times new roman", 15, "bold"), relief = GROOVE, textvariable = username_var, bg = "lightgray").grid(row = 1, column= 1, padx= 10, pady = 5)
    password_label = Label(login_frame, text = "Password", image = password_img, bg ="#EEEEEE", compound = LEFT, font = ("times new roman", 15, "bold")).grid(row = 2, column = 0, padx = 30, pady = 5) 
    password_entry = Entry(login_frame, show = "*", font = ("times new roman", 15,"bold"), relief = GROOVE, textvariable = password_var, bg = "lightgray").grid(row = 2, column = 1, padx = 20, pady = 5)
    submit_btn = Button(login_frame, text = "Log In",width = 10, activebackground = "#008DDA", activeforeground = "white", command = login , font = ("times new roman", 20, "bold"),relief = GROOVE, bg = "#22577E", fg="#FDFFE2").grid(row = 3, column = 1, pady =25, padx = 25) 

    def exit(event=None):
        face.destroy()
    face.bind("<Escape>", exit)
    face.mainloop()

if __name__ == "__main__":
    login_GUI()