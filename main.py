from tkinter import *
from PIL import Image, ImageTk
from main_menu import Main_menu
from game import Game
import cv2
import numpy as np
from pygame import mixer
# ============= Parameters =============

def create_main_win(w, h):
    # Simply initiates main window
    root = Tk()
    root.title("Don Simon's Quiz")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    return root

# Window dimensions 
window_width = 1920
window_height = 1080

# Pictures path
pictures_path = r"C:\Users\martook\Desktop\q_game\pics\\"

# Application icon
icon = Image.open(pictures_path + "billy.jpg")

# Initializing root and and canvas
root = create_main_win(window_width, window_height)
canvas = Canvas(root, width=window_width, height=window_height)
canvas.place(x=0, y=0)

##########################################################

file="C:\\Users\\martook\\Desktop\\q_game\\intro.mp4"

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(file)
  
# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")
  
# Read until video is completed
mixer.init()
mixer.music.load("C:\\Users\\martook\\Desktop\\intro.mp3")
mixer.music.play()
while(cap.isOpened()):
      
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    # Display the resulting frame
        cv2.imshow('Frame', frame)
          
    # Press Q on keyboard to exit
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
  
# Break the loop
    else:
        break
  
# When everything done, release
# the video capture object
cap.release()
  
# Closes all the frames
cv2.destroyAllWindows()

##########################################################

icon = ImageTk.PhotoImage(icon)
root.wm_iconphoto(True, icon)
game = Game(root, canvas, pictures_path)
main_menu = Main_menu(root, canvas, window_height, window_width, pictures_path, game)


root.mainloop()
