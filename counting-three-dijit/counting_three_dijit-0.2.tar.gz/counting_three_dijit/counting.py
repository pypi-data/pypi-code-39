import random

a = random.randint(1,10)
b = random.randint(10, 100)
c = random.randint(100, 1000)
count_list = []
def count_number():
    global a, b, c
    counting = a * b + c
    count_list.appand(counting)
    return None
if __name__ == '__main__':
    count_number()
