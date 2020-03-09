# pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + "/home/lmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)


# 学生表
class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    name = db.Column(db.String(64), nullable=False)  # 学生姓名
    gender = db.Column(db.Enum("男", "女"), nullable=False)  # 学生性别
    phone = db.Column(db.String(11), unique=True, nullable=False)  # 学生手机号
    courses = db.relationship("Course", secondary="student_course", backref="students")  # 关系关联
    grades = db.relationship("Grade", backref="student")  # 成绩关系关联


# 学生-课程中间表
class StudentCourse(db.Model):
    __tablename__ = "student_course"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    students_id = db.Column(db.Integer, db.ForeignKey("student.id"))  # 学生的id
    courses_id = db.Column(db.Integer, db.ForeignKey("course.id"))  # 课程的id


# 课程表
class Course(db.Model):
    __tablename__ = "course"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    name = db.Column(db.String(32), unique=True)  # 课程名字
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"))  # 所属老师的id
    grades = db.relationship("Grade", backref="course")  # 成绩关系关联


# 教师表
class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    name = db.Column(db.String(32), unique=True)  # 姓名
    phone = db.Column(db.String(11), unique=True, nullable=False)  # 手机号
    gender = db.Column(db.Enum("男", "女"), nullable=False)  # 性别
    course = db.relationship("Course", backref="teacher")  # 所教课程


# 成绩表
class Grade(db.Model):
    __tablename__ = "grade"
    id = db.Column(db.Integer, primary_key=True)  # id号(独一无二的)
    my_grade = db.Column(db.String(32), unique=True)  # 分数
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"))  # 所属课程
    students_id = db.Column(db.Integer, db.ForeignKey("student.id"))  # 所属学生


if __name__ == "__main__":
    db.create_all()
    # db.drop_all()
