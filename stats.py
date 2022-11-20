"""Utilities related to tracking game statistics"""
# Pseudo-database


class GameStats():

    def __init__(self):
        self.player_highscores = {0: 100}
        self.player_visits = {0: 0}

    # If the id exists it will return true
    def id_exists(self, player_id):
        return self.player_highscores.get(player_id) != None

    # Iterates to next player_id and returns it
    def new_id(self):
        new_id = list(self.player_highscores.keys())[-1]+1
        self.__add_player(new_id)
        return new_id

    # Adds new player id to stat variables
    # Private method
    def __add_player(self, player_id):
        try:
            player_id = int(player_id)
        except:
            print(f"Player ID: {player_id} is not a number")

        self.player_highscores.update({player_id: 0})
        self.player_visits.update({player_id: 0})

    # Adds new highscore to highscores and creates new player if not created yet
    # Requires a number as a player_id and a number as a score
    def add_score(self, player_id, score):
        try:
            score = int(score)
        except:
            print(f"Score: {score} is not a number")

        if self.id_exists(player_id):
            if self.player_highscores.get(player_id) < score:
                self.player_highscores.update({player_id: score})
        else:
            self.__add_player(player_id)
            self.add_score(player_id, score)

    # Adds new visit and creates new player if not created yet
    def add_visit(self, player_id):
        if self.id_exists(player_id):
            self.player_visits[player_id] += 1
        else:
            self.__add_player(player_id)
            self.add_visit(player_id)
