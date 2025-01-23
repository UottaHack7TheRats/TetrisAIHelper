import Board from './components/Board';
import UpcomingBlocks from './components/UpcomingBlocks';
import { useTetris } from './hooks/useTetris';

function App() {
  const { board, startGame, isPlaying, score, lines, level, upcomingBlocks } = useTetris();

  return (
    <div className="app">
      <h1>Tetris</h1>
      <Board currentBoard={board} />
      <div className="controls">
        <div className="scores">
          <p>Score: {score}</p>
          <p>Lines: {lines}</p>
          <p>Level: {level}</p>
        </div>
        <div className="misc">
          {isPlaying ? (
            <UpcomingBlocks upcomingBlocks={upcomingBlocks} />
          ) : (
            <button onClick={startGame}>Start Game</button>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;