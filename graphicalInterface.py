from tkinter import *
from tkinter import filedialog
import pygame
import os

root = Tk()
root.title("music player")
root.geometry("650x420")

def init_audio():
    if 'PULSE_SERVER' not in os.environ and os.path.exists('/mnt/wslg/PulseServer'):
        os.environ['PULSE_SERVER'] = 'unix:/mnt/wslg/PulseServer'
        os.environ.setdefault('SDL_AUDIODRIVER', 'pulse')

    try:
        pygame.mixer.init()
    except pygame.error as e:
        print("audio initialization failed")
        print(e)
        if 'SDL_AUDIODRIVER' not in os.environ or os.environ.get('SDL_AUDIODRIVER') != 'dummy':
            print("Retrying with dummy audio driver. Sound will not play.")
            os.environ['SDL_AUDIODRIVER'] = 'dummy'
            try:
                pygame.mixer.init()
            except pygame.error as e2:
                print("dummy audio initialization failed")
                print(e2)
                raise
        else:
            raise

init_audio()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
song_paths = []
Current_song = ""
paused = False
directory = ""

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


def load_music():
    global Current_song, songs, directory, song_paths

    songs.clear()
    song_paths.clear()
    songlist.delete(0, END)

    selected_folder = filedialog.askdirectory()
    if not selected_folder:
        return

    directory = selected_folder
    folder_label.config(text=f'Current folder: {directory}')

    for song in sorted(os.listdir(directory)):
        filepath = os.path.join(directory, song)
        if is_valid_mp3(filepath):
            songs.append(os.path.relpath(filepath, directory))
            song_paths.append(os.path.abspath(filepath))

    if not songs:
        folder_label.config(text=f'Current folder: {directory} (no playable MP3s found)')
        return

    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    Current_song = songs[songlist.curselection()[0]]
    now_playing_label.config(text='Now playing: none')

    folder_label.config(text=f'Current folder: {directory} ({len(songs)} songs)')


def load_all_music():
    """Scan the project for playable MP3s and load them."""
    global Current_song, songs, song_paths, directory
    songs.clear()
    song_paths.clear()
    songlist.delete(0, END)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    for root_dir, _, files in os.walk(BASE_DIR):
        for file in sorted(files):
            filepath = os.path.join(root_dir, file)
            if is_valid_mp3(filepath):
                songs.append(os.path.relpath(filepath, BASE_DIR))
                song_paths.append(os.path.abspath(filepath))

    if not songs:
        folder_label.config(text=f'Project: no playable MP3s found')
        return

    folder_label.config(text=f'Project: {BASE_DIR} ({len(songs)} songs)')
    for song in songs:
        songlist.insert('end', song)
    songlist.selection_set(0)
    Current_song = songs[0]
    now_playing_label.config(text='Now playing: none')


def play_music():
    global Current_song, paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        return

    if songlist.curselection():
        Current_song = songs[songlist.curselection()[0]]

    if not Current_song:
        return

    # determine index and absolute path
    try:
        idx = songlist.curselection()[0]
    except Exception:
        return
    if idx < 0 or idx >= len(song_paths):
        return
    path = song_paths[idx]

    try:
        # stop any existing music and play the selected file
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops=0)
        now_playing_label.config(text=f'Now playing: {songs[idx]}')
    except pygame.error as e:
        print('playback failed:', e)


def pause_music():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
        now_playing_label.config(text=f'Paused: {Current_song}')


def stop_music():
    global paused
    pygame.mixer.music.stop()
    paused = False
    now_playing_label.config(text='Now playing: none')


def next_music():
    global Current_song

    try:
        index = songlist.curselection()[0] + 1
        if index >= songlist.size():
            return
        songlist.selection_clear(0, END)
        songlist.selection_set(index)
        Current_song = songs[index]
        play_music()
    except Exception:
        pass


def prev_music():
    global Current_song

    try:
        index = songlist.curselection()[0] - 1
        if index < 0:
            return
        songlist.selection_clear(0, END)
        songlist.selection_set(index)
        Current_song = songs[index]
        play_music()
    except Exception:
        pass


organise_menu = Menu(menubar, tearoff=0)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

btn_frame = Frame(root)
btn_frame.pack(pady=6)

select_folder_btn = Button(btn_frame, text='Select Folder', command=load_music)
select_folder_btn.grid(row=0, column=0, padx=6)

load_all_btn = Button(btn_frame, text='Load All Songs', command=load_all_music)
load_all_btn.grid(row=0, column=1, padx=6)

folder_label = Label(root, text='Current folder: none', bg='white', anchor='w')
folder_label.pack(fill='x', padx=10, pady=(4, 10))

now_playing_label = Label(root, text='Now playing: none', anchor='w')
now_playing_label.pack(fill='x', padx=10, pady=(0, 8))

songlist = Listbox(root, bg="#222222", fg="white", width=100, height=14, selectbackground='#4a90e2')
songlist.pack(padx=10)
songlist.bind('<Double-Button-1>', lambda e: play_music())
root.bind('<space>', lambda e: play_music())
root.bind('<Left>', lambda e: prev_music())
root.bind('<Right>', lambda e: next_music())
root.bind('<s>', lambda e: stop_music())
root.bind('<S>', lambda e: stop_music())
root.bind('<p>', lambda e: pause_music())
root.bind('<P>', lambda e: pause_music())


def load_image(path):
    try:
        return PhotoImage(file=path)
    except Exception as e:
        print(f"Warning: failed to load image {path}: {e}")
        return None

play_btn_image = load_image('play.png')
pause_btn_image = load_image('pause.png')
next_btn_image = load_image('next.png')
prev_btn_image = load_image('previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, text="Play" if not play_btn_image else "", compound='top', borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, text="Pause" if not pause_btn_image else "", compound='top', borderwidth=0, command=pause_music)
stop_btn = Button(control_frame, text='Stop', borderwidth=0, command=stop_music)
next_btn = Button(control_frame, image=next_btn_image, text="Next" if not next_btn_image else "", compound='top', borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, text="Prev" if not prev_btn_image else "", compound='top', borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
stop_btn.grid(row=0, column=2, padx=7, pady=10)
pause_btn.grid(row=0, column=3, padx=7, pady=10)
next_btn.grid(row=0, column=4, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()