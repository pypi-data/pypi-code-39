'''This is the "nesterManoj.py" module. and it provides one function called print_lol() which prints lists that may of may include nested lists'''

def print_lol(the_list, indent=False, no_of_tabs=0):
    '''This function takes three positional argument called "the_list,indent and no_of_tabs", the_list is Python list(of, possibly nested lists).Each data item in the
     provided list is (recursively) printed to the screen of its own line'.Second arguments should be put True or 1 , in case indentation required.Third argument
     is for the number of tab stops required'''
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item, indent, no_of_tabs+1)
        else:
            if indent:
                for  tab in range(no_of_tabs):
                    print("\t",end='')
            print(each_item)
