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

import unittest
import os
import sys
import libxml2

this_dir=os.path.dirname(os.path.realpath(sys.argv[0]))

sys.path.append(os.path.join(this_dir, '..'))
from plain_mame_frontend import games

class TestGamesModule(unittest.TestCase):

    def setUp(self):
        global this_dir
        game_list = []
        game_list_file = open(os.path.join(this_dir, 'list'))
        for line in game_list_file.readlines():
            game_list.append(line.strip())
        game_list_file.close()
        self.mame_games = games.Games()
        self.mame_games.load_from_xml(os.path.join(this_dir, 'mame.xml'), 
                                      game_list)

    def test_attr_list(self):
        attr_list = games.AttrList(self.mame_games, "sourcefile")
        self.assertEqual(attr_list[10], 'cps2.c')
        attr_list = games.AttrList(self.mame_games, "year")
        self.assertEqual(attr_list[-2], '2005')
        attr_list = games.AttrList(self.mame_games, "manufacturer")
        self.assertEqual(attr_list[6], 'Capcom')
        attr_list = games.AttrList(self.mame_games, "type")
        self.assertEqual(attr_list[0], 'raster')
        self.assertEqual(attr_list[1], 'vector')
        attr_list = games.AttrList(self.mame_games, "orientation")
        self.assertEqual(attr_list[0], 'Horizontal')
        self.assertEqual(attr_list[1], 'Vertical')
        attr_list = games.AttrList(self.mame_games, "status")
        self.assertEqual(attr_list[-1], 'preliminary')
        attr_list = games.AttrList(self.mame_games, "parent")
        self.assertEqual(attr_list[0], False)
        attr_list = games.AttrList(self.mame_games, "isbios")
        self.assertEqual(attr_list[0], 'no')
        self.assertEqual(attr_list[1], 'yes')

    def test_game_filter(self):
        game_filter = games.GameFilter('sourcefile', 'cps2.c')
        game_list = games.Games(self.mame_games, game_filter)
        self.assertEqual(game_list[2]['name'], 'megaman2')
        self.assertEqual(game_list[3]['year'], '1995')
        self.assertEqual(game_list[4]['width'], '384')
        self.assertTrue(game_filter.test(game_list[0]))
        self.assertTrue(game_filter.test(game_list[1]))

    def test_game_class(self):
        doc = libxml2.parseFile(os.path.join(this_dir, 'mame.xml'))
        root = doc.children
        while root is not None and root.type != 'element': root = root.next
        game_node = root.children
        for i in range(567):
            game_node = game_node.next
        game = games.Game(game_node)
        doc.freeDoc()
        self.assertEqual(game['name'], 'turtles')
        self.assertEqual(game['description'], 'Turtles') 
        self.assertEqual(game['sourcefile'], 'galdrvr.c') 
        self.assertEqual(game['width'], '768') 


if __name__ == '__main__':
    unittest.main()
