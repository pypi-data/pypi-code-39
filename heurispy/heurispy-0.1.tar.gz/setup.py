from setuptools import setup

setup(name='heurispy',
      version='0.1',
      description='Framework para exploración de heurísticas de búsqueda local en problemas de optimización discreta',
      url='https://gitlab.com/escamilla.een/heurispy',
      author='Esteban Escamilla Navarro',
      author_email='escamilla.een@gmail.com',
      license='',
      packages=['heurispy'],
      install_requires=['pathos', 'tqdm', 'numpy', 'pandas'],
      zip_safe=False)
