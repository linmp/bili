from models import Student, Teacher, Course, Grade, db

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


# 增
def add_one_by_one(data):
    db.session.add(data)
    db.session.commit()


def add_all_sql():
    db.session.add_all(
        [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9, teacher0,
         teacher1, teacher2, teacher3, teacher4, teacher5, course0, course1, course2, course3, course4, course5])
    db.session.commit()


# 查
def get_test():
    """
    id查找
    :return:
    """
    s = Student.query.get(10)
    print(s.phone)


def filter_test():
    """
    表达式查找
    :return:
    """
    s = Student.query.filter(Student.id >= 5).all()
    print(s)

    print("---------------")

    sss = Student.query.filter(Student.id >= 5).order_by(Student.id.desc()).all()
    for ss in sss:
        print(ss.id)


def filter_by_test():
    """
    原生查找
    :return:
    """
    s = Student.query.filter_by(id=4).first()
    print(s)


# 改
def mod_test():
    user = Student.query.filter(Student.name == "李依").update({"name": "李毅", "gender": "男"})
    # user = Student.query.filter(Student.id > 3).update({"name": "李毅", "gender": "男"}) # 更新多条
    db.commit()
    print("-----------")
    user.name = "李毅"
    db.session.add(user)
    db.commit()


# 删
def delete_test():
    user = Student.query.filter(Student.name == "李依").delete()
    # user = Student.query.filter(Student.id > 3).delete() # 删除多条
    db.commit()


def one_to_more():
    # 为学生添加成绩
    # grade1 = Grade(my_grade="98", course_id=1, students_id=1)
    # grade2 = Grade(my_grade="97", course_id=2, students_id=1)
    # grade3 = Grade(my_grade="96", course_id=3, students_id=1)
    # grade4 = Grade(my_grade="95", course_id=4, students_id=1)
    # grade5 = Grade(my_grade="80", course_id=5, students_id=1)
    # grade6 = Grade(my_grade="59", course_id=6, students_id=1)
    # db.session.add_all([grade1, grade2, grade3, grade4, grade5, grade6])
    # db.session.commit()
    print("-------------------")

    # course_mod = Course.query.filter(Course.teacher_id == None).update({"teacher_id": 1})
    # print(course_mod)
    # db.session.commit()


if __name__ == '__main__':
    # add_one_by_one(student0)
    # add_all_sql()
    # get_test()
    # filter_test()
    # filter_by_test()
    # one_to_more()

    # 添加课程
    # c1 = Course.query.get(1)
    # c2 = Course.query.get(2)
    # c3 = Course.query.get(3)
    # c4 = Course.query.get(4)
    # c5 = Course.query.get(5)
    # c6 = Course.query.get(6)
    # stu.courses = [c1, c2, c3, c4, c5, c6]
    # db.session.add(stu)
    # db.session.commit()

    # 课程添加学生
    # s = Student.query.filter(Student.id >= 1).all()
    # c = Course.query.get(1)
    # c.students = s
    # db.session.add(c)
    # db.session.commit()

    # 查询第一个学生的信息
    stu = Student.query.get(1)
    for i in stu.courses:
        print(i.name, i.teacher.name, i.teacher.gender, i.teacher.phone)
    print("-----------")

    grades = stu.grades
    for i in grades:
        print(stu.name, stu.gender, stu.phone, i.my_grade, i.course.name, i.course.teacher.name,
              i.course.teacher.gender, i.course.teacher.phone)

    print("------")
    c = Course.query.get(1)
    for i in c.students:
        print(i.name, [j.my_grade for j in i.grades])
