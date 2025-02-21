from tkinter import Tk, Frame, Label, Button, StringVar, CENTER, NORMAL, DISABLED, RAISED
from database import Database
from game_logic import GameLogic

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x600")
        self.root.title("Math Game")
        self.root.configure(bg="lightblue")

        self.db = Database("data.csv")
        self.logic = GameLogic()
        self.time_left = 20

        self.text = StringVar(value="Question will appear here")
        self.sam1 = StringVar(value="START")
        self.timer_text = StringVar(value=f"Time Left: {self.time_left}s")
        self.score_text = StringVar(value="Score: 0/0")

        self.setup_ui()

    def setup_ui(self):
        self.frame = Frame(self.root, bg="lightblue", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(self.frame, text="MATH QUIZ", fg="white", bg="black", font=("Old English Text", 20), padx=10, pady=10).grid(row=0, column=0, columnspan=2, pady=10)

        self.timer_label = Label(self.frame, textvariable=self.timer_text, font=("Arial", 14, "bold"), bg="lightblue", fg="red")
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=10)

        Label(self.frame, textvariable=self.text, font=("Arial", 14), bg="lightblue").grid(row=2, column=0, columnspan=2, pady=20)

        self.score_label = Label(self.frame, textvariable=self.score_text, font=("Arial", 12, "bold"), bg="lightblue")
        self.score_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.start_button = Button(self.frame, textvariable=self.sam1, padx=20, font=("Arial", 14), bg="green", fg="white", relief=RAISED, bd=5, command=self.start_game)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

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
            btn.grid(row=5 + i, column=0, columnspan=2, pady=5)
            self.option_buttons.append(btn)

    def add_question(self):
        question, options, self.correct_answer = self.logic.generate_question()
        self.options_list = options  # Store options list
        self.text.set(f"Solve: {question}")

        for i, option in enumerate(options):
            self.option_buttons[i].config(
            text=round(option, 2),
            command=lambda btn=self.option_buttons[i], opt=option: self.check_answer(btn, opt),
            bg="white",
            state=NORMAL
        )

    def check_answer(self, button, selected):
        is_correct = self.logic.check_answer(selected)
        button.config(bg="green" if is_correct else "red")

        if not is_correct:
            for btn, opt in zip(self.option_buttons, self.options_list):  # Now options_list is defined
                if round(opt, 2) == round(self.correct_answer, 2):
                    btn.config(bg="green")

        self.db.store_answer(round(selected, 2), "Correct" if is_correct else "Incorrect")
        self.update_score()
        self.root.after(190, self.add_question)

    def skip_question(self):
        self.db.mark_skipped()
        self.update_score()
        self.add_question()

    def update_score(self):
        self.score_text.set(f"Score: {self.logic.correct_count}/{self.logic.total_questions}")

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
        self.text.set(f"Game Over! Final Score: {self.logic.correct_count}/{self.logic.total_questions}")
