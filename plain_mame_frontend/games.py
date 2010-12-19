import libxml2

def find_node(node, name):
    while node is not None:
        if node.name == name:
            return node
        node = node.next
    return None

class Game(dict):
    search_attributes = ["sourcefile", "year", "manufacturer", "type", "orientation", "status", "parent", "isbios"]

    def __init__(self, node):
        """Build a Game object from an xml node from a mame xml file."""
        def find_content(node, namelist, prop=False):
            while node is not None:
                if node.name in namelist:
                    if prop is True:
                        self[node.name] = node.children.content
                    else:
                        self[node.name] = node.content
                node = node.next
        find_content(node.properties, ["name", "sourcefile", "cloneof", "isbios"], True)
        find_content(node.children, ["description", "year", "manufacturer"])
        try:
            find_content(find_node(node.children, "display").properties, ["type", "rotate", "width", "height"], True)
            find_content(find_node(node.children, "driver").properties, ["status"], True)
        except AttributeError:
            self["rotate"] = None
            self["orientation"] = None
            self["type"] = None
            self["width"] = None
            self["height"] = None
            self["status"] = None

        try: self["year"]
        except KeyError: self["year"] = "unknown"
        try: self["isbios"]
        except KeyError: self["isbios"] = "no"
        try: self["cloneof"]
        except KeyError:
            self["parent"] = True
        else:
            self["parent"] = False

        if self["rotate"] == "0" or self["rotate"] == "180":
            self["orientation"] = "Horizontal"
        else:
            self["orientation"] = "Vertical"

        if self["type"] == "vector":
            self["width"] = None
            self["height"] = None

    def __repr__(self):
        return self["description"]

class Games(list):
    def __init__(self, copy_games=None, game_filter=None):
        """Build a Games object, list of Game objects.

        copy_games -- other Games object to copy
        game_filter -- GameFilter object to apply on copy of copy_games
        
        """
        if copy_games is not None:
            for game in copy_games:
                if game_filter is None or game_filter.test(game):
                    self.append(game)
                    
    def load_from_xml(self, xmlfile, gamelist=None):
        """Load this object with Game objects from a mame xml.

        xmlfile -- string specifying mame xml in filesystem
        gamelist -- list of srings of game names to import, ignore others

        """
        doc = libxml2.parseFile(xmlfile)
        root = doc.children
        while root is not None and root.type != 'element': root = root.next
        game_node = root.children
        while game_node is not None:
            if game_node.name == "game":
                if gamelist is None or find_node(game_node.properties, "name").children.content in gamelist:
                    self.append(Game(game_node))
            game_node = game_node.next
        doc.freeDoc()
        def sort_key(item):
            return repr(item).lower()
        self.sort(key=sort_key)
            

class GameFilter:
    def __init__(self, key, value):
        """Create a filter where property key must equal value."""
        self.key = key
        self.value = value

    def test(self, game):
        """Test arg game against this filter object."""
        return game[self.key] == self.value

class AttrList(list):
    def __init__(self, games, attr):
        """Create a list of values for 'attr' that a list of games has."""
        for game in games:
            try:
                if game[attr] not in self:
                    self.append(game[attr])
            except KeyError:
                pass
        self.sort()
