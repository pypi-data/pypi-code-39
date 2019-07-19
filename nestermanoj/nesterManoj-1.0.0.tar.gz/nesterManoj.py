'''This is the "nesterManoj.py" module. and it provides one function called
print_lol() which prints lists that may of may include nested lists'''

def print_lol(the_list):
    '''This function takes a positional argument called "the_list", which is
      Python list(of, possibly nested lists).Each data item in the provided list
      is (recursively) printed to the screen of its own line'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
