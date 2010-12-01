import games

class Core:
    def get_game_list(self):
        game_list = RomList(None, dummy=True)
        mame_games = games.Games()
        mame_games.load_from_xml(Conf.xml, game_list)
        return mame_games

    def generate_xml(self):
        pass

    def get_attr_list(self, game_list, category):
        return games.AttrList(game_list, category)

    def get_filter(self, attr, attr_value):
        return games.GameFilter(attr, attr_value)

    def get_search_attributes(self):
        return games.Game.search_attributes

    def filter_list(self, game_list, game_filter):
        return games.Games(game_list, game_filter)

    def play_game(self, game):
        print "Playing game %s now" % game["name"]


class __RomList(list):
    def __init__(self, rom_dir, dummy=False):
        if dummy:
            game_list_file = open('../test/list')
            self = [ line.strip() for line in game_list_file.readlines() ]
            game_list_file.close()
        else:
            pass


class __Conf:
    xml = '../test/mame.xml'
    mame_bin = "mamebin"
    rom_dir = "romdir"

