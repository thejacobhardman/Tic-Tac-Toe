# Jacob Hardman
# Intro To Programming
# Professor Marcus Longwell
# 4/10/19
# Python Version 3.7.3

# Credit for punch sound effect to Mike Koenig: http://soundbible.com/995-Jab.html
# Credit for cat scream sound effect to Ca9: http://soundbible.com/1509-Cat-Scream.html
# All other sounds are in public domain

# Importing pkgs
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
import ctypes
import sys
import winsound as sound
import random

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
Gameboard_Text = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(),
                 tk.StringVar(), tk.StringVar(), tk.StringVar()]

i = 0
for var in Gameboard_Text:
    var.set("")

# Tracks whether the game is in singleplayer mode or in multiplayer mode
Singleplayer = False

# Tracks if the game is over
Game_Over = False

########################################################## PROGRAM LOGIC ################################################################

### Initiating the GUI Framework and the static GUI elements
def Init_GUI():

    global Gameboard
    global Reset

    # Content Frame that holds all of the sub widgets
    Content = tk.Frame(Window, height="1000", width="600")
    Content.pack(expand="true", fill="both")

    # Displays a banner image
    Title = tk.Frame(Content)
    Title.place(relwidth="1", relheight="0.25")

    Title_Image = tk.Label(Title, image=Smaller_Background) 
    Title_Image.place(relwidth="1", relheight="1")

    # Displays whose turn it is as well alerts if there is a winner
    Display = tk.Frame(Content)
    Display.place(rely="0.25", relwidth="1", relheight="0.1")

    Display_Text = tk.Label(Display, font=Text_Font, textvariable=Turn_Tracker)
    Display_Text.place(relwidth="1", relheight="1")

    # The game board where the user will choose where to play
    Gameboard = tk.Frame(Content)
    Gameboard.place(rely="0.35", relwidth="1", relheight="0.55")

    # Provides the option for the user to reset the game (This will reset the Gameboard frame)
    Reset = tk.Frame(Content)
    Reset.place(rely="0.89", relwidth="1", relheight="0.11")

### Initiating the active GUI elements
def Active_GUI():

    North_West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[0], command=lambda:[Update_Grid(1), Check_Win()])
    North_West.place(relwidth="0.333", relheight="0.33")

    North = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[1], command=lambda:[Update_Grid(2), Check_Win()])
    North.place(relx="0.333", relwidth="0.333", relheight="0.33")

    North_East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[2], command=lambda:[Update_Grid(3), Check_Win()])
    North_East.place(relx="0.6663", relwidth="0.3335", relheight="0.33")

    West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[3], command=lambda:[Update_Grid(4), Check_Win()])
    West.place(rely="0.33", relwidth="0.333", relheight="0.33")

    Center = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[4], command=lambda:[Update_Grid(5), Check_Win()])
    Center.place(relx="0.333", rely="0.33", relwidth="0.333", relheight="0.33")

    East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[5], command=lambda:[Update_Grid(6), Check_Win()])
    East.place(relx="0.6663", rely="0.33", relwidth="0.3335", relheight="0.33")

    South_West = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[6], command=lambda:[Update_Grid(7), Check_Win()])
    South_West.place(rely="0.66", relwidth="0.333", relheight="0.33")

    South = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[7], command=lambda:[Update_Grid(8), Check_Win()])
    South.place(relx="0.333", rely="0.66", relwidth="0.333", relheight="0.33")

    South_East = HoverButton(Gameboard, bg="dark red", bd="2", fg="black", activebackground="red", activeforeground="black",
    font=Text_Font, textvariable=Gameboard_Text[8], command=lambda:[Update_Grid(9), Check_Win()])
    South_East.place(relx="0.6663", rely="0.66", relwidth="0.3335", relheight="0.33")

    Reset_Button = HoverButton(Reset, bg="black", font=Text_Font, text="Reset Game", fg="white", activebackground="red", activeforeground="white",
    command=lambda:Reset_Game())
    Reset_Button.place(relwidth="1", relheight="1")

### Updates the display to show whose turn it is.
def Update_Display():

    if Turn_Tracker.get() == "X's Turn":
        Turn_Tracker.set("O's Turn")
    elif Turn_Tracker.get() == "O's Turn":
        Turn_Tracker.set("X's Turn")

### Updates the gameboard to display the player's moves.
def Update_Grid(arg):

    global Singleplayer

    # The player selected the North-West button (Internal logic is the same for all buttons)
    if arg == 1:
        if Gameboard_Text[0].get() == "": # Checking if someone has already played on that space
            if Turn_Tracker.get() == "X's Turn": # It's the first player's turn
                sound.PlaySound("Jab.wav", 1) # Sound effects for fun
                Gameboard_Text[0].set("X") # Making the move
                Update_Display() # Updates the turn tracker
            else: # It's the second player's turn
                sound.PlaySound("Jab.wav", 1) # Sound effects for fun
                Gameboard_Text[0].set("O") # Making the move
                Update_Display() # Updates the turn tracker
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True: # Checks if the user has enabled the AI
                if Turn_Tracker.get() == "O's Turn": # Checks if the AI made the bad move
                    AI_Turn() # Has the computer guess again
                else: # The player made the bad guess
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else: # The player has not enabled the AI
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
    
    # The player selected the North button
    elif arg == 2:
        if Gameboard_Text[1].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[1].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[1].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the North-East button
    elif arg == 3:
        if Gameboard_Text[2].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[2].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[2].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the West button
    elif arg == 4:
        if Gameboard_Text[3].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[3].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[3].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the Center button
    elif arg == 5:
        if Gameboard_Text[4].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[4].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[4].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the East button
    elif arg == 6:
        if Gameboard_Text[5].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[5].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[5].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the South-West button
    elif arg == 7:
        if Gameboard_Text[6].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[6].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[6].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the South button
    elif arg == 8:
        if Gameboard_Text[7].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[7].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[7].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

    # The player selected the South-East button
    elif arg == 9:
        if Gameboard_Text[8].get() == "":
            if Turn_Tracker.get() == "X's Turn":
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[8].set("X")
                Update_Display()
            else:
                sound.PlaySound("Jab.wav", 1)
                Gameboard_Text[8].set("O")
                Update_Display()
        else: # Executes if someone has already played on the selected space
            if Singleplayer == True:
                if Turn_Tracker.get() == "O's Turn":
                    AI_Turn()
                else:
                    sound.PlaySound("A-Tone.wav", 1) # Error sound
                    messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")
            else:
                sound.PlaySound("A-Tone.wav", 1) # Error sound
                messagebox.showerror(title="ERROR", message="You cannot play on a space that has already been played on.")

### Resets the gameboard and the turn tracker
def Reset_Game():

    global Game_Over

    sound.PlaySound("Gong.wav", 1)

    Turn_Tracker.set("X's Turn")
    for var in Gameboard_Text:
        var.set("")

    Game_Over = False

### Pop up window that prompts the user to select either singleplayer or multiplayer
def Choose_Mode():

    global Mode

    Mode = tk.Tk()
    Mode.title("Choose A Mode")

    Selection = tk.Frame(Mode, height="200", width="400")
    Selection.pack(expand="true", fill="both")

    Single_Button = HoverButton(Selection, bg="dark red", font=Text_Font, text="Singleplayer",
    command=lambda:Mode_Select(1))
    Single_Button.place(relwidth="0.5", relheight="1")

    Multi_Button = HoverButton(Selection, bg="dark red", font=Text_Font, text="Multiplayer",
    command=lambda:Mode_Select(2))
    Multi_Button.place(relx="0.5", relwidth="0.5", relheight="1")

    Window.lower() # Fixes a graphical bug where the Mode window was hidden by a partially created game Window

    Mode.mainloop()

### Logic that enables the AI if selected
def Mode_Select(arg):

    global Singleplayer

    if arg == 1:
        Mode.quit()
        Singleplayer = True
    elif arg == 2:
        Mode.quit()

### The AI makes a move based on set conditions
def AI_Turn():

    global Singleplayer

    if Singleplayer == True: # This code only executes if singleplayer is enabled

        # Generating a random move for the computer to be used as a failsafe
        Computer_Move = random.randint(1,9)

        print(Computer_Move)

        if Turn_Tracker.get() == "O's Turn": # Makes sure that it's the computer's turn
            # Blocks player's horizontal attempts to win on the first row
            if Gameboard_Text[0].get() == "X" and Gameboard_Text[1].get() == "X" and Gameboard_Text[2].get() == "":
                Update_Grid(3)
            elif Gameboard_Text[1].get() == "X" and Gameboard_Text[2].get() == "X" and Gameboard_Text[0].get() == "":
                Update_Grid(1)
            elif Gameboard_Text[0].get() == "X" and Gameboard_Text[2].get() == "X" and Gameboard_Text[1].get() == "":
                Update_Grid(2)

            # Blocks player's horizontal attempts to win on the second row
            elif Gameboard_Text[3].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[5].get() == "":
                Update_Grid(6)
            elif Gameboard_Text[3].get() == "X" and Gameboard_Text[5].get() == "X" and Gameboard_Text[4].get() == "":
                Update_Grid(5)
            elif Gameboard_Text[4].get() == "X" and Gameboard_Text[5].get() == "X" and Gameboard_Text[3].get() == "":
                Update_Grid(4)

            # Blocks player's horizontal attempts to win on the third row
            elif Gameboard_Text[6].get() == "X" and Gameboard_Text[7].get() == "X" and Gameboard_Text[8].get() == "":
                Update_Grid(9)
            elif Gameboard_Text[6].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[7].get() == "":
                Update_Grid(8)
            elif Gameboard_Text[7].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[6].get() == "":
                Update_Grid(7)

            # Blocks player's vertical attempts to win on the first column
            elif Gameboard_Text[0].get() == "X" and Gameboard_Text[3].get() == "X" and Gameboard_Text[6].get() == "":
                Update_Grid(7)
            elif Gameboard_Text[0].get() == "X" and Gameboard_Text[6].get() == "X" and Gameboard_Text[3].get() == "":
                Update_Grid(4)
            elif Gameboard_Text[3].get() == "X" and Gameboard_Text[6].get() == "X" and Gameboard_Text[0].get() == "":
                Update_Grid(1)

            # Blocks player's vertical attempts to win on the second column
            elif Gameboard_Text[1].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[7].get() == "":
                Update_Grid(8)
            elif Gameboard_Text[1].get() == "X" and Gameboard_Text[7].get() == "X" and Gameboard_Text[4].get() == "":
                Update_Grid(5)
            elif Gameboard_Text[4].get() == "X" and Gameboard_Text[7].get() == "X" and Gameboard_Text[1].get() == "":
                Update_Grid(2)

            # Blocks player's vertical attempts to win on the third column
            elif Gameboard_Text[2].get() == "X" and Gameboard_Text[5].get() == "X" and Gameboard_Text[8].get() == "":
                Update_Grid(9)
            elif Gameboard_Text[2].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[5].get() == "":
                Update_Grid(6)
            elif Gameboard_Text[5].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[2].get() == "":
                Update_Grid(3)

            # Blocks the player's attempts to win diagonally in a positive x direction and a negative y direction
            elif Gameboard_Text[0].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[8].get() == "":
                Update_Grid(9)
            elif Gameboard_Text[0].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[4].get() == "":
                Update_Grid(5)
            elif Gameboard_Text[4].get() == "X" and Gameboard_Text[8].get() == "X" and Gameboard_Text[0].get() == "":
                Update_Grid(1)

            # Blocks the player's attempts to win diagonally in a negative x direction and a positive y direction
            elif Gameboard_Text[2].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[6].get() == "":
                Update_Grid(7)
            elif Gameboard_Text[2].get() == "X" and Gameboard_Text[6].get() == "X" and Gameboard_Text[4].get() == "":
                Update_Grid(5)
            elif Gameboard_Text[4].get() == "X" and Gameboard_Text[6].get() == "X" and Gameboard_Text[2].get() == "":
                Update_Grid(3)

            # If no conditions are met then the computer makes a random move
            else:
                Update_Grid(Computer_Move)

### Checks if someone has won the game
def Check_Win():

    global Game_Over

    # All possible combinations of X winning
    if Gameboard_Text[0].get() == "X" and Gameboard_Text[1].get() == "X" and Gameboard_Text[2].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[3].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[5].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[6].get() == "X" and Gameboard_Text[7].get() == "X" and Gameboard_Text[8].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[0].get() == "X" and Gameboard_Text[3].get() == "X" and Gameboard_Text[6].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[1].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[7].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[2].get() == "X" and Gameboard_Text[5].get() == "X" and Gameboard_Text[8].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[0].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[8].get() == "X":
        Game_Over = True
        Win_Message(1)
    elif Gameboard_Text[2].get() == "X" and Gameboard_Text[4].get() == "X" and Gameboard_Text[6].get() == "X":
        Game_Over = True
        Win_Message(1)

    # All possible combinations of O winning
    if Gameboard_Text[0].get() == "O" and Gameboard_Text[1].get() == "O" and Gameboard_Text[2].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[3].get() == "O" and Gameboard_Text[4].get() == "O" and Gameboard_Text[5].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[6].get() == "O" and Gameboard_Text[7].get() == "O" and Gameboard_Text[8].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[0].get() == "O" and Gameboard_Text[3].get() == "O" and Gameboard_Text[6].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[1].get() == "O" and Gameboard_Text[4].get() == "O" and Gameboard_Text[7].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[2].get() == "O" and Gameboard_Text[5].get() == "O" and Gameboard_Text[8].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[0].get() == "O" and Gameboard_Text[4].get() == "O" and Gameboard_Text[8].get() == "O":
        Game_Over = True
        Win_Message(2)
    elif Gameboard_Text[2].get() == "O" and Gameboard_Text[4].get() == "O" and Gameboard_Text[6].get() == "O":
        Game_Over = True
        Win_Message(2)

    # Executes if there is a tie
    if (
        Gameboard_Text[0].get() != "" and
        Gameboard_Text[1].get() != "" and
        Gameboard_Text[2].get() != "" and
        Gameboard_Text[3].get() != "" and
        Gameboard_Text[4].get() != "" and
        Gameboard_Text[5].get() != "" and
        Gameboard_Text[6].get() != "" and
        Gameboard_Text[7].get() != "" and
        Gameboard_Text[8].get() != ""
       ):
        Game_Over = True
        Win_Message(3)

    # Prevents a recursion error when the user quits the game
    if Game_Over == False:
        AI_Turn()

### Displays a message congratulating the winner and asking the user if they would like to play again
def Win_Message(arg):

    global Win_Box

    if arg == 1:
        sound.PlaySound("Kung-Fu-Yell.wav", 1)
        messagebox.showinfo(message="X's Win!!!")
    elif arg == 2:
        sound.PlaySound("Karate-Yell.wav", 1)
        messagebox.showinfo(message="O's Win!!!")
    elif arg == 3:
        sound.PlaySound("Cat-Scream.wav", 1)
        messagebox.showinfo(message="Cat Wins!!!")

    Win_Box = tk.Tk()
    Win_Box.title("GAME OVER")

    Choice = tk.Frame(Win_Box, height="200", width="400")
    Choice.pack(expand="true", fill="both")

    Quit_Button = HoverButton(Choice, bg="dark red", font=Text_Font, text="Quit",
    command=lambda:[Window.destroy(), Win_Box.destroy()])
    Quit_Button.place(relwidth="0.5", relheight="1")

    Continue_Button = HoverButton(Choice, bg="dark red", font=Text_Font, text="Play Again",
    command=lambda:[Reset_Game(), Win_Box.destroy()])
    Continue_Button.place(relx="0.5", relwidth="0.5", relheight="1")

    Win_Box.mainloop()

########################################################### PROGRAM FLOW ################################################################

# This code fixes the blurry text that tkinter has when being used on Windows. I got this solution from Stack Overflow:
# https://stackoverflow.com/questions/36514158/tkinter-output-blurry-for-icon-and-text-python-2-7/43033405
if __name__ == "__main__":   
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

Choose_Mode() # Prompts the user to choose whether to play in single player or multiplayer.

Init_GUI() # Initiating the static GUI elements
Active_GUI() # Initiating the active GUI elements

sound.PlaySound("Gong.wav", 1)

Mode.destroy() # Closes the select a mode window

Window.lift() # Brings the game window to the front of the screen

# Looping in the main window to accept User input
Window.mainloop()