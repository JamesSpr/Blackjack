import React, { useState } from 'react';
import GameLobby from './pages/GameLobby.tsx';
import BlackjackGame from './pages/Game.tsx';
import './App.css';

function App() {
  const [game, setGame] = useState();

  return (
    <>
      {game ?
        <BlackjackGame game={game} setGame={setGame} />
      :
        <GameLobby setGame={setGame} />
      }
    </>
  );
}

export default App;
