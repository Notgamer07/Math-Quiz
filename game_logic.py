import random as r

class GameLogic:
    def __init__(self):
        self.correct_answer = None
        self.total_questions = 0
        self.correct_count = 0

    def generate_question(self):
        a, b, c = r.randint(1, 9), r.randint(1, 20), r.randint(-9, 90)
        correct_answer = (c - b) / a
        question = f'{a}x + {b} = {c}'
        
        options = [correct_answer]
        while len(options) < 4:
            wrong_option = correct_answer + r.uniform(-10, 10)
            if round(wrong_option, 2) not in [round(o, 2) for o in options]:
                options.append(wrong_option)
        
        r.shuffle(options)
        self.correct_answer = round(correct_answer, 2)
        self.total_questions += 1
        
        return question, options, self.correct_answer

    def check_answer(self, selected):
        is_correct = round(selected, 2) == self.correct_answer
        if is_correct:
            self.correct_count += 1
        return is_correct
