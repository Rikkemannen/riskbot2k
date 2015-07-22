#coding: latin1

class Territory():
    def __init__(self, name, continent, start_soldiers):
        self.soldiers = start_soldiers
        self.continent = continent
        self.name = name
        self.owner = ""
        self.connections = []
    def get_soldiers(self):
        return self.soldiers
    def set_soldiers(self, s):
        self.soldiers = s
    def get_name(self):
        return self.name
    def get_connections(self):
        return self.connections
    def get_continent(self):
        return self.continent
    def add_connection(self, connection):
        self.connections.append(connection)
    def set_owner(self, owner):
        self.owner = owner
    def get_owner(self):
        return self.owner.get_name()
    def get_owner_obj(self):
        return self.owner
    def get_color(self):
        return self.owner.get_color()


class Continent():
    def __init__(self, name):
        self.territories = []
        self.name = name
        self.connections = []
    def get_name(self):
        return self.name

    def get_territories(self):
        return self.territories

    def get_nbr_territories(self):
        return len(self.territories)

    def add_territory(self, t):
        self.territories.append(t)

    def add_connection(self,c):
        self.connections.append(c)

    def get_connections(self):
        return self.connections

class Board(object):
    def __init__(self):
        self.continents = []
        self.world = {}
    def get_continents(self):
        return self.continents

    def get_nbr_continents(self):
        return len(self.continents)

    def add_continent(self, c):
        self.continents.append(c)

    def add_world(self, w):
        self.world = w

    def get_world(self):
        return self.world