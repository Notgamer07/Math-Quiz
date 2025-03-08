import random as r

class GameLogic:
    def __init__(self):
        self.correct_answer = None
        self.total_questions = 0
        self.correct_count = 0
        self.selected_difficulty = None
    
    def set_difficulty(self,value):
        self.selected_difficulty = value
    
    def choose_generator(self):
        if(self.selected_difficulty == 0):
            self.generate_question(self)
        elif(self.selected_difficulty == 1):
            self.generate_polynomial(self)
    
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
    
    def generate_polynomial(self):
        import math as m
        max_attempts=100
        for i in max_attempts:
            a=r.randint(1,10)
            b=r.randint(-10,10)
            c=r.randint(-5,5)
            di=(b**2) - (4*a*c)
            if di>=0:
                break
        question=f"{a}x² + {b}x + {c} = 0"
        root1=(-b + m.sqrt(di))/(2*a)
        root2=(-b - m.sqrt(di))/(2*a)
        correct_answer=(round(root1,2),(round(root2,2)))
        options={correct_answer}
        while len(options)<4:
            w_root1=root1 + r.uniform(-5,5)
            w_root2=r.uniform(root1,root2)
            wrong_option=(round(w_root1,2),round(w_root2,2))
            options.add(wrong_option)
        options=list(options)
        r.shuffle(options)
        return question,options,correct_answer

    def check_answer(self, selected):
        is_correct = round(selected, 2) == self.correct_answer
        if is_correct:
            self.correct_count += 1
        return is_correct
