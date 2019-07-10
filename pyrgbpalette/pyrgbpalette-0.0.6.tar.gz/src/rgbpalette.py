import colorsys

def rgb_in_rainbow(num, gamma=0.8):
    '''
    :param num: float number in the range 0 to 1.0
    :param gamma:
    :return: rgb-code for num in rainbow
    '''

    start = 380
    end = 750
    delta = end - start

    val2Use = delta * (num % 1.0) + start
    return wavelength_to_rgb(val2Use, gamma)


def rgb_in_palette(num, rainbowDisplay=True):
    '''
    :param num: float number in the range 0 to 1.0
    :param gamma:
    :return: rgb-code for num in rainbow
    '''

    if rainbowDisplay:
        return rgb_in_rainbow(num)
    else:
        ## Use shaded color
        r,g,b = colorsys.hsv_to_rgb(0, num, 1)
        return int(r*255),int(g*255),int(b*255)


def wavelength_to_rgb(wavelength, gamma=0.8):
    # based on https://www.noah.org/wiki/Wavelength_to_RGB_in_Python

    '''This converts a given wavelength of light to an
    approximate RGB color value. The wavelength must be given
    in nanometers in the range from 380 nm through 750 nm
    (789 THz through 400 THz).

    Based on code by Dan Bruton
    http://www.physics.sfasu.edu/astro/color/spectra.html
    '''

    wavelength = float(wavelength)
    if wavelength >= 380 and wavelength <= 440:
        attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
        R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma

    elif (wavelength >= 440 and wavelength <= 490):
        R = 0.0
        G = ((wavelength - 440) / (490 - 440)) ** gamma
        B = 1.0
    elif (wavelength >= 490 and wavelength <= 510):
        R = 0.0
        G = 1.0
        B = (-(wavelength - 510) / (510 - 490)) ** gamma
    elif (wavelength >= 510 and wavelength <= 580):
        R = ((wavelength - 510) / (580 - 510)) ** gamma
        G = 1.0
        B = 0.0
    elif (wavelength >= 580 and wavelength <= 645):
        R = 1.0
        G = (-(wavelength - 645) / (645 - 580)) ** gamma
        B = 0.0
    elif (wavelength >= 645 and wavelength <= 750):
        attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    R = R * 255
    G = G * 255
    B = B * 255
    return (int(R), int(G), int(B))


def hexcolor_from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb
