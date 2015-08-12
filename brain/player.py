__author__ = 'Rickard'

class AIPlayer():
    def __init__(self, name, aggressive, board):
        self.name = name
        self.aggressive = aggressive
        self.board = board

    def reinforce(self):
        my_territories = self.board.get_my_territories(self.name)
        soldiers = self.board.get_new_soldiers(self.name)
        for t in my_territories:


    def attack(self):

    def final_move(self):