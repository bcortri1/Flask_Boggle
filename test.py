from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        self.client = app.test_client()
        app.config["TESTING"] = True
        with self.client.session_transaction() as s:
            s["board"] =   [["T","E","S","T","T"],
                            ["T","E","S","T","E"],
                            ["T","E","S","T","S"],
                            ["T","E","S","T","T"],
                            ["T","E","S","T","S"]]
            

    def test_id_create(self):
        self.assertIn()
    
    def test_main(self):
        with self.client:
            with self.client.session_transaction() as s:
                s["board"] =   [["T","E","S","T","T"],
                                ["T","E","S","T","E"],
                                ["T","E","S","T","S"],
                                ["T","E","S","T","T"],
                                ["T","E","S","T","S"]]
            response = self.client.get("/")
            self.assertIn("board", session)

    def test_board_create(self):
        with self.client:
            with self.client.session_transaction() as s:
                s["board"] =   [["T","E","S","T","T"],
                                ["T","E","S","T","E"],
                                ["T","E","S","T","S"],
                                ["T","E","S","T","T"],
                                ["T","E","S","T","S"]]
            response = self.client.get("/")
            self.assertIn("board", session)


    def test_check_word(self):
        with self.client:
            response = self.client.post("/check-word",
                                        data={"wordGuess"})
            self.assertIn("board", session)
            
    def test_score_submit(self):
        with self.client:
            response = self.client.post("/score-submit",
                                        data={"scoreSubmission":})
            self.assertIn("board", session)