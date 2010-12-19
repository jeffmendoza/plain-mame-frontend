import games
import glob
import os
import subprocess
import string

class Core:
    def get_game_list(self):
        """Return a Games object containing the list of games available on the system."""
        game_list = RomList(Conf.rom_dir)
        mame_games = games.Games()
        mame_games.load_from_xml(Conf.xml, game_list)
        return mame_games

    def generate_xml(self):
        """Generate the mame xml if it does not exist."""
        pass

    def get_attr_list(self, game_list, category):
        """Return a list of values for a certian attribute in a list of games."""
        return games.AttrList(game_list, category)

    def get_filter(self, attr, attr_value):
        """Return a filter object."""
        return games.GameFilter(attr, attr_value)

    def get_search_attributes(self):
        """Return the list of attributes a game has that make sense to search on."""
        return games.Game.search_attributes

    def filter_list(self, game_list, game_filter):
        """Take the parameter game_list, apply game_filter, and return the filtered list of games."""
        return games.Games(game_list, game_filter)

    def play_game(self, game):
        """Execute mame to play game."""
        subprocess.Popen([Conf.mame_bin, game["name"]]).wait()


class RomList(list):
    def __init__(self, rom_dir, dummy=False):
        """Build this list of names of roms on the system.

        rom_dir -- directory on the filesystem where the roms are
        dummy -- build a dummy list for testing

        """
        if dummy:
            game_list_file = open('../test/list')
            for line in game_list_file.readlines():
                self.append(line.strip())
            game_list_file.close()
        else:
            for rom in glob.glob(os.path.join(rom_dir, '*.zip')):
                self.append(string.strip(os.path.basename(rom), ".zip"))

class Conf:
    import sys
    """Object to represend the system config, ini file."""
    xml = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),"..","test","mame.xml")
    mame_bin = "/usr/games/mame"
    rom_dir = os.path.expandvars("$HOME/.mame/roms")

