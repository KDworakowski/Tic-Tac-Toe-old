// const axios = require('axios').default;

let createGameButton = document.getElementById("create-game");

let gameData = document.getElementById("game-data");

const apiurl = "http://0.0.0.0:8080"
createGameButton.addEventListener("click", function(){
    axios.post(`${apiurl}/game`, {
        player1: 'kuba',
        player2: 'kacper'
      })
      .then(function (response) {
        console.log(response.data.detail);
        createGameButton.hidden = true;
        gameData.value = JSON.stringify(response.data.detail);
      })
      .catch(function (error) {
        console.log(error);
      });
});
