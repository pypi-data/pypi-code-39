def printer(y,indent=False,tab_no=0):
	for x in y:
		if isinstance(x,list):
			printer(x,indent,tab_no+1)
		else:
			if indent:
				for no in range(tab_no):
					print("\t",end='')
			print(x)
