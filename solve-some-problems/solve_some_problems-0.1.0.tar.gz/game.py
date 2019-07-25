"""游戏"""


def gobang():
    """该函数用于开始五子棋游戏"""
    from random import randint

    # 利用循环让用户输入是否进行五子棋游戏。如果输入y，则进入程序；如果输入n，则退出；如果输入其他字
    # 符，则让用户重新输入是否进行五子棋游戏
    while True:
        # 让用户输入是否进行五子棋游戏
        s = input('即将进行五子棋游戏，同意则输入y，不同意则输入n：')
        # 如果输入y，则进入程序
        if s == 'y':
            """
            第一步：创建棋盘
                让用户输入棋盘的大小，再根据棋盘的大小创建棋盘。
            """
            # 让用户输入棋盘的大小
            size = int(input('请输入棋盘的大小：'))
            # 创建一个列表充当棋盘
            checkerboard = []
            # 使用循环给列表添加元素
            for i1 in range(size, 0, -1):   # i1代表棋盘每一行的序号，第一行的序号为size的值
                # 创建一个列表给checkerboard添加元素，checkerboard的每个子列表都代表一行，它们的第一
                # 个元素都是这一行的序号
                checkerboard1 = [i1]
                # 使用循环给checkerboard1添加size个'╋'
                for _ in range(size):
                    checkerboard1.append('╋')
                # 将checkerboard1添加到checkerboard里
                checkerboard.append(checkerboard1)
            # 再给checkerboard添加一个列表（[1, 2, ..., size]）作为每一列的序号
            checkerboard.append(list(range(1, size + 1)))
            """
                执行以上代码，如果给出的棋盘的大小为5，则创建的二位列表checkerboard为：
            [[5, '╋', '╋', '╋', '╋', '╋'],
             [4, '╋', '╋', '╋', '╋', '╋'],
             [3, '╋', '╋', '╋', '╋', '╋'],
             [2, '╋', '╋', '╋', '╋', '╋'],
             [1, '╋', '╋', '╋', '╋', '╋'],
             [1, 2, 3, 4, 5]]
                在这个列表中，除了前五个子列表中的第一个元素是每一行的序号，以及第六个子列表是每
            一列的序号以外，其他元素都是'╋'。

                接下来开始完善棋盘。
            """
            # 将checkerboard中的第一个子列表的第二个元素（即除序号外，棋盘的左上角）改为'┏'
            # （原'╋'）
            checkerboard[0][1] = '┏'
            # 将checkerboard中的第一个子列表的最后一个元素（即除序号外，棋盘的右上角）改为'┓'
            # （原'╋'）
            checkerboard[0][-1] = '┓'
            # 将checkerboard中的倒数第二个子列表的第二个元素（即除序号外，棋盘的左下角）改为'┗'
            # （原'╋'）
            checkerboard[-2][1] = '┗'
            # 将checkerboard中的倒数第二个子列表的最后一个元素（即除序号外，棋盘的右下角）改为'┛'
            # （原'╋'）
            checkerboard[-2][-1] = '┛'
            """
                执行以上代码，如果给出的棋盘的大小为5，则创建的二位列表checkerboard为：
            [[5, '┏', '╋', '╋', '╋', '┓'],
             [4, '╋', '╋', '╋', '╋', '╋'],
             [3, '╋', '╋', '╋', '╋', '╋'],
             [2, '╋', '╋', '╋', '╋', '╋'],
             [1, '┗', '╋', '╋', '╋', '┛'],
             [1, 2, 3, 4, 5]]

                继续完善棋盘。
            """
            # 使用循环将除序号外棋盘的第一行中间的元素改为'┳'（原'╋'），再将除序号外棋盘的最后一行
            # 中间的元素改为'┻'（原'╋'）
            for i2 in range(2, size):   # i2代表第一行和最后一行中间的元素
                # 将除序号外棋盘的第一行中间的元素改为'┳'（原'╋'）
                checkerboard[0][i2] = '┳'
                # 将除序号外棋盘的最后一行中间的元素改为'┻'（原'╋'）
                checkerboard[-2][i2] = '┻'
            # 使用循环将除序号外棋盘的第一列中间的元素改为'┣'（原'╋'），再将除序号外棋盘的最后一列
            # 中间的元素改为'┻'（原'┫'）
            for i3 in range(1, size - 1):
                # 将除序号外棋盘的第一列中间的元素改为'┣'（原'╋'）
                checkerboard[i3][1] = '┣'
                # 将除序号外棋盘的最后一列中间的元素改为'┻'（原'┫'）
                checkerboard[i3][-1] = '┫'
            """
                执行以上代码，如果给出的棋盘的大小为5，则创建的二位列表checkerboard为：
            [[5, '┏', '┳', '┳', '┳', '┓'],
             [4, '┣', '╋', '╋', '╋', '┫'],
             [3, '┣', '╋', '╋', '╋', '┫'],
             [2, '┣', '╋', '╋', '╋', '┫'],
             [1, '┗', '┻', '┻', '┻', '┛'],
             [1, 2, 3, 4, 5]]

            第二步：打印棋盘
                定义一个函数用于打印棋盘。
            """

            def print_checkerboard():
                """用于打印棋盘"""
                # 使用循环打印每一行的元素
                for j1 in checkerboard:     # j1代表每一行的元素
                    # 使用索引判断j1是不是checkerboard的第size个元素（即储存每一列的序号的列表）
                    if checkerboard.index(j1) == size:
                        # 在打印前先打印一个空格，并且不换行
                        print(' ', end='')
                        # 再遍历j1，提取出每个序号
                        for j2 in j1:   # j2表示序号
                            # 如果j2是一位数，则在打印前先打印一个空格；如果j2是两位数，则不打印空
                            # 格，直接打印序号。每打印一个序号之后都不换行
                            print('%2d' % j2, end='')
                            if j2 == 9:
                                print(' ', end='')
                    else:
                        # 遍历j1，提取出每个元素
                        for j2 in j1:   # j2表示元素
                            # 如果j2是j1的第一个元素（即每一行的序号）
                            if j1.index(j2) == 0:
                                # 如果j2是一位数，则再打印前先打印一个空格；如果j2是两位数，则不打
                                # 印空格，直接打印序号。每打印一个序号之后都不换行
                                print('%2d' % j2, end='')
                            else:
                                # 直接打印j2，并且不换行
                                print(j2, end='')
                    # 每打印一行之后换一行，准备打印下一行
                    print()

            """
                执行以上代码，如果给出的棋盘的大小为5，则调用函数print_checkerboard()打印出来
            为：
             5┏┳┳┳┓
             4┣╋╋╋┫
             3┣╋╋╋┫
             2┣╋╋╋┫
             1┗┻┻┻┛
              1 2 3 4 5

            第三步：下棋
                让用户和电脑下棋。
            """
            print_checkerboard()
            while True:
                i = input('请输入您下棋的坐标，应以x,y（x代表列数，y代表行数）的形式输入：\n')
                if not i:
                    break
                while True:
                    x = int(tuple(i.split(sep=','))[0])
                    y = int(tuple(i.split(sep=','))[1])
                    if x > size or y > size or x <= 0 or y <= 0 or\
                            checkerboard[size-y][x] == '●' or checkerboard[size-y][x] == '○':
                        print('该位置不能下棋！')
                        print_checkerboard()
                        i = input('请重新输入您下棋的坐标，应以x,y（x代表列数，y代表行数）的形式\
输入：\n')
                    else:
                        checkerboard[size-y][x] = '●'
                        break
                while True:
                    x = randint(1, size)
                    y = randint(1, size)
                    if not (checkerboard[size-y][x] == '●' or checkerboard[size-y][x] == '○'):
                        checkerboard[size - y][x] = '○'
                        print_checkerboard()
                        print('电脑下在%d,%d' % (x, y))
                        break
            break
        # 如果输入n，则退出
        elif s == 'n':
            break
