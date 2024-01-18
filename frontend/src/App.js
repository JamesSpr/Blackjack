import { useState } from 'react';
import './App.css';

function App() {
  const [game, setGame] = useState();

  return (
    <>
      {game ?
        <ReactGame game={game} setGame={setGame} />
      :
        <GameLobby setGame={setGame} />
      }
    </>
  );
}

const GameLobby = ({setGame}) => {

  const [players, setPlayers] = useState(1);

  const getGame = async () => {
    fetch(`/blackjack/${players}`).then(res => res.json()).then(data => {
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
      <input type="number" onChange={(e) => setPlayers(e.target.value)} min={1} step={1} value={players}/>
      <button onClick={getGame}>Play</button>
    </div>
  )
}

const ReactGame = ({game, setGame}) => {
  const cardValues = {
    "Ace": "A",
    "Two": "2",
    "Three": "3",
    "Four": "4",
    "Five": "5",
    "Six": "6",
    "Seven": "7",
    "Eight": "8",
    "Nine": "9",
    "Ten": "10",
    "Jack": "J",
    "Queen": "Q",
    "King": "K",
  }

  const [turn, setTurn] = useState(0);

  const drawCard = async (player) => {
    await fetch(`/draw/${player}`, {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game: game})
    }).then(res => res.json()).then(data => {
      console.log(data)
      setGame(prev => ({...prev, deck: data.deck, players: [...prev.players.map(obj => {
        if(obj.id === player) {
          return data.players[player]
        }
        return obj
      })]}));
    }).catch(error => {
      console.log(error)
    });
  }

  const finishGame = async () => {
    setTurn(-1);
    await fetch(`/draw/dealer`, {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game: game})
    }).then(res => res.json()).then(data => {
      // setGame(prev => ({...prev, dealer: data.dealer}));
      setGame(data);
    }).catch(error => {
      console.log(error)
    });
  }

  const resetGame = async () => {
    setTurn(0);
    await fetch(`/reset`, {
      method: "POST",
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({game: game})
    }).then(res => res.json()).then(data => {
      // console.log(data)
      setGame(data);
    }).catch(error => {
      console.log(error)
    });
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={() => setGame()}>Back</button>
        <button onClick={() => finishGame()}>Dealers Turn</button>
        <button onClick={() => resetGame()}>Reset</button>
      </header>
      <div>
        <h1>Dealer - {game?.dealer.hand_value}</h1>
        {game?.dealer.hand.map((card, i) => {
          if(i === 0 && turn >= 0) {
            return ( <>
              <img className="playing-card" src="/cards/Back.jpg" alt={"Face Down Card"}/>
            </>);
          }
          
          let cardPath = `/cards/${cardValues[card.value]}${card.suit[0]}.jpg`
          return ( <>
            <img className="playing-card" src={cardPath} alt={"Card " + card.value + " of " + card.suit}/>
          </>);
        })}
      </div>
      {game?.players.map(player => (
        <>
        <h1>Player{player.id} - {player.hand_value}</h1>
        <button className="hit-button" onClick={() => drawCard(player.id)} disabled={player.hand_value >= 21}>Hit</button>
        {player?.hand.map((card) => {
          let cardPath = `/cards/${cardValues[card.value]}${card.suit[0]}.jpg`
          return ( <>
            <img className="playing-card" src={cardPath} alt={"Card " + card.value + " of " + card.suit}/>
          </>);
        })}
        </>
      ))}
    </div>
  )
}

export default App;
