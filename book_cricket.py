# ----------------------------------------------------- Imports --------------------------------------------------------
from tkinter import *
from tkinter import messagebox, ttk
from scoreboard import Scoreboarde
from PIL import Image, ImageTk
# ------------------------------------------------ Global Variables ----------------------------------------------------
width = 800
height = 600

main_bg = "white"
gray_out_bg = "#cdcdcd"
# --------------------------------------------------- Main Class -------------------------------------------------------
class BookCricket:
    def __init__(self):

        self.windows = Tk()
        self.windows.title("MOCS")
        self.windows.minsize(width,height)
        self.windows.resizable(False, False)
        self.windows.config(bg=main_bg)

        # Variables
        self.teamA = {}
        self.teamB = {}
        self.match_overs = None

        self.main_image = Image.open("images/main.jpg")
        aspect_ratio = self.main_image.height / self.main_image.width
        widther = 500
        self.main_image = self.main_image.resize((widther, int(widther * aspect_ratio)))
        self.main_image = ImageTk.PhotoImage(self.main_image)

        self.main_image_label = Label(self.windows, image=self.main_image, font=("arial", 40, "bold"), justify=CENTER,
                                bg=main_bg, fg="white")
        self.main_image_label.place(relx=0, rely=0.5, anchor=W)

        self.main_label = Label(self.windows, text="My Own\nCricket\nSimulator", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=main_bg, fg="green")
        self.main_label.place(relx=0.8, rely=0.4, anchor=CENTER)

        self.score_button = Button(self.windows, text="Play!!", width=10, command=self.open_details_form, bg="#6dbd25",
                                   fg='white', activebackground="#6dbd25", font=("arial", 16, "bold"), height=2,
                                   relief=FLAT, activeforeground="white")
        self.score_button.place(relx=0.8, rely=0.75, anchor=CENTER)

        self.windows.mainloop()

# ---------------------------------------------------- Methods ---------------------------------------------------------
# -------------------------------------------- Open Match Details Form -------------------------------------------------
    def open_details_form(self):
        scoreboard_window = Scoreboarde(self)
        self.windows.withdraw()
# -------------------------------------------------- Run Program -------------------------------------------------------
if __name__ == "__main__":
    BookCricket()
