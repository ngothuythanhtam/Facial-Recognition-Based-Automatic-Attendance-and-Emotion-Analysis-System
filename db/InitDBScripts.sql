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
    ins_academicRank varchar(255) default null,
    ins_phone_number varchar(255) default null unique,
    ins_gmail varchar(255) default null unique
);

select * from instructor;

select ins_instructorCode, ins_name, ins_academicRank, ins_phone_number, ins_gmail 
from instructor 
where ins_instructorCode = '1229';

update instructor set ins_phone_number = '0908678710' where ins_instructorCode = '1229';
update instructor set ins_gmail = 'ptphi@cit.ctu.edu.vn' where ins_instructorCode = '1229';

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
    ad_rank varchar(255) default null,
    ad_phoneNumber varchar(10) default null,
    ad_gmail varchar(255) default null unique 
);

select * from administrator;
insert into administrator (ad_code, ad_name, ad_rank, ad_phoneNumber, ad_gmail) value ('admin', 'Khúc Bảo Minh', 'B.Sc.', '0890765124', 'kbminh@gmail.com');

select ad_code, ad_name, ad_rank, ad_phoneNumber, ad_gmail from administrator where ad_code = 'admin';
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

select * from classCourse;

-- Giảng Dạy 
create table teaching (
	teaching_ID int auto_increment primary key,
	clCourse_ID int,
    ins_ID int,
    constraint fk_clc_instructor foreign key (clCourse_ID) references classCourse (clCourse_ID),
    constraint fk_instructor_clc foreign key (ins_ID) references instructor (ins_ID)
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


CREATE TABLE emotion (
    emo_ID INT AUTO_INCREMENT,
    emo_fromCourse_ID int,
    emo_name varchar(50),
    emo_session_date DATE,
    emo_time_status TIME,
    FOREIGN KEY (emo_fromCourse_ID) 
        REFERENCES studying (clCourse_ID),
    PRIMARY KEY (emo_ID)
);

select * from emotion;

CREATE TABLE timeTable (
    tt_ID INT PRIMARY KEY AUTO_INCREMENT,
    clCourse_ID INT,
    tt_start INT NOT NULL,
    tt_classPeriod int,
    DOW_ID INT,
    room_id int,
    FOREIGN KEY (room_id) REFERENCES classRoom (room_id),
    FOREIGN KEY (clCourse_ID) REFERENCES classCourse (clCourse_ID),
    FOREIGN KEY (DOW_ID) REFERENCES dayOfWeak (DOW_ID)
);

-- Chèn dữ liệu cho học phần 4 nhóm (cfa_ID = 4)
INSERT INTO timeTable (clCourse_ID, tt_start, tt_classPeriod, DOW_ID, room_id)
VALUES 
(1, 8, 2, 1, 1),  -- Nhóm 1 học vào thứ 2 (Monday), tại Phòng 201
(1, 9, 2, 2, 2),  -- Nhóm 2 học vào thứ 3 (Tuesday), tại Phòng 202
(1, 10, 2, 3, 3), -- Nhóm 3 học vào thứ 4 (Wednesday), tại Phòng 203
(1, 11, 2, 4, 4); -- Nhóm 4 học vào thứ 5 (Thursday), tại Phòng 204

-- Chèn dữ liệu cho học phần tiếp theo (cfa_ID = 5)
INSERT INTO timeTable (clCourse_ID, tt_start, tt_classPeriod, DOW_ID, room_id)
VALUES 
(3, 8, 2, 1, 5),  -- Nhóm 1 học vào thứ 2 (Monday), tại Phòng 205
(3, 9, 2, 2, 6),  -- Nhóm 2 học vào thứ 3 (Tuesday), tại Phòng 206
(3, 10, 2, 3, 7), -- Nhóm 3 học vào thứ 4 (Wednesday), tại Phòng 207
(3, 11, 2, 4, 8); -- Nhóm 4 học vào thứ 5 (Thursday), tại Phòng 208

-- Chèn dữ liệu cho học phần tiếp theo (cfa_ID = 9)
INSERT INTO timeTable (clCourse_ID, tt_start, tt_classPeriod, DOW_ID, room_id)
VALUES 
(22, 8, 2, 1, 9),  -- Nhóm 1 học vào thứ 2 (Monday), tại Phòng 209
(22, 9, 2, 2, 10), -- Nhóm 2 học vào thứ 3 (Tuesday), tại Phòng 210
(22, 10, 2, 3, 11),-- Nhóm 3 học vào thứ 4 (Wednesday), tại Phòng 211
(22, 11, 2, 4, 12);-- Nhóm 4 học vào thứ 5 (Thursday), tại Phòng 212

-- Chèn dữ liệu cho học phần tiếp theo (cfa_ID = 27)
INSERT INTO timeTable (clCourse_ID, tt_start, tt_classPeriod, DOW_ID, room_id)
VALUES 
(23, 8, 2, 1, 13),  -- Nhóm 1 học vào thứ 2 (Monday), tại Phòng 213
(23, 9, 2, 2, 14),  -- Nhóm 2 học vào thứ 3 (Tuesday), tại Phòng 214
(23, 10, 2, 3, 15), -- Nhóm 3 học vào thứ 4 (Wednesday), tại Phòng 215
(23, 11, 2, 4, 16); -- Nhóm 4 học vào thứ 5 (Thursday), tại Phòng 216

-- Chèn dữ liệu cho học phần tiếp theo (cfa_ID = 38)
INSERT INTO timeTable (clCourse_ID, tt_start, tt_classPeriod, DOW_ID, room_id)
VALUES 
(28, 8, 2, 1, 17),  -- Nhóm 1 học vào thứ 2 (Monday), tại Phòng 217
(28, 9, 2, 2, 18),  -- Nhóm 2 học vào thứ 3 (Tuesday), tại Phòng 218
(28, 10, 2, 3, 19), -- Nhóm 3 học vào thứ 4 (Wednesday), tại Phòng 219
(28, 11, 2, 4, 20); -- Nhóm 4 học vào thứ 5 (Thursday), tại Phòng 220


CREATE TABLE dayOfWeak (
    DOW_ID INT PRIMARY KEY AUTO_INCREMENT,
    DOW_day VARCHAR(50) NOT NULL
);

INSERT INTO dayOfWeak (DOW_day) VALUES 
('Monday'), 
('Tuesday'), 
('Wednesday'), 
('Thursday'), 
('Friday'), 
('Saturday'), 
('Sunday');

create table classRoom (
	room_id int auto_increment primary key,
    room_name varchar(255) not null unique
);

INSERT INTO classRoom (room_name) VALUES 
('Phòng 201'),
('Phòng 202'),
('Phòng 203'),
('Phòng 204'),
('Phòng 205'),
('Phòng 206'),
('Phòng 207'),
('Phòng 208'),
('Phòng 209'),
('Phòng 210'),
('Phòng 211'),
('Phòng 212'),
('Phòng 213'),
('Phòng 214'),
('Phòng 215'),
('Phòng 216'),
('Phòng 217'),
('Phòng 218'),
('Phòng 219'),
('Phòng 220');

CREATE TABLE timeTable (
    tt_ID INT PRIMARY KEY AUTO_INCREMENT,
    clCourse_ID INT,
    tt_start INT NOT NULL,
    tt_classPeriod int,
    DOW_ID INT,
    room_id int,
    FOREIGN KEY (room_id) REFERENCES classRoom (room_id),
    FOREIGN KEY (clCourse_ID) REFERENCES classCourse (clCourse_ID),
    FOREIGN KEY (DOW_ID) REFERENCES dayOfWeak (DOW_ID)
);
SELECT s.st_code, a.session_date, a.time_status, t.tt_start, cr.room_name, d.DOW_day 
FROM attendance a
JOIN studying s ON a.studying_st_code = s.st_code
JOIN timeTable t ON t.clCourse_ID = s.clCourse_ID
JOIN classRoom cr ON t.room_id = cr.room_id
JOIN dayofweak d ON t.DOW_ID = d.DOW_ID;

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
insert into accounts values('Nguyen Van A',"1",1);
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

alter table administrator change ad_mail ad_gmail varchar(55);
update administrator set ad_gmail = "tamb2111949@admin.com" where ad_ID  = 1;
update administrator set ad_code = "admin" where ad_ID  = 1;