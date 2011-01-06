# Copyright 2011 Jeff Mendoza <jefflmendoza@gmail.com>
#
# This file is part of Plain MAME Frontend.
#
# Plain MAME Frontend is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Plain MAME Frontend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Plain MAME Frontend.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup

name='plain-mame-frontend'

setup(name=name,
      version='0.1',
      description='Plain MAME Frontend',
      author='Jeff Mendoza',
      author_email='jefflmendoza@gmail.com',
      packages=['plain_mame_frontend',],
      requires=[
        'ConfigParser',
        'curses',
        'glob',
        'libxml2',
        'os',
        'subprocess',
        'sys',],
      scripts=['bindir/pmfe',],
      license='GPL',
      data_files=[("share/%s" % name, ['datadir/pmfe_cli.py',
                                       'datadir/pmfe_tui.py']),
                  ("/etc/%s" % name, ['sysconfdir/pmfe.ini'])],
      long_description="""Plain MAME Frontend is a basic, easy to use frontend to mame.
It works out of the box with no config, and provides menus customized to the set of games you have, not the whole mame set.
PMFE is a console program used with the keyboard.
"""
      )
