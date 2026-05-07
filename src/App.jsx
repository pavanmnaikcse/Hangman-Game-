import React, { useState, useEffect } from 'react';
import ParticleBackground from './components/ParticleBackground';
import HangmanVisuals from './components/HangmanVisuals';
import { getWord } from './words';
import { playSound } from './audio';
import confetti from 'canvas-confetti';

const App = () => {
  const [state, setState] = useState('NAME_INPUT');
  const [playerName, setPlayerName] = useState('');
  const [score, setScore] = useState(0);
  
  const [word, setWord] = useState('');
  const [guessedLetters, setGuessedLetters] = useState(new Set());
  const [mistakes, setMistakes] = useState(0);
  
  const MAX_MISTAKES = 6;
  const ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

  const handleStartGame = () => {
    playSound('click');
    setWord(getWord());
    setGuessedLetters(new Set());
    setMistakes(0);
    setState('PLAYING');
  };

  const handleGuess = (letter) => {
    if (guessedLetters.has(letter) || state !== 'PLAYING') return;
    
    playSound('click');
    const newGuessed = new Set(guessedLetters);
    newGuessed.add(letter);
    setGuessedLetters(newGuessed);

    if (!word.includes(letter)) {
      const newMistakes = mistakes + 1;
      setMistakes(newMistakes);
      
      if (newMistakes >= MAX_MISTAKES) {
        playSound('thunder');
        setTimeout(() => setState('GAME_OVER'), 500);
      }
    } else {
      const isWin = word.split('').every(char => newGuessed.has(char));
      if (isWin) {
        playSound('win');
        setScore(s => s + 100);
        confetti({ particleCount: 150, spread: 70, origin: { y: 0.6 } });
        setTimeout(() => setState('VICTORY'), 500);
      }
    }
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (state === 'PLAYING' && /^[a-zA-Z]$/.test(e.key)) {
        handleGuess(e.key.toUpperCase());
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [state, guessedLetters, word, mistakes]);

  return (
    <>
      <ParticleBackground />
      <div className="app-container">
        
        {state === 'NAME_INPUT' && (
          <div className="glass-panel">
            <h1 className="title">Dark Hangman</h1>
            <p style={{marginBottom: '20px'}}>Enter your name to begin the execution.</p>
            <form onSubmit={(e) => { e.preventDefault(); if(playerName) { playSound('click'); setState('MENU'); } }}>
              <input 
                type="text" 
                className="input-field" 
                placeholder="Your Name..." 
                value={playerName}
                onChange={(e) => setPlayerName(e.target.value)}
                maxLength={15}
                autoFocus
              />
              <button type="submit" className="btn primary" disabled={!playerName}>Enter</button>
            </form>
          </div>
        )}

        {state === 'MENU' && (
          <div className="glass-panel">
            <h1 className="title">Welcome, {playerName}</h1>
            <button className="btn primary" onClick={handleStartGame}>Start Game</button>
            <button className="btn" onClick={() => { playSound('click'); alert("Instructions:\nGuess the hidden word by selecting letters.\nYou have 6 attempts before you are executed.\nGood luck."); }}>Instructions</button>
            <div style={{marginTop: '20px', color: '#aaa'}}>Score: {score}</div>
          </div>
        )}

        {state === 'PLAYING' && (
          <div className="glass-panel" style={{ maxWidth: '800px', width: '95%' }}>
            <div className="stats-bar">
              <span>Player: {playerName}</span>
              <span style={{color: mistakes >= 4 ? '#ff4444' : '#fff'}}>Attempts: {MAX_MISTAKES - mistakes}</span>
              <span>Score: {score}</span>
            </div>
            
            <div className="hangman-container">
              <HangmanVisuals mistakes={mistakes} />
            </div>

            <div className="word-display">
              {word.split('').map((char, i) => (
                <span key={i}>{guessedLetters.has(char) ? char : '_'}</span>
              ))}
            </div>

            <div className="keyboard">
              {ALPHABET.map(letter => {
                const isGuessed = guessedLetters.has(letter);
                const isCorrect = isGuessed && word.includes(letter);
                const isIncorrect = isGuessed && !word.includes(letter);
                
                return (
                  <button 
                    key={letter}
                    className={`key ${isCorrect ? 'correct' : ''} ${isIncorrect ? 'incorrect' : ''}`}
                    onClick={() => handleGuess(letter)}
                    disabled={isGuessed}
                  >
                    {letter}
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {state === 'GAME_OVER' && (
          <div className="glass-panel danger">
            <h1 className="title" style={{color: '#ff4444'}}>YOU DIED</h1>
            <p style={{fontSize: '1.2rem', marginBottom: '20px'}}>The word was: <strong style={{color: '#fff'}}>{word}</strong></p>
            <button className="btn primary" onClick={() => { playSound('click'); setState('MENU'); }}>Return to Menu</button>
          </div>
        )}

        {state === 'VICTORY' && (
          <div className="glass-panel">
            <h1 className="title" style={{color: '#44ff88'}}>SURVIVED</h1>
            <p style={{fontSize: '1.2rem', marginBottom: '20px'}}>You have escaped the gallows.</p>
            <p style={{color: '#aaa', marginBottom: '20px'}}>Score: {score}</p>
            <button className="btn primary" onClick={handleStartGame}>Play Again</button>
            <button className="btn" onClick={() => { playSound('click'); setState('MENU'); }}>Menu</button>
          </div>
        )}

      </div>
    </>
  );
};

export default App;
