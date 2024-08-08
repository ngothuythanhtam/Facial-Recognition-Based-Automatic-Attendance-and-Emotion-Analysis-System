import tkinter as tk
from tkinter import filedialog
import pandas as pd
import pymysql
import unicodedata
import re
from tkinter import messagebox, Button, RIDGE, Label
from tkinter import *

# def remove_accents(input_str):
#     input_str = input_str.replace("Đ", "D").replace("đ", "d")
#     nfkd_str = unicodedata.normalize('NFKD', input_str)
#     no_accents_str = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
#     return re.sub(r'[^a-zA-Z0-9\s]', '', no_accents_str)

# def import_student(file_paths):
#     if not file_paths:
#         print("No files selected for import.")
#         return
    
#     conn = pymysql.connect(
#         user='root',
#         password='',
#         host='localhost',
#         database='face_recognition'
#     )
#     cur = conn.cursor()
    
#     try:
#         with cur:
#             for file_path in file_paths:
#                 df = pd.read_excel(file_path, sheet_name='Worksheet')

#                 # cols = ['STT', 'Điểm 10', 'Vi phạm quy chế', 'Phái', 'Khóa nhập điểm']
#                 # df.drop(cols, inplace=True, axis=1)

#                 df.rename(columns={
#                     'Lớp': 'cl_className',
#                     'Mã sinh viên': 'st_code',
#                     'Họ và Tên': 'st_fullName'
#                 }, inplace=True)

#                 df = df[['st_code', 'st_fullName', 'cl_className']]

#                 def create_email(full_name, st_code):
#                     full_name_no_accents = remove_accents(full_name)
#                     last_name = full_name_no_accents.split()[-1].lower()
#                     email = f"{last_name}{st_code.lower()}@student.ctu.edu.vn"
#                     return email

#                 df['st_email'] = df.apply(lambda row: create_email(row['st_fullName'], row['st_code']), axis=1)

#                 insert_query = """
#                 INSERT INTO students (st_code, st_fullName, st_email, cl_className)
#                 VALUES (%s, %s, %s, %s)
#                 """
#                 for index, row in df.iterrows():
#                     cur.execute(insert_query, (row['st_code'], row['st_fullName'], row['st_email'], row['cl_className']))
#             conn.commit()
#             messagebox.showinfo("Success","Data imported successfully into the 'students' table.")
#     except Exception as e:
#         messagebox.showerror("Error",f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         conn.close()


# def choose_files():
#     file_paths = filedialog.askopenfilenames(
#         filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
#     )
#     if file_paths:
#         entry_var.set(", ".join(file_paths))

# def import_courses(file_paths):
#     if not file_paths:
#         print("No files selected for import.")
#         return
    
#     conn = pymysql.connect(
#         user='root',
#         password='',
#         host='localhost',
#         database='face_recognition'
#     )
#     cur = conn.cursor()
    
#     try:
#         with cur:
#             for file_path in file_paths:
#                 df = pd.read_excel(file_path, sheet_name='Sheet1')

#                 cols = ['STT', 'Năm học', 'HK']
#                 df.drop(cols, inplace=True, axis=1)

#                 df.rename(columns={
#                     'Mã HP': 'course_code',
#                     'Tên học phần': 'course_name',
#                     'Số TC': 'course_credits',
#                     'Mã ngành': 'maj_Code'
#                 }, inplace=True)

#                 if 'maj_Code' not in df.columns:
#                     raise ValueError("Required column 'maj_Code' is missing in the Excel file.")

#                 df['course_credits'] = df['course_credits'].astype(int)
#                 df = df[['course_code', 'course_name', 'course_credits', 'maj_Code']]


#                 insert_query = """
#                 INSERT INTO courses (course_code, course_name, course_credits, maj_Code)
#                 VALUES (%s, %s, %s, %s)
#                 """
#                 for index, row in df.iterrows():
#                     cur.execute(insert_query, (row['course_code'], row['course_name'], row['course_credits'], row['maj_Code']))
#             conn.commit()
#             messagebox.showinfo("Success","Data imported successfully into the 'courses' table.")
#     except Exception as e:
#         messagebox.showerror("Error",f"An error occurred: {e}")
#         print(f"An error occurred: {e}")
#         conn.rollback()
#     finally:
#         conn.close()


# import_window = tk.Tk()
# import_window.title("Load file")
# import_window.configure(bg="#ccd9de")
# import_window.geometry('1350x700+0+0')

# title = tk.Label(import_window, text="Import Excel", font=("times new roman", 25, "bold"), bg="#134B70", fg="#FDFFE2", bd=7, relief=tk.GROOVE)
# title.place(x=0, y=0, relwidth=1)

# frame = tk.Frame(import_window, bg="#EEEEEE")
# frame.place(x=50, y=200, width=1200, height=50)

# label = tk.Label(frame, text="Choose Files:", bg="#EEEEEE", compound=tk.LEFT, font=("times new roman", 15, "bold"))
# label.grid(row=0, column=0, padx=10, pady=5)

# entry_var = tk.StringVar()
# entry = tk.Entry(frame, font=("times new roman", 15, "bold"), relief=tk.GROOVE, bg="lightgray", width=100, textvariable=entry_var)
# entry.grid(row=0, column=1, padx=10, pady=5)

# choose_button = tk.Button(import_window, text="Choose Excel Files", font=("times new roman", 15, "bold"), command=choose_files, bg="#134B70", fg="#FDFFE2")
# choose_button.place(x=50, y=300)

# import_student_button = tk.Button(import_window, text="Import Student's Files", font=("times new roman", 15, "bold"), command=lambda: import_student(entry_var.get().split(", ")), bg="#134B70", fg="#FDFFE2")
# import_student_button.place(x=250, y=300)

# import_courses_button = tk.Button(import_window, text="Import Course IDs", font=("times new roman", 15, "bold"), command=lambda: import_courses(entry_var.get().split(", ")), bg="#134B70", fg="#FDFFE2")
# import_courses_button.place(x=500, y=300)

# import_window.mainloop()

def import_data():
                    try:
                        conn = pymysql.connect(host="localhost", user="root", password="", database="face_recognition")
                        cur = conn.cursor()
                        import_window = tk.Tk()
                        # import_window = Toplevel()
                        import_window.state('zoomed')
                        import_window.configure(bg="#ccd9de")
                        import_window.title("Import Excel")
                        title = Label(import_window, text="Import Data from Excel", bg="#134B70", fg="#FDFFE2", padx=15, pady=15, 
                                    font=("Times New Roman", 20, "bold"), borderwidth=5, relief=RIDGE).place(x=600, y=80)       
                        
                        def back():
                            import_window.destroy()

                        backbtn = Button(import_window, text='Back', font=('Times new Roman', 15), fg='#E7F6F2', bg='#2C3333', height=1, width=7, command=back)
                        backbtn.place(x=1400, y=20)    
                        #All Required variables for database
                        entry_var = tk.StringVar()
                        
                        def choose_files():
                            file_paths = filedialog.askopenfilenames(
                                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                parent=import_window
                            )
                            if file_paths:
                                entry_var.set(", ".join(file_paths))
                        
                        def remove_accents(input_str):
                            input_str = input_str.replace("Đ", "D").replace("đ", "d")
                            nfkd_str = unicodedata.normalize('NFKD', input_str)
                            no_accents_str = u"".join([c for c in nfkd_str if not unicodedata.combining(c)])
                            return re.sub(r'[^a-zA-Z0-9\s]', '', no_accents_str)

                        def import_student(file_paths):
                            if not file_paths:
                                messagebox.showerror("Error", "No files selected for import.", parent=import_window)
                                return
                            
                            conn = pymysql.connect(user='root', password='', host='localhost', database='face_recognition')
                            cur1 = conn.cursor()
                            
                            try:
                                with cur1:
                                    for file_path in file_paths:
                                        df = pd.read_excel(file_path, sheet_name='Worksheet')

                                        df.rename(columns={
                                            'Lớp': 'cl_className',
                                            'Mã sinh viên': 'st_code',
                                            'Họ và Tên': 'st_fullName'
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
                                    messagebox.showinfo("Success", "Data imported successfully into the 'students' table.",parent=import_window)
                            except Exception as e:
                                messagebox.showerror("Error", f"An error occurred: {e}", parent=import_window)
                                conn.rollback()
                            finally:
                                conn.close()

                        def import_courses(file_paths):
                            if not file_paths:
                                messagebox.showerror("Error","No files selected for import.", parent=import_window)
                                return
                            
                            conn = pymysql.connect(user='root', password='', host='localhost', database='face_recognition')
                            cur = conn.cursor()
                            
                            try:
                                with cur:
                                    for file_path in file_paths:
                                        df = pd.read_excel(file_path, sheet_name='Sheet1')

                                        cols = ['STT', 'Năm học', 'HK']
                                        df.drop(cols, inplace=True, axis=1)

                                        df.rename(columns={
                                            'Mã HP': 'course_code',
                                            'Tên học phần': 'course_name',
                                            'Số TC': 'course_credits',
                                            'Mã ngành': 'maj_Code'
                                        }, inplace=True)

                                        if 'maj_Code' not in df.columns:
                                            raise ValueError("Required column 'maj_Code' is missing in the Excel file.")

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

                        frame = tk.Frame(import_window, bg="#DCF2F1")
                        frame.place(x=350, y=220, width=800, height=400)

                        entry = tk.Entry(frame, font=("times new roman", 15, "bold"), relief=tk.GROOVE, bg="#ccd9de", width=60, textvariable=entry_var)
                        entry.grid(row=0, column=1, padx=50, pady=35)

                        choose_button = tk.Button(frame, text="Browse", font=("times new roman", 15, "bold"), command=choose_files, bg="#134B70", fg="#FDFFE2")
                        choose_button.place(x=670, y=25)

                        import_student_button = tk.Button(frame, text="Import Student's Files", font=("times new roman", 15, "bold"), command=lambda: import_student(entry_var.get().split(", ")), bg="#134B70", fg="#FDFFE2")
                        import_student_button.place(x=50, y=100)

                        import_courses_button = tk.Button(frame, text="Import Course IDs", font=("times new roman", 15, "bold"), command=lambda: import_courses(entry_var.get().split(", ")), bg="#134B70", fg="#FDFFE2")
                        import_courses_button.place(x=300, y=100)
                        
                        import_window.mainloop()

                    except pymysql.err.OperationalError as e:
                        messagebox.showerror("Error", "Sql Connection Error... Open Xamp Control Panel and then start MySql Server")
                    except Exception as e:
                        print(e)
                        messagebox.showerror("Error", "Close all the windows and restart your program")

import_data()