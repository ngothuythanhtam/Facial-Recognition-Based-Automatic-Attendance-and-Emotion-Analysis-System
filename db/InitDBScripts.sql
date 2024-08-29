create database face_recognition default charset utf8mb4;
use face_recognition;
drop database face_recognition;


-- Ngành Học
create table majors (
	maj_Code varchar(8) primary key,
    maj_name varchar(255) unique not null
);

-- Lớp Ngành
create table class (
    cl_className varchar(10) primary key ,
    maj_Code varchar(8),
    foreign key (maj_Code) references majors(maj_Code) on delete cascade
);

-- Giảng Viên
create table instructor (
	ins_ID int primary key auto_increment,
	ins_instructorCode varchar(8) unique not null,
    ins_name varchar(255) not null,
    ins_academicRank varchar(255) default null
);

-- Sinh Viên
create table students (
	st_ID int auto_increment primary key,
	st_code varchar(8) not null unique,
    st_fullName varchar(255) not null,
    st_birthDay date,
    st_phone char(10) default null,
    st_email varchar(255) default null,
    # st_status varchar(255) default 'chưa điểm danh',
    cl_className varchar(10) ,
    foreign key (cl_className) references class(cl_className) on delete cascade
);

-- Quản Trị Viên
-- làm rõ ai là người quản lí
create table administrator (
	ad_ID int auto_increment primary key,
	ad_code varchar(10) unique not null,
    ad_name varchar(255) not null,
    ad_phoneNumber varchar(10) default null,
    ad_pass varchar(15) not null
);

-- Vai Trò
create table roles (
	role_ID int primary key,
    role_name varchar(255)
);

-- Tài Khoản
create table accounts (
	acc_ID int primary key auto_increment,
    acc_username varchar(255) unique not null,
    acc_password varchar(255) not null,
    role_ID int,
    foreign key (role_ID) references roles (role_ID)
);

-- Năm Học
create table years (
    ay_schoolYear varchar(255) not null primary key
);

-- Học Kỳ
create table semester (
	se_ID int primary key,
    se_semesterName varchar(255)
);

-- Niên Khoá 
create table academicYear (
	aca_ID int auto_increment primary key,
	ay_schoolYear varchar(255),
    se_ID int,
    foreign key (se_ID) references semester (se_ID),
    foreign key (ay_schoolYear) references years (ay_schoolYear)
);

-- Học Phần 
create table courses (
	course_ID int auto_increment primary key,
	course_code varchar(10) unique,
    course_name varchar(255) not null,
    course_credits int not null,
	maj_Code varchar(8),
    foreign key (maj_Code) references majors(maj_Code) on delete cascade
);
-- Quản Lí Môn Học Theo Niên Khoá
create table courseFollowAcaYear (
	cfa_ID int primary key auto_increment,
	course_code varchar(10),
    ay_schoolYear varchar(255),
    se_ID int,
    foreign key (course_code) references courses (course_code),
    foreign key (se_ID) references semester (se_ID),
    foreign key (ay_schoolYear) references years (ay_schoolYear)
);

-- Nhóm Học Phần
# create table classCourse (
# 	clCourse_ID int auto_increment primary key,
# 	clCourse_code varchar(10),
#     clCourse_className varchar(255) not null,
#     clCourse_amount int not null,
#     clCourse_remainAmount int default 0,
# 	cfa_ID int,
#     foreign key (cfa_ID) references courseFollowAcaYear (cfa_ID)
# );
create table classCourse (
	clCourse_ID int auto_increment primary key,
	clCourse_code varchar(10),
    clCourse_amount int not null,
	cfa_ID int,
    foreign key (cfa_ID) references courseFollowAcaYear (cfa_ID)
);

-- Học Phần thuộc Ngành
-- create table courseOfMajor (
-- 	course_ID int,
--     maj_ID int,
--     constraint fk_course_major foreign key (course_ID) references courses (course_ID),
--     constraint fk_major_course foreign key (maj_ID) references majors (maj_ID),
--     primary key (course_ID, maj_ID)
-- );

-- Giảng Dạy 
create table teaching (
	teaching_ID int auto_increment primary key,
	cfa_ID int,
    ins_ID int,
    constraint fk_cfa_instructor foreign key (cfa_ID) references courseFollowAcaYear (cfa_ID),
    constraint fk_instructor_cfa foreign key (ins_ID) references instructor (ins_ID)
);	

-- Học 
create table studying (
	st_code varchar(8),
    clCourse_ID int,
    foreign key (st_code) references students (st_code),
    foreign key (clCourse_ID) references classCourse (clCourse_ID),
    primary key (st_code, clCourse_ID)
);
select * from studying;

CREATE TABLE attendance (
    att_ID INT AUTO_INCREMENT,
    studying_st_code varchar(8),
    studying_clCourse_ID INT,
    session_date DATE,
    time_status TIME,
    FOREIGN KEY (studying_st_code, studying_clCourse_ID) 
        REFERENCES studying (st_code, clCourse_ID),
    PRIMARY KEY (att_ID),
    UNIQUE KEY (studying_st_code, studying_clCourse_ID, session_date)
);
select * from attendance;

insert into attendance values ('', "B2111949", 5,current_date(), curtime());

-- TESTING 
-- insert
insert into years (ay_schoolYear)
values 
('2021-2022'),
('2022-2023'),
('2023-2024'),
('2024-2025'),
('2025-2026');

insert into semester values 
(1, 'Học Kỳ 1'),
(2, 'Học Kỳ 2'),
(3, 'Học Kỳ Hè');

insert into academicYear (ay_schoolYear, se_ID) values 
('2021-2022', '1'),
('2021-2022', '2'),
('2021-2022', '3'),
('2022-2023', '1'),
('2022-2023', '2'),
('2022-2023', '3'),
('2023-2024', '1'),
('2023-2024', '2'),
('2023-2024', '3'),
('2024-2025', '1'),
('2024-2025', '2'),
('2024-2025', '3'),
('2025-2026', '1'),
('2025-2026', '2'),
('2025-2026', '3');

insert into majors (maj_Code, maj_name) 
value ('7480201C', 'Công Nghệ Thông Tin - CLC');

insert into class (cl_className, maj_Code) values
 ('DI21V7F1', '7480201C'),
 ('DI21V7F2', '7480201C'),
 ('DI21V7F3', '7480201C'),
 ('DI21V7F4', '7480201C');
 
 insert into roles values(1, 'teacher'),(2,'student');

insert into administrator(ad_code, ad_name, ad_phoneNumber, ad_pass) values('1','Thanh Tam', '0123456789','1');
select * from administrator;

select * from class;
select * from courses;
select * from students;
select * from majors;
select * from academicYear;
select * from years;
select * from classcourse;
select * from coursefollowacayear;
select * from studying;
select * from students;
select * from accounts;
select * from roles;
drop table accounts;
select * from attendance;
select * from semester;

select c.clCourse_code, cfa.course_code, s.st_code from classcourse c 
	join coursefollowacayear cfa on c.cfa_ID = cfa.cfa_ID
	join studying s on c.clCourse_ID = s.clCourse_ID
    ;

SELECT cl.clCourse_ID, cl.clCourse_code, c.course_name FROM classcourse cl 
join coursefollowacayear cfa on cl.cfa_ID = cfa.cfa_ID
join courses c on c.course_code = cfa.course_code;

SELECT * from coursefollowacayear ;
insert into classcourse values("", "M01","21", '44');
