count = 0
a = []
for i in range(0, 10):
    a.append(" ")
print("井字棋挑战开始")
print("|----|----|----|")
print("|    |    |    |")
print("|----|----|----|")
print("|    |    |    |")
print("|----|----|----|")
print("|    |    |    |")
print("|----|----|----|")


def is_win(a):
    if (a[1] == a[2] == a[3] != " ") or (a[4] == a[5] == a[6] != " ") or (a[7] == a[8] == a[9] != " ") \
            or (a[1] == a[4] == a[7] != " ") or (a[2] == a[5] == a[8] != " ") or (a[3] == a[6] == a[9] != " ") or (
            a[1] == a[5] == a[9] != " ") or (
            a[3] == a[5] == a[7] != " "):
        return True
    for i in range(1, 10):
        if a[i] == " ":
            return False
    return True


while True:

    count += 1
    flag = "X" if count % 2 == 1 else "O"
    number = int(input("\n输入位置坐标: "))
    a[number] = flag

    print("---------------------------")
    print("|----|----|----|")
    print("|  %s |  %s | %s  |" % (a[7], a[8], a[9]))
    print("|----|----|----|")
    print("|  %s |  %s | %s  |" % (a[4], a[5], a[6]))
    print("|----|----|----|")
    print("|  %s |  %s | %s  |" % (a[1], a[2], a[3]))
    print("|----|----|----|")

    if is_win(a):
        print("---------------------------")
        print("\n\t\t游戏结束\n")
        print("---------------------------")
        break