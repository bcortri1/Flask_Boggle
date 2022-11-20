from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from stats import GameStats


class MainTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_id_in_session(self):
        response = self.client.get("/")
        self.assertIn("player_id", session)

    def test_board_in_session(self):
        with self.client:
            response = self.client.get("/")
            self.assertIn("board", session)

    def test_boardsession_is_board(self):
        with self.client:
            response = self.client.get("/")
            html = response.get_data(as_text=True)
            test_board = session["board"]
            for row in test_board:
                for letter in row:
                    self.assertIn(f'<td class="boggle-letter">{letter}</td>', html)

