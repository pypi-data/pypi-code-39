__MAJOR__ = 0
__MINOR__ = 3
__MICRO__ = 1
__VERSION__ = (__MAJOR__, __MINOR__, __MICRO__)
__version__ = '.'.join(str(n) for n in __VERSION__)
__github_url__ = 'http://github.com/JWKennington/pelican-render-math'

from pelican_render_math.math import *
