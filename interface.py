import os
#hides the pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
#using pygame to play music, and os to handle file paths
def playmusic(folder, songname):
    filepath = os.path.join(folder, songname)#file path to the song
    if not os.path.exists(filepath):
        print("file not found")
        return
    pygame.mixer.music.load(filepath)#pygame mixer loads the song
    pygame.mixer.music.play()
    print(f"\nNow playing: {songname}")
    print("commands: P for pause, R for resume, S for stop")
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
    try:#try to initialize the pygame mixer, if it fails, print an error message and return
        pygame.mixer.init()#initialize the pygame mixer
    except pygame.error as e:
        print("audio initialization failed")
        print(e)
        return

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))#BASE_DIR is the directory where the script is located
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
        for index, song in enumerate(mp3_files, start=1):#enumerate the mp3 files and print them with their index
            print(f"{index}. {song}")

        choice_input = input("\nEnter num and ply, or L to leave: ")#choice_input is the user input for the song choice or leave command

        if choice_input.upper() == 'L':
            print("bye")
            break

        if not choice_input.isdigit():#isdigit checks if the input is a number, if not, print an error message and continue the loop
            print("enter a valid num")
            continue

        choice = int(choice_input) - 1

        if 0 <= choice < len(mp3_files):
            playmusic(folder, mp3_files[choice])
        else:
            print("invalid choice")

if __name__ == '__main__':
    main()
    #