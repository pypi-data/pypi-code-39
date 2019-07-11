def say_hello(name=None):
	if name is None:
		return "Hello, World!"
	else:
		return f"Hello, {name}!"

if __name__ == "__main__":
	say_hello()