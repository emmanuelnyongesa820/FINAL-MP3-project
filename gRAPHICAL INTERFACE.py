from tkinter import *
from tkinter import filedialog
import pygame
import os

root = Tk()
root.title("music player")
root.geometry("550x350")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu=menubar)

songs = []
Current_song = ""
paused = False
directory = ""

def load_music():
    global Current_song, songs, directory

    songs.clear()
    songlist.delete(0, END)

    root.directory = filedialog.askdirectory()
    directory = root.directory

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert("end", song)

    if songs:
        songlist.selection_set(0)
        Current_song = songs[songlist.curselection()[0]]


def play_music():
    global Current_song, paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        return

    if songlist.curselection():
        Current_song = songs[songlist.curselection()[0]]

    pygame.mixer.music.load(os.path.join(directory, Current_song))
    pygame.mixer.music.play(loops=0)


def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True


def next_music():
    global Current_song

    try:
        index = songs.index(Current_song) + 1

        songlist.selection_clear(0, END)
        songlist.selection_set(index)

        Current_song = songs[index]
        play_music()
    except:
        pass


def prev_music():
    global Current_song

    try:
        index = songs.index(Current_song) - 1

        songlist.selection_clear(0, END)
        songlist.selection_set(index)

        Current_song = songs[index]
        play_music()
    except:
        pass


organise_menu = Menu(menubar, tearoff=0)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

songlist = Listbox(root, bg="black", fg="white", width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
prev_btn_image = PhotoImage(file='previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()