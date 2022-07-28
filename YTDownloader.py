# import normal modules
from tkinter import *
from turtle import bgcolor
import customtkinter as ctk
import os
import asyncio
from tkinter import filedialog
from tkinter.ttk import Progressbar
from pytube import YouTube, Playlist


# imoprt custom modules


Dmp3 = False
isPlaylist = False
dest = ""
tasks = 0
completed_tasks = 0


def get_default_path():
    global dest

    username = os.environ.get("USERNAME")
    dest = "C:\\"+username+"\\Music\\MUSIC_DOWNLOADS"


def update_bar(i):
    global tasks, text_tasks, completed_tasks

    completed_tasks += i
    bar.set((completed_tasks/tasks)*100)

    text_tasks.set(str(completed_tasks) + "/"+str(tasks))
    window.update_idletasks()


def status_change(stuff, tag=None):
    global status
    status.config(state=NORMAL)
    status.insert(END, stuff + "\n", tag)
    status.config(state=DISABLED)

    window.update_idletasks()


def browse_file():
    global dest, label_dest
    dest = filedialog.askdirectory()
    label_dest.config(text="Current dest folder: " + dest)

    status_change("Set destination folder to " + dest)


def get_urls():
    global tasks, text_tasks, completed_tasks

    urls = []
    bar.set(0)
    text_tasks.set("0/0")
    completed_tasks = 0

    input_urls = textbox.get("1.0", "end-1c")
    urls = input_urls.split("\n")
    status_change("Got urls")

    tasks = len(urls)
    text_tasks.set("0/"+str(tasks))

    download(urls)


def dowmload_videos(urls, dest):
    for video in urls:

        try:
            yt = YouTube(video)
        except:
            status_change("Error: " + video + "is not a valid url", 'error')
            update_bar(1)
            return

        status_change("Downloading " + yt.title, 'special')

        if Dmp3:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        out_file = stream.download(dest)

        base, ext = os.path.splitext(out_file)

        if Dmp3:
            new_file = base + ".mp3"
        else:
            new_file = base + ".mp4"
        try:
            os.rename(out_file, new_file)

        except:
            status_change("Error: " + yt.title +
                          " already exists", 'error')
            update_bar(1)
            continue
        status_change("Downloaded " + yt.title)
        update_bar(1)


def dowmload_playlists(urls, dest):
    global tasks

    for playlist in urls:
        status_change("Downloading playlist " + playlist)

        try:
            p = Playlist(playlist)
        except:
            status_change("Error: " + p.title +
                          " is not a valid playlist url", 'error')
            return
        tasks += len(p.videos)

        try:
            for video in p.videos:
                status_change("Downloading " + video.title, 'special')

                if Dmp3:
                    stream = video.streams.filter(only_audio=True).first()
                else:
                    stream = video.streams.get_highest_resolution()
                out_file = stream.download(dest)
                base, ext = os.path.splitext(out_file)
                if Dmp3:
                    new_file = base + ".mp3"
                else:
                    new_file = base + ".mp4"
                os.rename(out_file, new_file)
                status_change("Downloaded " + video.title)
                update_bar(1)
        except:
            status_change("Error: " + p.title +
                          " is not a valid playlist url", 'error')
            return
        status_change("Download completed playlist " +
                      p.title, 'success')
        update_bar(1)


def download(urls):
    global Dmp3, dest, tasks

    status_change("Downloading...")

    # download all the videos

    if isPlaylist:
        dowmload_playlists(urls, dest)

    else:
        dowmload_videos(urls, dest)

    status_change("Download complete!!", 'success')


def check_mp():
    global Dmp3
    if(x.get()):
        Dmp3 = True
        status_change("File type is set to mp3")

    else:
        Dmp3 = False
        status_change("File type is set to mp4")


def check_p():
    global isPlaylist
    if(y.get()):
        isPlaylist = True
        status_change("Playlist is set to true")
    else:
        isPlaylist = False
        status_change("Playlist is set to false")


def open_file_directory():
    global dest, status

    try:
        os.startfile(dest)
    except Exception:
        status_change("Error: Folder does not exist", 'error')
        status_change("Creating the folder!!", 'special')
        if not os.path.exists(dest):
            os.makedirs(dest)

    status_change("Opened destination folder", 'success')


##################################
#  runing the main program parts
get_default_path()
##############################


# create the GUI
window = ctk.CTk()
window.title("YTDownload")
window.geometry("800x500")
# window.configure(background='darkgrey')
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


# create the labels(title and message)

title = ctk.CTkLabel(window, text="YTDownloader",
                     text_font=('Arial', 22, 'bold'))
title.pack()
label = ctk.CTkLabel(window, text="Enter the URL's of the videos:",
                     text_font=('Arial', 14, 'bold'))
label.place(x=10, y=60)

# create checkbox for mp3 or mp4
x = BooleanVar()
check_btn_mp = ctk.CTkCheckBox(window, text="MP3?",  text_font=(
    'Arial', 10, 'bold'), variable=x, onvalue=True, offvalue=False, command=check_mp)
check_btn_mp.place(x=10, y=100)

# create checkbox for playlist or single video
y = BooleanVar()
check_btn_p = ctk.CTkCheckBox(window, text="Playlist?",  text_font=(
    'Arial', 10, 'bold'), variable=y, onvalue=True, offvalue=False, command=check_p)
check_btn_p.place(x=200, y=100)

# create the textbox
textbox = Text(window, height=7, width=45,
               padx=15, pady=15, highlightthickness=0, bg='light yellow', font=('Times New Roman', 12, 'bold'), spacing1=7)
textbox.place(x=10, y=130)

# create textbox for the status
status = Text(window, height=7, width=40, padx=15, pady=15,
              bg='light yellow', highlightthickness=0, font=('Times New Roman', 12, 'bold'), state=DISABLED, spacing1=7)
status.tag_configure("error", foreground="red")
status.tag_configure("success", foreground="green")
status.tag_configure("special", foreground="blue")
status.place(x=430, y=130)


# create the browse button

label_dest = ctk.CTkLabel(window, text="Current dest folder: " + dest,
                          text_font=('Arial', 10, 'bold'))
label_dest.place(x=10, y=355)


browse_btn = ctk.CTkButton(window, text="Browse", text_font=(
    'Arial', 14, 'bold'), command=browse_file)
browse_btn.place(x=10, y=385)

# create the progress bar
bar = ctk.CTkProgressBar(window, orient="horizontal", width=300)
bar.place(x=490, y=360)
bar.set(0)


text_tasks = StringVar()
text_tasks.set("0/0")
label_task = ctk.CTkLabel(
    window, textvariable=text_tasks,)
label_task.place(x=710, y=370)

# create the button

down_btn = ctk.CTkButton(window, text="Download", text_font=(
    'Arial', 14, 'bold'), command=get_urls)
down_btn.place(x=10, y=430)


# create open file driectory button
open_btn = ctk.CTkButton(window, text="Open File", text_font=(
    'Arial', 14, 'bold'), command=open_file_directory)
# open_btn.place(x=100, y=430)
open_btn.pack(side=BOTTOM, pady=10)


window.mainloop()
