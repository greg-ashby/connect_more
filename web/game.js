var tokens = {};
tokens.token0 = "&nbsp;";
tokens.token1 = "<img src='/images/red.png' />";
tokens.token2 = "<img src='/images/yellow.png' />";
tokens.token3 = "<img src='/images/blue.png' />";
tokens.token4 = "<img src='/images/green.png' />";
tokens.token5 = "<img src='/images/purple.png' />";
tokens.token6 = "<img src='/images/grey.png' />";

function drawBoard(game){
  var board = "<table><caption>Click a column header to drop a token in the column</caption><tr>";
  for(var i = 0; i < game.width; i++) {
    board += "<th onclick='play(" + (i+1) +")'>" + (i+1) + "</th>";
  }
  board += "</tr>";

  for(var i = game.height-1; i >= 0; i--){
    board += "<tr>";
    for(var j = 0; j < game.width; j++){
      token = "token" + game._squares[i][j];
      board += "<td class='gameSquare'>";
      board += tokens[token];
      board += "</td>";
    }
    board += "</tr>";
  }

  board += "</table>";
  $('#board').html(board);
}

function drawScores(game){
  var scores = "<table><tr><th colspan='2'>SCORE</th></tr>";
  for(var i = 0; i < game.num_players; i++){

    scores += "<tr>";
    if(i == game.current_player - 1){
      scores += "<td class='gameSquare current'>";
    } else {
      scores += "<td class='gameSquare other'>";
    }

    token = "token" + (i+1);
    scores += tokens[token];
    scores += "</td><td class='gameSquare'>" + game.scores[i] + "</td></tr>";
  }

  scores += "</table>";
  $('#score').html(scores);
}

function displayWinner(game){
  if(game.leaders.length > 1) {
    alert("Tie Game! Players " + game.leaders.join(", ") + " all win!!!");
  } else {
    alert("Game Over! Player " + game.leaders[0] + " wins!!!");
  }
}

function drawGame(data){
  var game = JSON.parse(data);

  if(game.error){
    alert(game.error);
  } else {
    drawBoard(game);
    drawScores(game);
    if(game.empty_squares == 0){
      displayWinner(game);
    }
  }
}

function createGame(numPlayers){
  if(isNaN(numPlayers) || numPlayers < 2 || numPlayers > 6){
    alert("Invalid Number of Players, please enter a number between 2 and 6");
  } else {
    url = "/create/" + numPlayers;
    $.get(url, drawGame);
  }
}

function play(colnum){
  url = "/play/" + colnum;
  $.get(url, drawGame);
}
