# import normal modules
from tkinter import *
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

    bar['value'] += (i/tasks)*100
    completed_tasks += 1

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
    bar["value"] = 0
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

label_dest = Label(window, text="Current dest folder: " + dest,
                   bg='darkgrey', fg='white', font=('Arial', 10, 'bold'))
label_dest.place(x=10, y=340)


browse_btn = Button(window, text="Browse", bg='darkgrey',
                    fg='white', font=('Arial', 14, 'bold'), command=browse_file)
browse_btn.place(x=10, y=380)

# create the progress bar
bar = Progressbar(window, orient="horizontal", length=300)
bar.place(x=490, y=340)


text_tasks = StringVar()
text_tasks.set("0/0")
label_task = Label(window, textvariable=text_tasks, bg='darkgrey', fg='black')
label_task.place(x=760, y=362)

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
