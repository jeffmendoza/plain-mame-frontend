import curses

def play_query(game):
    print_game_info(game)
    if raw_input("Play game? (y/n): ") == "y":
        return True
    else:
        return False

def get_selection(choose, titles):
    return curses.wrapper(get_selection_wrapped, choose, titles)

def get_selection_wrapped(stdscr, choose, titles):
    curses.curs_set(0)
    (height, width) = stdscr.getmaxyx()
    stdscr.clear()
    pad_len = max(len(choose), len(titles) + 1)
    pad = curses.newpad(pad_len, width)
    pad.keypad(1)
    selection = 0
    pad_loc = 0
    title_len = max(len(title) for title in titles)
    while True:
        line = 0
        for item in choose:
            if line == selection:
                pad.addnstr(line, 0, str(item), width, curses.A_REVERSE)
            else:
                pad.addnstr(line, 0, str(item), width)
            line += 1
        if selection - pad_loc > height - 4 and len(choose) - pad_loc > height: pad_loc += 1
        if selection - pad_loc < 3 and pad_loc != 0: pad_loc -= 1
        for title in titles:
            pad.addstr(pad_loc + 1 + titles.index(title), width - title_len - 1, str(title))
        pad.refresh(pad_loc,0, 0,0, min(height, pad_len) - 1, width)
        char = pad.getch()
        if char == curses.KEY_UP and selection != 0: selection -= 1
        if char == curses.KEY_DOWN and selection != len(choose) - 1: selection += 1
        if char == curses.KEY_ENTER or char == 10: break
        for j in range(len(titles)):
            for i in range(title_len): pad.addch(pad_loc + 1 + j, width - title_len - 1 + i, ord(" "))
    rv = choose[selection]
    curses.curs_set(1)
    pad.keypad(0)
    return rv

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
