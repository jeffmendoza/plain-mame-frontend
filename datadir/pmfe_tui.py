
def play_query(game):
    print_game_info(game)
    if raw_input("Play game? (y/n): ") == "y":
        return True
    else:
        return False

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
