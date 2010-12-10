from distutils.core import setup

setup(name='plain-mame-frontend',
      version='0.1',
      description='Plain MAME Frontend',
      author='Jeff Mendoza',
      author_email='jefflmendoza@gmail.com',
      packages=['plain_mame_frontend',],
      requires=['libxml2', 'curses', 'sys',],
      scripts=['bindir/pmfe',],
      license='GPL',
      long_description="""Plain MAME Frontend is a basic, easy to use frontend to mame.
It works out of the box with no config, and provides menus customized to the set of games you have, not the whole mame set.
PMFE is a console program used with the keyboard.
"""
      )
