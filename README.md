# Cyber Wordle Infinity

A modern, stable, and feature-rich Wordle-style game with a Cyberpunk aesthetic.

## Features

- **Themed Categories**: Choose from Basketball, Football, Countries, and Cyber.
- **Hints and Emojis**: Each word comes with a helpful hint and a themed emoji.
- **Modern UI**: Neon-themed interface with smooth background animations and responsive design.
- **Accessibility**: Full keyboard support and clear visual feedback for all game states.
- **Stability**: Modular code architecture with separated logic and UI.

## Getting Started

### Prerequisites

- Python 3.x
- Tkinter (usually included with Python)

### Running the Game

```bash
python3 main.py
```

### Running Tests

```bash
python3 -m unittest tests/test_engine.py
```

## Project Structure

- `main.py`: Entry point for the application.
- `src/cyber_wordle/`: Core package.
    - `engine.py`: Game logic and guess evaluation.
    - `ui.py`: Tkinter-based user interface.
    - `data.py`: Word lists, hints, and emojis.
    - `config.py`: Centralized configuration for colors, fonts, and game rules.
- `tests/`: Unit tests for the application.

## Accessibility

- Keyboard controls:
    - **A-Z**: Type letters.
    - **Backspace**: Remove letters.
    - **Enter**: Submit guess.
- High-contrast neon theme for better visibility.
- Real-time feedback as you type.

## License

This project is open-source and free to use.
