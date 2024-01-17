import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [game, setGame] = useState();

  useEffect(() => {
    fetch('/blackjack/4').then(res => res.json()).then(data => {
		setGame(data);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>{JSON.stringify(game?.dealer)}</p>
        <p>{JSON.stringify(game?.players)}</p>
        <p>{JSON.stringify(game)}</p>
      </header>
    </div>
  );
}

export default App;
