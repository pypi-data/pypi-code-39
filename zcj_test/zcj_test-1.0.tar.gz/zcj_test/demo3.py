# -*- coding: utf-8 -*-
# python_test
# @Time    : 2019/7/14 0014 14:03
# @Author  : 曾经
"""
棋盘18*18，可配
"""
import turtle
t = turtle.Pen()
t.hideturtle()
cycle_index = 18  # 格数
width = 20  # 宽度
lenth = 20  # 长度
t.speed(0)
for i in range(cycle_index+1):
    t.penup()  # 抬笔
    t.goto(0, -i*lenth)
    t.pendown()  # 放下笔
    t.forward(cycle_index*width)
    t.penup()
    t.goto(i*width, 0)
    t.pendown()
    t.right(90)
    t.forward(cycle_index*lenth)
    t.left(90)
