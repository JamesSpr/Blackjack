import React, { useState } from 'react';

const BlackjackGame = ({game, setGame}) => {
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
      await fetch(`blackjack/draw/${player}`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({game: game})
      }).then(res => res.json()).then(data => {
        setGame(prev => ({...prev, deck: data.deck, players: [...prev.players.map(obj => {
          if(obj.id === player) {
            return data.players[player]
          }
          return obj
        })]}));

        if(data.players[player].hand_value >= 21) {
            setTurn(turn + 1)
        }
      }).catch(error => {
        console.log(error)
      });
    }
  
    const finishGame = async () => {
      setTurn(-1);
      await fetch(`blackjack/draw/dealer`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({game: game})
      }).then(res => res.json()).then(data => {
        setGame(data);
      }).catch(error => {
        console.log(error)
      });
    }
  
    const resetGame = async () => {
      setTurn(0);
      await fetch(`blackjack/reset`, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({game: game})
      }).then(res => res.json()).then(data => {
        setGame(data);
      }).catch(error => {
        console.log(error)
      });
    }
  
    return ( <>
        <div className='game-space'>
            <div className="controls">
                <button onClick={() => setGame()}>Back</button>
                <button onClick={() => finishGame()}>Dealers Turn</button>
                <button onClick={() => resetGame()}>Reset</button>

                <div className='dealer'>
                    <div>
                        <h1>Dealer - {game?.dealer.hand_value}</h1>
                    </div>
                    <div>
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
                </div>
            </div>
            <div className="players">
            {game?.players.map(player => (
                <div className={`playerhand ${turn === player.id ? 'active' : ''} ${player.outcome}`}>
                <div className='player-info'>
                    <h1>Player{player.id} - {player.hand_value}</h1>
                </div>
                <div className='player-cards'>
                    {player?.hand.map((card) => {
                        let cardPath = `/cards/${cardValues[card.value]}${card.suit[0]}.jpg`
                        return ( <>
                        <img className="playing-card" src={cardPath} alt={"Card " + card.value + " of " + card.suit}/>
                        </>);
                    })}
                </div>
                <div className={`actions ${turn === player.id ? 'active' : ''}`}>
                    <button className="action-button" onClick={() => drawCard(player.id)} disabled={turn !== player.id}>Hit</button>
                    <button className="action-button" onClick={() => setTurn(turn + 1)} disabled={turn !== player.id}>Stand</button>
                </div>
            </div>
            ))}
            </div>
        </div>
    </>
    )
}

export default BlackjackGame;