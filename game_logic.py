import random as r

class GameLogic:
    def __init__(self):
        self.correct_answer = None
        self.total_questions = 0
        self.correct_count = 0
        self.selected_difficulty = None
    
    def set_difficulty(self,value):
        self.selected_difficulty = value
    
    def generator(self):
        if(self.selected_difficulty == 0):
            return self.generate_question
        elif(self.selected_difficulty == 1):
            return self.generate_polynomial
        else:
            return self.generate_question
    
    def generate_question(self):
        a, b, c = r.randint(1, 9), r.randint(-20, 20), r.randint(-9, 90)
        correct_answer = round((c - b) / a ,2) 
        question = f'''{a}x {'+' if b>=0 else '-'} {abs(b)} = {c}'''
        
        options = [correct_answer]
        while len(options) < 4:
            wrong_option = round(correct_answer + r.uniform(-10, 10),2)
            if wrong_option not in [o for o in options]:
                options.append(wrong_option)
        
        r.shuffle(options)
        self.correct_answer = round(correct_answer, 2)
        self.total_questions += 1
        
        return question, options, self.correct_answer
    
    def generate_polynomial(self):
        import math as m
        max_attempts=100
        for i in range(max_attempts):
            a=r.randint(1,10)
            b=r.randint(-10,10)
            c=r.randint(-5,5)
            di=(b**2) - (4*a*c)
            if di>=0:
                break
        question=f'''{a}x² {'+' if b>=0 else '-'} {abs(b)}x {'+' if b>=0 else '-'} {abs(c)} = 0'''
        root1=round((-b + m.sqrt(di))/(2*a),2)
        root2=round((-b - m.sqrt(di))/(2*a),2)
        self.correct_ans=(root1, root2)
        options=[root1 , root2]
        while len(options)<4:
            w_root1=root1 + r.uniform(-5,5)
            w_root2=r.uniform(root1,root2)
            options.append(round(w_root1,2))
            options.append(round(w_root2,2))
        options=list(options)
        r.shuffle(options)
        return question,options,self.correct_ans

    def check_answer(self, selected):
        if self.selected_difficulty == 0 :
            is_correct = (selected == self.correct_answer)
            if is_correct:
                self.correct_count += 1
            return is_correct
        elif self.selected_difficulty == 1:
            if(selected in self.correct_ans):
                self.correct_count+=1
                return 1
            else:
                return 0
            