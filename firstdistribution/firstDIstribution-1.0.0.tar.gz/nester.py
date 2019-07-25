
print('this is nester')


def print_lol(li):
    for l in li:
        if isinstance(l, list):
            print_lol(l)
        else:
            print(l)
    
