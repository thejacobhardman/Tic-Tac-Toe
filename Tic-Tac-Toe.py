# Jacob Hardman
# Intro To Programming
# Professor Marcus Longwell
# 4/10/19
# Python Version 3.7.3

# Credit for punch sound effect to Mike Koenig: http://soundbible.com/995-Jab.html
# All other sounds are in public domain

# Importing pkgs
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import ctypes
import sys
import winsound as sound

########################################################## GLOBAL VARIABLES ##############################################################

# Initializing the main window
Window = tk.Tk()
Window.title("Tic-Tac-Toe")

# I wanted the buttons on the keypad to change color when you mouse over them so I found this code on Stack Overflow:
# https://stackoverflow.com/questions/49888623/tkinter-hovering-over-button-color-change
class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

# Creating a custom font for the program to use
Text_Font = tkFont.Font(family='Helvetica', size=40, weight='bold')

# Background image to store in the Title Frame
Title_Background = tk.PhotoImage(file="Tic-Tac-Toe-Background.png")
Smaller_Background = Title_Background.subsample(2,2)

# Displays whose turn it is
Turn_Tracker = tk.StringVar()
Turn_Tracker.set("X's Turn")

# Tracks whether the the gameboard should display an 'X' or an 'O'
North_West_Text = tk.StringVar()
North_West_Text.set("")

North_Text = tk.StringVar()
North_Text.set("")

North_East_Text = tk.StringVar()
North_East_Text.set("")

West_Text = tk.StringVar()
West_Text.set("")

Center_Text = tk.StringVar()
Center_Text.set("")

East_Text = tk.StringVar()
East_Text.set("")

South_West_Text = tk.StringVar()
South_West_Text.set("")

South_Text = tk.StringVar()
South_Text.set("")

South_East_Text = tk.StringVar()
South_East_Text.set("")

########################################################## PROGRAM LOGIC ################################################################

### Initiating the GUI Framework and static GUI elements
def Init_GUI():

    global Gameboard
    global Reset

    # Content Frame that holds all of the sub widgets
    Content = tk.Frame(Window, height="1000", width="600")
    Content.pack(expand="true", fill="both")

    # Displays the name of the game
    Title = tk.Frame(Content)
    Title.place(relwidth="1", relheight="0.25")

    Title_Image = tk.Label(Title, image=Smaller_Background) 
    Title_Image.place(relwidth="1", relheight="1")

    # Displays whose turn it is as well alerts if there is a winner
    Display = tk.Frame(Content)
    Display.place(rely="0.25", relwidth="1", relheight="0.1")

    Display_Text = tk.Label(Display, font=Text_Font, textvariable=Turn_Tracker)
    Display_Text.place(relwidth=1, relheight=1)

    # The game board where the user will choose where to play
    Gameboard = tk.Frame(Content, bg="blue")
    Gameboard.place(rely="0.35", relwidth="1", relheight="0.55")

    # Provides the option for the user to reset the game (This will reset the Gameboard frame)
    Reset = tk.Frame(Content)
    Reset.place(rely="0.89", relwidth="1", relheight="0.11")

### Initiating the active GUI elements
def Active_GUI():

    North_West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=North_West_Text, command=lambda:[Update_Grid(1)])
    North_West.place(relwidth="0.333", relheight="0.33")

    North = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=North_Text, command=lambda:[Update_Grid(2)])
    North.place(relx="0.333", relwidth="0.333", relheight="0.33")

    North_East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=North_East_Text, command=lambda:[Update_Grid(3)])
    North_East.place(relx="0.6663", relwidth="0.3335", relheight="0.33")

    West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=West_Text, command=lambda:[Update_Grid(4)])
    West.place(rely="0.33", relwidth="0.333", relheight="0.33")

    Center = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Center_Text, command=lambda:[Update_Grid(5)])
    Center.place(relx="0.333", rely="0.33", relwidth="0.333", relheight="0.33")

    East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=East_Text, command=lambda:[Update_Grid(6)])
    East.place(relx="0.6663", rely="0.33", relwidth="0.3335", relheight="0.33")

    South_West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=South_West_Text, command=lambda:[Update_Grid(7)])
    South_West.place(rely="0.66", relwidth="0.333", relheight="0.33")

    South = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=South_Text, command=lambda:[Update_Grid(8)])
    South.place(relx="0.333", rely="0.66", relwidth="0.333", relheight="0.33")

    South_East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=South_East_Text, command=lambda:[Update_Grid(9)])
    South_East.place(relx="0.6663", rely="0.66", relwidth="0.3335", relheight="0.33")

    Reset_Button = HoverButton(Reset, bg="dark red", font=Text_Font, text="Reset Game", fg="black", activebackground="red", activeforeground="black",
    command=lambda:Reset_Game())
    Reset_Button.place(relwidth="1", relheight="1")

### Updates the display to show whose turn it is.
def Update_Display():

    if Turn_Tracker.get() == "X's Turn":
        Turn_Tracker.set("O's Turn")
    elif Turn_Tracker.get() == "O's Turn":
        Turn_Tracker.set("X's Turn")
    
    print("Button was pushed")

### Updates the gameboard to display the player's moves.
def Update_Grid(arg):

    if arg == 1:
        if North_West_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                North_West_Text.set("X")
                Update_Display()
            else:
                North_West_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")
            
    elif arg == 2:
        if North_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                North_Text.set("X")
                Update_Display()
            else:
                North_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 3:
        if North_East_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                North_East_Text.set("X")
                Update_Display()
            else:
                North_East_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 4:
        if West_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                West_Text.set("X")
                Update_Display()
            else:
                West_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 5:
        if Center_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                Center_Text.set("X")
                Update_Display()
            else:
                Center_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 6:
        if East_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                East_Text.set("X")
                Update_Display()
            else:
                East_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 7:
        if South_West_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                South_West_Text.set("X")
                Update_Display()
            else:
                South_West_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 8:
        if South_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                South_Text.set("X")
                Update_Display()
            else:
                South_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

    elif arg == 9:
        if South_East_Text.get() == "":
            if Turn_Tracker.get() == "X's Turn":
                South_East_Text.set("X")
                Update_Display()
            else:
                South_East_Text.set("O")
                Update_Display()
        else:
            sound.PlaySound("A-Tone.wav", 1)
            messagebox.showerror(title="ERROR", message="You cannot play on a place that has already been played on.")

### Resets the gameboard and the turn tracker
def Reset_Game():

    

    Turn_Tracker.set("X's Turn")
    North_West_Text.set("")
    North_Text.set("")
    North_East_Text.set("")
    West_Text.set("")
    Center_Text.set("")
    East_Text.set("")
    South_West_Text.set("")
    South_Text.set("")
    South_East_Text.set("")

    print("Reset button pushed")

########################################################### PROGRAM FLOW ################################################################

# This code fixes the blurry text that tkinter has when being used on Windows. I got this solution from Stack Overflow:
# https://stackoverflow.com/questions/36514158/tkinter-output-blurry-for-icon-and-text-python-2-7/43033405
if __name__ == "__main__":   
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

Init_GUI() # Initiating the static GUI elements
Active_GUI() # Initiating the active GUI elements

sound.PlaySound("Gong.wav", sound.SND_ASYNC | sound.SND_NOSTOP)

# Looping in the main window to accept User input
Window.mainloop()