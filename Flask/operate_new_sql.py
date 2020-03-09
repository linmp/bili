from learn_sql import db, Student, Grade, Teacher, Course

# 增

# s = Student(name="张三", gender="男", phone="12345678900")

# s1 = Student(name="kk", gender="女")
# s2 = Student(name="张蛋", gender="女")
# s3 = Student(name="李四", gender="男")
# s4 = Student(name="李鬼", gender="男", phone="12345678900")

# 语句 第一种
# db.session.add(s1)
# db.session.commit()
#
# db.session.add_all([s1, s2, s3, s4])
# db.session.commit()

# 查

# get(id) 查 单一个
# stu = Student.query.get(1)
# print(stu.name)
# print(stu.gender)
# print(stu.phone)

# all() 查全部
# stu = Student.query.all()
# for i in stu:
#     print(i.name, i.gender, i.phone)

# filter() 条件查询
# stu = Student.query.filter(Student.gender == "女")
# for i in stu:
#     print(i.name, i.id,i.gender)


# filter_by() 比较类似SQL的查询  first() 查询到的第一个
# stu = Student.query.filter_by(name="张三").filter(Student.id >= 2)
# for i in stu:
#     print(i.name, i.id)

# 改
# 第一种
# stu = Student.query.filter(Student.id == 1).update({"name": "张毅"})# 返回动了多少条数据
# db.session.commit()

# stu = Student.query.filter(Student.gender == "男").update({"gender": "女"})  # 返回动了多少条数据
# print(stu)
# db.session.commit()

# 第二种
# stu = Student.query.filter(Student.gender == "女").all()
# for i in stu:
#     i.gender = "男"
#     db.session.add(i)
# db.session.commit()


# 删
#
# stu = Student.query.filter(Student.id >= 5).delete()  # 返回动了多少条数据
# print(stu)
# db.session.commit()

# stu = Student.query.all()
# for i in stu:
#     print(i.gender,i.name)

print("--------------------------")

# grade1 = Grade(grade=100, student_id=1)
# grade2 = Grade(grade=95, student_id=1)
#
# db.session.add(grade1)
# db.session.add(grade2)
# db.session.commit()

# stu = Student.query.all()
# for i in stu:
#     print(i.gender, i.name)

# grade = Grade.query.filter(Grade.student_id==1).all()
# for i in grade:
#     print(i.student)

# 通过 一 访问 多
# stu = Student.query.get(1)
# for i in stu.grades:
#     print(stu.name,i.grade)


# 通过 多 访问 一

# grade = Grade.query.filter(Grade.grade == "100").all()
# for i in grade:
#     print(i.student.name,i.student.gender)


# 多对多
# student0 = Student(name="李玲", gender="女", phone="12345678900")
# student1 = Student(name="李依", gender="女", phone="12345678901")
# student2 = Student(name="李贰", gender="男", phone="12345678902")
# student3 = Student(name="李叁", gender="男", phone="12345678903")
# student4 = Student(name="李斯", gender="男", phone="12345678904")
# student5 = Student(name="李舞", gender="女", phone="12345678905")
# student6 = Student(name="李榴", gender="男", phone="12345678906")
# student7 = Student(name="李淇", gender="女", phone="12345678907")
# student8 = Student(name="李巴", gender="男", phone="12345678908")
# student9 = Student(name="李玖", gender="男", phone="12345678909")
#
# teacher0 = Teacher(name="老数", gender="男", phone="12345678910")
# teacher1 = Teacher(name="老语", gender="女", phone="12345678911")
# teacher2 = Teacher(name="老英", gender="女", phone="12345678912")
# teacher3 = Teacher(name="老物", gender="男", phone="12345678913")
# teacher4 = Teacher(name="老化", gender="男", phone="12345678914")
# teacher5 = Teacher(name="老生", gender="男", phone="12345678915")
#
# course0 = Course(name="数学")
# course1 = Course(name="语文")
# course2 = Course(name="英语")
# course3 = Course(name="物理")
# course4 = Course(name="化学")
# course5 = Course(name="生物")
#
# db.session.add_all(
#     [student0, student1, student2, student3, student4, student5, student6, student7, student8, student9, teacher0,
#      teacher1, teacher2, teacher3, teacher4, teacher5, course0, course1, course2, course3, course4, course5])
# db.session.commit()

# for i in range(1, 7):
#     c = Course.query.filter(Course.id == i).update({"teacher_id": i})
# db.session.commit()






# 查询课程表
cs = Course.query.filter(Course.id >= 2).all()
print(cs)
# 查询学生
stu = Student.query.filter(Student.id >= 2).all()
for s in stu:
    s.courses = cs
    db.session.add(s)
    db.session.commit()

# 学生查询课程
stu = Student.query.get(1)
for s in stu.courses:
    print(s.name)
print(stu.courses)

print("===================")

# 课程查询学生
c = Course.query.get(2)
for s in c.students:
    print(s.name)