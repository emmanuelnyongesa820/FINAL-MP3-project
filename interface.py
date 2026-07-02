import tkinter as tk
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Python MP3 Player")
root.geometry("400x500")
root.configure(bg="#2c3e50")  # Dark modern background

# --- 1. Track Info Section ---
info_frame = tk.Frame(root, bg="#2c3e50")
info_frame.pack(pady=20)

song_label = tk.Label(info_frame, text="No Song Playing", font=("Helvetica", 14, "bold"), fg="#ecf0f1", bg="#2c3e50")
song_label.pack()

progress_bar = ttk.Scale(info_frame, from_=0, to=100, orient="horizontal", length=300)
progress_bar.pack(pady=10)

# --- 2. Playlist Section ---
list_frame = tk.Frame(root, bg="#2c3e50")
list_frame.pack(pady=10, fill="both", expand=True, padx=20)

playlist = tk.Listbox(list_frame, bg="#34495e", fg="#ecf0f1", selectbackground="#1abc9c", bd=0, font=("Helvetica", 11))
playlist.pack(fill="both", expand=True)

# --- 3. Control Buttons Section ---
control_frame = tk.Frame(root, bg="#2c3e50")
control_frame.pack(pady=20)

# Simple placeholder functions for buttons
def play_song(): print("Play pressed")
def pause_song(): print("Pause pressed")

btn_prev = tk.Button(control_frame, text="⏮️", font=("Helvetica", 14), width=4, bg="#34495e", fg="#ecf0f1", bd=0)
btn_play = tk.Button(control_frame, text="▶️", font=("Helvetica", 14), width=4, bg="#1abc9c", fg="#ecf0f1", bd=0, command=play_song)
btn_pause = tk.Button(control_frame, text="⏸️", font=("Helvetica", 14), width=4, bg="#34495e", fg="#ecf0f1", bd=0, command=pause_song)
btn_next = tk.Button(control_frame, text="⏭️", font=("Helvetica", 14), width=4, bg="#34495e", fg="#ecf0f1", bd=0)

btn_prev.grid(row=0, column=0, padx=5)
btn_play.grid(row=0, column=1, padx=5)
btn_pause.grid(row=0, column=2, padx=5)
btn_next.grid(row=0, column=3, padx=5)

# Start the application loop
root.mainloop()