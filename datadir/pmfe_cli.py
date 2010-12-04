from plain_mame_frontend import core
import pmfe_tui

def main(args):
    """Main entry into the cli version of pmfe."""
    pmfe_core = core.Core()
    mame_games = pmfe_core.get_game_list()
    attributes = pmfe_core.get_search_attributes()
    attributes.insert(0, "all")
    attributes.append("exit")
    while True:
        attribute = pmfe_tui.get_selection(attributes, ["Choose an attribute"])
        if attribute == "all":
            while True:
                mame_games.append("back")
                game = pmfe_tui.get_selection(mame_games, ["Choose a game from all games"])
                mame_games.pop()
                if game == "back":
                    break
                if pmfe_tui.play_query(game):
                    pmfe_core.play_game(game)
        elif attribute == "exit":
            break
        else:
            while True:
                attr_list = pmfe_core.get_attr_list(mame_games, attribute)
                attr_list.append("back")
                attr_value = pmfe_tui.get_selection(attr_list, ["Choose the value of", str(attribute)])
                if attr_value == "back":
                    break
                while True:
                    game_list = pmfe_core.filter_list(mame_games, pmfe_core.get_filter(attribute, attr_value))
                    game_list.append("back")
                    game = pmfe_tui.get_selection(game_list, ["Choose a game from", str(attribute), "is %s" % attr_value])
                    if game == "back":
                        break
                    if pmfe_tui.play_query(game):
                        pmfe_core.play_game(game)
