# Texas Hold'em vs. Gemini AI

A command-line Texas Hold'em poker game where you play against two AI opponents powered by Google's Gemini API. Built from scratch in Python — deck/shuffling, hand evaluation, multi-round betting logic, and live AI decision-making.

> ⚠️ **Note:** Due to changes in AI API access policies, the AI opponents (Bob and Charlie) are currently inactive. The poker engine, hand evaluation, and betting logic remain fully functional — the AI players will default to folding without a valid API key.

## Features

- **Full poker engine** — deck creation, shuffling, and dealing
- **Hand evaluation** — detects everything from High Card through Royal Flush, including edge cases like the ace-low straight (A-2-3-4-5)
- **Multi-round betting** — bet, call, raise, and fold logic with pot tracking and stack management
- **AI opponents** — Bob and Charlie decide their bets by querying Gemini with the current hand, pot size, and amount to call
- **Terminal polish** — colorized suits and a custom loading animation on startup

## How it works

The game deals two private cards to each player and runs through the standard Hold'em betting rounds. When it's an AI player's turn, the game builds a prompt describing their hand, the community cards, the pot, and their stack, then sends it to Gemini and parses the response into a bet or raise amount. If the API call fails or returns something unparseable, the AI defaults to folding.

Hands are scored by a custom evaluator that ranks all standard poker hands and breaks ties using the highest card.

## Getting started

```bash
git clone https://github.com/racingv12/User-Vs-Google-AI-python-game.git
cd User-Vs-Google-AI-python-game
pip install google-generativeai
python main.py
```

You'll be prompted for your name, then dealt into a three-player game against Bob and Charlie.

**To re-enable the AI opponents:** you'll need your own Gemini API key from [Google AI Studio](https://aistudio.google.com/), which you can set as an environment variable and reference in the `genai.configure()` call rather than hardcoding it.

## Skills demonstrated

- Python object-oriented design (`Card`, `Deck`, `Hand`, `Player`, `Game` classes)
- Algorithm design (poker hand ranking and tie-breaking logic)
- Third-party API integration and prompt engineering
- Error handling and input validation
- State management across multi-round gameplay
- Terminal UI (ANSI colors, loading animation)
