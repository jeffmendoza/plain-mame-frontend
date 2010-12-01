#!/usr/bin/python

import games

def get_selection(choose, title):
    print title
    index = 1
    for item in choose:
        print "%d) %s" % (index, item)
        index = index + 1
    return choose[int(raw_input("Make a selection: ")) - 1]

def print_game_info(game):
    print "Name: " + repr(game)
    print "FileName: " + game["name"]
    print "Driver: " + game["sourcefile"]
    print "Orientation: " + game["orientation"]
    print "IsBios: " + game["isbios"]
    print "IsParent: " + repr(game["parent"])
    print "Year: " + game["year"]
    print "Manufacturer: " + game["manufacturer"]
    print "DisplayType: " + game["type"]
    if game["type"] == "raster":
        print "Resolution: " + game["width"] + "x" + game["height"]
    print "DriverStatus: " + game["status"]

def play_game(game):
    print_game_info(game)
    if raw_input("Play game? (y/n): ") == "y":
        return True
    else:
        return False

def read_in_dummy_list():
    game_list_file = open('./list')
    game_list = [ line.strip() for line in game_list_file.readlines() ]
    game_list_file.close()
    return game_list

game_list = read_in_dummy_list()
mame_games = games.Games().load_from_xml('./mame.xml', game_list)
categories = ["all", "sourcefile", "year", "manufacturer", "type", "orientation", "status", "parent", "isbios", "exit"]

while True:
    category = get_selection(categories, "Choose a category")
    if category == "all":
        while True:
            temp_games = games.Games(mame_games)
            temp_games.append("back")
            game = get_selection(temp_games, "Choose a game from all games")
            if game == "back":
                break
            if play_game(game):
                print "PLAYING GAME"
    elif category == "exit":
        break
    else:
        while True:
            attr_list = games.AttrList(mame_games, category)
            attr_list.append("back")
            cat_sel = get_selection(attr_list, "Choose the value of %s" % category)
            if cat_sel == "back":
                break
            while True:
                game_list = games.Games(mame_games, games.GameFilter(category, cat_sel))
                game_list.append("back")
                game = get_selection(game_list, "Choose a game from %s is %s" % (category, cat_sel))
                if game == "back":
                    break
                if play_game(game):
                    print "PLAYING GAME"
                
