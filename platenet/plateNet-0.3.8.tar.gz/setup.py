from distutils.core import setup

setup(
    name='plateNet',  # How you named your package folder (MyLib)
    packages=['plateNet'],  # Chose the same as "name"
    version='0.3.8',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here:
    description='plate detect with Yolov3',  # Give a short description about your library
    author='Hacı',  # Type in your name
    author_email='karakus.haciveli@gmail.com',  # Type in your E-Mail
    install_requires=[  # I get to this in a second
        'opencv-python',
        'imutils',
        'numpy',
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
