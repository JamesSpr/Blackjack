import React, { useState } from "react";

const GameLobby = ({setGame}) => {

    const [players, setPlayers] = useState<number>(1);
  
    const getGame = async () => {
      fetch(`blackjack/${players}`).then(res => res.json()).then(data => {
        console.log(data);
            setGame(data);
      }).catch(error => {
        console.log(error)
      });
  
    };
  
    return (
      <div>
        <h1>Blackjack</h1>
        <p>Enter the number of players:</p>
        <input type="number" onChange={(e) => setPlayers(parseInt(e.target.value))} min={1} step={1} value={players}/>
        <button onClick={getGame}>Play</button>
      </div>
    )
}

export default GameLobby;