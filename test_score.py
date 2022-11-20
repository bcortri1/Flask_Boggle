from unittest import TestCase
from app import app, game_stats
from flask import session
from boggle import Boggle
from stats import GameStats


class StatTests(TestCase):
    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        with self.client.session_transaction() as s:
            s["player_id"] = 2
            game_stats.player_highscores = {0:100}
            game_stats.player_visits = {0:0}

    def test_score_submit(self):
        with self.client:
            response = self.client.post("/score-submit",json = {"scoreSubmission": "10"})
            self.assertEqual({"message": "Accepted"}, response.json)
            self.assertEqual(10, game_stats.player_highscores.get(2))
            self.assertEqual(100, game_stats.player_highscores.get(0))
            self.assertEqual(1, game_stats.player_visits.get(2))

    def test_new_highscore(self):
        with self.client:
            response = self.client.post("/score-submit",json = {"scoreSubmission": "10"})
            self.assertEqual({"message": "Accepted"}, response.json)
            self.assertEqual(10, game_stats.player_highscores.get(2))
            response = self.client.post("/score-submit",json = {"scoreSubmission": "20"})
            self.assertEqual({"message": "Accepted"}, response.json)
            self.assertEqual(20, game_stats.player_highscores.get(2))
            self.assertEqual(100, game_stats.player_highscores.get(0))
            self.assertEqual(2, game_stats.player_visits.get(2))
