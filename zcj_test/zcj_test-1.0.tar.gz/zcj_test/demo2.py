# -*- coding: utf-8 -*-
# python_test
# @Time    : 2019/7/6 0006 16:02
# @Author  : 曾经


def ligature():
    """
    海龟模块，连接任意两点
    :return:
    """
    try:
        import turtle
        t = turtle.Pen()
        t.hideturtle()
        t.color('red')
        point_list = [(100, 0), (50, 0), (70, 70), (20, 30), (99, 62), (51, 85)]
        for i in range(len(point_list)):
            if i == 0:  # 从起点到第一个点的时候抬笔
                t.penup()
            for j in point_list[i+1:]:  # 每一个点去相连他后面的所有点，他前面的点已经相连过
                t.goto(point_list[i])
                t.pendown()
                t.goto(j)
                t.penup()
        turtle.done()
    except Exception as e:
        print(e)  # 打印出报错信息


ligature()

