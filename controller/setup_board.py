__author__ = 'riqv'
from random import randint

import configobj
from GUI.StdColors import black, red, clear, green, blue, yellow

from test.conf import test_connections, test_players
from model.world import Territory, Board, Continent
from view.blobapp import BlobApp

board = Board()
colors = {'black': black, 'red': red, 'clear': clear, 'green': green, 'blue': blue, 'yellow': yellow}


class Player():
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color


powned_territories = []


def decide_player():
    unique_players = set(powned_territories)
    if len(unique_players) == len(players_list):
        min_player = min(set(powned_territories), key=powned_territories.count)
        powned_territories.append(min_player)
        return players_list[min_player]
    else:
        player = players_conf.keys()[randint(0, len(players_list) - 1)]
        powned_territories.append(player)
        return players_list[player]


if __name__ == '__main__':
    world_conf = configobj.ConfigObj('..\\conf\\earth_world.ini', configspec='..\\conf\\board_spec.ini')
    players_conf = configobj.ConfigObj('..\\conf\\players.ini', configspec='..\\conf\\players_spec.ini')

    if not test_connections.test_connections(world_conf):
        raise RuntimeError()

    if not test_players.test_players(players_conf):
        raise RuntimeError()

    world_dict = {}

    players_list = {}
    for p in players_conf:
        player = Player(p, colors[players_conf[p]['color']])
        players_list[p] = player

    for continent in world_conf.keys():
        c = Continent(continent)
        board.add_continent(c)

        for territory in world_conf[continent]:
            ss = world_conf[continent][territory]['start_soldiers']
            t = Territory(territory, continent, int(ss))
            t.set_owner(decide_player())
            c.add_territory(t)
            world_dict[territory] = t

    for continent in world_conf.keys():
        for territory in world_conf[continent]:
            for c in world_conf[continent][territory]['connections']:
                world_dict[territory].add_connection(world_dict[c])

    continent_connections = {}
    for continent in board.get_continents():
        connections_list = []
        connections_set = set()
        connections_dict = {}
        territory_list = []
        for territory in continent.get_territories():
            territory_list.append(territory)
            for connections in territory.get_connections():
                connections_list.append(connections.get_continent())
                connections_set.add(connections.get_continent())
            connections_set.remove(continent.get_name())
            for ranker in [x for x in connections_set]:
                connections_dict[ranker] = connections_list.count(ranker)
        continent_connections[continent.get_name()] = {'connecting_continents': connections_dict,
                                                       'territories': territory_list}

    for name in set(powned_territories):
        print name + " har: " + str(powned_territories.count(name)) + " territorier."

    board.add_world(continent_connections)
    b = BlobApp(board)
    b.run()
