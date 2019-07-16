#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
polaroidme - converts an image into vintage polaroid style

Usage:
  polaroidme <source-image> [--output=<filename>] [--title=<str>]
  polaroidme <source-image> [--title=<str>] [--font=<f>] [--output=<filename>]
  polaroidme <source-image> [--size=<n>] [--alignment=<str>] [--title=<str>] [--output=<filename>] [--font=<f>]
  polaroidme <source-image> [--nocrop|--crop] [--title=<str>] [--font=<str>] [--size=<n>] [--output=<filename>] [--alignment=<str>]
  polaroidme <source-image> [--clockwise|--anticlock] [--nocrop|--crop] [--title=<str>] [--font=<f>] [--size=<n>] [--output=<filename>] [--alignment=<str>]


Where:
  source-image    Name of the image file to convert.
  size            Size of the picture-part of the polaroid in pixels (default=800)
  alignment       Used for cropping - specifies the portion of the image
                  to include in the final output.
                  One of 'top', 'left', 'bottom', 'right' or 'center'.
                  'top' and 'left' are synonomous as are 'bottom' and
                  'right'. (default="center").
                  Not of any use if --nocrop option is set.
  title           Defines an optional caption to be displayed at the
                  bottom of the image. (default=None)
  font            Specify (ttf-)font to use (full path!)

Options:
  --nocrop         Rescale the image to fit fullframe in the final output
                   (default="--crop"). btw. alignment is ignored if option is set.
  -o, --output=<s> Defines the name of the outputfile. If omitted a filename
                   based on the original will be used - example:
                   'test.polaroid.png' will be used as filename if input-file is 'test.png'
  -f, --font=<f>   Specify (ttf-)font to use (full path!)
  -s, --size=<s>   Specifiy width of thumbnail in pixels (default=200)
  --clockwise      Rotate the image clockwise before processing
  --anticlockwise  Rotate the image anti-clockwise before processing

  -h, --help       Print this.
      --version    Print version.

The `latest version is available on github: https://github.com/s3h10r/polaroidme>
"""
import os
import site
import sys
import logging
from docopt import docopt
from PIL import Image, ImageDraw, ImageFont

# --- configure logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
handler = logging.StreamHandler() # console-handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)
# ---

# Image size constraints
IMAGE_SIZE   = 800
IMAGE_TOP    = int(IMAGE_SIZE / 16)
IMAGE_BOTTOM = int(IMAGE_SIZE / 5.333)
IMAGE_LEFT   = int(IMAGE_SIZE / 16)
IMAGE_RIGHT  = int(IMAGE_SIZE / 16)
BORDER_SIZE  = 3
# Colors
COLOR_FRAME   = (237, 243, 214)
COLOR_BORDER  = (0, 0, 0)
COLOR_TEXT_TITLE = (58, 68, 163)
COLOR_TEXT_DESCR = COLOR_TEXT_TITLE
# Font for the caption text
RESOURCE_FONT      = "fonts/default.ttf"
RESOURCE_FONT_SIZE = 142
PACKAGE_NAME = "polaroidme"

__version__ = (0,9,2)

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

def get_option(args):
    """
    Check the argument list for an option (starting with '--').

    Returns the adjusted argument list and the option found.
    """
    if len(args) == 0:
        return None, args
    if args[0][:2] == "--":
        return args[0][2:], args[1:]
    return None, args

def get_argument(args):
    """
    Get the next argument from the command line parameters

    Returns the adjusted argument list and the value of the argument.
    """
    if len(args) == 0:
        return None, args
    return args[0], args[1:]

def show_error(msg):
    """
    Show an error message and exit
    """
    log.critical("Error: %s" % msg)
    sys.exit(1)
# ---

def setup_globals(size):
    global IMAGE_SIZE
    global IMAGE_TOP
    global IMAGE_BOTTOM
    global IMAGE_LEFT
    global IMAGE_RIGHT
    global BORDER_SIZE
    IMAGE_SIZE   = size
    IMAGE_TOP    = int(IMAGE_SIZE / 16)
    IMAGE_BOTTOM = int(IMAGE_SIZE / 5.333)
    IMAGE_LEFT   = int(IMAGE_SIZE / 16)
    IMAGE_RIGHT  = int(IMAGE_SIZE / 16)
    BORDER_SIZE  = 3


def make_polaroid(source, size, options, align, title, f_font = None, font_size = RESOURCE_FONT_SIZE):
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
        img = scale_image_to_square(img)
    img = scale_image(img, size)
    img = add_frame(img)
    description = None
    img = add_text(img, caption, description, f_font = f_font, font_size = font_size)
    return img


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
        add_border = image.size[0] * (( 1 + image_ratio ) / 16)
    else:
        add_border = image.size[1] * ((image_ratio - 1) / 16)
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

def add_text(image, title = None, description = None, f_font = None, font_size = None):
    """
    adds the title & description to the image
    """
    if title is None:
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
    if (size <= 0):
        showError("Text is too large")
    draw = ImageDraw.Draw(image)
    draw.text(((IMAGE_SIZE + IMAGE_LEFT + IMAGE_RIGHT - width) / 2, IMAGE_SIZE + IMAGE_TOP + ((IMAGE_BOTTOM - height) / 2)), title, font = font_title, fill = COLOR_TEXT_TITLE)
    return image



if __name__ == '__main__':
    # --- process args & options
    args = docopt(__doc__, version=__version__)
    options = { 'rotate': None, 'crop' : True } # defaults
    source = None
    size = IMAGE_SIZE
    target = None
    align = "center"
    title = None
    f_font = None
    # process options
    source = args['<source-image>']
    if args['--clockwise']:
        option['rotate'] = 'clockwise'
    elif args['--anticlock']:
        option['rotate'] = 'anticlockwise'
    if args['--crop']:
        option['crop'] = True
    elif args['--nocrop']:
        option['crop'] = False
    if args['--size']:
        size = int(args['--size'])
    if args['--alignment']: # only used if --crop
        align = args['--alignment']
    if args['--title']:
        title = args['--title']
    if args['--font']:
        f_font = args['--font']
    else:
        f_font = RESOURCE_FONT
    if args['--output']:
        target = args['--output']
    # ---
    setup_globals(size)
    # heree we go...
    name, ext = os.path.splitext(source)
    if not os.path.isfile(source):
        show_error("Source file '%s' does not exist." % source)
    if not target:
        target = name + ".polaroid.png"
    if not align in ("left", "right", "top", "bottom", "center"):
        show_error("Unknown alignment '%s'." % align)
    # Prepare our resources
    f_font = get_resource_file(f_font)
    font_size = RESOURCE_FONT_SIZE

    # finally create the polaroid.
    img = make_polaroid(
        source = source, size = size, options = options, align =align,
        title = title, f_font = f_font, font_size = RESOURCE_FONT_SIZE)
    # Save the result
    log.debug("size: %i %i" % (img.size[0], img.size[1]))
    print(target)
    img.save(target)
