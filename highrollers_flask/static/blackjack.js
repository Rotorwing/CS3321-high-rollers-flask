let gameID = "";

function newGame() {
    let data = { "data": "newgame" };
    sendAPICall(data, (response) => {
        console.debug(response);
        if (response && response.id) {
            gameID = response.id;

            // Clear the HTML elements for dealer and player cards
            document.getElementById("dealer-cards").innerHTML = "";
            document.getElementById("player-cards").innerHTML = "";

            // Display dealer cards
            if (response.data.dealer && Array.isArray(response.data.dealer)) {
                response.data.dealer.forEach((card) => {
                    displayCard(card, true);
                });
            }

            // Display player cards
            if (response.data.player && Array.isArray(response.data.player)) {
                response.data.player.forEach((card) => {
                    displayCard(card, false);
                });
            }

            // Additional UI updates if necessary
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
            
            // Check for player bust
            if (response.player_value > 21) {
                console.log("Player bust!"); // Add a console message for debugging
                // Send a message to the server indicating player bust
                sendBustMessage("player");
                // Additional UI updates if necessary
            }
        }
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
            
            // Check for dealer bust
            if (response.dealer_value > 21) {
                console.log("Dealer bust!"); // Add a console message for debugging
                // Send a message to the server indicating dealer bust
                sendBustMessage("dealer");
                // Additional UI updates if necessary
            }
        }
    });
}

function sendBustMessage(player) {
    // Send a message to the server indicating the player (player or dealer) has busted
    let data = {
        "id": gameID,
        "data": { "action": "bust", "player": player }
    };
    sendAPICall(data, (response) => {
        // Handle the server response if needed
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

function calculateHandValue(cards) {
    let handValue = 0;
    let aceCount = 0;

    // Iterate through the cards and calculate the hand value
    for (const card of cards) {
        const value = card.slice(0, -1);
        if (value === 'A') {
            // Handle Ace separately, as it can be 1 or 11
            aceCount++;
            handValue += 11;
        } else if (value === 'K' || value === 'Q' || value === 'J') {
            // Face cards are worth 10 points
            handValue += 10;
        } else {
            // Numeric cards are worth their face value
            handValue += parseInt(value);
        }
    }

    // Adjust the hand value if there are Aces and the total value exceeds 21
    while (aceCount > 0 && handValue > 21) {
        handValue -= 10;
        aceCount--;
    }

    return handValue;
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