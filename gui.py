from tkinter import *
import random as r
from database import Database

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Math Game")
        self.root.configure(bg="lightblue")

        self.db = Database("data.csv")
        self.time_left = 20
        self.count = 0
        self.total = 0
        self.correct_answer = None

        self.text = StringVar(value="Question will appear here")
        self.sam1 = StringVar(value="START")
        self.timer_text = StringVar(value=f"Time Left: {self.time_left}s")

        self.setup_ui()

    def setup_ui(self):
        self.frame = Frame(self.root, bg="lightblue", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text="MATH QUIZ", fg="white", bg="black", font=("Old English Text", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2, pady=10)

        self.timer_label = Label(self.frame, textvariable=self.timer_text, font=("Arial", 14, "bold"), bg="lightblue", fg="red")
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=10)

        Label(self.frame, textvariable=self.text, font=("Arial", 14), bg="lightblue").grid(row=2, column=0, columnspan=2, pady=20)

        self.start_button = Button(self.frame, textvariable=self.sam1, padx=20, font=("Arial", 14), bg="green", fg="white", relief=RAISED, bd=5, command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

    def start_game(self):
        self.sam1.set("SKIP")
        self.start_button.config(command=self.skip_question)
        self.create_options()
        self.add_question()
        self.update_timer(self.time_left)

    def create_options(self):
        self.option_buttons = []
        for i in range(4):
            btn = Button(self.frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
            btn.grid(row=4 + i, column=0, columnspan=2, pady=5)
            self.option_buttons.append(btn)

    def generate_question(self):
        a, b, c = r.randint(1, 9), r.randint(1, 20), r.randint(-9, 90)
        correct_answer = (c - b) / a
        question = f'{a}x + {b} = {c}'
        options = [correct_answer] + [correct_answer + r.uniform(-10, 10) for _ in range(3)]
        r.shuffle(options)
        self.db.store_question(question, round(correct_answer, 2))
        return question, options, correct_answer

    def add_question(self):
        self.equation, self.options_list, self.correct_answer = self.generate_question()
        self.text.set(f"Solve: {self.equation}")

        for i, option in enumerate(self.options_list):
            self.option_buttons[i].config(
                text=round(option, 2),
                command=lambda btn=self.option_buttons[i], opt=option: self.check_answer(btn, opt),
                bg="white",
                state=NORMAL
            )

    def skip_question(self):
        self.db.mark_skipped()
        self.add_question()

    def check_answer(self, button, selected):
        is_correct = round(selected, 2) == round(self.correct_answer, 2)
        button.config(bg="green" if is_correct else "red")
        self.db.store_answer(round(selected, 2), "Correct" if is_correct else "Incorrect")

        if not is_correct:
            for btn, opt in zip(self.option_buttons, self.options_list):
                if round(opt, 2) == round(self.correct_answer, 2):
                    btn.config(bg="green")

        self.root.after(190, self.add_question)

    def update_timer(self, time_left):
        if time_left > 0:
            self.timer_text.set(f"Time Left: {time_left}s")
            self.root.after(1000, self.update_timer, time_left - 1)
        else:
            self.timer_text.set("Time's Up!")
            self.disable_game()

    def disable_game(self):
        for btn in self.option_buttons:
            btn.config(state=DISABLED)
        self.start_button.config(command=self.root.quit)
        self.db.save_to_csv()
