import os
from tkinter import *
import tkinter.ttk as ttk #for better looking slidebars
import pygame  
from PIL import Image, ImageTk
from lyrics_extractor import SongLyrics
from mutagen.mp3 import MP3 # for song length
# Make sure all these libraries are installed

class MusicPlayer():
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("BOP IT")
        # Window Geometry
        self.root.geometry("950x450")
        self.root.resizable(width=False, height=False)
        
        # Initiating Pygame
        pygame.init()
        # Initiating Pygame Mixer
        pygame.mixer.init()
        # Declaring track Variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()

        # Declaring Song length varible to store the current song's length
        self.songlength = 0

        path = os.path.dirname(os.path.abspath(__file__))

        # menu bar
        menubar = Menu(self.root)
        # file menu
        filemenu = Menu(menubar)
        #filemenu.add_command(label="Lyrics", command=self.lyrics)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="Options", menu=filemenu)
        root.config(menu=menubar)

        logo = PhotoImage(file=os.path.join(path,"images","logotrans.png"))
        logoframe = Label(self.root, image=logo, bg="Pink")
        logoframe.image = logo
        logoframe.place(x=0, y=0, width=650, height=350)

        queueframe = LabelFrame(self.root, text="Queue", font=(
            "verdana", 15, "bold"), bg="pink", fg="black", bd=5, relief=FLAT)
        queueframe.place(x=650, y=0, width=300, height=350)
        # Inserting scrollbar
        scrol_y = Scrollbar(queueframe, orient=VERTICAL)
        # Inserting Playlist listbox
        self.playlist = Listbox(queueframe, yscrollcommand=scrol_y.set, selectbackground="pink", selectforeground="black",
                                selectmode=SINGLE, font=("verdana", 10, "bold"), bg="white", fg="black", bd=5, relief=FLAT)
        # Applying Scrollbar to listbox
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH, expand=YES)

        trackframe = LabelFrame(self.root, text=" ", font=(
            "verdana", 15, "bold"), bg="grey", fg="pink", bd=5, relief=FLAT)
        trackframe.place(x=650, y=350, width=300, height=100)
        # Inserting Song Track Label
        songtrack = Label(trackframe, textvariable=self.track, width=40, font=(
            "arial", 10, "bold"), bg="grey", fg="white", anchor=W).grid(row=0, column=0, padx=0, pady=1)
        # Inserting Status Label
        trackstatus = Label(trackframe, textvariable=self.status, width=40, font=(
            "arial", 10, "bold"), bg="grey", fg="white", anchor=W).grid(row=1, column=0, padx=0, pady=1)

        # Creating Button Frame and music slider
        buttonframe = Frame(self.root, bg="grey", relief=FLAT)
        buttonframe.place(x=0, y=350, width=650, height=50)
        sliderframe = Frame(self.root, bg="grey", relief=FLAT)
        sliderframe.place(x=0, y=400, width=650, height=50)

        # Inserting Play Button
        playbtn = Button(buttonframe, text=u'\u25B6', command=self.playsong, width=3, height=1, font=(
            "verdana", 9, "bold"), fg="black", bg="pink").grid(row=0, column=0, padx=40, pady=5)
        # Inserting Pause Button
        playbtn = Button(buttonframe, text="\u23F8", command=self.pausesong, width=5, height=1, font=(
            "verdana", 9, "bold"), fg="black", bg="pink").grid(row=0, column=1, padx=40, pady=5)
        # Inserting Unpause Button
        playbtn = Button(buttonframe, text="\u23EF", command=self.unpausesong, width=5, height=1, font=(
            "verdana", 9, "bold"), fg="black", bg="pink").grid(row=0, column=2, padx=40, pady=5)
        # Inserting Stop Button
        playbtn = Button(buttonframe, text="\u23F9", command=self.stopsong, width=5, height=1, font=(
            "verdana", 9, "bold"), fg="black", bg="pink").grid(row=0, column=3, padx=40, pady=5)
        # Inserting Lyric Button
        playbtn = Button(buttonframe, text="\u2630", command=self.lyrics, width=5, height=1, font=(
            "verdana", 9, "bold"), fg="black", bg="pink").grid(row=0, column=4, padx=40, pady=5)

        self.volslider = ttk.Scale(logoframe, from_=1, to=0, orient='vertical', command=lambda x: self.volctl())
        self.volslider.set(0.5)
        self.volslider.place(x=620, y=120, width=20, height=100)

        self.musicslider = ttk.Scale(sliderframe, from_=0, to=1, orient='horizontal',length=500, style="TScale", command=lambda x: self.update_music())
        self.musicslider.grid(row=0, column=0, padx=60, pady=10)
        # Check the sliders by dragging them

        # Changing Directory for fetching Songs
        os.chdir("./songs")
        # Fetching Songs
        songtracks = os.listdir()
        # Inserting Songs into Playlist
        for track in songtracks:
            self.playlist.insert(END, track)

    def volctl(self):
        volume = self.volslider.get()
        pygame.mixer.music.set_volume(volume)


    def update_music(self):
        try:
            pygame.mixer.music.pause()
            pygame.mixer.music.rewind()
            pygame.mixer.music.set_pos(self.songlength * self.musicslider.get())
            pygame.mixer.music.unpause()
        except pygame.error:
            pass

    def playsong(self):
        # Displaying Selected Song title
        self.track.set(self.playlist.get(ACTIVE))

        # Get song length
        self.songlength = MP3(self.playlist.get(ACTIVE)).info.length

        # Displaying Status
        self.status.set("Playing")
        # Loading Selected Song
        pygame.mixer.music.load(self.playlist.get(ACTIVE))

        # Reset music slider
        self.musicslider.set(0)

        # Playing Selected Song
        pygame.mixer.music.play()


    def stopsong(self):
        # Displaying Status
        self.status.set("Stopped")
        # Stopped Song
        pygame.mixer.music.stop()
        # Reset music slider
        self.musicslider.set(0)
    

    def pausesong(self):
        # Displaying Status
        self.status.set("Paused")
        # Paused Song
        pygame.mixer.music.pause()

    def unpausesong(self):
        # It will Display the  Status
        self.status.set("Playing")
        # Playing back Song
        pygame.mixer.music.unpause()

    def lyrics(self):
        lyricwindow = Toplevel(root)
        lyricwindow.title("Lyrics")
        lyricwindow.geometry("510x600")
        lyricwindow.resizable(width=False, height=False)
        # background set to light grey
        lyricwindow.configure(bg='pink')

        # Variable Classes in tkinter
        result = StringVar()

        def get_lyrics(ly):

            extract_lyrics = SongLyrics(
                "AIzaSyDiwnKlqrbtXWN7bocdwU1qGBbespd8yNc", "e45ca772a7696db24")

            temp = extract_lyrics.get_lyrics(str(e.get()))
            res = temp['lyrics']
            result.set(res)
            ly.config(state=NORMAL) 
            ly.delete(1.0, END)
            ly.insert(END, result.get())
            ly.config(state=DISABLED)

        lyframe = Frame(lyricwindow, bg="pink")
        lyframe.place(x=0, y=0, width=510, height=600)

        # name using widget Label
        Label(lyframe, text="  Enter Song name : ",
              bg="pink", fg="black").grid(row=0, sticky=W)

        e = Entry(lyframe, width=50)
        e.grid(row=0, column=1)

        ly = Text(lyframe, font="arial 10", width=60,
                  height=33, bg="#ffe4e1", fg="black")
        ly.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # creating a button using the widget
        b = Button(lyframe, text="Show", command=lambda: get_lyrics(
            ly), bg="white", fg="black")
        b.grid(row=0, column=2, padx=5, pady=5)




        

if __name__ == '__main__':
    root = Tk()
    x = MusicPlayer(root)
    x.root.mainloop()