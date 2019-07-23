def printer(y,tab_no=0):
	for x in y:
		if isinstance(x,list):
			printer(x,tab_no+1)
		else:
			for no in range(tab_no):
				print("\t",end='')
			print(x)
