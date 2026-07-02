import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

def playmusic(folder, songname):
    filepath = os.path.join(folder, songname)
    if not os.path.exists(filepath):
        print("file not found")
        return
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    print(f"\nNow playing: {songname}")
    print("commands: P for pause, R for resume, S for stop")
    while True:
        command = input("> ").upper()
        if command == 'P':
            pygame.mixer.music.pause()
            print("paused")
        elif command == 'R':
            pygame.mixer.music.unpause()
            print("resumed")
        elif command == 'S':
            pygame.mixer.music.stop()
            print("stopped")
            return
        else:
            print("invalid command")

def main():
    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("audio initialization failed")
        print(e)
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(BASE_DIR, "Mp3 player")
    if not os.path.isdir(folder):
        print(f"{folder} not found")
        return

    mp3_files = [file for file in os.listdir(folder) if file.endswith("mp3")]

    if not mp3_files:
        print("no MP3 files found")
        return

    while True:
        print("* MP3 player *")
        print("my song list")
        for index, song in enumerate(mp3_files, start=1):
            print(f"{index}. {song}")

        choice_input = input("\nEnter the song number to play, or Q to quit: ")

        if choice_input.upper() == 'Q':
            print("bye")
            break

        if not choice_input.isdigit():
            print("enter a valid number")
            continue

        choice = int(choice_input) - 1

        if 0 <= choice < len(mp3_files):
            playmusic(folder, mp3_files[choice])
        else:
            print("invalid choice")

if __name__ == '__main__':
    main()