import ConfigParser
import games
import glob
import os
import subprocess

class XMLError(Exception):
    pass

class Core:
    def __init__(self):
        self.conf = Conf()

    def get_game_list(self):
        """Return a Games object containing the list of games available on the system."""
        game_list = RomList(self.conf.rom_dirs)
        mame_games = games.Games()
        try:
            mame_games.load_from_xml(self.conf.mame_xml, game_list)
        except games.XMLError:
            raise XMLError
        return mame_games

    def generate_xml(self):
        """Generate the mame xml if it does not exist."""
        xml_file = open(self.conf.mame_xml, 'wb')
        subprocess.Popen([self.conf.mame_bin, '-listxml'],
                         stdout=xml_file).wait()
        xml_file.close()


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
        subprocess.Popen([self.conf.mame_bin, game["name"]]).wait()


class RomList(list):
    def __init__(self, rom_dirs, dummy=False):
        """Build this list of names of roms on the system.

        rom_dirs -- directorys on the filesystem where the roms are
        dummy -- build a dummy list for testing

        """
        if dummy:
            game_list_file = open('../test/list')
            for line in game_list_file.readlines():
                self.append(line.strip())
            game_list_file.close()
        else:
            for rom_dir in rom_dirs:
                for rom in glob.glob(os.path.join(rom_dir, '*.zip')):
                    self.append(os.path.basename(rom).split('.')[0])

class Conf:
    """Object to represent the system config, ini file."""

    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        config.readfp(open('../sysconfdir/pmfe.ini'))
        self.mame_bin = config.get('pmfe', 'mame_bin')
        self.mame_ini = config.get('pmfe', 'mame_ini')
        self.mame_xml = config.get('pmfe', 'mame_xml')
        mi_file = open(self.mame_ini)
        line = ''
        while line.startswith('rompath') is False:
            line = mi_file.readline()
        mi_file.close()
        romdirs = line.split()[1]
        romdirs = romdirs.split(';')
        self.rom_dirs = [os.path.expandvars(romdir) for romdir in romdirs]
