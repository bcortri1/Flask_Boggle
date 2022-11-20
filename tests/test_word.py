from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from stats import GameStats


class WordTests(TestCase):
    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        with self.client.session_transaction() as s:
            s["board"] = [["T", "T", "E", "S", "T"],
                          ["E", "T", "E", "S", "T"],
                          ["S", "T", "E", "S", "T"],
                          ["T", "T", "E", "S", "T"],
                          ["S", "T", "E", "S", "T"]]
            s["words_used"]=[]

    def test_valid_word(self):
        """Check that valid words are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        json={"wordGuess": "test"})
            self.assertEqual("ok", response.json["message"])

    def test_duplicate_word(self):
        """Checks that duplicate words are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        json={"wordGuess": "test"})
            self.assertEqual("ok", response.json["message"])

            response = self.client.post("/check-word",
                                        json={"wordGuess": "test"})
            self.assertEqual("already-used", response.json["message"])

    def test_not_on_board(self):
        """Check that words not on the board are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        json={"wordGuess": "best"})
            self.assertEqual("not-on-board", response.json["message"])

    def test_not_word(self):
        """Check that not words are recognized"""
        with self.client:
            home = self.client.get("/")
            response = self.client.post("/check-word",
                                        json={"wordGuess": "abcdef"})
            
            self.assertEqual("not-word", response.json["message"])
