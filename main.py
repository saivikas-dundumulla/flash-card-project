import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
flip_timer = None
current_card = {}
#===================== FUNCTIONALITY ================#
try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("data/french_words.csv")
data = df.to_dict(orient="records")
print(len(data))

def next_card():
    global current_card, flip_timer
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    current_card = random.choice(data)
    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card.get("French"), fill="black")
    flip_timer = window.after(3000, flip_card)

def right_choice():
    data.remove(current_card)
    print(len(data))
    data_frame = pandas.DataFrame(data)
    data_frame.to_csv(path_or_buf="data/words_to_learn.csv", index=False)
    next_card()

def wrong_choice():
    next_card()

def flip_card():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card.get("English"), fill="white")

#=================== UI SETUP =======================#
window = Tk()
window.config(background=BACKGROUND_COLOR, pady=40, padx=40)
window.title("Flashy")

front_img = PhotoImage(file="images/card_front.png")
back_img = PhotoImage(file="images/card_back.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=False)
canvas_image = canvas.create_image(400, 263, image=front_img)
title_text = canvas.create_text(400, 150, text="", font=("Courier", 28, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 32, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, command=right_choice)
right_btn.grid(row=1, column=0)

wrong_img = PhotoImage(file="images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=wrong_choice)
wrong_btn.grid(row=1, column=1)

next_card()

window.mainloop()

