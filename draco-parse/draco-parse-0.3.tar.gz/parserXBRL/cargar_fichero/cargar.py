import urllib.request


def get_file(arg):
    try:
        return open(arg, "r", encoding = "ISO-8859-1")
    except IOError:
        print("Error cargando el fichero")

def get_fileByUrl(urlFile):
    try:
        response = urllib.request.urlopen(urlFile)
        data = response.read()      # a `bytes` object
        text = data.decode('ISO-8859-1')
        return  text

    except IOError as error:
        print(error)
