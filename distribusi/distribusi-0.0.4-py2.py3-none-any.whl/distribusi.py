import base64
import os
import subprocess
from io import BytesIO

import magic
from PIL import Image

from distribusi.page_template import html_footer, html_head

CODE_TYPES = ['x-c', 'html']

FILE_TYPES = {
    'image': '<figure><img class="image" src="{}">{}</figure>',
    'pdf': (
        '<object data="{}" class="pdf" type="application/pdf">'
        '<embed src="{}" type="application/pdf" /></object>'
    ),
    'text': '<a href="{}" class="text">{}</a>',
    'video': ('<video class="video" controls>' '<source src="{}"></source></video>'),
    'audio': ('<audio controls class="audio">' '<source src="{}"></source></audio>'),
}


MIME_TYPE = magic.Magic(mime=True)


def caption(image):
    process = subprocess.Popen(['exiftool', '-Comment', image], stdout=subprocess.PIPE)
    out, err = process.communicate()
    try:
        caption = out.decode("utf-8").split(": ", 1)[1]
    except:
        caption = ''
    return caption


def thumbnail(image, name, args):
    size = (450, 450)
    im = Image.open(image)
    im.thumbnail(size)
    output = BytesIO()
    im.save(output, format='JPEG')
    im_data = output.getvalue()
    data_url = base64.b64encode(im_data).decode()
    cap = caption(image)
    if cap and args.captions:
        cap = "<figcaption>{}</figcaption>".format(cap)
    else:
        cap = ''
    return (
        "<figure><a href='{}'><img class='thumbnail' src='data:image/jpg;base64,{}'></a>{}</figure>"
    ).format(name, data_url, cap)


def div(args, mime, tag, *values):
    id_name = values[0].split('.')[0].replace(' ', '_')
    if not args.no_filenames:
        filename = '<br><span class="filename">{}</span>'
    else:
        filename = ''
    if 'image' in mime:
        html = '<div id="{}">{}' + filename + '</div>'
    elif 'pdf' in mime:
        html = '<div id="{}">{}' + filename + '</div>'
    else:
        html = '<div id="{}">{}</div>'

    return html.format(id_name, tag, values[0])


def distribusify(args, directory):  # noqa
    for root, dirs, files in os.walk(directory):
        html = []

        if args.verbose:
            print('Listing', root)

        for name in files:
            if args.verbose:
                print('Adding', name)
            if 'index.html' not in name:
                full_path = os.path.join(root, name)
                mime = MIME_TYPE.from_file(full_path)
                mime, format = mime.split('/')  # example: plain text

                if args.verbose:
                    print(mime, format)

                if mime in FILE_TYPES:
                    # expansion for different kind of textfiles
                    if mime == 'text':
                        if name.endswith('.html') or name.endswith('.txt'):
                            # what types of text files to expand
                            a = open(full_path).read()
                        elif format in CODE_TYPES:
                            # if the plain text is code,
                            # which types do we wrap in pre-tags?
                            a = "<pre>" + open(full_path).read() + "</pre>"
                        else:
                            a = FILE_TYPES[mime]

                    if mime == 'image' and args.thumbnail:
                        a = thumbnail(full_path, name, args)
                    else:
                        cap = caption(full_path)
                        if cap and args.captions:
                            cap = "<figcaption>{}</figcaption>".format(cap)
                        else:
                            cap = ''
                        a = FILE_TYPES[mime].format(full_path, cap)

                if format in FILE_TYPES:
                    a = FILE_TYPES[format]

                if mime not in FILE_TYPES and format not in FILE_TYPES:
                    # catch exceptions not defined in FILE_TYPES before
                    a = "<a href='{}'>{}</a>"
                    if args.verbose:
                        message = 'mime-type not in list, adding as href: \n'
                        print(message, mime, format, name)

                a = a.replace('{}', name)
                html.append(div(args, mime, a, name))

        if root != directory:
            html.append('<a href="../">../</a>')

        for name in dirs:
            a = "<a href='{}' class='dir'>{}/</a>".replace('{}', name)
            html.append(div(args, 'dir', a, 'folder'))

        with open(os.path.join(root, 'index.html'), 'w') as f:
            if not args.no_template:
                if args.style:
                    fs = open(args.style, "r")
                    style = fs.read()
                    styled_html_head = html_head % style
                else:
                    styled_html_head = html_head % ''
                f.write(styled_html_head)

            for line in html:
                f.write(line + '\n')

            if not args.no_template:
                f.write(html_footer)
