import webbrowser

def createindex():
    f = open('index.html', 'w+')
    f.close()

def createpage(name):
    f = open(name+'.html', 'w+')
    f.close()

def header(file, text):
        f=open(file+'.html', 'a+')
        f.write('<h1>'+text+'</h1>')
        f.close()

def text(file, text):
        f=open(file+'.html', 'a+')
        f.write('<p>'+text+'</p>')
        f.close()

def link(file, page, text):
    f=open(file+'.html', 'a+')
    f.write('<a href='+page+'.html>'+text+'</h1>')
    f.close()

def start(file):
    webbrowser.open_new(file+'.html')
