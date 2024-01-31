import threading


from tkinter import *
from MainApp import Main
import customtkinter
from PIL import ImageTk, Image
import time


def resizeImage1(param, size):
    originalImage = Image.open(param)
    newImage = originalImage.resize(size)
    return ImageTk.PhotoImage(newImage)


def resizeImage2(imagePath, imageSize):
    originalImage = Image.open(imagePath)
    resized = originalImage.resize(imageSize)
    return ImageTk.PhotoImage(resized)


def initialize_main_with_delay():
    # Introduce a delay (e.g., 0.5 seconds)
    time.sleep(0.5)

    # Initialize the Main class
    Main()


class BillApp:

    def __init__(self):
        self.window = Tk()
        self.window.geometry("1300x680+20+20")
        # self.image = ImageTk.PhotoImage(file="images2/bg2.jpg")
        # self.bgLabel = customtkinter.CTkLabel(self.window, image=self.image, text='')
        # self.bgLabel.place(x=0, y=0)
        self.size = (1300, 680)
        self.imagePath = resizeImage1("images2/bg2.jpg", self.size)
        self.bgLabel = Label(self.window, image=self.imagePath, text='')
        self.bgLabel.place(x=-3, y=0)

        self.imageSize = (80, 70)
        self.launchImage = resizeImage2("images2/control hide and show.png", self.imageSize)
        self.LaunchingButton = Button(self.window, image=self.launchImage, compound="top", text="Click to \nLaunch",
                                      width=100,
                                      font=("arial", 14), foreground="Dark Cyan")
        self.LaunchingButton.place(x=10, y=10)

        self.imageSize = (80, 75)
        self.customerDetailsImage = resizeImage2("images2/buyer Details.png", self.imageSize)

        self.customerDetailsButton = Button(self.window, image=self.customerDetailsImage, compound="top",
                                            text="Customer\nDetails ",
                                            font=("arial", 14), foreground="Dark Cyan")

        self.customerDetailsButton.place(x=150, y=10)
        self.imageSize = (80, 75)
        self.productDetailsImage = resizeImage2("images2/Details product.png", self.imageSize)

        self.productDetailsButton = Button(self.window, image=self.productDetailsImage, compound="top", text="Product"
                                                                                                             "\nDetails",
                                           font=("arial", 14), foreground="Dark Cyan")
        self.productDetailsButton.place(x=270, y=10)

        self.imageSize = (80, 75)
        self.billImage = resizeImage2("images2/billing.png", self.imageSize)

        self.billingButton = Button(self.window, image=self.billImage, compound="top", text="Billing",
                                    font=("arial", 14), foreground="Dark Cyan", command=self.launch_main)

        def billMethod():
            self.window.destroy()
            return Main()

        self.billingButton.place(x=390, y=10)

        self.window.mainloop()

    def launch_main(self):
        # Close current window
        self.window.destroy()

        # Create a thread to initialize the Main class with a delay
        thread = threading.Thread(target=initialize_main_with_delay)
        thread.start()


if __name__ == '__main__':
    BillApp()
