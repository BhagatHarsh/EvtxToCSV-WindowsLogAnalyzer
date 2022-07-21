import os
import tkinter as tk
# python imaging library(PIL) to process images for buttons and backgrounds of windows
from PIL import ImageTk, Image

def homeScreen():
    root = tk.Tk()
    heightWindow = root.winfo_screenheight()
    widthWindow = root.winfo_screenwidth()
    # here +0+0 specifies the window must be placed at the origin of the screen
    strForGeometry = str(850) + "x" + str(600) + "+-10+0"
    # setting the size of the calculator window
    root.geometry(strForGeometry)

    # to change the title of your window you can use title function
    root.title("Windows Log Analyzer")

    im = Image.open(os.path.join(os.getcwd(),'homepage.jpeg'))
    im = im.resize((850,500), Image.ANTIALIAS)
    ph = ImageTk.PhotoImage(im)

    frame1 = tk.LabelFrame(root, bg="#050a30",
                        width=widthWindow, height=heightWindow)
    frame1.pack(pady=5, padx=5)
    mainBackGroundImg = tk.Label(frame1, image=ph)
    mainBackGroundImg.place(anchor=tk.CENTER,width=widthWindow,y = 50,
                                height=heightWindow, rely=0.5, relx=0.5)
    TitleLabel = tk.Label(frame1,
                        text="""
                        
Welcome to windows 
log analyzer system
                            """,
                        width=50, height=5, font=("BankGothic Md BT ", 20, "bold"), bg="#cae8ff", fg="#1f15ad")
    TitleLabel.place(y=-250,rely=0.5, relx=0.5, anchor=tk.CENTER)
    # Button for closing
    exit_button = tk.Button(root, text="Proceed", command=root.destroy,font=("Modern No.", 20, "bold"))
    exit_button.place(x=270,y=250,rely=0.5, relx=0.5, anchor=tk.CENTER)
    root.mainloop()
# homeScreen()

