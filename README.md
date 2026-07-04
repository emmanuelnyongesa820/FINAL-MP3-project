# MP3 Player (modular)

This project is a small command-line MP3 player split across simple modules for clarity.

Files added:

- `player.py`: encapsulates `Player` which controls `pygame.mixer` in a background thread. Play/pause/resume/stop are non-blocking so the CLI stays responsive.
- `scanner.py`: finds `.mp3` files recursively under the `Mp3 player` folder.
- `cli.py`: command-line UI that lists songs, supports shuffle, and accepts playback commands.
- `interface.py`: tiny runner that calls `cli.main()` (keeps your original entrypoint).
- `requirements.txt`: lists `pygame`.

How it works (high-level):

1. `cli.main()` locates MP3 files using `scanner.find_mp3s()`.
2. It builds a playlist and shows a numbered list to the user.
3. When a song is selected, `cli` calls `Player.play(filepath)`.
   - `Player.play` starts a background thread that loads the file and calls `pygame.mixer.music.play()`.
   - The thread polls `pygame.mixer.music.get_busy()` to detect when playback finishes and then clears internal state.
4. While audio plays in the background, the CLI accepts commands:
   - `P`: pause
   - `R`: resume
   - `S`: stop and return to song list
   - `N` / `B`: next / previous track
   - `SH`: toggle shuffle
   - `L`: reprint the list

Why split into modules:

- Separation of concerns: playback, file discovery, and UI are easier to read and test individually.
- Background playback avoids blocking input; the CLI can send control commands concurrently.

Run locally:

1. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

2. Put your `.mp3` files in the `Mp3 player` folder next to `interface.py`.

3. Start the player:

```bash
python3 interface.py
```

Notes and caveats:

- `pygame` must be installable on your system; on some headless Linux servers additional system libraries may be required.
- This is a minimal CLI demonstration — a GUI or more advanced features can be added if you want.
# MP3-PROJECT
# FINAL-MP3-project
