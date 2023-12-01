document.addEventListener("DOMContentLoaded", function() {
  showGame('game1'); // Default game to show

  const buttons = document.querySelectorAll('.navbar .button');
  buttons.forEach(button => {
      button.addEventListener('click', function() {
          const gameToShow = this.getAttribute('data-game');
          showGame(gameToShow);
      });
  });
});

function showGame(gameId) {
  // Hide all game contents
  const games = document.querySelectorAll('.game-content');
  games.forEach(game => {
      game.style.display = 'none';
  });

  // Show the selected game
  const gameToShow = document.getElementById(gameId + '-body');
  if (gameToShow) {
      gameToShow.style.display = 'block';

      // Initialize Game 1 (Blackjack)
      if (gameId === 'game1') {
          // Assuming newGame() is in blackjack.js
          newGame();
      }
  }
}

function sendAPICall(data, callback) {
  const Http = new XMLHttpRequest();
  const url = '/api/test/';
  Http.open("POST", url);
  Http.setRequestHeader("Content-Type", "application/json");

  Http.onreadystatechange = function() {
      if (Http.readyState === XMLHttpRequest.DONE) {
          const json = JSON.parse(Http.responseText);
          callback(json);
      }
  };

  let jsonData = JSON.stringify(data);
  Http.send(jsonData);
}