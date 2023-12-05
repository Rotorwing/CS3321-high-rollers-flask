let gameID = "";

function newGame() {
    sendAPICall({ "data": "newgame" }, (response) => {
        if (response && response.id) {
            gameID = response.id;
            document.getElementById("dealer-cards").innerHTML = "";
            document.getElementById("player-cards").innerHTML = "";
            response.data.dealer.forEach(card => displayCard(card, true));
            response.data.player.forEach(card => displayCard(card, false));
        }
    });
    hideNewGameButton();
    enableButtons();
    updateGameStatus("");
}


function showNewGameButton() {
    document.getElementById("newGameButton").style.display = "inline-block";
}

function hideNewGameButton() {
    document.getElementById("newGameButton").style.display = "none";
}

function disableButtons() {
    document.getElementById("hitButton").disabled = true;
    document.getElementById("standButton").disabled = true;
}

function enableButtons() {
    document.getElementById("hitButton").disabled = false;
    document.getElementById("standButton").disabled = false;
}

function playerHit() {
    sendAPICall({ "id": gameID, "data": { "action": "hit" } }, (response) => {
        if (response.result === "dealer") {
            updateGameStatus("Player Busts! Dealer Wins!");
            disableButtons();
            showNewGameButton();
        } //else if (response.card) {
            displayCard(response.card, false);
        //}
    });
}

function playerStand() {
    disableButtons();
    sendAPICall({ "id": gameID, "data": { "action": "stand" } }, (response) => {
        if (response) {
            if (response.dealer) {
                document.getElementById("dealer-cards").innerHTML = "";
                response.dealer.forEach(card => displayCard(card, true));
                if (response.result === "player") {
                    updateGameStatus("Player Wins!");
                } else if (response.result === "dealer") {
                    updateGameStatus("Dealer Wins!");
                } else {
                    updateGameStatus("Tie!");
                }
                showNewGameButton();
            } else {
                console.error("Unexpected response format from server:", response);
            }
        } else {
            updateGameStatus("Error: No response from server");
            showNewGameButton();
        }
    });
}

function updateGameStatus(message) {
    const pointsBar = document.getElementById("points-bar");
    if (message === "") {
        // Hide the points bar if the message is empty
        pointsBar.style.display = "none";
    } else {
        // Show the points bar and update the message
        pointsBar.style.display = "block";
        pointsBar.textContent = message;
    }
}

function displayCard(backendCardName, isDealerCard) {
    const cardFilename = convertCardName(backendCardName);
    const cardImage = document.createElement("img");
    cardImage.src = "static/images/cards/" + cardFilename;
    cardImage.style.width = "100px";
    document.getElementById(isDealerCard ? "dealer-cards" : "player-cards").appendChild(cardImage);
}

function convertCardName(backendCardName) {
    const suits = { 'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades' };
    const values = { 'A': 'ace', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten', 'J': 'jack', 'Q': 'queen', 'K': 'king' };
    let value = backendCardName.slice(0, -1);
    let suit = backendCardName.slice(-1);
    return backendCardName == "B" ? "Card_back.png" : `${suits[suit]}_${values[value === '1' ? '10' : value]}.png`;
}

document.addEventListener("DOMContentLoaded", function() {
    const hitButton = document.getElementById("hitButton");
    const standButton = document.getElementById("standButton");
    const newGameButton = document.getElementById("newGameButton");

    if (hitButton) {
        hitButton.addEventListener("click", playerHit);
    } else {
        console.error("Hit button not found");
    }

    if (standButton) {
        standButton.addEventListener("click", playerStand);
    } else {
        console.error("Stand button not found");
    }

    if (newGameButton) {
        newGameButton.addEventListener("click", newGame);
    } else {
        console.error("New game button not found");
    }

    newGame();
});