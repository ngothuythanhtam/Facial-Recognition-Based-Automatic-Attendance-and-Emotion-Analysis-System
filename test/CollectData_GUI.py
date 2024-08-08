import tkinter as tk
from tkinter import Message, Text
import cv2, os
import csv
import numpy as np
from PIL import Image, ImageTk
import tkinter.font as font
from tkinter import messagebox, ttk

window = tk.Tk()
window.title("Collecting Dataset")
window.configure(bg="#ccd9de")
window.geometry('1350x700+0+0')

lbl = tk.Label(window, text="Face Recognition Based Attendance System", bg="#ccd9de" , fg="#3289a8" , width=50 , height=3, font=('times', 30, 'italic bold')) 
lbl.place(x=100, y=20)

lbl1 = tk.Label(window, text="Enter ID", width=20 , height=2 , fg="#3289a8" , bg="white", font=('times', 15, ' bold ') ) 
lbl1.place(x=200, y=200)

txt1 = tk.Entry(window, width=20, bg="white", fg="#3289a8", font=('times', 15, ' bold '))
txt1.place(x=550, y=215)

lbl2 = tk.Label(window, text="Class ID", width=20 , fg="#3289a8", bg="white", height=2, font=('times', 15, ' bold ')) 
lbl2.place(x=200, y=300)

classID=['DI21V7F1', 'DI21V7F2','DI21V7F3','DI21V7F4']

txt2=ttk.Combobox(window, values=classID,font=("Consolas", 15), width=13)
# txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 15, ' bold ')  )
txt2.place(x=550, y=315)
txt2.set('Select...')

lbl3 = tk.Label(window, text="Notification →", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
lbl3.place(x=200, y=400)

message = tk.Label(window, text="", bg="white", fg="black", width=30, height=2, font=('times', 15, ' bold ')) 
message.place(x=550, y=400)
 
def clearSId():
    txt1.delete(0, 'end')

def clearCId():
    txt2.delete(0, 'end')
    txt2.set('Select...')

def takeImages():        
    
    if(txt1.get()=="" or txt2.get()=="Select..." or txt2.get()==""):
        res = "Please fill all information!"
        lbl3 = tk.Label(window, text="Notification →", width=20 , fg="red", bg="white", height=2, font=('times', 15, ' bold ')) 
        lbl3.place(x=200, y=400)
        message.configure(text= res, fg="black", bg="red")
        # messagebox.showinfo('Result', 'Please fill all information!')
    else:
        SId=(txt1.get())
        CId=(txt2.get())
        lbl3 = tk.Label(window, text="Notification →", width=20 , fg="black", bg="white", height=2, font=('times', 15, ' bold ')) 
        lbl3.place(x=200, y=400)
        message.configure(text="",fg="black", bg="white")
        folder_name = f"./face-db/{CId}/{SId}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        cam = cv2.VideoCapture("http://192.168.117.120/video")
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                sampleNum=sampleNum+1
                cv2.putText(img, str(sampleNum), (60, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 3)
                file_name_path = f"{folder_name}/img{sampleNum}.jpg"
                cv2.imwrite(file_name_path, gray[y:y+h,x:x+w])
                resized = cv2.resize(img, (600,400))
                cv2.imshow('Face Detecting',resized)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum>50:
                break
        cam.release()
        cv2.destroyAllWindows() 


clearButton1 = tk.Button(window, text="Clear", command=clearSId, fg="white", bg="gray", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
clearButton1.place(x=850, y=200)

clearButton2 = tk.Button(window, text="Clear", command=clearCId, fg="white", bg="gray", width=20, height=2, activebackground = "Red", font=('times', 15, ' bold '))
clearButton2.place(x=850, y=300)  

takeImg = tk.Button(window, text="Take Images", command=takeImages, fg="white", bg="#3289a8", width=20, height=3, activebackground = "Green", font=('times', 15, ' bold '))
takeImg.place(x=400, y=500)

quitWindow = tk.Button(window, text="Quit", command=window.destroy, fg="white", bg="gray", width=20, height=3, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=700, y=500)

window.mainloop()