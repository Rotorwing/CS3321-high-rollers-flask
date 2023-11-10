document.addEventListener("DOMContentLoaded", function() {
    const gamePlaceholder = document.getElementById("game-placeholder");
    const resultsContainer = document.createElement("div");
    resultsContainer.style.display = "flex";
    resultsContainer.style.flexWrap = "wrap";
    resultsContainer.style.maxWidth = "600px";
    resultsContainer.style.justifyContent = "center";

    // Get a reference to the "Generate Random Card" button and add a click event listener
    const cardButton = document.getElementById("generateRandomCard");
    cardButton.addEventListener("click", () => {
      const numberOfCards = 5;

      // Clear the results container
      resultsContainer.innerHTML = "";

      for (let i = 0; i < numberOfCards; i++) {
        // Generate a random card for each slot
        const cardTypes = ["Hearts", "Diamonds", "Clubs", "Spades"];
        const cardType = cardTypes[Math.floor(Math.random() * cardTypes.length)];
        let cardNumber;
        let cardName;

        if (Math.random() < 0.5) {
          // Generate a numbered card (e.g., "Clubs_seven")
          const phoneticNumbers = ["two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"];
          cardNumber = phoneticNumbers[Math.floor(Math.random() * phoneticNumbers.length)];
          cardName = `${cardType}_${cardNumber}`;
        } else {
          // Generate a face card (e.g., "Spades_jack")
          const faceCards = ["ace", "jack", "queen", "king"];
          const selectedFaceCard = faceCards[Math.floor(Math.random() * faceCards.length)];
          cardName = `${cardType}_${selectedFaceCard}`;
        }

        // Create an image element for each card
        const cardImage = document.createElement("img");
        cardImage.src = "static/images/cards/" + cardName + ".png";
        cardImage.style.width = "100px";
        cardImage.style.margin = "5px";

        // Append the card image to the results container
        resultsContainer.appendChild(cardImage);
      }
    });

    // Get a reference to the "Roll the Dice" button and add a click event listener
    const diceButton = document.getElementById("generateRandomDice");
    diceButton.addEventListener("click", () => {
      const numberOfDice = 2;

      // Clear the results container
      resultsContainer.innerHTML = "";

      for (let i = 0; i < numberOfDice; i++) {
        // Generate a random dice
        const phoneticDiceNumbers = ["one", "two", "three", "four", "five", "six"];
        const diceRoll = phoneticDiceNumbers[Math.floor(Math.random() * phoneticDiceNumbers.length)];

        // Create an image element for the dice
        const diceImage = document.createElement("img");
        diceImage.src = "static/images/dice/Dice_" + diceRoll + ".png";
        diceImage.style.width = "100px";
        diceImage.style.margin = "5px";

        // Append the dice image to the results container
        resultsContainer.appendChild(diceImage);
      }
    });

    // Append the results container to the gamePlaceholder
    gamePlaceholder.appendChild(resultsContainer);

    // ---------------------------TESTING--------------------------- //

    // Points tracker
    let points = 0; // Initialize points
    const pointsContainer = document.getElementById('points-placeholder'); // Get the existing div from the HTML
    const pointsDisplay = document.createElement('div'); // Create a new div for displaying points
    pointsDisplay.id = 'pointsDisplay';
    pointsDisplay.textContent = `Points: ${points}`;
    pointsContainer.appendChild(pointsDisplay); // Append the new points display div

    // Get references to buttons from the HTML
    const incrementButton = document.getElementById('incrementPoints');
    const decrementButton = document.getElementById('decrementPoints');

    // Function to update points display
    function updatePointsDisplay() {
        pointsDisplay.textContent = `Points: ${points}`; // Update text content of the new points display div
    }

    // Add event listeners to buttons
    incrementButton.addEventListener('click', () => {
        points += 5; // Increment points by 5
        updatePointsDisplay();
    });

    decrementButton.addEventListener('click', () => {
        points = Math.max(0, points - 5); // Decrement points by 5 but not below 0
        updatePointsDisplay();
    });

    // ---------------------------TESTING--------------------------- //
});