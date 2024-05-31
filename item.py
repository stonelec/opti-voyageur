import time


class Item:
    def __init__(self, name, mass, utility):
        self.name = name
        self.mass = mass
        self.utility = utility

    def __str__(self):
        return f'{self.name} ({self.mass} kg, {self.utility} utils)'

    def __repr__(self):
        return f'Item({self.name}, {self.mass}, {self.utility})'

    def __eq__(self, other):
        return self.name == other.name and self.mass == other.mass and self.utility == other.utility
