class WordTests(TestCase):
    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        with self.client.session_transaction() as s:
            s["board"] = [["T", "T", "E", "S", "T"],
                          ["E", "T", "E", "S", "T"],
                          ["S", "T", "E", "S", "T"],
                          ["T", "T", "E", "S", "T"],
                          ["S", "T", "E", "S", "T"]]

    def test_valid_word(self):
        """Check that valid words are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        data={"wordGuess": "test"})
            self.assertEqual("ok", response.data)

    def test_duplicate_word(self):
        """Checks that duplicate words are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        data={"wordGuess": "test"})
            self.assertEqual("ok", response.data)

            response = self.client.post("/check-word",
                                        data={"wordGuess": "test"})
            self.assertEqual("already-used", response.data)

    def test_not_on_board(self):
        """Check that words not on the board are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        data={"wordGuess": "best"})
            self.assertEqual("not-on-board", response.data)

    def test_not_word(self):
        """Check that not words are recognized"""
        with self.client:
            response = self.client.post("/check-word",
                                        data={"wordGuess": "abcdef"})
            self.assertEqual("not-word", response.data)