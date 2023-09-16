class Player:
    def __init__(self, character):
        self.name = None
        self.score = 0
        self.starting_artifact = None
        self.character = character

    def add_points(self, points):
        self.score += points

    def sub_points(self, points):
        self.score -= points

    def assign_name(self, name):
        self.name = name