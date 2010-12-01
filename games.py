
import libxml2

def find_node(node, name):
    while node is not None:
        if node.name == name:
            return node
        node = node.next
    return None

class Game(dict):
    def __init__(self, node):
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
        try: self["year"]
        except: self["year"] = "unknown"
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

        try: self["cloneof"]
        except KeyError:
            self["parent"] = True
        else:
            self["parent"] = False

        if self["rotate"] == 0 or self["rotate"] == 180:
            self["orientation"] = "Horizontal"
        else:
            self["orientation"] = "Vertical"

        if self["type"] == "vector":
            self["width"] = None
            self["height"] = None

        try: self["isbios"]
        except KeyError:
            self["isbios"] = "no"

class Games(list):
    def __init__(self, copy_games=None, game_filter=None):
        if copy_games is not None:
            for game in copy_games:
                if game_filter is None or game_filter.test(game):
                    self.append(game)

    def load_from_xml(self, xmlfile, gamelist=None):
        doc = libxml2.parseFile(xmlfile)
        root = doc.children
        def find_games(node):
            while node is not None:
                if node.type == "element" and node.name == "game":
                    if gamelist is None or find_node(node.properties, "name").children.content in gamelist:
                        self.append(Game(node))
                find_games(node.children)
                node = node.next
        find_games(root)
        doc.freeDoc()
            

class GameFilter:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def test(self, game):
        return game[self.key] == self.value

class AttrList(list):
    def __init__(self, games, attr):
        for game in games:
            try:
                if game[attr] not in self:
                    self.append(game[attr])
            except KeyError:
                pass
