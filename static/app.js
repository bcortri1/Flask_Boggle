$boggleSubmit = $("#boggle-submit");
$boggleGuess = $("#boggle-guess");
$boggleScore = $("#boggle-score");
$boggleTimer = $("#boggle-timer");
$boggleResult = $("#boggle-result");
$boggleContainer = $("#boggle-container");
$("form")[0].reset()

class Player {
    constructor() {
        this.score = 0;
        this.timer = 60;
        this.timerStart();
    }

    scoreSubmit() {
        axios.post('/score-submit', {
            scoreSubmission: this.score
        })
    }

    timerStart() {
        this.interval = setInterval(function () {
            $boggleTimer.text(this.timer)
            if (this.timer > 0)
                this.timer = this.timer - 1;
            else {
                updateStats("Time's Up")
                this.scoreSubmit()
                clearInterval(this.interval)
            }
        }.bind(this), 1000);
    }

}

currPlayer = new Player();

//Resets form inputs and boggle selected letters
function resetForm() {
    $("form")[0].reset()
    $(".selected").removeClass("selected")
}

//Takes a str to display and the number of points to add to score
function updateStats(str, num = 0) {
    currPlayer.score += num;
    $boggleResult.text(str)
    $boggleScore.text(currPlayer.score)
}

//Changes UI depending on response
function checkResponse(response) {
    if (response.status === 200) {
        if (response.data === "ok") {
            updateStats("Good Word!", guess.length);
        }

        else if (response.data === "not-on-board") {
            updateStats("Not on the board");
        }

        else if (response.data === "already-used") {
            updateStats("Word already used");
        }

        else {
            updateStats("Not a word");
        }
    }
    else {
        updateStats(`${response.status} error from server`)
    }

}

$boggleSubmit.on("click", async function (evt) {
    evt.preventDefault();
    if (currPlayer.timer > 0) {
        guess = $boggleGuess.val()
        response = await axios.post('/check-word', {
            wordGuess: guess
        })
        checkResponse(response);
    }
    resetForm();
});

$boggleContainer.on("click", ".boggle-letter", function () {
    $(this).toggleClass("selected");

    if ($(this).hasClass("selected")) {
        $boggleGuess.val($boggleGuess.val() + $(this).text());
    }
    //Removing last occurence of letter deselected
    else {
        index = $boggleGuess.val().lastIndexOf($(this).text())
        $boggleGuess.val($boggleGuess.val().substring(0, index) + $boggleGuess.val().substring(index + 1))
    }
});

