from tkinter import *


class Main():
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1530x790+0+0")
        #self.root.overrideredirect(True)
        self.root.iconbitmap("images/favicon (2).ico")
        self.root.mainloop()
        
        

if __name__ == '__main__':
     Main()