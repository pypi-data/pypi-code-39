import webbrowser

files = []
def createindex(bc='white'):
    f = open('index.html', 'w+')
    files.append('index')
    f.write("<body style='background-color: %s;'>" % bc)
    f.close()
    
def title(file, text):
    f=open(file+'.html', 'a+')
    if file=='all':
        for item in files:
            f=open(item+'.html', 'a+')
            f.write('<title>%s</title>'% text)
            f.close()
    else:
        f=open(file+'.html', 'a+')
        f.write('<title>%s</title>'% text)
        f.close()
def createpage(file, bc='white'):
    f = open(file+'.html', 'w+')
    files.append(file)
    f.write("<body style='background-color: %s ;'" % bc)
    f.close()

def header(file, text, centered=False):
        f=open(file+'.html', 'a+')
        if centered==True:
            f.write('<h1 style="text-align: center;">'+text+'</h1>')
        elif centered==False:
            f.write('<h1>'+text+'</h1>')
        f.close()

def text(file, text, centered=False):
        f=open(file+'.html', 'a+')
        if centered==False:
            f.write('<p>'+text+'</p>')
        elif centered==True:
            f.write('<p  style="text-align: center;">'+text+'</p>')
        f.close()

def link(file, page, text, style='text', centered=False):
    f=open(file+'.html', 'a+')
    if style=='text':
        if centered==True:
            f.write('<a href='+page+'.html>'+text+'</h1>')
        else:
            f.write('<a href='+page+'.html>'+text+'</h1>')
    elif style=='button':
        if centered==True:
            f.write("""
    <form>
    <input style='text-align: center;' type="button" value="""+text+""" onclick="window.location.href='"""+page+"""'" />
    </form>
            """)
        else:
            f.write("""
<form>
<input type="button" value="""+text+""" onclick="window.location.href='"""+page+"""'" />
</form>
        """)
    f.close()

def search(file, centered=False):
    f=open(file+'.html', 'a+')
    if centered==True:
        f.write("""
    <div id='a' style='text-align:center;'>
    <input type='text' id='link_id'>
    <input type='button' id='link' value='Search' onClick='javascript:goTo()'>
    </div>
    <script>
    function goTo()
    {
        input = document.getElementById('link_id').value;
        location.href = 'https://www.google.com/search?safe=active&source=hp&ei=qBgiXYDCFtDVtAay2ovIAg&q='+input+'&oq='+input+'p&gs_l=psy-ab.3..0l10.4800.5462..5922...0.0..1.236.818.5j2j1......0....1..gws-wiz.....0..0i131j0i3.wh3C02wdyCM&safe=active'
    }
    </script>
        """)
    else:
        f.write("""
<input type='text' id='link_id'>
<input type='button' id='link' value='Search' onClick='javascript:goTo()'>
<script>
function goTo()
{
    input = document.getElementById('link_id').value;
    location.href = 'https://www.google.com/search?safe=active&source=hp&ei=qBgiXYDCFtDVtAay2ovIAg&q='+input+'&oq='+input+'p&gs_l=psy-ab.3..0l10.4800.5462..5922...0.0..1.236.818.5j2j1......0....1..gws-wiz.....0..0i131j0i3.wh3C02wdyCM&safe=active'
}
</script>
    """)
    f.close()

def start(file):
    webbrowser.open_new(file+'.html')
