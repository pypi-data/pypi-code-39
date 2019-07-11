"""
This is nester.py module and i provides one function called print_lol()
which prints nested files may or may not include nested lists.
"""
def print_lol(the_list,indent=False,lev=0):
    """ This function takes one argument  calles "the_list", which is any python list.
    Each data in tge item will be printed on the screen=
    """
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,lev+1)       
        else:
            if indent:
                for tab_stop in range(lev):
                    print("\t",end='')
            print(each_item)

