create database face_recognition default charset utf8mb4;
use face_recognition;


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

select * from students;

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
	ay_ID int primary key auto_increment,
    ay_schoolYear varchar(255) not null
);

-- Học Kỳ
create table semester (
	se_ID int primary key,
    se_semesterName varchar(255)
);

-- Niên Khoá 
create table academicYear (
	aca_ID int auto_increment primary key,
	ay_ID int,
    se_ID int,
    foreign key (se_ID) references semester (se_ID),
    foreign key (ay_ID) references years (ay_ID)
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
select * from courses;

-- Quản Lí Môn Học Theo Niên Khoá
create table courseFollowAcaYear (
	cfa_ID int primary key auto_increment,
	course_ID int,
    aca_ID int,
    foreign key (course_ID) references courses (course_ID),
    foreign key (aca_ID) references academicYear (aca_ID)
);

-- Nhóm Học Phần
create table classCourse (
	clCourse_ID int auto_increment primary key,
	clCourse_code varchar(10),
    clCourse_className varchar(255) not null,
    clCourse_amount int not null,
    clCourse_remainAmount int default 0,
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
	st_ID int,
    clCourse_ID int,
    foreign key (st_ID) references students (st_ID),
    foreign key (clCourse_ID) references classCourse (clCourse_ID),
    primary key (st_ID, clCourse_ID)
);



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

insert into academicYear (ay_ID, se_ID) values 
('1', '1'),
('1', '2'),
('1', '3');

insert into majors (maj_Code, maj_name) 
value ('7480201C', 'Công Nghệ Thông Tin');

insert into class (cl_className, maj_Code) values
 ('DI21V7F1', '7480201C'),
 ('DI21V7F2', '7480201C'),
 ('DI21V7F3', '7480201C'),
 ('DI21V7F4', '7480201C');
select * from courses;
 select * from students;
insert into administrator values('','1','Thanh Tam', '0123456789','1');
select * from administrator;
delete from administrator where ad_ID = 1;
