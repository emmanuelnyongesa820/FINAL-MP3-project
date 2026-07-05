import os
#hides the pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

# using pygame to play music, and os to handle file paths
def init_audio():
    if 'PULSE_SERVER' not in os.environ and os.path.exists('/mnt/wslg/PulseServer'):
        os.environ['PULSE_SERVER'] = 'unix:/mnt/wslg/PulseServer'
        os.environ.setdefault('SDL_AUDIODRIVER', 'pulse')

    try:
        pygame.mixer.init()
        return True
    except pygame.error as e:
        print("audio initialization failed")
        print(e)
        if 'SDL_AUDIODRIVER' not in os.environ or os.environ.get('SDL_AUDIODRIVER') != 'dummy':
            print("Retrying with dummy audio driver. Sound will not play.")
            os.environ['SDL_AUDIODRIVER'] = 'dummy'
            try:
                pygame.mixer.init()
                return True
            except pygame.error as e2:
                print("dummy audio initialization failed")
                print(e2)
                return False
        return False

def is_valid_mp3(filepath):
    if not filepath.lower().endswith('.mp3'):
        return False
    try:
        with open(filepath, 'rb') as f:
            header = f.read(4)
    except OSError:
        return False
    if header.startswith(b'ID3'):
        return True
    if len(header) >= 2 and header[0] == 0xFF and (header[1] & 0xE0) == 0xE0:
        return True
    return False

def playmusic(folder, songname):
    filepath = songname if os.path.isabs(songname) else os.path.join(folder, songname)
    if not os.path.exists(filepath):
        print("file not found")
        return
    try:
        pygame.mixer.music.load(filepath)#pygame mixer loads the song
        pygame.mixer.music.play()
        print(f"\nNow playing: {songname}")
        print("commands: P for pause, R for resume, S for stop")
    except pygame.error as e:
        print("playback failed:", e)
        return
    #command loop to control the music playback
    while True:
        command = input("> ").upper()#uppercase the command to make it case insensitive
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
    if not init_audio():
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))#BASE_DIR is the directory where the script is located
    mp3_files = []
    for root_dir, _, files in os.walk(BASE_DIR):
        for file in sorted(files):
            filepath = os.path.join(root_dir, file)
            if is_valid_mp3(filepath):
                mp3_files.append(filepath)

    if not mp3_files:
        print("no playable MP3 files found in the project")
        return

    while True:
        print("* MP3 player *")
        print("my song list")
        for index, song in enumerate(mp3_files, start=1):#enumerate the mp3 files and print them with their index
            print(f"{index}. {os.path.relpath(song, BASE_DIR)}")

        choice_input = input("\nEnter song number, or L to leave: ")#choice_input is the user input for the song choice or leave command

        if choice_input.upper() == 'L':
            print("bye")
            break

        if not choice_input.isdigit():#isdigit checks if the input is a number, if not, print an error message and continue the loop
            print("enter a valid num")
            continue

        choice = int(choice_input) - 1

        if 0 <= choice < len(mp3_files):
            playmusic(BASE_DIR, mp3_files[choice])
        else:
            print("invalid choice")

if __name__ == '__main__':
    main()
    #