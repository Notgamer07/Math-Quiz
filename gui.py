from tkinter import Tk, Frame, Label, Button, StringVar, CENTER, NORMAL, DISABLED, RAISED
from database import Database
from game_logic import GameLogic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")  # Increased width to fit timer, quiz, and graph
        self.root.title("Math Game")
        self.root.configure(bg="lightblue")

        self.db = Database()
        self.logic = GameLogic()
        self.time_left = 3

        self.text = StringVar(value="Question will appear here")
        self.sam1 = StringVar(value="START")
        self.timer_text = StringVar(value=f"{self.time_left:02d}:00")  # Digital clock format
        self.score_text = StringVar(value="Score: 0/0")

        self.setup_ui()

    def setup_ui(self):
        # Left Frame for Timer
        self.left_frame = Frame(self.root, bg="black", padx=20, pady=20)
        self.left_frame.pack(side="left", fill="y")
        
        self.timer_label = Label(self.left_frame, textvariable=self.timer_text, font=("Arial", 24, "bold"), bg="black", fg="red")
        self.timer_label.pack(pady=50)
        
        # Center Frame for Quiz
        self.center_frame = Frame(self.root, bg="lightblue", padx=20, pady=20)
        self.center_frame.pack(side="left", fill="both", expand=True)

        Label(self.center_frame, text="MATH QUIZ", fg="white", bg="black", font=("Old English Text", 20), padx=10, pady=10).pack()

        Label(self.center_frame, textvariable=self.text, font=("Arial", 14), bg="lightblue").pack(pady=20)

        self.score_label = Label(self.center_frame, textvariable=self.score_text, font=("Arial", 12, "bold"), bg="lightblue")
        self.score_label.pack(pady=10)

        self.start_button = Button(self.center_frame, textvariable=self.sam1, padx=20, font=("Arial", 14), bg="green", fg="white", relief=RAISED, bd=5, command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        self.sam1.set("SKIP")
        self.start_button.config(command=self.skip_question)
        self.create_options()
        self.add_question()
        self.update_timer(self.time_left)

    def create_options(self):
        self.option_buttons = []
        for i in range(4):
            btn = Button(self.center_frame, padx=50, font=("Arial", 12, "bold"), relief=RAISED, bd=5)
            btn.pack(pady=5)
            self.option_buttons.append(btn)

    def add_question(self):
        question, options, self.correct_answer = self.logic.generate_question()
        self.db.store_question(question, self.correct_answer)
        self.options_list = options
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
            for btn, opt in zip(self.option_buttons, self.options_list):
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
            minutes = time_left // 60
            seconds = time_left % 60
            self.timer_text.set(f"{minutes:02d}:{seconds:02d}")  # Digital clock format
            self.root.after(1000, self.update_timer, time_left - 1)
        else:
            self.timer_text.set("00:00")
            self.disable_game()

    def disable_game(self):
        for btn in self.option_buttons:
            btn.config(state=DISABLED)
        self.start_button.config(command=self.root.quit)
        self.db.save_to_csv()
        self.text.set(f"Game Over! Final Score: {self.logic.correct_count}/{self.logic.total_questions}")

        # ✅ Create the right frame and show the graph only after time runs out
        self.right_frame = Frame(self.root, bg="white", padx=10, pady=10)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.update_graph()

    def update_graph(self):
        df = self.db.read().dropna()
        if df.empty:
            return

        x = range(len(df))
        correct_answers = df['Correct_Answer']
        inputted_answers = df['Inputted_Answer']

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(x, correct_answers, label="Correct Answer", color='g', linestyle='-', marker='o')
        ax.plot(x, inputted_answers, label="Inputted Answer", color='r', linestyle='--', marker='x')
        ax.fill_between(x, correct_answers, inputted_answers, color='gray', alpha=0.3)
        ax.set_xlabel("Question Index")
        ax.set_ylabel("Answer Value")
        ax.set_title("Correct vs Inputted Answer")
        ax.legend()
        ax.grid(True)

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.right_frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()
