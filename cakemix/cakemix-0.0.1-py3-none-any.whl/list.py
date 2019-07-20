


def findUniqueList(param1):
    ''' it returns the unique subset of the list
	# Usage: findUniqueList([1,3,3,4,5,5,6])
	'''
    used=set()
    
    
    if len(param1) < 2:
        print("this is not a list")
    else:
        unique_list = [x for x in param1 if x not in used and (used.add(x) or True)]
        return unique_list