from model import *
import time
import random

def users(count=20):
    fake = Faker('zh_CN')
    i = 1
    while i <= count:
        u = User(username=fake.user_name(),
                 nickname=fake.name(),
                 pwd='password',
                 school='scau',
                 face="/static/photo/8.jpeg")
        db.session.add(u)
        try:
            db.session.commit()
            print("user成功添加")
            print(i)
            i += 1
        except:
            print("error users")
            db.session.rollback()
    print("用户成功!!!!")


def blogs(count=3000):
    fake = Faker('zh_CN')
    i = 1
    while i <= count:
        k = i % 4
        if k == 0:
            k = 4
        s = random.randint(100000,500000000)
        b = Blog(title=

                 fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                 content=fake.text(),
                 user_id=k,
                 num_of_view=s,
                 )

        db.session.add(b)
        try:
            db.session.commit()
            print("博客成功添加")
            print(i)
            i += 1
        except:
            print("Error blog")
            db.session.rollback()
    print("博客成功！！！！")


def compet(count=20):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        c = Competition(title=

                        fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                        content=fake.text() + "<img src=\"http://188888888.xyz:5000/static/photo/8.jpeg\"/>　内容内容内容　",
                        author=fake.name(),
                        num_of_view=fake.ean(length=8)

                        )

        db.session.add(c)
        try:
            db.session.commit()
            print("竞赛成添加")
            print(i)
            i += 1
        except:
            print("error compete")
            db.session.rollback()
    print("竞赛成功！！！")


def acti(count=20):
    fake = Faker('zh_CN')
    i = 0
    while i < count:
        c = Activity(title=

                     fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                     content=fake.text() + "<img src=\"http://188888888.xyz:5000/static/photo/8.jpeg\"/>　内容内容内容　",
                     author=fake.name(),
                     num_of_view=fake.ean8()
                     )

        db.session.add(c)
        try:
            db.session.commit()
            print("活动成功添加")
            print(i)
            i += 1
        except:
            print("活动 error")
            db.session.rollback()
    print("活动成功！！！！")


def actcomments():
    fake = Faker('zh_CN')
    for i in range(1, 6):
        for j in range(1, 6):
            comment = Reply(sender_id=i, content=fake.text(), type=1, activity_id=j)
            db.session.add(comment)
            try:
                db.session.commit()
                print("actcomments")
                print(i)
                print(j)
            except:
                print("actcomments error")
                db.session.rollback()
    print("活动评论成功！！！！")


def blogcomments():
    fake = Faker('zh_CN')
    for i in range(1, 6):
        for j in range(1, 6):
            comment = Reply(sender_id=i, content=fake.text(), type=1, blog_id=j)
            db.session.add(comment)
            try:
                db.session.commit()
                print("正在添加blogcomments")
                print(i)
                print(j)
            except:
                print("blogcomments error")
                db.session.rollback()
    print("博客评论成功！！！！")


# blogs()
# actcomments()
# blogcomments()