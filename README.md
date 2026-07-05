# MP3 Player Project

A simple MP3 player project built with Python and `pygame`. This repository includes:

- `interface.py` – command-line MP3 player
- `graphicalInterface.py` – Tkinter GUI music player
- `Mp3 player/` – default folder for storing local MP3 files
- control button assets: `play.png`, `pause.png`, `next.png`, `previous.png`

## Features

- Play MP3 files from a local folder
- Pause, resume, and stop playback in the command-line player
- Select a folder and play songs with control buttons in the GUI player
- Automatic `.mp3` detection (case-insensitive)

## Requirements

- Python 3.8+
- `pygame` installed
- `tkinter` available for the GUI version

## Installation

1. Install `pygame`:

```bash
pip install pygame
```

2. If you want to run the GUI app, make sure `tkinter` is installed. On Debian/Ubuntu:

```bash
sudo apt-get install python3-tk
```

## Usage

### Command-line player

1. Place your MP3 files in the `Mp3 player` folder.
2. Run:

```bash
python3 interface.py
```

3. Enter the song number to play.
4. Use commands while the song is playing:
   - `P` = pause
   - `R` = resume
   - `S` = stop and return to menu

### GUI player

1. Run:

```bash
python3 graphicalInterface.py
```

2. Select a folder that contains MP3 files.
3. Use the play, pause, next, and previous buttons.

If your system has no audio device, you can still open the window for testing with:

```bash
SDL_AUDIODRIVER=dummy python3 graphicalInterface.py
```

The GUI and CLI list only files that appear to be valid MP3s. Some files labeled `.mp3` may be unsupported if they contain streaming or invalid data.

## Notes

- The command-line player blocks until the current song is stopped.
- The GUI player allows folder selection and list-based playback.
- The `Mp3 player` folder is used by default for the CLI player, but the GUI player can open any folder.
- If your machine has no sound card, both players can still start using a dummy audio driver, but no audio will play.

## License

This project is provided as-is for learning and demonstration purposes.

