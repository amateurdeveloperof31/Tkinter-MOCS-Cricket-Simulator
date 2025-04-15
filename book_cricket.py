# ----------------------------------------------------- Imports --------------------------------------------------------
from tkinter import *
from scoreboard import Scoreboarde
from image_resizer import ImageResizer
# ------------------------------------------------ Global Variables ----------------------------------------------------
width = 800
height = 600

main_bg = "white"
gray_out_bg = "#cdcdcd"
charcoal_bg = "#36454F"
# --------------------------------------------------- Main Class -------------------------------------------------------
class BookCricket:
    def __init__(self):

        self.windows = Tk()
        self.windows.title("MOCS")
        self.windows.minsize(width,height)
        self.windows.resizable(False, False)
        self.windows.config(bg=charcoal_bg)

        self.main_image = ImageResizer("assets/images/main.png", 500)
        self.main_image_label = Label(self.windows, image=self.main_image.image, bg=charcoal_bg)
        self.main_image_label.place(relx=0, rely=0.5, anchor=W)

        self.main_label = Label(self.windows, text="My Own\nCricket\nSimulator", font=("arial", 40, "bold"), justify=CENTER,
                                    bg=charcoal_bg, fg="#35b690")
        self.main_label.place(relx=0.8, rely=0.4, anchor=CENTER)

        self.start_button_image = ImageResizer("assets/images/start.png", 200)
        self.start_button = Button(self.windows, image=self.start_button_image.image, bg=charcoal_bg,
                                   activebackground=charcoal_bg, command=self.open_details_form, borderwidth=0)
        self.start_button.place(relx=0.8, rely=0.75, anchor=CENTER)

        self.windows.mainloop()

# ---------------------------------------------------- Methods ---------------------------------------------------------
# -------------------------------------------- Open Match Details Form -------------------------------------------------
    def open_details_form(self):
        scoreboard_window = Scoreboarde(self)
        self.windows.withdraw()
# -------------------------------------------------- Run Program -------------------------------------------------------
if __name__ == "__main__":
    BookCricket()
