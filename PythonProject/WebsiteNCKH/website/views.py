from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
from datetime import datetime 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator
import subprocess
from django.core.files.storage import FileSystemStorage
import os
from django.core.exceptions import ValidationError

def gosystem(request):
    try:
        # Dynamically construct the path to the batch file in the same directory as view.py
        current_directory = os.path.dirname(os.path.abspath(__file__))
        batch_file_path = os.path.join(current_directory, 'gosystem.bat')

        # Execute the batch file
        subprocess.run([batch_file_path], shell=True)

        return redirect('home')  # Redirect after executing the batch file
    except Exception as e:
        return HttpResponse(f"Error executing the batch file: {e}")

# hàm để kiểm tra định dạng file
def validate_image_file(file):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1]
    if not ext.lower() in valid_extensions:
        raise ValidationError('Please upload a JPG, JPEG, PNG or GIF file!')


def profile(request):
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login if no session exists

    username = request.session.get('username')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.role_ID, a.acc_username, r.role_name
            FROM accounts a
            JOIN roles r ON a.role_ID = r.role_ID
            WHERE a.acc_username = %s
        """, [username])
        account_info = cursor.fetchone()

        if not account_info:
            messages.error(request, 'No profile found for this user.')
            return redirect('login')

        role_id, acc_username, role_name = account_info
        profile_data = {'username': acc_username, 'role': role_name}

        # Fetch data based on role
        if role_name == 'Students':
            cursor.execute("""
                SELECT st_fullName, st_email, st_birthDay, st_phone, cl_className, avatar
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                profile_data.update({
                    'fullname': student_info[0],
                    'email': student_info[1],
                    'birthday': student_info[2],
                    'phone': student_info[3],
                    'classname': student_info[4],
                    'avatar': student_info[5],
                })

        elif role_name == 'Instructors':  # Instructor
            cursor.execute("""
                SELECT ins_name, ins_academicRank, avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                profile_data.update({
                    'fullname': instructor_info[0],
                    'academic_rank': instructor_info[1],
                    'avatar': instructor_info[2]
                })

        # Handle POST requests for avatar upload and profile update
        if request.method == 'POST':
            if 'avatar' in request.FILES:
                # Handle avatar upload
                avatar_file = request.FILES['avatar']
                try:
                    validate_image_file(avatar_file)

                    fs = FileSystemStorage()
                    filename = fs.save(avatar_file.name, avatar_file)
                    uploaded_file_url = fs.url(filename)
                    
                    if role_name == 'Students':
                        # Update avatar link in the database if necessary
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                UPDATE students
                                SET avatar = %s
                                WHERE st_code = %s
                            """, [uploaded_file_url, username])
                    
                    if role_name == 'Instructors':
                        with connection.cursor() as cursor:
                            cursor.execute("""
                                UPDATE instructor
                                SET avatar = %s
                                WHERE ins_instructorCode = %s
                            """, [uploaded_file_url, username])
                    messages.success(request, 'Avatar uploaded successfully!')
                except ValidationError as e:
                    messages.error(request, str(e))

            else:
                # Update profile information
                fullname = request.POST.get('fullname')
                phone = request.POST.get('phone')
                birthday = request.POST.get('birthday')

                try:
                    if birthday:
                        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

                    with connection.cursor() as cursor:
                        cursor.execute("""
                            UPDATE students
                            SET st_fullName = %s, st_phone = %s, st_birthDay = %s
                            WHERE st_code = %s
                        """, [fullname, phone, birthday, username])
                    messages.success(request, 'Update information successfully!')

                    # Update profile data for rendering after successful update
                    profile_data.update({
                        'fullname': fullname,
                        'phone': phone,
                        'birthday': birthday
                    })
                except Exception as e:
                    messages.error(request, f'Error : {str(e)}')

    return render(request, 'website/profile.html', profile_data)


def login_view(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        request.method == 'POST'
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'website/login.html')

        with connection.cursor() as cursor:
            # Retrieve role_id and acc_password if the username existed 
            cursor.execute("SELECT acc_password, role_ID FROM accounts WHERE acc_username = %s", [username])
            result = cursor.fetchone()

            if result:
                stored_password, role_id = result
                if stored_password == password:
                    # Set session data
                    request.session['username'] = username

                    # Retrieve the role name using the role_ID (After Set session data and valid the login already)
                    cursor.execute("SELECT role_name FROM roles WHERE role_ID = %s", [role_id])
                    role_result = cursor.fetchone()

                    if role_result:
                        user_role = role_result[0] # Assign the result of the rolename corressponding to its username and to the session
                        request.session['user_role'] = user_role

                        # Handle successful login based on role
                    if user_role == 'Students':
                        return redirect('home')
                    elif user_role == 'Instructors':
                        return redirect('home')
                    elif user_role == 'Administrators':
                        return redirect('manageaccsystem')
                    else:
                        messages.error(request, 'Không thể xác định vai trò của tài khoản')
                        return redirect('login')
                else:
                    messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
                    return redirect('login')
            else:
                messages.error(request, 'Tài khoản hoặc mật khẩu không đúng') 
                return redirect('login')

def logout_view(request):

    request.session.flush()
    return redirect('login')

def manage_acc_system(request):
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login if no session exists

    username = request.session.get('username')

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.role_name
            FROM accounts a
            JOIN roles r ON a.role_ID = r.role_ID
            WHERE a.acc_username = %s
        """, [username])
        result = cursor.fetchone()

        if result and result[0] == 'Ad':
            filter_type = request.GET.get('filter', 'students')  # Default to 'students'
            table_data = []

            if filter_type == 'Students':
                cursor.execute("""
                    SELECT st_code AS username, st_fullName AS fullname, st_email AS email, 
                           st_birthDay AS birthday, st_phone AS phone, cl_className AS classname
                    FROM students
                """)
                table_data = cursor.fetchall()
            
            elif filter_type == 'Instructors':
                cursor.execute("""
                    SELECT ins_instructorCode AS username, ins_name AS fullname, ins_academicRank AS academic_rank
                    FROM instructor
                """)
                table_data = cursor.fetchall()
            
            elif filter_type == 'Administrators':
                cursor.execute("""
                    SELECT ad_code AS username, ad_name AS fullname, ad_phoneNumber AS phone
                    FROM administrator
                """)
                table_data = cursor.fetchall()
            
            return render(request, 'website/manageaccsystem.html', {
                'filter_type': filter_type,
                'table_data': table_data
            })
        else:
            if not request.session.get('error_message_shown'):
                messages.error(request, 'Bạn không có quyền truy cập vào trang quản lí của admin.')
                request.session['error_message_shown'] = True
            return redirect('login')
        
def search_profile(request):
    username = request.GET.get('username')
    
    if not username:
        return JsonResponse({'exists': False})
    
    with connection.cursor() as cursor:
        # Check role and fetch profile data based on role
        cursor.execute("""
            SELECT a.role_ID, a.acc_username, r.role_name
            FROM accounts a
            JOIN roles r ON a.role_ID = r.role_ID
            WHERE a.acc_username = %s
        """, [username])
        account_info = cursor.fetchone()
        
        if not account_info:
            return JsonResponse({'exists': False})
        
        role_id, acc_username, role_name = account_info
        profile_data = {'exists': True, 'profile_html': ''}

        if role_id == 1:  # Student
            cursor.execute("""
                SELECT st_fullName, st_email, st_birthDay, st_phone, cl_className
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                profile_data['profile_html'] = f"""
                    <p><strong>Mã người dùng:</strong> {username}</p>
                    <p><strong>Họ và tên:</strong> {student_info[0]}</p>
                    <p><strong>Email:</strong> {student_info[1]}</p>
                    <p><strong>Ngày sinh:</strong> {student_info[2]}</p>
                    <p><strong>Điện thoại:</strong> {student_info[3]}</p>
                    <p><strong>Tên lớp:</strong> {student_info[4]}</p>
                """
        
        elif role_id == 2:  # Instructor
            cursor.execute("""
                SELECT ins_name, ins_academicRank
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                profile_data['profile_html'] = f"""
                    <p><strong>Mã người dùng:</strong> {username}</p>
                    <p><strong>Họ và tên:</strong> {instructor_info[0]}</p>
                    <p><strong>Trình độ giảng viên:</strong> {instructor_info[1]}</p>
                """
        
        elif role_id == 3:  # Administrator
            cursor.execute("""
                SELECT ad_name, ad_phoneNumber
                FROM administrator
                WHERE ad_code = %s
            """, [username])
            admin_info = cursor.fetchone()
            if admin_info:
                profile_data['profile_html'] = f"""
                    <p><strong>Mã người dùng:</strong> {username}</p>
                    <p><strong>Họ và tên:</strong> {admin_info[0]}</p>
                    <p><strong>Điện thoại:</strong> {admin_info[1]}</p>
                """

    return JsonResponse(profile_data)

def home(request):
    if 'username' not in request.session:
        return redirect('login')  # Redirect to login if no session exists
    else:
        username = request.session.get('username')
        user_role = request.session.get('user_role')
    if user_role == 'Students':
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                avatar = student_info[0]
                request.session['avatar'] = avatar

            cursor.execute("SELECT YEAR(CURDATE());")
            resulty = cursor.fetchone()
            curyear = resulty[0]  # Extract value from tuple
            
            cursor.execute("SELECT MONTH(CURDATE());")
            resultm = cursor.fetchone()
            curmon = resultm[0]  
            cursemester = 0
            curscholastic = ""
            
            if curmon >= 9 and curmon <= 12:
                cursemester = 1
                nextyear = curyear + 1
                curscholastic = f"{curyear}-{nextyear}"
            elif curmon >= 1 and curmon <= 5:
                cursemester = 2
                curscholastic = f"{curyear}-{curyear + 1}"
            elif curmon >= 6 and curmon <= 8:
                cursemester = 3
                curscholastic = f"{curyear}-{curyear + 1}"

            cursor.execute("""
                select DISTINCT cs.course_code,cs.course_name,i.ins_name,clCourse_code,cfa.ay_schoolYear,se_ID 
                    FROM studying s
                        JOIN classCourse clc ON s.clCourse_ID = clc.clCourse_ID
                        JOIN students sts ON s.st_code = sts.st_code
                        JOIN coursefollowacayear cfa ON clc.cfa_ID = cfa.cfa_ID
                        JOIN teaching t ON cfa.cfa_ID = t.cfa_ID
                        JOIN instructor i ON t.ins_ID = i.ins_ID
                        JOIN courses cs ON cfa.course_code = cs.course_code
                        WHERE sts.st_code = %s 
                            AND cfa.ay_schoolYear = %s
                            AND se_ID = %s;
                """, [username, curscholastic,cursemester])
                
            std_course = cursor.fetchall()

            if std_course:
                curCourse_code = std_course[0][0]
                request.session['curCourse_code'] = curCourse_code

                curCourse_name = std_course[0][1]
                request.session['curCourse_name'] = curCourse_name

                curclCourse_code = std_course[0][3]
                request.session['curclCourse_code'] = curclCourse_code

                curscholastic = std_course[0][4]
                request.session['curscholastic'] = curscholastic

                cursemester = std_course[0][5]
                request.session['cursemester'] = cursemester
            else:
                curCourse_code = None
                curclCourse_code = None
                curCourse_name = None
                curscholastic = None
                cursemester = None

            return render(request, 'website/home.html', {
                'std_course': std_course,
                'avatar': avatar    
            })
    elif user_role == 'Instructors':
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                avatar =  instructor_info[0]
                request.session['avatar'] = avatar
            
            # get infor for current semester course  
            cursor.execute("SELECT YEAR(CURDATE());")
            resulty = cursor.fetchone()
            curyear = resulty[0] 
            
            cursor.execute("SELECT MONTH(CURDATE());")
            resultm = cursor.fetchone()
            curmon = resultm[0]  
            cursemester=0
            if curmon >= 9 and curmon <= 12:
                cursemester = 1
                nextyear = curyear + 1
                curscholastic = f"{curyear}-{nextyear}"
            else:
                cursemester = 2
                curscholastic = f"{curyear}-{curyear + 1}"  

            cursor.execute("""
                select DISTINCT cfa.course_code, cs.course_name,ins_name, clc.clCourse_code, cfa.ay_schoolYear, cfa.se_ID 
                    FROM teaching t 
                    JOIN instructor i ON t.ins_ID = i.ins_ID
                    JOIN coursefollowacayear cfa ON t.cfa_ID = cfa.cfa_ID
                    JOIN courses cs ON cfa.course_code = cs.course_code
                    JOIN classCourse clc ON cfa.cfa_ID = clc.cfa_ID
                    where cfa.ay_schoolYear = %s and cfa.se_ID = %s and ins_instructorCode = %s;
                        """, [curscholastic,cursemester, username])
            
            ins_course = cursor.fetchall()
            if ins_course:
                curCourse_code = ins_course[0][0]
                request.session['curCourse_code'] = curCourse_code

                curclCourse_code = ins_course[0][3]
                request.session['curclCourse_code'] = curclCourse_code

                curCourse_name = ins_course[0][1]
                request.session['curCourse_name'] = curCourse_name

                curscholastic = ins_course[0][4]
                request.session['curscholastic'] = curscholastic

                cursemester = ins_course[0][5]
                request.session['cursemester'] = cursemester
            else:
                curCourse_code = None
                curclCourse_code = None
                curCourse_name = None
                curscholastic = None
                cursemester = None

            return render(request, 'website/home.html', {
                'ins_course': ins_course,
                'avatar': avatar    
            })  
    else:
        return redirect('login')

def attendance_currentcourse(request):
    if 'username' not in request.session:
        return redirect('login')
    course_code_from_url = request.GET.get('course_code')
    clCourse_code_from_url = request.GET.get('classcourse')
    course_name_from_url = request.GET.get('course_name')
    curscholastic_from_url = request.GET.get('curscholastic')
    cursemester_from_url = request.GET.get('cursemester')

    if course_code_from_url and clCourse_code_from_url and course_name_from_url and curscholastic_from_url and cursemester_from_url:
        request.session['curCourse_code'] = course_code_from_url
        request.session['curclCourse_code'] = clCourse_code_from_url
        request.session['curCourse_name'] = course_name_from_url
        request.session['curscholastic'] = curscholastic_from_url
        request.session['cursemester'] = cursemester_from_url


    curCourse_code = request.session.get('curCourse_code')
    curclCourse_code = request.session.get('curclCourse_code')
    curCourse_name = request.session.get('curCourse_name')
    curscholastic = request.session.get('curscholastic')
    cursemester = request.session.get('cursemester')

    if not curCourse_code or not curclCourse_code or not curCourse_name or not curscholastic or not cursemester:
        return redirect('home')

    username = request.session.get('username')
    user_role = request.session.get('user_role')
    
    date = request.GET.get('date')
    status = request.GET.get('status')
    if user_role == 'Students':    
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                avatar = student_info[0]
                request.session['avatar'] = avatar

            # Query to get attendance data
            cursor.execute("""
                SELECT c.clCourse_code, cfa.course_code, a.session_date, a.time_status,cs.course_name 
                FROM attendance a 
                JOIN classcourse c ON a.studying_clCourse_ID = c.clCourse_ID
                JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                JOIN courses cs on cs.course_code = cfa.course_code
                WHERE a.studying_st_code = %s 
					AND cfa.course_code = %s
                    AND cs.course_name = %s
                    AND cfa.ay_schoolYear = %s
					AND cfa.se_ID = %s;""", 
                    [username, curCourse_code, curCourse_name, curscholastic, cursemester])
            
            attendance_data = cursor.fetchall()
        if attendance_data:
            coursename = attendance_data[0][4]
            request.session['coursename'] = coursename    
        paginator = Paginator(attendance_data, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'website/attendance.html', {
            'page_obj': page_obj,
            'status': status,
            'date':date,
            'coursename' : coursename,
            'avatar': avatar
        })

    elif user_role == 'Instructors':
        query = """SELECT c.clCourse_code, cfa.course_code, a.session_date, a.time_status, cs.course_name, std.st_fullname, std.st_code
                    FROM attendance a 
                    JOIN students std ON a.studying_st_code = std.st_code
                    JOIN classcourse c ON a.studying_clCourse_ID = c.clCourse_ID
                    JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                    JOIN teaching t ON c.cfa_ID = t.cfa_ID
                    JOIN instructor i ON t.ins_ID = i.ins_ID
                    JOIN courses cs ON cs.course_code = cfa.course_code
                    WHERE i.ins_instructorCode = %s
                        AND cfa.course_code = %s
                        AND cs.course_name = %s
                        AND cfa.ay_schoolYear = %s
                        AND cfa.se_ID = %s"""
        query_params = [username, curCourse_code, curCourse_name, curscholastic, cursemester]

        if date:
            query += " AND a.session_date = %s"
            query_params.append(date)
        
            if status == 'Absent':
                query += " AND a.time_status IS NULL"
            elif status == 'Present':
                query += " AND a.time_status IS NOT NULL"

        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                avatar =  instructor_info[0]
                request.session['avatar'] = avatar

            print("Executing query:", query)
            print("With parameters:", query_params)
            cursor.execute(query, query_params)
            attendance_data = cursor.fetchall()
        if attendance_data:
            coursename = attendance_data[0][4]
            request.session['coursename'] = coursename    
            paginator = Paginator(attendance_data, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'website/attendance.html', {
                'page_obj': page_obj,
                'status': status,
                'date':date,
                'coursename' : coursename,
                'avatar': avatar
            })
        else:
            return render(request, 'website/attendance.html', {
                'status': status,
                'date':date,
                'avatar': avatar
            })

# @csrf_exempt
# def clear_course_session(request):
#     session_keys = [
#         'curCourse_code', 
#         'curclCourse_code', 
#         'course_code', 
#         'clCourse_code', 
#         'search_year', 
#         'search_semester',
#         'cursemester',
#         'curscholastic'
#     ]
#     for key in session_keys:
#         if key in request.session:
#             del request.session[key]
#     return HttpResponse(status=200)

def search_result_attendance(request):
    if 'username' not in request.session:
        return redirect('login')
    else :
        username = request.session.get('username')
        user_role = request.session.get('user_role')
    if username and user_role == 'Students':    
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                avatar = student_info[0]
                request.session['avatar'] = avatar

            cursor.execute("""
                select DISTINCT cfa.ay_schoolYear from studying s
                    join classCourse clc on s.clCourse_ID = clc.clCourse_ID
                    join students sts on s.st_code = sts.st_code
                    join coursefollowacayear cfa on clc.cfa_ID = cfa.cfa_ID
                    JOIN teaching t on cfa.cfa_ID = t.cfa_ID
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    join courses cs on cfa.course_code = cs.course_code 
                where sts.st_code = %s;""", [username])
            
            list_year = cursor.fetchall()
        
            cursor.execute("""
                select * from semester;""")
            
            list_sem = cursor.fetchall()

        # Retrieve the search filters from the URL query parameters
        academic_year = request.GET.get('academic_year')
        semester = request.GET.get('semester')

        if academic_year and semester:
            with connection.cursor() as cursor:
                cursor.execute("""
                    select DISTINCT cs.course_code, cs.course_name, i.ins_name, clCourse_code, cfa.ay_schoolYear, se_ID 
                    from studying s
                        join classCourse clc on s.clCourse_ID = clc.clCourse_ID
                        join students sts on s.st_code = sts.st_code
                        join coursefollowacayear cfa on clc.cfa_ID = cfa.cfa_ID
                        JOIN teaching t on cfa.cfa_ID = t.cfa_ID
                        JOIN instructor i on t.ins_ID = i.ins_ID
                        join courses cs on cfa.course_code = cs.course_code 
                    where sts.st_code = %s 
                        AND cfa.ay_schoolYear = %s
                        AND se_ID = %s;""", [username, academic_year, semester])
                
                data = cursor.fetchall()

            return render(request, 'website/search_result_attendance.html', {
                'data': data,
                'list_year': list_year,  
                'list_sem': list_sem,
                'selected_year': academic_year,  # To keep the selected values in the form
                'selected_semester': semester,  # To keep the selected values in the form
                'avatar': avatar
            })
        
        return render(request, 'website/search_result_attendance.html', {
            'list_year': list_year,
            'list_sem': list_sem,
            'avatar': avatar
        })
    
    elif user_role == 'Instructors':
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                avatar =  instructor_info[0]
                request.session['avatar'] = avatar

            cursor.execute("""
                select DISTINCT cfa.ay_schoolYear from teaching t
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    join coursefollowacayear cfa on t.cfa_ID = cfa.cfa_ID
                    join classCourse clc on cfa.cfa_ID = clc.cfa_ID
                where i.ins_instructorCode = %s;""", [username])
            
            list_year = cursor.fetchall()
        
            cursor.execute("""
                select * from semester;""")
            
            list_sem = cursor.fetchall()

        # Retrieve the search filters from the URL query parameters
        academic_year = request.GET.get('academic_year')
        semester = request.GET.get('semester')

        if academic_year and semester:
            with connection.cursor() as cursor:
                cursor.execute("""
                    select c.course_code, c.course_name, i.ins_name, clc.clCourse_code, cfa.ay_schoolYear, cfa.se_ID 
                    from teaching t
                        JOIN instructor i on t.ins_ID = i.ins_ID
                        join coursefollowacayear cfa on t.cfa_ID = cfa.cfa_ID
                        join classCourse clc on cfa.cfa_ID = clc.cfa_ID
                        join courses c on cfa.course_code = c.course_code
                    where ins_instructorCode = %s 
                        and cfa.ay_schoolYear = %s
                        and cfa.se_ID = %s;""", [username, academic_year, semester])
                
                data = cursor.fetchall()

            return render(request, 'website/search_result_attendance.html', {
                'data': data,
                'list_year': list_year,
                'list_sem': list_sem,
                'selected_year': academic_year,  # To keep the selected values in the form
                'selected_semester': semester,  # To keep the selected values in the form
                'avatar': avatar
            })

        return render(request, 'website/search_result_attendance.html', {
            'list_year': list_year,
            'list_sem': list_sem,
            'avatar': avatar
        })

    else:
        return redirect('login')

def result_search_attendance(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session.get('username')
        user_role = request.session.get('user_role')

        course_code_from_url = request.GET.get('course_code')
        clCourse_code_from_url = request.GET.get('classcourse')
        academicyear_from_url = request.GET.get('academicyear')
        semester_from_url = request.GET.get('semester')

        if course_code_from_url and clCourse_code_from_url and academicyear_from_url and semester_from_url:
            request.session['course_code'] = course_code_from_url
            request.session['clCourse_code'] = clCourse_code_from_url
            request.session['search_year'] = academicyear_from_url
            request.session['search_semester'] = semester_from_url

        course_code = request.session.get('course_code')
        clCourse_code = request.session.get('clCourse_code')
        academicyear = request.session.get('search_year')
        semester = request.session.get('search_semester')

        if not course_code or not clCourse_code or not academicyear or not semester:
            return redirect('home')

        date = request.GET.get('date')
        status = request.GET.get('status')

        # Define the base query
        query = """
                SELECT c.clCourse_code, cfa.course_code, a.session_date, a.time_status, cs.course_name 
                FROM attendance a 
                JOIN classcourse c ON a.studying_clCourse_ID = c.clCourse_ID
                JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                JOIN courses cs on cs.course_code = cfa.course_code
                WHERE a.studying_st_code = %s AND cfa.course_code = %s AND ay_schoolYear = %s AND se_ID = %s
                """
        
        # Prepare initial query parameters
        query_params = [username, course_code, academicyear, semester]

        if date:
            query += " AND a.session_date = %s"
            query_params.append(date)

            if status == 'Absent':
                query += ' AND a.time_status IS NULL'
            elif status == 'Present':
                query += ' AND a.time_status IS NOT NULL'
        if status == 'all':
            query += " AND a.session_date = %s"
            query_params.append(date)

        # Execute the query
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM students
                WHERE st_code = %s
            """, [username])
            student_info = cursor.fetchone()
            if student_info:
                avatar = student_info[0]
                request.session['avatar'] = avatar

            cursor.execute(query, query_params)
            attendance_data = cursor.fetchall()

        if attendance_data:
            coursename = attendance_data[0][4]
            request.session['coursename'] = coursename
            paginator = Paginator(attendance_data, 10)
            page_number = request.GET.get('page')
            page_course = paginator.get_page(page_number)

            return render(request, 'website/result_search_attendance.html', {
                'page_course': page_course,
                'status': status,
                'date': date,
                'coursename': coursename,
                'avatar': avatar
            })

        else:
            paginator = Paginator(attendance_data, 10)
            page_number = request.GET.get('page')
            page_course = paginator.get_page(page_number)

            return render(request, 'website/result_search_attendance.html', {
                'page_course': page_course,
                'status': status,
                'date': date,
                'avatar': avatar
            })


def ls_attflw_course(request):
    if 'username' not in request.session:
        return redirect('login')
    else :
        username = request.session.get('username')
        course_code_from_url = request.GET.get('course_code')
        clCourse_code_from_url = request.GET.get('classcourse')
        academicyear_from_url = request.GET.get('academicyear')
        semester_from_url = request.GET.get('semester')

        if course_code_from_url and clCourse_code_from_url and academicyear_from_url and semester_from_url:
            request.session['course_code'] = course_code_from_url
            request.session['clCourse_code'] = clCourse_code_from_url
            request.session['search_year'] = academicyear_from_url
            request.session['search_semester'] = semester_from_url

        course_code = request.session.get('course_code')
        clCourse_code = request.session.get('clCourse_code')
        academicyear = request.session.get('search_year')
        semester = request.session.get('search_semester')

        if not course_code or not clCourse_code or not academicyear or not semester :
            return redirect('home')
        
        date = request.GET.get('date')
        status = request.GET.get('status')

        # Base query to fetch attendance data
        query = """
            SELECT a.session_date, a.studying_st_code, std.st_fullName, a.time_status
            FROM attendance a
            JOIN classcourse c ON a.studying_clCourse_ID = c.clCourse_ID
            JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID
            JOIN teaching t on t.cfa_ID = cfa.cfa_ID
            JOIN instructor ins on ins.ins_ID = t.ins_ID
            JOIN courses cs ON cs.course_code = cfa.course_code
            JOIN students std ON a.studying_st_code = std.st_code
            WHERE ins.ins_instructorCode = %s and cs.course_code = %s AND c.clCourse_code = %s
            AND ay_schoolYear = %s AND se_ID = %s
        """
        query_params = [username, course_code, clCourse_code, academicyear, semester]

        # Append filters if date and status are present
        if date and status:
            query += " AND a.session_date = %s"
            query_params.append(date)

            if status == 'Absent':
                query += ' AND a.time_status IS NULL'
            elif status == 'Present':
                query += ' AND a.time_status IS NOT NULL'
        elif date and status and status == 'all':  
            query += " AND a.session_date = %s"
            query_params.append(date)
        else:
            query = """
                SELECT a.session_date, a.studying_st_code, std.st_fullName, a.time_status
                FROM attendance a
                JOIN classcourse c ON a.studying_clCourse_ID = c.clCourse_ID
                JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID
                JOIN teaching t on t.cfa_ID = cfa.cfa_ID
                JOIN instructor ins on ins.ins_ID = t.ins_ID
                JOIN courses cs ON cs.course_code = cfa.course_code
                JOIN students std ON a.studying_st_code = std.st_code
                WHERE ins.ins_instructorCode = %s and cs.course_code = %s AND c.clCourse_code = %s
                AND ay_schoolYear = %s AND se_ID = %s
            """
            query_params = [username, course_code, clCourse_code, academicyear, semester]

        # Execute the query and fetch results
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                avatar =  instructor_info[0]
                request.session['avatar'] = avatar

            cursor.execute(query, query_params)
            ls_attflw_course = cursor.fetchall()

        # Pagination (7 records per page)
        paginator = Paginator(ls_attflw_course, 7)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Render the page with filtered results
        return render(request, 'website/ls_attflw_course.html', {
            'page_obj': page_obj,
            'status': status,  
            'date': date,
            'course_code': course_code,
            'clCourse_code': clCourse_code,
            'academicyear': academicyear,
            'semester': semester,
            'avatar': avatar
        })
        
def emotion(request):
    if 'username' not in request.session:
        return redirect('login')
    else:
        username = request.session.get('username')
        # extract avatar url
        with connection.cursor() as cursor:
            # extract avatar url
            cursor.execute("""
                SELECT avatar
                FROM instructor
                WHERE ins_instructorCode = %s
            """, [username])
            instructor_info = cursor.fetchone()
            if instructor_info:
                avatar =  instructor_info[0]
                request.session['avatar'] = avatar

        course_code_from_url = request.GET.get('course_code')
        clCourse_code_from_url = request.GET.get('classcourse')
        academicyear_from_url = request.GET.get('curscholastic')
        semester_from_url = request.GET.get('cursemester')
    
        if course_code_from_url and clCourse_code_from_url and academicyear_from_url and semester_from_url:
            request.session['course_code'] = course_code_from_url
            request.session['clCourse_code'] = clCourse_code_from_url
            request.session['curscholastic'] = academicyear_from_url
            request.session['cursemester'] = semester_from_url

        course_code = request.session.get('course_code')
        clCourse_code = request.session.get('clCourse_code')
        academicyear = request.session.get('curscholastic')
        semester = request.session.get('cursemester')

        if not course_code or not clCourse_code or not academicyear or not semester :
            return redirect('home')
        
        query = """
           SELECT e.emo_name, e.emo_session_date,e.emo_time_status FROM emotion e
                    JOIN classcourse c ON e.emo_fromCourse_ID = c.clCourse_ID
                    JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                    JOIN teaching t ON c.cfa_ID = t.cfa_ID
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    JOIN courses cs on cs.course_code = cfa.course_code
                    WHERE i.ins_instructorCode = %s and cfa.course_code = %s
                        AND cfa.ay_schoolYear = %s
                        AND cfa.se_ID = %s"""
        query_params = [username, course_code, academicyear, semester]

        date = request.GET.get('date')
        status = request.GET.get('status')
        if date and status and status != 'all':
            query += " AND e.emo_session_date = %s"
            query_params.append(date)

            if status in ['happy', 'sad', 'fear', 'surprise', 'angry', 'neutral']:
                query += " AND e.emo_name = %s"
                query_params.append(status)

                query2 = """SELECT e.emo_name, COUNT(e.emo_name) as emo_count
                    FROM emotion e
                    JOIN classcourse c ON e.emo_fromCourse_ID = c.clCourse_ID
                    JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                    JOIN teaching t ON c.cfa_ID = t.cfa_ID
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    JOIN courses cs on cs.course_code = cfa.course_code
                    WHERE i.ins_instructorCode = %s AND cfa.course_code = %s
                        AND cfa.ay_schoolYear = %s
                        AND cfa.se_ID =%s anD e.emo_session_date = %s
                        AND e.emo_name = %s GROUP BY e.emo_name;"""
                query_params2 = [username, course_code, academicyear, semester,date,status]
            
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                emotion = cursor.fetchall()
            paginator = Paginator(emotion, 7)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            with connection.cursor() as cursor:
                cursor.execute(query2, query_params2)
                emotion_data = cursor.fetchall()

            labels = [row[0] for row in emotion_data]  
            values = [row[1] for row in emotion_data]
            return render(request, 'website/emotion.html', {
                'labels': labels,
                'values': values,
                'page_obj': page_obj,
                'status': status,
                'date': date,
                'course_code': course_code,
                'clCourse_code': clCourse_code,
                'academicyear': academicyear,
                'semester': semester,
                'avatar': avatar
            })

        elif date and status and status == 'all': 
            # extract avatar url
            with connection.cursor() as cursor:
                # extract avatar url
                cursor.execute("""
                    SELECT avatar
                    FROM instructor
                    WHERE ins_instructorCode = %s
                """, [username])
                instructor_info = cursor.fetchone()
                if instructor_info:
                    avatar =  instructor_info[0]
                    request.session['avatar'] = avatar

            query += " AND e.emo_session_date = %s"
            query_params.append(date)
            query2 = """SELECT e.emo_name, COUNT(e.emo_name) as emo_count
                    FROM emotion e
                    JOIN classcourse c ON e.emo_fromCourse_ID = c.clCourse_ID
                    JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                    JOIN teaching t ON c.cfa_ID = t.cfa_ID
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    JOIN courses cs on cs.course_code = cfa.course_code
                    WHERE i.ins_instructorCode = %s AND cfa.course_code = %s
                        AND cfa.ay_schoolYear = %s
                        AND cfa.se_ID =%s anD e.emo_session_date = %s
                        GROUP BY e.emo_name;"""
            query_params2 = [username, course_code, academicyear, semester, date]
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                emotion = cursor.fetchall()
            paginator = Paginator(emotion, 7)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            with connection.cursor() as cursor:
                cursor.execute(query2, query_params2)
                emotion_data = cursor.fetchall()
            labels = [row[0] for row in emotion_data]  # row[0] là tên cảm xúc (emo_name)
            values = [row[1] for row in emotion_data]  # row[1] là số lần xuất hiện (emo_count)
            return render(request, 'website/emotion.html', {
                'labels': labels,
                'values': values,
                'page_obj': page_obj,
                'status': status,
                'date': date,
                'course_code': course_code,
                'clCourse_code': clCourse_code,
                'academicyear': academicyear,
                'semester': semester,
                'avatar': avatar
            })
        else:
            query = """
                SELECT e.emo_name, e.emo_session_date,e.emo_time_status FROM emotion e 
                    JOIN classcourse c ON e.emo_fromCourse_ID = c.clCourse_ID
                    JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                    JOIN teaching t ON c.cfa_ID = t.cfa_ID
                    JOIN instructor i on t.ins_ID = i.ins_ID
                    JOIN courses cs on cs.course_code = cfa.course_code
                    WHERE i.ins_instructorCode = %s and cfa.course_code = %s
                        AND cfa.ay_schoolYear = %s
                        AND cfa.se_ID = %s"""
            query_params = [username, course_code, academicyear, semester] 
            with connection.cursor() as cursor:
                cursor.execute(query, query_params)
                emotion = cursor.fetchall()
            paginator = Paginator(emotion, 7)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            query2 = """
                SELECT e.emo_name, COUNT(e.emo_name) as emo_count
                FROM emotion e 
                JOIN classcourse c ON c.clCourse_ID =e.emo_fromCourse_ID
                JOIN coursefollowacayear cfa ON c.cfa_ID = cfa.cfa_ID 
                JOIN teaching t ON c.cfa_ID = t.cfa_ID
                JOIN instructor i on t.ins_ID = i.ins_ID
                JOIN courses cs on cs.course_code = cfa.course_code
                WHERE i.ins_instructorCode = %s and cfa.course_code = %s
                    AND cfa.ay_schoolYear = %s
                    AND cfa.se_ID = %s
                GROUP BY e.emo_name
            """
            query_params2 = [username, course_code, academicyear, semester]
            with connection.cursor() as cursor:
                cursor.execute(query2, query_params2)
                emotion_data = cursor.fetchall()
            labels = [row[0] for row in emotion_data]  # row[0] là tên cảm xúc (emo_name)
            values = [row[1] for row in emotion_data]  # row[1] là số lần xuất hiện (emo_count)
            return render(request, 'website/emotion.html', {
                'labels': labels,
                'values': values,
                'page_obj': page_obj,
                'status': status,
                'date': date,
                'course_code': course_code,
                'clCourse_code': clCourse_code,
                'academicyear': academicyear,
                'semester': semester,
                'avatar': avatar
            })