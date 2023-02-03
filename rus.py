import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import itertools
from random import randint
from time import sleep
from os import system
import os
import sys

window = tk.Tk()
window.title('Rus')
window.geometry('640x360+0+0')

# image compilation
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
# win animation
display = tk.Label(window)
filename = resource_path('./win.webp')
pil_image = Image.open(filename)
no_of_frames = pil_image.n_frames

# Get frame duration, assuming all frame durations are the same
duration = pil_image.info.get('duration', None)   # None for WEBP
if duration is None:
    with open(filename, 'rb') as binfile:
        data = binfile.read()
    pos = data.find(b'ANMF')    # Extract duration for WEBP sequences
    duration = int.from_bytes(data[pos+12:pos+15], byteorder='big')

# Create an infinite cycle of PIL ImageTk images for display on label
frame_list = []
for frame in ImageSequence.Iterator(pil_image):
    cp = frame.copy()
    frame_list.append(cp)
tkframe_list = [ImageTk.PhotoImage(image=fr) for fr in frame_list]
tkframe_sequence = itertools.cycle(tkframe_list)
tkframe_iterator = iter(tkframe_list)

def show_animation():
    global after_id
    after_id = window.after(duration, show_animation)
    img = next(tkframe_sequence)
    display.config(image=img)

def stop_animation(*event):
    window.after_cancel(after_id)
    window.destroy()

def run_animation_once():
    global after_id
    after_id = window.after(duration, run_animation_once)
    try:
        img = next(tkframe_iterator)
    except StopIteration:
        stop_animation()
    else:
        display.config(image=img)


cyrillic = [
    ['А а', ('a'), '"a" in father', 0],
    ['Б б', ('b'), '"b" in bad', 0],
    ['В в', ('v'), '"v" in video', 0],
    ['Г г', ('g'), '"g" in go or "g" in gamma', 0],
    ['Д д', ('d'), '"d" in done or "d" in delta', 0],
    ['Е е', ('ye', 'yeh'), '"ye" in yes', 0],
    ['Ё ё', ('yo', 'yoh'), '"yo" in your', 0],
    ['Ж ж', ('zh', 'szh', 'zsh'), '"s" in pleasure', 0],
    ['З з', ('z'), '"z" in zebra', 0],
    ['И и', ('i', 'ee'), '"ee" in see', 0],
    ['Й й', ('y', 'i'), '"y" in boy/may or "y" in yellow', 0],
    ['К к', ('k'), '"k" in key', 0],
    ['Л л', ('l'), '"l" in leave or "l" in lambda', 0],
    ['М м', ('m'), '"m" in mother', 0],
    ['Н н', ('n'), '"n" in nose', 0],
    ['О о', ('o'), '"o" in more', 0],
    ['П п', ('p'), '"p" in sport or "p" in pi', 0],
    ['Р р', ('r', 'rr'), '"rr" in perro (rolled r)', 0],
    ['С с', ('s'), '"s" in stoned', 0],
    ['Т т', ('t'), '"t" in touch', 0],
    ['У у', ('u', 'oo'), '"oo" in cartoon', 0],
    ['Ф ф', ('f', 'ph'), '"f" in face or "ph" in phi', 0],
    ['Х х', ('kh', 'h', 'ch'), '"h" in house or "ch" in loch', 0],
    ['Ц ц', ('ts', 'tsu'), '"ts" in sits or Japanese つ・ツ・ｔｓｕ', 0],
    ['Ч ч', ('ch', 'chuh'), '"ch" in Chernobyl or Chernarus', 0],
    ['Ш ш', ('sh', 'hard'), '"sh" in share (hard)', 0],
    ['Щ щ', ('sh', 'soft'), '"sh" in sheep (soft)', 0],
    ['Ы ы', ('i', 'y', 'e'), '"e" in roses or "i" in ill', 0],
    ['Э э', ('e', 'eh'), '"e" in bet', 0],
    ['Ю ю', ('yu', 'yoo'), '"u" in use or "Yu" in Yugoslavia', 0],
    ['Я я', ('ya', 'yah'), '"ya" in yard', 0],
    ['Ь', ('soft', 'soften', 'n/a'), "No sound. Used to soften letter before it", 0],
    ['Ъ', ('hard', 'harden', 'n/a'), "No sound. Used to harden letter before it.\n Rarely used since 1918", 0]
]

num_correct = 0
num_incorrect = 0
summary = []
nextcard = False
finished = False

i = randint(0, len(cyrillic) - 1)

parent = tk.Frame(window)
parent.pack(pady=50, padx=32)

final_parent = tk.Frame(window)

canvas = tk.Canvas(final_parent)
scrollbar = tk.Scrollbar(final_parent, orient = 'vertical', command=canvas.yview)
scrollable_frame = tk.Frame(canvas)
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=scrollable_frame,anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
info = tk.Label(parent, text = "Correct: " + str(num_correct) + " Incorrect: " + str(num_incorrect) + " Remaining: " + str(len(cyrillic)), font = ('arial', 16))
info.pack()

letters = tk.Label(parent, text = cyrillic[i][0], font = ('arial', 42))
letters.pack(pady = 16, padx = 32)

you_guessed = tk.Label(parent, text = '', font = ('arial', 16))

like = tk.Label(parent, text = '', font = ('arial', 16))

answertext = tk.Label(parent, text = '', font = ('arial', 16))

entry = tk.Entry(parent)
entry.insert(0, 'Type guess here...')
entry.pack()


enter = tk.Label(parent, text = '', font = ('arial', 16, 'bold'))

def click(*args):
    entry.delete(0, 'end')

entry.bind("<Button-1>", click)

def submit(e):
    global num_correct
    global num_incorrect
    global summary
    global i
    global nextcard
    if nextcard:
        enter.pack_forget()
        like.pack_forget()
        answertext.pack_forget()
        you_guessed.pack_forget()
        entry.delete(0, 'end')
        if finished:
            window.destroy()
            return
        if len(cyrillic) > 0:
            i = randint(0, len(cyrillic) - 1)
            letters.configure(text = cyrillic[i][0])
            entry.pack()
            nextcard = False
        else:
            show_summary()
    else:
        guess = entry.get()
        answer_str = ''
        if guess == '' or guess == None:
            return
        entry.delete(0, 'end')
        correct = False
        correcttext = ''
        correctcolor = ''
        guess = guess.lower()
        for answer in cyrillic[i][1]:
            answer_str += '"' + answer + '" '
            if guess == answer:
                correct = True
        answer_str = answer_str.replace(' ', ', ')
        answer_str = answer_str[0:-2]
        if correct:
            correcttext = " is correct!"
            correctcolor = '#078C66'
        else:
            correcttext = " is incorrect!"
            correctcolor = '#D91818'
        you_guessed.configure(text = guess + correcttext, fg = correctcolor)
        you_guessed.pack()
        like.configure(text = "Pronunciation: " + cyrillic[i][2] + ".")
        like.pack()
        if correct:
            num_correct += 1
            summary.append(cyrillic[i])
            del cyrillic[i]
        else:
            cyrillic[i][3] += 1
            num_incorrect += 1
            ans = "answer: "
            if len(cyrillic[i][1]) > 1:
                ans = "answers: "
            answertext.configure(text = 'Correct ' + ans + answer_str)
            answertext.pack()
        info.configure(text = "Correct: " + str(num_correct) + " Incorrect: " + str(num_incorrect) + " Remaining: " + str(len(cyrillic)))
        entry.pack_forget()
        enter.configure(text = "Press Enter key to continue...")
        enter.pack(pady=16)
        nextcard = True



def show_summary():
    global summary
    global finished
    global num_incorrect
    letters.pack_forget()
    summary_text = ''
    summary.sort(key=lambda x: x[3], reverse=True)
    all_correct = True
    for row in summary:
        if row[3] > 0:
            all_correct = False
            summary_text += row[0] + ": incorrect " + str(row[3]) + " times.\n"
    if num_incorrect in range(70, 100):
        summary_text += "\nGotta start somewhere."
    elif num_incorrect == 69:
        summary_text += "\nFormerly Chuck's."
    elif num_incorrect in range(41, 68):
        summary_text += "\nDon't lose faith."
    elif num_incorrect in range(31, 40):
        summary_text += "\nKeep practicing."
    elif num_incorrect in range(21, 30):
        summary_text += "\nYou can do it!"
    elif num_incorrect in range(11, 20):
        summary_text += "\nGetting there!"
    elif num_incorrect in range(6, 10):
        summary_text += "\nKeep it up!"
    elif num_incorrect in range(2, 5):
        summary_text += "\nJust a little more practice!"
    elif num_incorrect == 1:
        summary_text += "\nSo close!!"

    info.pack_forget()
    parent.pack_forget()
    if all_correct:
        window.configure(background='#028104')
        display.pack()
        window.after(1000, run_animation_once)
    else:
        final_parent.pack()
        final_info = tk.Label(scrollable_frame, text = "Correct: " + str(num_correct) + " Incorrect: " + str(num_incorrect), font = ('arial', 16))
        final_info.pack()
        summary_label = tk.Label(scrollable_frame, text = summary_text, font = ('arial', 16))
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        summary_label.pack()
        final_enter = tk.Label(scrollable_frame, text="Press Enter key to close the program...", font = ('arial', 16, 'bold'))
        final_enter.pack(pady=16)
        finished = True

window.bind('<space>', stop_animation)
window.bind('<Return>', submit)

window.mainloop()
