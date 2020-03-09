from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + "/home/lmp/sql/first.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jjjsks"

db = SQLAlchemy(app)  # 实例化的数据库


# 学生表
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(64), nullable=False)  # 学生姓名 nullable能否为空
    gender = db.Column(db.Enum("男", "女"), nullable=False)  # 性别 Enum枚举 不能为空
    phone = db.Column(db.String(11))  # 手机号 可以为空
    grades = db.relationship("Grade", backref="student")  # 成绩关系关联
    courses = db.relationship("Course", secondary="student_to_course", backref="students")  # 关系关联


# 中间表
class StudenToCourse(db.Model):
    __tablename__ = "student_to_course"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))  # 所属学生
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))  # 所属课程


# 课程表
class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(64), nullable=False)  # 课名
    grades = db.relationship("Grade", backref="course")  # 成绩关系关联
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))  # 所属教师


# 教师表
class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(64), nullable=False)  # 教师姓名 nullable能否为空
    gender = db.Column(db.Enum("男", "女"), nullable=False)  # 性别 Enum枚举 不能为空
    phone = db.Column(db.String(11))  # 手机号 可以为空
    course = db.relationship("Course", backref="teacher")  # 课程关系关联


# 成绩表
class Grade(db.Model):
    __tablename__ = "grade"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    grade = db.Column(db.String(3), nullable=False)  # 成绩 nullable能否为空
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"))  # 所属学生
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))  # 所属课程


if __name__ == '__main__':
    db.create_all()
    # db.drop_all()
