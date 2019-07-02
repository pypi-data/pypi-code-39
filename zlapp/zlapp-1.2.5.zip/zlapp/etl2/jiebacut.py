import jieba 


class zljieba:
    def __init__(self):
        jieba.initialize()

    def cut(slef,txt):
        arr=jieba.lcut(txt)
        s=' '.join(arr)
        return s 

#a=zljieba()