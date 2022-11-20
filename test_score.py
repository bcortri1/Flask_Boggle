class ScoreTests(TestCase):
    def setUp(self):
        """Before Test"""
        self.client = app.test_client()
        app.config["TESTING"] = True
        with self.client.session_transaction() as s:
            s["player_id"] = 2

    def test_score_submit(self):
        with self.client:
            response = self.client.post("/score-submit",
                                        data={"scoreSubmission": "10"})
            self.assertEqual({"message":"Accepted"}, response.data)
            self.assertEqual(10, app.game_stats.player_highscores.get(2))
            self.assertEqual(0, app.game_stats.player_highscores.get(0))