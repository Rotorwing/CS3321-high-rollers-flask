let resultsContainer;

document.addEventListener("DOMContentLoaded", function(){
  resultsContainer = document.getElementById("game-placeholder");

  const drawCardButton = document.getElementById("drawCardButton");
  drawCardButton.addEventListener("click", function() {
    drawCard(false); // Ensure this is false for player cards
  });

  newGame();

  function sendAPICall(data, callback){
    const Http = new XMLHttpRequest();
    const url='/api/test/';
    Http.open("POST", url);
    Http.setRequestHeader("Content-Type", "application/json");
  
    this.callback = callback;
    Http.onreadystatechange = ((e) => {
        if(Http.readyState === XMLHttpRequest.DONE){
            const json = JSON.parse(Http.responseText);
            this.callback(json);
        }
    }).bind(this);
    console.debug(data)
    let jsonData = JSON.stringify(data);
    Http.send(jsonData);
  }
  
  window.gameID = ""
  function newGame(){
    let data = {
        "data": "newgame"
    };
    sendAPICall(data, (response) => {
        console.debug(response);
        if (response && response.id) {
            window.gameID = response.id;
            // Clear all previous cards
            document.getElementById("dealer-cards").innerHTML = "";
            document.getElementById("player-cards").innerHTML = "";

            // Draw two cards for the dealer
            drawCard(true); // Draw first card for the dealer
            drawCard(true); // Draw second card for the dealer
        }
    });
  }
  
  function drawCard(isDealerCard){
    let data = {
        "id": window.gameID,
        "data": { "action": "draw" }
    };
    sendAPICall(data, (response) => {
        console.debug(response);
        if (response && response.data && response.data.card) {
            displayCard(response.data.card, isDealerCard);
        }
    });
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

    if (backendCardName == "B")
    {
      return "Card_back.png";
    }

    if (value === '1') {
        value = '10';
    }

    let fullSuitName = suits[suit];
    let fullValueName = values[value];

    return `${fullSuitName}_${fullValueName}.png`;
  }

  // Modify this function to accept a second parameter
  function displayCard(backendCardName, isDealerCard) {
    let cardFilename = convertCardName(backendCardName);
    const cardImage = document.createElement("img");
    cardImage.src = "static/images/cards/" + cardFilename;
    cardImage.style.width = "100px";

    let targetContainerId = isDealerCard ? "dealer-cards" : "player-cards";
    let targetContainer = document.getElementById(targetContainerId);

    console.log("Target container ID:", targetContainerId);
    console.log("Target container element:", targetContainer);

    if (!targetContainer) {
        console.error("Element with ID '" + targetContainerId + "' not found.");
        return;
    }

    targetContainer.appendChild(cardImage);
  }
});