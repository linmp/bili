# (♠ ♥ ♦ ♣ )
import random

"""
     黑桃 ♠ 按照从小到大依次为：1-13

　　　红心 ♥ 按照从小到大依次为：14-26

　　　梅花 ♣ 按照从小到大依次为：27-39

　　　方块 ♦ 按照从小到大依次为：40-52

     小王 XW 53

     大王 DW 54

"""


def init_cards():
    card_list = []
    for i in range(0, 54):
        card_list.append(i + 1)
    return card_list


def swap(array, a, b):
    temp = array[a]
    array[a] = array[b]
    array[b] = temp


def make_card_random(array):
    for i in range(100):
        a = random.randint(0, 53)
        b = random.randint(0, 53)
        swap(array, a, b)


def get_back_card(array):
    index_a = random.randint(36, 53)
    index_b = random.randint(18, 35)
    index_c = random.randint(0, 17)

    get_a = array.pop(index_a)
    get_b = array.pop(index_b)
    get_c = array.pop(index_c)

    return get_a, get_b, get_c


def get_cards(array):
    return array[0:17], array[17:34], array[34:51]


def to_card(number):
    if (number % 13) == 1:
        number = "A"
    elif (number % 13) == 11:
        number = "J"
    elif (number % 13) == 12:
        number = "Q"
    elif (number % 13) == 0:
        number = "K"
    else:
        number = number % 13
    return str(number)


def show_card(array):
    for i in array:
        if i <= 13:
            print("♠" + to_card(i), end=' ')
        elif i > 13 and i <= 26:
            print("♥" + to_card(i), end=' ')
        elif i > 26 and i <= 39:
            print("♣" + to_card(i), end=' ')
        elif i > 39 and i <= 52:
            print("♦" + to_card(i), end=' ')
        elif i == 53:
            print("小王", end=' ')
        elif i == 54:
            print("大王", end=' ')
        else:
            print("出错了")


def play_game():
    cards = init_cards()
    make_card_random(cards)
    backs = get_back_card(cards)
    a, b, c = get_cards(cards)
    for back in backs:
        a.append(back)

    a.sort()
    b.sort()
    c.sort()

    print("底牌是: ")
    show_card(backs)
    print("\n地主: ")
    show_card(a)
    print("\n农民1: ")
    show_card(b)
    print("\n农民2: ")
    show_card(c)


if __name__ == '__main__':
    play_game()
