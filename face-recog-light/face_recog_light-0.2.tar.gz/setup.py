import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='face_recog_light',
     version='0.2',
     scripts=['face_recog_light/face_recognition.py'],
     author="Dewald Abrie",
     author_email="dewaldabrie@gmail.com",
     description="light-weight face recognition",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/dewaldabrie/face_recognition",
     packages=['face_recog_light'],
     package_dir={'face_recog_light': 'face_recog_light'},
     package_data={'face_recog_light': ['models/facenet.tflite']},
     include_package_data=True,
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )