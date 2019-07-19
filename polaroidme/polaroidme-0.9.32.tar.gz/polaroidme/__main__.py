#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polaroidme - converts an image into vintage polaroid style

Usage:
  polaroidme <source-image> [--output=<filename>]
  polaroidme <source-image> [-o=<filename>] [--title=<str>] [--title-meta] [--font=<f>]
  polaroidme <source-image> [-o=<fn>] [--size-inner=<n>] [--max-size=<w>] [--template=<str>] [--config=<str>] [--title=<str>][--title-meta]
  polaroidme <source-image> [-o=<fn>] [--template=<str>] [--config=<str>] [--title=<str>][--title-meta] [--font=<f>] [--size-inner=<n>] [--max-size=<w>]
  polaroidme <source-image> [-o=<fn>] [--size-inner=<n>] [--alignment=<str>] [--title=<str>][--title-meta] [-f=<f>] [--template=<str>] [-c=<str>] [-m=<w>]
  polaroidme <source-image> [--nocrop|--crop] [--alignment=<str>] [--title=<str>] [--title-meta] [-f=<str>] [-s=<n>] [-o=<filename>] [--template=<str>] [--config=<str>] [--max-size=<w>]
  polaroidme <source-image> [--clockwise|--anticlock] [--nocrop|--crop] [--title=<str>] [--title-meta] [-f=<f>] [-s=<n>] [-o=<fn>] [--alignment=<str>] [--template=<str>] [-config=<str>] [-m=<w>] [--title-meta]

Where:
  source-image    Name of the image file to convert.
  font            Specify (ttf-)font to use (full path!)

Options:
  --alignment=<str> Used for cropping - specifies the portion of the image
                    to include in the final output.
                    One of 'top', 'left', 'bottom', 'right' or 'center'.
                    'top' and 'left' are synonomous as are 'bottom' and
                    'right'. (default="center").
                    Not of any use if --nocrop option is set.
  --anticlockwise   Rotate the image anti-clockwise before processing
  -c,--config=<py>  a config is only necessary if --template is used (see docs)
  --clockwise       Rotate the image clockwise before processing
  --crop            the images will be cropped to fit. see --alignment
  -f, --font=<f>    Specify (ttf-)font to use (full path!)
  -s,--size-inner=<n> Size of the picture-part of the polaroid in pixels (default=800)
  --title=<str>     Defines an optional caption to be displayed at the
                    bottom of the image. (default=None)
  --title-meta      Adds EXIF-data (date of capturing) to the title.
  -m,--max-size=<w> Sets maximum size (width) of the created polaroid.
                    (size-inner + frame <= max-size)
  --nocrop          Rescale the image to fit fullframe in the final output
                    (default="--crop"). btw. alignment is ignored if option is set.
  -o, --output=<s>  Defines the name of the outputfile. If omitted a filename
                    based on the original will be used - example:
                    'test.polaroid.png' will be used as filename if input-file is 'test.png'
  --template=<t>    Specify a template to use. A template can be a high-res
                    scan of a real Polaroid or something of its shape.
                    By using a template the visual output quality gains on
                    expression & authenticity.

  -h, --help        Print this.
      --version     Print version.

The `latest version is available on github: https://github.com/s3h10r/polaroidme>
"""
import datetime as dt
import json
import os
import site
import sys
import logging
from docopt import docopt
import exifread
from PIL import Image, ImageDraw, ImageFont, ExifTags

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

# Image size constraints
IMAGE_SIZE   = 800                      # the thumbnail size (= the inner picture)
IMAGE_TOP    = int(IMAGE_SIZE / 16)     # added space on top
IMAGE_BOTTOM = int(IMAGE_SIZE / 5.333)  # added space on bottom
IMAGE_LEFT   = int(IMAGE_SIZE / 16)     # ...
IMAGE_RIGHT  = int(IMAGE_SIZE / 16)     # ...
BORDER_SIZE  = 3
# Colors
COLOR_FRAME   = (237, 243, 214)
COLOR_BORDER  = (0, 0, 0)
COLOR_TEXT_TITLE = (58, 68, 163)
COLOR_TEXT_DESCR = COLOR_TEXT_TITLE
COLOR_BG_INNER = (0,0,0)                # usefull if --nocrop
# Font for the caption text
RESOURCE_FONT      = "fonts/default.ttf"
RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.9))
RESOURCE_CONFIG_FILE="polaroidme.conf"
PACKAGE_NAME = "polaroidme"

TEMPLATE_BOXES = {} # if --template is used we need a dict with templatename and box-definition for the image

__version__ = (0,9,32)


def get_exif(source):
    """
    """
    if isinstance(source, Image.Image):
        if hasattr(source, filename):
            source = source.filename
        else:
            raise Exception("Sorry, source is an Image-instance and i could not determine the filename. Please geve me a FQFN instead.")
    elif not isinstance(source, str):
        raise Exception("Ouch. Sorry, source must be a valid filename.")
    with open(source, 'rb') as f:
        exif_data = exifread.process_file(f, details=True)
    for tag in exif_data:
        log.debug("exif_data has key: %s" % (tag))
        if tag in ('Image DateTime', 'EXIF DateTimeOriginal'):
            log.debug("EXIF data of %s for key %s is %s" % (source, tag, exif_data[tag]))
    return exif_data

# --- argparsing helpers etc
def get_resource_file(basefile):
    """
    gets the fully qualified name of a resource file
    """
    fqn = os.path.join(os.path.dirname(os.path.realpath(__file__)), basefile)
    if not os.path.isfile(fqn):
        # when installed via pip the package_data (see MANIFEST.in, setup.py)
        # should be located somewhere in site-packages path of the (virtual-)env
        for dir in site.getsitepackages():
            fqn = dir + "/" + PACKAGE_NAME + "/" + basefile
            if os.path.isfile(fqn):
                return fqn
                break
    return fqn

def show_error(msg):
    """
    Show an error message and exit
    """
    log.critical("Error: %s" % msg)
    sys.exit(1)
# ---

def setup_globals(size, configfile=None, template = None, show = True):
    global IMAGE_SIZE
    global IMAGE_TOP
    global IMAGE_BOTTOM
    global IMAGE_LEFT
    global IMAGE_RIGHT
    global BORDER_SIZE
    global RESOURCE_FONT_SIZE
    global TEMPLATE_BOXES

    if configfile:
        if not (os.path.isfile(configfile)):
            log.warning("configfile {} not found... please always give absolute paths to config-file to avoid confusions :D".format(configfile))
            sys.exit(1)
        # --- load config file (if any)
        with open(configfile) as f:
            log.info("reading config...")
            code = compile(f.read(), configfile, 'exec')
            global_vars ={}
            local_vars = {}
            exec(code,global_vars, local_vars)
            TEMPLATE_BOXES=local_vars['TEMPLATE_BOXES']
    else:
        if template:
            log.critical("to use --template you need to define a config-file")
            sys.exit(1)

    if not template:
        IMAGE_SIZE   = size
        IMAGE_TOP    = int(IMAGE_SIZE / 16)
        IMAGE_BOTTOM = int(IMAGE_SIZE / 5.333)
        IMAGE_LEFT   = int(IMAGE_SIZE / 16)
        IMAGE_RIGHT  = int(IMAGE_SIZE / 16)
        BORDER_SIZE  = 3
        RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.2))
    else:
        # calculate the values based on the properties of the template image
        # --- setup templates
        for k in TEMPLATE_BOXES:
            TEMPLATE_BOXES[k] = [int(round(f)) for f in TEMPLATE_BOXES[k]]
        # ---

        box = TEMPLATE_BOXES[os.path.basename(template)]
        w = box[2] - box[0]
        h = box[3] - box[1]
        if w != h:
            log.warning("boxdefinition for template {} is not a square. w,h {},{}".format(k,w,h))
            log.warning("auto-fixing => making it square...")
            if w > h: #AUTO_FIX
                box[3] += (w - h)
            else:
                box[2] += (h - w)
            TEMPLATE_BOXES[os.path.basename(template)] = [box[0], box[1], box[2], box[3]]
            box = TEMPLATE_BOXES[os.path.basename(template)]
            w = box[2] - box[0]
            h = box[3] - box[1]
            log.warning("boxdefinition for template {} auto-adjusted to: w,h {},{}".format(k,w,h))
            assert(w == h)
        size = w
        assert((size == w) and (size== h))
        IMAGE_SIZE = size
        # overwrite the above calculated  _TOP,_BOTTOM, ... values
        # by the one our template "dictates"
        try:
            tpl = Image.open(template)
        except:
            tpl = Image.open(get_resource_file(template))

        tpl_x, tpl_y = tpl.size
        tpl.close()
        IMAGE_TOP = box[1]
        IMAGE_BOTTOM = tpl_y - (IMAGE_TOP + IMAGE_SIZE)
        IMAGE_LEFT = box[0]
        IMAGE_RIGHT = tpl_x - (IMAGE_LEFT + w)
        BORDER_SIZE  = 3
        RESOURCE_FONT_SIZE = int(IMAGE_BOTTOM - (IMAGE_BOTTOM * 0.2))

    # --- show
    if show:
        SETTINGS = {
        'IMAGE_SIZE' : IMAGE_SIZE,
        'IMAGE_TOP' : IMAGE_TOP,
        'IMAGE_BOTTOM' : IMAGE_BOTTOM,
        'IMAGE_LEFT' : IMAGE_LEFT,
        'IMAGE_RIGHT' : IMAGE_RIGHT,
        'BORDER_SIZE' : BORDER_SIZE,
        'RESOURCE_FONT_SIZE' : RESOURCE_FONT_SIZE,
        'TEMPLATE_KEY' : template,
        'TEMPLATE_VALUE': None,# we fill this if template ist != None
        }
        if template:
            SETTINGS['TEMPLATE_KEY'] = os.path.basename(template),
            SETTINGS['TEMPLATE_VALUE'] = TEMPLATE_BOXES[os.path.basename(template)],
        print(json.dumps(SETTINGS,indent=4,sort_keys=True))


def make_polaroid(source, size, options, align, title, f_font = None, font_size = None, template = None, bg_color_inner=(255,255,255)):
    """
    Converts an image into polaroid-style. This is the main-function of the module
    and it is exposed. It can be imported and used by any Python-Script.

    returns
        PIL image instance
    """
    caption = title
    img_in = Image.open(source)
    img_in.load()
    img = rotate_image(img_in, options['rotate'])
    [w, h] = img.size
    # Determine ratio of image length to width to
    # determine oriantation (portrait, landscape or square)
    image_ratio = float(float(h)/float(w))
    log.debug("image_ratio: %f size_w: %i size_h: %i" % (image_ratio, w, h))
    if round(image_ratio, 1) >= 1.3: # is_portrait
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_portrait'))
    elif round(image_ratio, 1) == 1.0: # is_square
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_square'))
    elif round(image_ratio, 1) <= 0.8: # is_landscape
        log.info("source image ratio is %f (%s)" % (image_ratio, 'is_landscape'))
    if options['crop']:
        img = crop_image_to_square(img, align)
    else:
        img = scale_image_to_square(img, bg_color=bg_color_inner)
    img = scale_image(img, size)
    if template:
        log.warning("--template is experimental!")
        img = _paste_into_template(image=img, template=template)
        description = None
        img = add_text(img, caption, description, f_font = f_font, font_size = font_size)
    else:
        img = add_frame(img)
        description = None
        img = add_text(img, caption, description, f_font = f_font, font_size = font_size)
    return img


def _paste_into_template(image = None, template = './templates/fzm-Polaroid.Frame-01.jpg', box=None):
    """
    """
    if not box:
        box = TEMPLATE_BOXES[os.path.basename(template)]
    try:
        img_tpl = Image.open(template)
    except:
        img_tpl = Image.open(get_resource_file(template))

    w = int(box[2] - box[0])
    h = int(box[3] - box[1])
    log.debug("box-size the picture will be pasted into is (w,h) {} {}".format(w,h))
    region2copy = image.crop((0,0,image.size[0],image.size[1]))
    if region2copy.size[0] > w:
        # Downsample
        log.info("downsampling... (good)")
        region2copy = region2copy.resize((w,h),Image.ANTIALIAS)
    else:
        log.info("upscaling... (not so good ;)")
        region2copy = region2copy.resize((w,h), Image.BICUBIC)
    assert(region2copy.size == (w,h))
    #print(region2copy.size, (w,h))
    #print(region2copy.size, box)
    img_tpl.paste(region2copy,box)
    return img_tpl


def rotate_image(image, rotation):
    """
    rotates the image appropriately
    """
    if rotation == "clockwise":
        image = image.rotate(-90)
    elif rotation == "anticlockwise":
        image = image.rotate(90)
    return image

def crop_image_to_square(image, align):
    """
    crops the image into square-format

    returns cropped Image
    """
    # Do the cropping needed
    if image.size[0] > image.size[1]:
        if align in ("left", "top"):
            box = (0, 0, image.size[1], image.size[1])
        elif align in ("right", "bottom"):
            delta = image.size[0] - image.size[1]
            box = (delta, 0, image.size[0], image.size[1])
        elif align == "center":
            delta = (image.size[0] - image.size[1]) / 2
            box = (delta, 0, image.size[0] - delta, image.size[1])
        image = image.crop(box)
        image.load()
    elif image.size[1] > image.size[0]:
        if align in ("left", "top"):
            box = (0, 0, image.size[0], image.size[0])
        elif align in ("right", "bottom"):
            delta = image.size[1] - image.size[0]
            box = (0, delta, image.size[0], image.size[1])
        elif align == "center":
            delta = (image.size[1] - image.size[0]) / 2
            box = (0, delta, image.size[0], image.size[1] - delta)
        image = image.crop(box)
        image.load()
    # make sure we have a perfect square
    log.debug("cropped to size: %i %i" % (image.size[0], image.size[1]))
    if image.size[0] != image.size[1]:
        if image.size[0] > image.size[1]:
            box = (0, 0, image.size[1], image.size[1])
        else:
            box = (0, 0, image.size[0], image.size[0])
        image = image.crop(box)
        image.load()
        log.debug("re-cropped to size: %i %i" % (image.size[0], image.size[1]))
    return image

def scale_image_to_square(image, bg_color = (255,255,255)):
    img_w, img_h = image.size
    image_ratio = float(float(img_h)/float(img_w))
    add_border = 0
    if image_ratio < 1:
        add_border = image.size[0] * (( 1 + image_ratio ) / 64)
    else:
        add_border = image.size[1] * ((image_ratio - 1) / 64)
    add_border = int(add_border)
    background = None
    if image.size[0] > image.size[1]:
        background = Image.new('RGBA', (image.size[0] + add_border, image.size[0] + add_border), bg_color)
    elif image.size[1] > image.size[0]:
        background = Image.new('RGBA', (image.size[1] + add_border, image.size[1] + add_border), bg_color)
    else:
        return image # already square
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(image, offset)
    background.load()
    return background

def scale_image(image, size):
    """
    scales the image to size (up-/downsampling)

    returns scaled image
    """
    if image.size[0] != image.size[1]:
        raise Exception("ouch - no square image.")
    if image.size[0] > size:
        # Downsample
        image = image.resize((size, size), Image.ANTIALIAS)
    else:
        image = image.resize((size, size), Image.BICUBIC)
    log.debug("scaled to size: %i %i" % (image.size[0], image.size[1]))
    return image

def add_frame(image, border_size = 3, color_frame = COLOR_FRAME, color_border = COLOR_BORDER):
    """
    adds the frame around the image
    """
    frame = Image.new("RGB", (IMAGE_SIZE + IMAGE_LEFT + IMAGE_RIGHT, IMAGE_SIZE + IMAGE_TOP + IMAGE_BOTTOM), COLOR_BORDER)
    # Create outer and inner borders
    draw = ImageDraw.Draw(frame)
    draw.rectangle((BORDER_SIZE, BORDER_SIZE, frame.size[0] - BORDER_SIZE, frame.size[1] - BORDER_SIZE), fill = COLOR_FRAME)
    draw.rectangle((IMAGE_LEFT - BORDER_SIZE, IMAGE_TOP - BORDER_SIZE, IMAGE_LEFT + IMAGE_SIZE + BORDER_SIZE, IMAGE_TOP + IMAGE_SIZE + BORDER_SIZE), fill = COLOR_BORDER)
    # Add the source image
    frame.paste(image, (IMAGE_LEFT, IMAGE_TOP))
    return frame

def add_text(image, title = None, description = None, f_font = RESOURCE_FONT, font_size = RESOURCE_FONT_SIZE):
    """
    adds a title (string) to the image
    description is unused at the moment

    returns
        PIL Image instance
    """
    if (title is None) or (len(title)==0):
        return image
    size = font_size
    f_font = get_resource_file(f_font)
    try:
        font_title = ImageFont.truetype(f_font, font_size)
    except:
        show_error("Could not load resource '%s'." % f_font)
    width, height = font_title.getsize(title)
    while ((width > IMAGE_SIZE) or (height > IMAGE_BOTTOM)) and (size > 0):
        size = size - 2
        try:
            font_title = ImageFont.truetype(f_font, font_size)
        except:
            show_error("Could not load resource '%s'." % f_font)
        font_title = ImageFont.truetype(get_resource_file(f_font), size)
        width, height = font_title.getsize(title)
        log.debug("searching suiting font_size... trying {}".format(size))
    if (size <= 0):
        showError("Text is too large")
    draw = ImageDraw.Draw(image)
    pos_x = (IMAGE_SIZE + IMAGE_LEFT + IMAGE_RIGHT - width) / 2
    pos_y = IMAGE_SIZE + IMAGE_TOP + ((IMAGE_BOTTOM - height)) / 2
    log.info("title fontsize {} pos_x, pos_y {},{}".format(size, pos_x, pos_y))
    draw.text(
        (pos_x, pos_y),
        title, font = font_title, fill = COLOR_TEXT_TITLE,
    )
    return image


if __name__ == '__main__':
    # --- process args & options
    args = docopt(__doc__, version=__version__)
    options = { 'rotate': None, 'crop' : True } # defaults
    source = None
    size = IMAGE_SIZE # inner size, only the picture without surrounding frame
    target = None
    align = "center"
    title = ""
    f_font = None
    template = None
    configfile = get_resource_file(RESOURCE_CONFIG_FILE)
    max_size = None # max size (width) of the contactsheet
    add_exif_to_title = None

    bg_color_inner = COLOR_BG_INNER
    # process options
    source = args['<source-image>']
    if source.lower() in('-', 'stdin'):
        raise Exception("hey, great idea! :) reading from STDIN isn't supported yet but it's on the TODO-list.")
    if args['--clockwise']:
        option['rotate'] = 'clockwise'
    elif args['--anticlock']:
        option['rotate'] = 'anticlockwise'
    if args['--crop']:
        options['crop'] = True
    elif args['--nocrop']:
        options['crop'] = False
    if args['--size-inner']:
        size = int(args['--size-inner'])
    if args['--alignment']: # only used if --crop
        align = args['--alignment']
    if args['--title']:
        title = args['--title']
    if args['--title-meta']:
        add_exif_to_title = True
    if args['--font']:
        f_font = args['--font']
    else:
        f_font = RESOURCE_FONT
    if args['--output']:
        target = args['--output']
    if args['--template']:
        template = args['--template']
    if args['--config']:
        configfile = args['--config']
    # ---
    if template:
        size = None # needs to be calculated
    show_setup_info = False
    if log.level <= logging.INFO:
        show_setup_info = True
    setup_globals(size = size, configfile = configfile, template = template, show = show_setup_info)
    size = IMAGE_SIZE
    if args['--max-size']:
        max_size = int(args['--max-size'])
    # heree we go...
    if add_exif_to_title:
        exif_data = get_exif(source)
        if ('EXIF DateTimeOriginal') in exif_data:
            v = exif_data['EXIF DateTimeOriginal']
            timestamp = dt.datetime.strptime(str(v), '%Y:%m:%d %H:%M:%S')
            meta = timestamp
            if len(title) > 0:
                title += " "
            title += "%s" % (timestamp)
        else:
            log.warning("--title-meta set but exif_data about DateTime unavailable for the input-image. :-/ : {}; ;".format(fn))
    name, ext = os.path.splitext(source)
    if not os.path.isfile(source):
        show_error("Source file '%s' does not exist." % source)
    if not target:
        target = name + ".polaroid.png"
    if not align in ("left", "right", "top", "bottom", "center"):
        show_error("Unknown alignment %s." % align)
    # Prepare our resources
    f_font = get_resource_file(f_font)
    font_size = IMAGE_BOTTOM
    # finally create the polaroid.
    img = make_polaroid(
        source = source, size = size, options = options, align =align,
        title = title, f_font = f_font, font_size = font_size,
        template = template,
        bg_color_inner = bg_color_inner)
    log.debug("size: %i %i" % (img.size[0], img.size[1]))
    # ---  if --max-size is given: check if currently bigger and downscale if necessary...
    if max_size:
        xs, ys = img.size
        if (xs > max_size) or (ys > max_size):
            log.info('scaling result down to --max_size %i' % max_size)
            factor = 1
            if xs >= ys:
                factor = max_size / xs
            else:
                factor = max_size / ys
            x_new = int(img.width * factor)
            y_new = int(img.height * factor)
            img = img.resize((x_new,y_new),Image.ANTIALIAS)
    # yai, finally ... :)
    img.save(target)
    print(target)
