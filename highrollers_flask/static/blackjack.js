let gameID = "";

function newGame() {
    let data = {
        "data": "newgame"
    };
    sendAPICall(data, (response) => {
        console.debug("Response:", response); // Debugging statement to log the response

        // Check if the response contains an 'id'
        if (response && response.id) {
            gameID = response.id;

            // Clear the HTML elements for dealer and player cards
            document.getElementById("dealer-cards").innerHTML = "";
            document.getElementById("player-cards").innerHTML = "";

            // Check if dealer cards exist in the response
            if (response.dealer && Array.isArray(response.dealer) && response.dealer.length > 0) {
                // Draw the dealer's cards
                response.dealer.forEach((card) => {
                    displayCard(card, true);
                });
            } else {
                console.error("Dealer cards not found in the response:", response);
                // Handle the error or log the response for debugging
            }

            // Check if player cards exist in the response and draw them
            if (response.player && Array.isArray(response.player) && response.player.length > 0) {
                response.player.forEach((card) => {
                    displayCard(card, false);
                });
            }
        } else {
            console.error("No 'id' found in the response:", response);
            // Handle the error or log the response for debugging
        }
    });
}

function playerHit() {
    let data = {
        "id": gameID,
        "data": { "action": "hit" }
    };
    sendAPICall(data, (response) => {
        console.debug(response);
        if (response && response.card) {
            displayCard(response.card, false); // false for player card
        }
        // Additional UI updates if necessary
    });
}

function dealerHit() {
    let data = {
        "id": gameID,
        "data": { "action": "hit" }
    };
    sendAPICall(data, (response) => {
        console.debug(response);
        if (response && response.card) {
            displayCard(response.card, true); // true for dealer card
        }
        // Additional UI updates if necessary
    });
}

function playerStand() {
    let data = {
        "id": gameID,
        "data": { "action": "stand" }
    };
    sendAPICall(data, (response) => {
        console.debug(response);
        // Handle the response for the stand action
        // Update the UI accordingly
    });
}

function displayCard(backendCardName, isDealerCard) {
    let cardFilename = convertCardName(backendCardName);
    const cardImage = document.createElement("img");
    cardImage.src = "static/images/cards/" + cardFilename;
    cardImage.style.width = "100px";
    let targetContainerId = isDealerCard ? "dealer-cards" : "player-cards";
    let targetContainer = document.getElementById(targetContainerId);
    targetContainer.appendChild(cardImage);
}

function convertCardName(backendCardName) {
    const suits = { 'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades' };
    const values = {
        'A': 'ace', '2': 'two', '3': 'three', '4': 'four', '5': 'five',
        '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
        '10': 'ten', 'J': 'jack', 'Q': 'queen', 'K': 'king'
    };
    let value = backendCardName.slice(0, -1);
    let suit = backendCardName.slice(-1);
    if (backendCardName == "B") {
        return "Card_back.png";
    }
    if (value === '1') {
        value = '10';
    }
    let fullSuitName = suits[suit];
    let fullValueName = values[value];
    return `${fullSuitName}_${fullValueName}.png`;
}

document.addEventListener("DOMContentLoaded", function() {
    const hitButton = document.getElementById("hitButton");
    const standButton = document.getElementById("standButton");

    hitButton.addEventListener("click", playerHit);
    standButton.addEventListener("click", playerStand);

    // Initialize the game
    newGame();
});