from boggle import Boggle
from stats import GameStats
from flask import Flask, request, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret Code"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)


boggle_game = Boggle()
games_stats = GameStats()


# Creates unique ids for each new player
def id_create():
    if session.get("player_id") == None:
        session["player_id"] = games_stats.new_id()


@app.route("/")
def main():
    """Creation of initial session variables are handled here"""
    session["board"] = boggle_game.make_board()
    session["words_used"] = []
    id_create()
    board = session["board"]
    return render_template("board.html", board=board)


@app.route("/check-word", methods=["POST"])
def check_word():
    """Handles all word submissions and responses"""
    board = session["board"]
    req = request.get_json()
    word_guess = req["wordGuess"]
    words_used = session["words_used"]
    if word_guess in words_used:
        response = "already-used"
    else:
        words_used.append(word_guess)
        session["words_used"] = words_used
        response = boggle_game.check_valid_word(board, word_guess)
    return response


@app.route("/score-submit", methods=["POST"])
def score_submit():
    req = request.get_json()
    player_id = session["player_id"]
    games_stats.add_score(player_id, req["scoreSubmission"])
    games_stats.add_visit(player_id)
    return {"message": "Accepted"}, 202
