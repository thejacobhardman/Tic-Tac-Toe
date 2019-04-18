# Jacob Hardman
# Intro To Programming
# Professor Marcus Longwell
# 4/10/19
# Python Version 3.7.3

# Credit for sound effects to Marianne Gagnon
# http://soundbible.com/1682-Robot-Blip.html
# http://soundbible.com/1669-Robot-Blip-2.html

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
Text_Font = tkFont.Font(family='Helvetica', size=30, weight='bold')

# Background image to store in the Title Frame
Title_Background = tk.PhotoImage(file="Tic-Tac-Toe-Background.png")
Smaller_Background = Title_Background.subsample(2,2)

# Displays whose turn it is
Turn_Tracker = tk.StringVar()
Turn_Tracker.set("X's Turn")

# Tracks whether the the gameboard should display an 'X' or an 'O'
Game_Piece = tk.StringVar()
Game_Piece.set("")

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

    North_West = HoverButton(Gameboard, bg="black", bd="2")
    North_West.place(relwidth="0.333", relheight="0.33")

    North = HoverButton(Gameboard, bg="black", bd="2")
    North.place(relx="0.333", relwidth="0.333", relheight="0.33")

    North_East = HoverButton(Gameboard, bg="black", bd="2")
    North_East.place(relx="0.6663", relwidth="0.3335", relheight="0.33")

    West = HoverButton(Gameboard, bg="black", bd="2")
    West.place(rely="0.33", relwidth="0.333", relheight="0.33")

    Center = HoverButton(Gameboard, bg="black", bd="2")
    Center.place(relx="0.333", rely="0.33", relwidth="0.333", relheight="0.33")

    East = HoverButton(Gameboard, bg="black", bd="2")
    East.place(relx="0.6663", rely="0.33", relwidth="0.3335", relheight="0.33")

    South_West = HoverButton(Gameboard, bg="black", bd="2")
    South_West.place(rely="0.66", relwidth="0.333", relheight="0.33")

    South = HoverButton(Gameboard, bg="black", bd="2")
    South.place(relx="0.333", rely="0.66", relwidth="0.333", relheight="0.33")

    South_East = HoverButton(Gameboard, bg="black", bd="2")
    South_East.place(relx="0.6663", rely="0.66", relwidth="0.3335", relheight="0.33")

    Reset_Button = HoverButton(Reset, bg="red", font=Text_Font, text="Reset Game")
    Reset_Button.place(relwidth="1", relheight="1")

########################################################### PROGRAM FLOW ################################################################

# This code fixes the blurry text that tkinter has when being used on Windows. I got this solution from Stack Overflow:
# https://stackoverflow.com/questions/36514158/tkinter-output-blurry-for-icon-and-text-python-2-7/43033405
if __name__ == "__main__":   
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

Init_GUI() # Initiating the GUI
Active_GUI()

# Looping in the main window to accept User input
Window.mainloop()