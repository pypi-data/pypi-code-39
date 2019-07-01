import os
import sys
import requests, zipfile, io
imgExtensions = 'png', 'jpg'
gifExtensions = 'gif'

zip_file_url = 'https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.2-windows-x64.zip'
r = requests.get(zip_file_url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()

cmdPath = os.path.join(os.getcwd(),  'libwebp-1.0.2-windows-x64','bin' )
os.environ['PATH'] += os.pathsep + cmdPath

for entry in os.scandir():
    print(entry.name)
    if entry.name.lower().endswith(imgExtensions):
      os.system('cwebp {name} -o {finalname}.webp'.format(name=entry.name, finalname=entry.name[0:-4], cmdPath=cmdPath))
    elif entry.name.lower().endswith(gifExtensions):
      os.system('gif2webp {name} -o {finalname}.webp'.format(name=entry.name, finalname=entry.name[0:-4], cmdPath=cmdPath))

"""
for entry in os.scandir():
  if entry.name.lower().endswith('.webp'):
    print(entry.name[0:-3] )
    #os.rename(entry.name, '{begin}{end}'.format(begin=entry.name[0:],end=entry.name[-1:-4]  ))
    #s = s[ beginning : beginning + LENGTH]
"""
