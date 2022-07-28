# import normal modules
from tkinter import *
import os
import asyncio
from tkinter import filedialog
from pytube import YouTube, Playlist


# imoprt custom modules


Dmp3 = False
isPlaylist = False

dest = "D:\\Music2\\MUSIC_DOWNLOADS"


def status_change(stuff, tag=None):
    global status
    status.config(state=NORMAL)

    status.insert(END, stuff + "\n", tag, "\n")

    status.config(state=DISABLED)


def browse_file():
    global dest, label_b
    dest = filedialog.askdirectory()
    label_b.config(text="Current dest folder: " + dest)

    status_change("Set destination folder to " + dest)


def get_urls():

    urls = []
    input_urls = textbox.get("1.0", "end-1c")
    urls = input_urls.split("\n")
    status_change("Got urls")

    download(urls)


def dowmload_videos(urls, dest):
    for video in urls:

        try:
            yt = YouTube(video)
        except:
            status_change("Error: " + video + " is not a valid url", 'error')
            return

        status_change("Downloading " + video.title, 'special')

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
        os.rename(out_file, new_file)

        status_change("Downloaded " + video.title)

    urls = []
    status_change("Download complete!!")


def dowmload_playlists(urls, dest):
    for playlist in urls:
        status_change("Downloading playlist " + playlist)

        try:
            p = Playlist(playlist)
        except:
            status_change("Error: " + p.title +
                          " is not a valid playlist url", 'error')
            return

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
        except:
            status_change("Error: " + p.title +
                          " is not a valid playlist url", 'error')
            return
        status_change("Download completed playlist " +
                      p.title, 'success')
    status_change("Download complete!!", 'success')


def download(urls):
    global Dmp3, dest

    status_change("Downloading...")

    # download all the videos

    if isPlaylist:
        dowmload_playlists(urls, dest)

    else:
        dowmload_videos(urls, dest)


def check_mp():
    global Dmp3
    if(x.get()):
        Dmp3 = True
        print(Dmp3)
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
    status_change("Opened destination folder", 'success')


# create the GUI
window = Tk()
window.title("YTDownload")
window.geometry("800x500")
window.configure(background='darkgrey')

# create the labels(title and message)

title = Label(window, text="YTDownloader", bg='darkgrey',
              fg='white', font=('Arial', 22, 'bold'))
title.pack()
label = Label(window, text="Enter the URL's of the videos:",
              bg='darkgrey', fg='white', font=('Arial', 14, 'bold'))
label.place(x=10, y=60)

# create checkbox for mp3 or mp4
x = BooleanVar()
check_btn_mp = Checkbutton(window, text="MP3?", bg="darkgrey", activebackground='darkgrey', font=(
    'Arial', 10, 'bold'), variable=x, onvalue=True, offvalue=False, command=check_mp)
check_btn_mp.place(x=10, y=100)

# create checkbox for playlist or single video
y = BooleanVar()
check_btn_p = Checkbutton(window, text="Playlist?", bg="darkgrey", activebackground='darkgrey', font=(
    'Arial', 10, 'bold'), variable=y, onvalue=True, offvalue=False, command=check_p)
check_btn_p.place(x=200, y=100)

# create the textbox
textbox = Text(window, height=10, width=45, padx=20, pady=20)
textbox.place(x=10, y=130)

# create textbox for the status
status = Text(window, height=10, width=40, padx=20, pady=20, state=DISABLED)
status.tag_configure("error", foreground="red")
status.tag_configure("success", foreground="green")
status.tag_configure("special", foreground="blue")
status.place(x=430, y=130)


# create the browse button

label_b = Label(window, text="Current dest folder: " + dest,
                bg='darkgrey', fg='white', font=('Arial', 10, 'bold'))
label_b.place(x=10, y=340)

browse_btn = Button(window, text="Browse", bg='darkgrey',
                    fg='white', font=('Arial', 14, 'bold'), command=browse_file)
browse_btn.place(x=10, y=380)


# create the button

down_btn = Button(window, text="Download", bg='white',
                  fg='black', font=('Arial', 14, 'bold'), command=get_urls)
down_btn.place(x=10, y=430)


# create open file driectory button
open_btn = Button(window, text="Open File", bg='white', fg='black', font=(
    'Arial', 14, 'bold'), command=open_file_directory)
# open_btn.place(x=100, y=430)
open_btn.pack(side=BOTTOM)


window.mainloop()
