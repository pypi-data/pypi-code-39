def printer(y):
	for x in y:
		if isinstance(x,list):
			printer(x)
		else:
			print(x)
