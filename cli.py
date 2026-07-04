import os
import random
from player import Player, PlayerInitError
from scanner import find_mp3s


def _show_list(playlist, base_folder):
    print("* MP3 player *")
    print("my song list")
    for i, p in enumerate(playlist, start=1):
        print(f"{i}. {os.path.relpath(p, base_folder)}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base_dir, "Mp3 player")
    if not os.path.isdir(folder):
        print(f"{folder} not found")
        return

    mp3_files = find_mp3s(folder)
    if not mp3_files:
        print("no MP3 files found")
        return

    try:
        player = Player()
    except PlayerInitError as e:
        print(e)
        return

    original = mp3_files.copy()
    playlist = mp3_files.copy()
    index = 0
    shuffled = False

    while True:
        _show_list(playlist, folder)
        choice_input = input("\nEnter the song number to play, 'SH' to toggle shuffle, 'Q' to quit, or 'H' for help: ")
        if choice_input.upper() == 'Q':
            player.stop()
            print("bye")
            break
        if choice_input.upper() == 'H':
            print("Commands after play: P pause, R resume, S stop, N next, B prev, L list, Q quit")
            continue
        if choice_input.upper() == 'SH':
            shuffled = not shuffled
            if shuffled:
                random.shuffle(playlist)
                print("shuffle ON")
            else:
                playlist = original.copy()
                print("shuffle OFF")
            continue

        if not choice_input.isdigit():
            print("enter a valid number")
            continue

        choice = int(choice_input) - 1
        if 0 <= choice < len(playlist):
            index = choice
            player.play(playlist[index])
            print(f"Now playing: {os.path.basename(playlist[index])}")
        else:
            print("invalid choice")
            continue

        # Playback control loop (non-blocking playback)
        while True:
            command = input("> ").upper()
            if command == 'P':
                player.pause()
                print("paused")
            elif command == 'R':
                player.resume()
                print("resumed")
            elif command == 'S':
                player.stop()
                print("stopped")
                break
            elif command == 'N':
                index = (index + 1) % len(playlist)
                player.play(playlist[index])
                print(f"Now playing: {os.path.basename(playlist[index])}")
            elif command == 'B':
                index = (index - 1) % len(playlist)
                player.play(playlist[index])
                print(f"Now playing: {os.path.basename(playlist[index])}")
            elif command == 'L':
                _show_list(playlist, folder)
            elif command == 'Q':
                player.stop()
                print("bye")
                return
            else:
                print("invalid command; H shows help")


if __name__ == '__main__':
    main()
