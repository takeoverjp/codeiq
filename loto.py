# coding: UTF-8

"""
[INPUT]
 - 5個の数字

[OUTPUT]
 - 全体の売り上げ金額
 - 主催者の取り分
 - 当たりの数字
 - 1等から3等までの当籤口数と当籤金額
 - あらかじめ選んだ数字の当籤状況
"""

import sys
import random

def is_first_prise(ticket,win_ticket):
    return len(ticket.intersection(win_ticket)) == 5

def is_second_prise(ticket,win_ticket):
    return len(ticket.intersection(win_ticket)) == 4

def is_third_prise(ticket,win_ticket):
    return len(ticket.intersection(win_ticket)) == 3

def create_rand_ticket():
    ret = set()
    while len(ret) < 5:
        num = random.randint(1,50)
        if num not in ret:
            ret.add(num)
    return ret


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 6):
        print 'Usage: "python %s num1 num2 num3 num4 num5' % argvs[0]
        quit()

    ticket_num = 0
    while ticket_num < 200000 or ticket_num > 300000:
        ticket_num = int(random.gauss(250000, 100000))
    total_sales = ticket_num * 500
    print ticket_num, total_sales

    my_ticket = set()
    for i, num in enumerate(argvs):
        if (i == 0):
            continue
        my_ticket.add(num)
    #print my_ticket

    win_ticket = create_rand_ticket()
    #print win_ticket

    first_count = 0
    second_count = 0
    third_count = 0
    first_prize = "N/A"
    second_prize = "N/A"
    third_prize = "N/A"
    for i in range(ticket_num-1):
        ticket = create_rand_ticket()
        if is_first_prise(ticket, win_ticket):
            first_count += 1
        if is_second_prise(ticket, win_ticket):
            second_count += 1
        if is_third_prise(ticket, win_ticket):
            third_count += 1
    if is_first_prise(my_ticket, win_ticket):
        first_count += 1
    if is_second_prise(my_ticket, win_ticket):
        second_count += 1
    if is_third_prise(my_ticket, win_ticket):
        third_count += 1
    if first_count != 0:
        first_prize = int(total_sales*0.3/first_count)
    if second_count != 0:
        second_prize = int(total_sales*0.2/second_count)
    if third_count != 0:
        third_prize = int(total_sales*0.1/third_count)
    #print first_count, second_count, third_count

    print u"- 全体の売り上げ金額"
    print u"    ", total_sales, u"円"
    print u"- 主催者の取り分"
    print u"    ", int(total_sales*0.4), u"円"
    print u"- 当たりの数字"
    print u"    ", list(win_ticket)
    print u"- 1等から3等までの当籤口数と当籤金額"
    print u"    1等:", first_count,  "口, ", first_prize,  "円"
    print u"    2等:", second_count, "口, ", second_prize, "円"
    print u"    3等:", third_count,  "口, ", third_prize,  "円"
    print u"- あらかじめ選んだ数字の当籤状況"
    if is_first_prise(my_ticket, win_ticket):
        print u"    1等!!!"
    elif is_second_prise(my_ticket, win_ticket):
        print u"    2等!!"
    elif is_third_prise(my_ticket, win_ticket):
        print u"    3等!"
    else:
        print u"    はずれ。。。"
