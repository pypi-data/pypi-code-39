import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	 name='rubypass',
	 version='0.1',
	 author="okawo",
	 author_email="okawo.198@gmail.com",
	 description="A package to extract video urls from 2 russian websites",
	 long_description=long_description,
	 long_description_content_type="text/markdown",
	 url="https://github.com/okawo80085/russianWebBypass",
	 packages=setuptools.find_packages(),
	 classifiers=[
		 "Programming Language :: Python :: 3",
		 "License :: OSI Approved :: MIT License",
		 "Operating System :: OS Independent",
	 ],
	 py_modules=['rubypass'],
)