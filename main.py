from pytube import YouTube, Playlist
import tkinter as tk
import customtkinter as ctk
import threading
import time

b_force_loop = False
num_pending_downloads = 0

def set_info_text(text):
    info_text.configure(text = text)

def on_option_changed(new_option):
    if new_option == "Video":
        title_textbox.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
    elif new_option == "Playlist":
        title_textbox.place_forget()

def download_video(url, title):
    youtube = YouTube(url, on_complete_callback = on_download_complete)
    youtube = youtube.streams.get_audio_only()
    youtube.download(filename = title + ".mp3" if title != "NONE_PROVIDED" else youtube.default_filename)

def download_playlist(url):
    global num_pending_downloads
    global window
    global b_force_loop

    playlist = Playlist(url)

    num_pending_downloads = len(playlist.videos)

    for video in playlist.videos:
        t = threading.Thread(target = download_playlist_video, args = (video,))
        t.start()

    while b_force_loop:
        window.update()
        time.sleep(0.001)

def download_playlist_video(video):
    video.register_on_complete_callback(on_download_complete)
    video.register_on_progress_callback(on_download_progress)
    video.streams.get_audio_only().download()

def download():
    if "https://www.youtube.com/" not in url_textbox.get() and "https://youtube.com/" not in url_textbox.get():
        set_info_text("Please Enter A Valid URL")
        return

    set_info_text("Downloading")
    option_menu.configure(state = "disabled")
    title_textbox.configure(state = "disabled")
    url_textbox.configure(state = "disabled")
    download_button.configure(state = "disabled")

    if option_menu.get() == "Playlist":
        download_playlist(url_textbox.get())
    elif option_menu.get() == "Video":
        download_video(url_textbox.get(), title_textbox.get())

def on_download_complete(stream, file_path):
    global num_pending_downloads
    global b_force_loop

    num_pending_downloads = num_pending_downloads - 1
    if num_pending_downloads <= 0:
        b_force_loop = False
        set_info_text("Download Complete")
        option_menu.configure(state = "normal")
        title_textbox.configure(state = "normal")
        url_textbox.configure(state = "normal")
        download_button.configure(state = "normal")    

def on_download_progress(stream, chunk, bytes_remaining):
    i = 0

window = ctk.CTk()
window.title("Eshy's YouTube Video Downloader")
window.geometry("800x600")
window.configure(bg = "#222222")

title = ctk.CTkLabel(
    master = window,
    text="Eshy's YouTube Video Downloader",
    font = ("Lato", 30)
)
option_menu = ctk.CTkOptionMenu(
    master = window,
    values = ["Video", "Playlist"],
    command = on_option_changed
)
title_textbox = ctk.CTkEntry(
    master = window,
    font = ("Lato", 20),
    placeholder_text = "Video Title (Leave Black For Original Title)",
    width = 600,
    height = 50,
    corner_radius = 10,
    fg_color = "#333333",
    border_color = "#222222"
)
url_textbox = ctk.CTkEntry(
    master = window,
    font = ("Lato", 20),
    placeholder_text = "Video or Playlist URL",
    width = 600,
    height = 50,
    corner_radius = 10,
    fg_color = "#333333",
    border_color = "#222222"
)
download_button = ctk.CTkButton(
    master = window,
    text = "DOWNLOAD",
    command = download,
    font = ("Lato", 20),
    width = 300,
    height = 50
)
info_text = ctk.CTkLabel(
    master = window,
    text = "",
    font = ("Lato", 15)
)

option_menu.place(relx = 0.1, rely = 0.025, anchor = tk.N)
title.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)
title_textbox.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)
url_textbox.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
download_button.place(relx = 0.5, rely = 0.7, anchor = tk.CENTER)
info_text.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)

window.mainloop()