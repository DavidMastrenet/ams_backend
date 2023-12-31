-- 创建库
create database if not exists ams_dev;

-- 切换库
use ams_dev;

-- 班级表
CREATE TABLE class
(
    class_id   INT PRIMARY KEY AUTO_INCREMENT,
    class_name VARCHAR(255) NOT NULL
);

-- 学院表
CREATE TABLE department
(
    department_id   INT PRIMARY KEY AUTO_INCREMENT,
    department_name VARCHAR(255) NOT NULL
);

-- 学院班级对应表
CREATE TABLE class_department_mapping
(
    class_id      INT PRIMARY KEY,
    department_id INT,
    FOREIGN KEY (class_id) REFERENCES class (class_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

-- 用户信息
CREATE TABLE user_info
(
    cuid          INT PRIMARY KEY,
    uid           VARCHAR(10)                 NOT NULL,
    username      VARCHAR(20)                 NOT NULL,
    user_type     ENUM ('teacher', 'student') NOT NULL, -- 老师或学生
    password      VARCHAR(128)                NOT NULL,
    is_admin      BOOLEAN   DEFAULT FALSE,
    class_id      INT,
    department_id INT,
    last_update   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (class_id) REFERENCES class (class_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

-- 用户权限
CREATE TABLE user_role
(
    user_role_id INT PRIMARY KEY AUTO_INCREMENT,
    cuid         INT,
    role         VARCHAR(20) NOT NULL, -- e.g., 'class_admin', 'department_admin', 'school_admin'
    start_date   DATE,
    end_date     DATE,
    auth_by      INT,
    FOREIGN KEY (cuid) REFERENCES user_info (cuid),
    FOREIGN KEY (auth_by) REFERENCES user_info (cuid)
);

-- 活动信息
CREATE TABLE activity
(
    activity_id    INT PRIMARY KEY AUTO_INCREMENT,
    name           VARCHAR(255)                      NOT NULL,
    time           DATETIME                          NOT NULL,
    location       VARCHAR(255)                      NOT NULL,
    can_sign_up    ENUM ('no', 'yes', 'conditional') NOT NULL,
    start_register DATETIME,
    end_register   DATETIME,
    can_quit       BOOLEAN DEFAULT TRUE,
    description    TEXT,
    organizer_id   INT,
    FOREIGN KEY (organizer_id) REFERENCES user_info (cuid)
);

-- 活动权限
CREATE TABLE activity_permission
(
    permission_id INT PRIMARY KEY AUTO_INCREMENT,
    cuid          INT,
    activity_id   INT,
    FOREIGN KEY (cuid) REFERENCES user_info (cuid),
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id)
);

-- 活动参与表 -- 学院及班级的
CREATE TABLE group_activity
(
    activity_participation_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_id               INT,
    class_id                  INT,
    department_id             INT,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (class_id) REFERENCES class (class_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE group_activity_registration
(
    registration_id    INT PRIMARY KEY AUTO_INCREMENT,
    activity_id        INT,
    department_id      INT,
    allow_registration BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (department_id) REFERENCES department (department_id)
);

-- 活动参与表 -- 个人的
CREATE TABLE user_activity
(
    user_activity_id  INT PRIMARY KEY AUTO_INCREMENT,
    cuid              INT,
    activity_id       INT,
    is_approved       BOOLEAN DEFAULT FALSE,
    registration_time DATETIME NOT NULL,
    approved_time     DATETIME,
    FOREIGN KEY (cuid) REFERENCES user_info (cuid),
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id)
);

-- 签到方式
CREATE TABLE check_in_method
(
    method_id   INT PRIMARY KEY AUTO_INCREMENT,
    method_name VARCHAR(255) NOT NULL
);

-- 活动签到发布
CREATE TABLE check_in
(
    check_in_id INT PRIMARY KEY AUTO_INCREMENT,
    activity_id INT,
    method_id   INT,
    start_date  DATETIME,
    end_date    DATETIME,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (method_id) REFERENCES check_in_method (method_id)
);

-- 活动签到
CREATE TABLE check_in_record
(
    check_in_record_id INT PRIMARY KEY AUTO_INCREMENT,
    check_in_id        INT,
    cuid               INT,
    latitude           DOUBLE,
    longitude          DOUBLE,
    check_in_time      DATETIME NOT NULL,
    FOREIGN KEY (check_in_id) REFERENCES check_in (check_in_id),
    FOREIGN KEY (cuid) REFERENCES user_info (cuid)
);

-- 互动评论
CREATE TABLE comment
(
    comment_id   INT PRIMARY KEY AUTO_INCREMENT,
    activity_id  INT,
    cuid         INT,
    content      TEXT     NOT NULL,
    comment_time DATETIME NOT NULL,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (cuid) REFERENCES user_info (cuid)
);

-- 活动反馈
CREATE TABLE feedback
(
    feedback_id        INT PRIMARY KEY AUTO_INCREMENT,
    activity_id        INT,
    cuid               INT,
    satisfaction_level INT,
    suggestions        TEXT,
    feedback_time      DATETIME NOT NULL,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (cuid) REFERENCES user_info (cuid)
);

-- 活动通知
CREATE TABLE notification
(
    notification_id   INT PRIMARY KEY AUTO_INCREMENT,
    activity_id       INT,
    message           TEXT     NOT NULL,
    notification_time DATETIME NOT NULL,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id)
);

-- 活动分类
CREATE TABLE activity_category
(
    category_id   INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(255) NOT NULL
);

-- 活动与分类的关联
CREATE TABLE activity_category_mapping
(
    activity_id INT,
    category_id INT,
    PRIMARY KEY (activity_id, category_id),
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (category_id) REFERENCES activity_category (category_id)
);

-- 资金管理
CREATE TABLE financial_transaction
(
    transaction_id   INT PRIMARY KEY AUTO_INCREMENT,
    activity_id      INT,
    cuid             INT,
    amount           DECIMAL(10, 2) NOT NULL,
    transaction_time DATETIME       NOT NULL,
    FOREIGN KEY (activity_id) REFERENCES activity (activity_id),
    FOREIGN KEY (cuid) REFERENCES user_info (cuid)
);
