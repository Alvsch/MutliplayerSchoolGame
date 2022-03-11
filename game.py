class Game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.p1Went = False
        self.p2Went = False
        self.winner = -1
        self.wins = [0, 0]
        self.answers = [0, 0]

    def get_answers(self, p):
        pass