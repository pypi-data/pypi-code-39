'''This is the "nesterManoj.py" module. and it provides one function called
print_lol() which prints lists that may of may include nested lists'''

def print_lol(the_list,no_of_tabs):
    '''This function takes a positional argument called "the_list", which is
      Python list(of, possibly nested lists).Each data item in the provided list
      is (recursively) printed to the screen of its own line'.Second arguments giving
      number of tabs required'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,no_of_tabs+1)
        else:
            for  tab in range(no_of_tabs):
                print("\t",end='')
            print(each_item)
