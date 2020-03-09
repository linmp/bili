## Python 操作数据库

### 创建数据库

```python
# pip install flask-sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + "/home/lmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'xxx'
db = SQLAlchemy(app)

if __name__ == "__main__":
    # db.create_all()
    # db.drop_all()

```
### 创建表

学生表

|学生编号 |学生姓名 |学生性别 |手机号|
|:---:|:---:|:---:|:---:|
| id | name | gender | phone |

学生-课程中间表
|学生编号 |学生id |课程id |
|:---:|:---:|:---:|
| id | students_id | courses_id |

课程表
|课程编号 |课程名 |教师id|
|:---:|:---:|:---:|
| id | name | teacher_id|

教师表
|教师编号 |教师姓名 | 性别|教师手机号|
|:---:|:---:|:---:|:---:|
| id | name | gender |phone|


成绩表
|课程编号 |分数 |课程id|学生id|
|:---:|:---:|:---:|:---:|
| id | my_grade | course_id |students_id  |



```python
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

```


```python
student0 = Student(name="李玲", gender="女", phone="12345678900")
student1 = Student(name="李依", gender="女", phone="12345678901")
student2 = Student(name="李贰", gender="男", phone="12345678902")
student3 = Student(name="李叁", gender="男", phone="12345678903")
student4 = Student(name="李斯", gender="男", phone="12345678904")
student5 = Student(name="李舞", gender="女", phone="12345678905")
student6 = Student(name="李榴", gender="男", phone="12345678906")
student7 = Student(name="李淇", gender="女", phone="12345678907")
student8 = Student(name="李巴", gender="男", phone="12345678908")
student9 = Student(name="李玖", gender="男", phone="12345678909")

teacher0 = Teacher(name="老数", gender="男", phone="12345678910")
teacher1 = Teacher(name="老语", gender="女", phone="12345678911")
teacher2 = Teacher(name="老英", gender="女", phone="12345678912")
teacher3 = Teacher(name="老物", gender="男", phone="12345678913")
teacher4 = Teacher(name="老化", gender="男", phone="12345678914")
teacher5 = Teacher(name="老生", gender="男", phone="12345678915")

course0 = Course(name="数学")
course1 = Course(name="语文")
course2 = Course(name="英语")
course3 = Course(name="物理")
course4 = Course(name="化学")
course5 = Course(name="生物")

    db.session.add_all(
        [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9, teacher0,
         teacher1, teacher2, teacher3, teacher4, teacher5, course0, course1, course2, course3, course4, course5])
    db.session.commit()
```



### 增删查改

- 增
 -  db.session.add(one)
```
    db.session.add(student0)
    db.session.commit()
```
   -  db.session.add_all([one,two,three])

```
    db.session.add_all(
        [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9, teacher0,
         teacher1, teacher2, teacher3, teacher4, teacher5, course0, course1, course2, course3, course4, course5])
    db.session.commit()
```


- 查
  - get
 ```
   #id查找
   s = Student.query.get(10)
    print(s.phone)
 ```
  - filter
 ```
# 表达式查找
   s = Student.query.filter(Student.id >= 5).all()
    print(s) # 多条内容

    print("---------------")
# 排序
    sss = Student.query.filter(Student.id >= 5).order_by(Student.id.desc()).all()
    for ss in sss:
        print(ss.id)
 ```
  - filter_by
```
	#原生查找
    s = Student.query.filter_by(id=4).first()
    print(s)
```
  - order_by()
    - desc()



- 删
  
  - delete() 
 ```
     user = Student.query.filter(Student.name == "李依").delete()
    # user = Student.query.filter(Student.id > 3).delete() # 删除多条
    db.commit()
 ```


- 改
  - update({"name" : "099"})
  -  add() 
```
    user = Student.query.filter(Student.name == "李依").update({"name": "李毅", "gender": "男"})
    # user = Student.query.filter(Student.id > 3).update({"name": "李毅", "gender": "男"}) # 更新多条
    db.commit()
    print("-----------")
    user.name = "李毅"
    db.session.add(user)
    db.commit()

```

### 一对多

- ForeignKey 多方

- relationship 一方

 - 增删查改


### 多对多
- 第三张表