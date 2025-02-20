from tkinter import *
import random as r
import pandas as pd
import os

file_path='D:/python/Project/Math Game - Copy/data.csv'
time_left = 20  # timer in seconds
count=0 # count the correct answer
total=0 #count the total questions
data={
        'Questions':[],
        'Correct_Answer':[],
        'Inputted_Answer':[],
        'Result':[]
    }

#Function to save the data in csv file using panda
def save():
    global file_path,data
    while len(data['Inputted_Answer']) < len(data['Questions']):
        data['Inputted_Answer'].append(pd.NA)  # Mark unanswered questions
        data['Result'].append("Skipped")
    # Convert dictionary to DataFrame and save
    df = pd.DataFrame(data)

    # Check if file exists
    if os.path.exists(file_path):
        # Append without headers
        df.to_csv(file_path, mode='a', header=False, index=False, na_rep="NaN")
    else:
        # Write with headers if file doesn't exist
        df.to_csv(file_path, mode='w', header=True, index=False, na_rep="NaN")

    # Clear data dictionary after saving to avoid duplicate entries
    for key in data.keys():
        data[key] = []


# Function to generate a question
def ques():
    global total
    a = r.randint(1, 9)
    b = r.randint(1, 20)
    c = r.randint(-9, 90)
    correct_answer = (c - b) / a
    question = f'{a}x + {b} = {c}'
    options = [correct_answer]
    while len(options) < 4:
        wrong_option = correct_answer + r.uniform(-10, 10)
        if round(wrong_option, 2) not in [round(o, 2) for o in options]:
            options.append(wrong_option)
    r.shuffle(options)
    data['Questions'].append(question)
    data['Correct_Answer'].append(round(correct_answer,2))
    total+=1 #increase 1 everytime a new question is made.
    return question, options, correct_answer

# Function to update the timer
def update_timer(time_left):
    if time_left > 0:
        timer_text.set(f"Time Left: {time_left}s")  # Update Timer Label
        root.after(1000, update_timer, time_left - 1)  # Call function again after 1 second
    else:
        timer_text.set("Time's Up!")  # Display "Time's Up!" when time reaches 0
        disable_options()  # Disable all buttons except "NEXT"


# Function to disable options and change NEXT to QUIT
def disable_options():
    global total,count
    option1.config(state=DISABLED)
    option2.config(state=DISABLED)
    option3.config(state=DISABLED)
    option4.config(state=DISABLED)
    sam1.set(f"Total Question:{total} Correct:{count}")
    Start_button.config(command=quit)
    save()

# Function to add a new question
def add():
    global equation, options_list, correct_answer
    option1.config(bg="white", state=NORMAL)
    option2.config(bg="white", state=NORMAL)
    option3.config(bg="white", state=NORMAL)
    option4.config(bg="white", state=NORMAL)

    equation, options_list, correct_answer = ques()
    text.set(f"Solve: {equation}")
    option1.config(text=round(options_list[0], 2), command=lambda: check_answer(option1, options_list[0]))
    option2.config(text=round(options_list[1], 2), command=lambda: check_answer(option2, options_list[1]))
    option3.config(text=round(options_list[2], 2), command=lambda: check_answer(option3, options_list[2]))
    option4.config(text=round(options_list[3], 2), command=lambda: check_answer(option4, options_list[3]))

#Function to add skip question
def skip():
    data['Inputted_Answer'].append(pd.NA)  # Mark unanswered questions
    data['Result'].append("Skipped")
    add()

# Function to check selected answer
def check_answer(button, selected):
    global count
    if round(selected, 2) == round(correct_answer, 2):
        button.config(bg="green")
        count+=1
        result='Correct'
    else:
        result='Incorrect'
        button.config(bg="red")
        if round(options_list[0], 2) == round(correct_answer, 2):
            option1.config(bg="green")
        elif round(options_list[1], 2) == round(correct_answer, 2):
            option2.config(bg="green")
        elif round(options_list[2], 2) == round(correct_answer, 2):
            option3.config(bg="green")
        elif round(options_list[3], 2) == round(correct_answer, 2):
            option4.config(bg="green")
    data['Result'].append(result)
    data["Inputted_Answer"].append(round(selected,2))
    root.after(190, add)

# Function to create option buttons
def options():
    global option1, option2, option3, option4
    
    option1 = Button(frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
    option1.grid(row=4, column=0, columnspan=2, pady=5)

    option2 = Button(frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
    option2.grid(row=5, column=0, columnspan=2, pady=5)

    option3 = Button(frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
    option3.grid(row=6, column=0, columnspan=2, pady=5)

    option4 = Button(frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
    option4.grid(row=7, column=0, columnspan=2, pady=5)
    
    sam1.set("SKIP")
    Start_button.config(command=skip)
    add()
    update_timer(time_left)  # Start the countdown

# Create main GUI window
root = Tk()
root.geometry("600x600")
root.title("Math Game")
root.configure(bg="lightblue")

# Create a canvas for the background watermark
canvas = Canvas(root, width=600, height=600, bg="lightblue")
canvas.pack(fill="both", expand=True)
canvas.create_text(300, 300, text="MATH GAME", font=("Arial", 50, "bold"), fill="gray", anchor=NW, angle=30, stipple="gray50")

frame = Frame(root, bg="lightblue", padx=20, pady=20)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

Label(frame, text="MATH QUIZ", fg="white", bg="black", font=("Old English Text", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2, pady=10)

text = StringVar()
text.set("Question will appear here")
sam1 = StringVar()
sam1.set("START")

timer_text = StringVar()
timer_text.set(f"Time Left: {time_left}s")  # Initial Timer Text

timer_label = Label(frame, textvariable=timer_text, font=("Arial", 14, "bold"), bg="lightblue", fg="red")
timer_label.grid(row=1, column=0, columnspan=2, pady=10)  # Place inside the frame

Label(frame, textvariable=text, font=("Arial", 14), bg="lightblue").grid(row=2, column=0, columnspan=2, pady=20)

Start_button = Button(frame, textvariable=sam1, padx=20, font=("Arial", 14), bg="green", fg="white", relief=RAISED, bd=5, command=options)
Start_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()