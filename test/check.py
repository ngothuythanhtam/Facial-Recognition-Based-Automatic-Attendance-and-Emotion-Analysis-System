# import hashlib, binascii, os

# def hash_password(password):
#     salt =  hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
#     password_hash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt,100000)
#     password_hash = binascii.hexlify(password_hash)
#     return (salt+password_hash).decode('ascii')

# def check_password(stored_password, user_password):
#     salt = stored_password[:64]
#     stored_password = stored_password[64:]
#     password_hash = hashlib.pbkdf2_hmac('sha512', user_password.encode('utf-8'), salt.encode('ascii'), 100000)
#     password_hash = binascii.hexlify(password_hash).decode('ascii')
#     return password_hash == stored_password

# user_password = input("Enter your password: ")
# stored_password = hash_password(user_password)
# print(user_password)
# print(stored_password)
# print(check_password(stored_password, user_password))

import tkinter as tk
from tkinter import ttk

def on_select(event):
    selected_value = course_btn.get()
    print(f"Selected: {selected_value}")

def update_options(event):
    input_value = course_btn.get()
    filtered_options = [option for option in course_options if option.lower().startswith(input_value.lower())]
    
    # Cập nhật danh sách các tùy chọn nhưng không mở dropdown ngay lập tức
    course_btn['values'] = filtered_options
    course_btn.config(foreground='black')

def open_dropdown(event=None):
    # Kiểm tra nếu người dùng nhập một giá trị và danh sách có các tùy chọn phù hợp
    if course_btn.get() != placeholder_text and len(course_btn['values']) > 0:
        course_btn.event_generate('<Down>')  # Mở dropdown
    
def clear_placeholder(event):
    if course_btn.get() == placeholder_text:
        course_btn.delete(0, tk.END)
        course_btn.config(foreground='black')

def reset_placeholder(event):
    if course_btn.get() == '':
        course_btn.set(placeholder_text)
        course_btn.config(foreground='grey')

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Input and Select Example")

# Dữ liệu ví dụ
course_options = ["Python Programming", "Java Programming", "C++ Programming", "C# Programming", "Web Development"]

# Placeholder cho Combobox
placeholder_text = "Select Course ID"

# Tạo Combobox cho khóa học với placeholder
course_btn = ttk.Combobox(root, values=course_options, width=30, font=('Times New Roman', 18), foreground='grey')
course_btn.place(x=50, y=50)
course_btn.set(placeholder_text)

# Liên kết sự kiện khi người dùng chọn từ danh sách
course_btn.bind("<<ComboboxSelected>>", on_select)

# Liên kết sự kiện khi người dùng gõ phím
course_btn.bind("<KeyRelease>", update_options)

# Liên kết sự kiện khi người dùng nhấn Enter để mở dropdown
course_btn.bind("<Return>", open_dropdown)

# Liên kết sự kiện khi người dùng ngừng nhập một thời gian ngắn (500ms)
course_btn.bind("<FocusOut>", open_dropdown)

# Liên kết sự kiện khi người dùng focus vào Combobox
course_btn.bind("<FocusIn>", clear_placeholder)

# Liên kết sự kiện khi người dùng rời khỏi Combobox
course_btn.bind("<FocusOut>", reset_placeholder)

# Hiển thị cửa sổ
root.mainloop()
