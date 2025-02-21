import pandas as pd
import os

class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {
            'Questions': [],
            'Correct_Answer': [],
            'Inputted_Answer': [],
            'Result': []
        }

    def store_question(self, question, correct_answer):
        self.data['Questions'].append(question)
        self.data['Correct_Answer'].append(correct_answer)

    def store_answer(self, answer, result):
        self.data['Inputted_Answer'].append(answer)
        self.data['Result'].append(result)

    def mark_skipped(self):
        self.data['Inputted_Answer'].append(pd.NA)
        self.data['Result'].append("Skipped")

    def save_to_csv(self):
        max_len = len(self.data["Questions"])  # Get the total questions count
    
    # Ensure all lists have the same length by appending missing values
        while len(self.data["Inputted_Answer"]) < max_len:
            self.data["Inputted_Answer"].append(pd.NA)
            self.data["Result"].append("Skipped")

    # Convert dictionary to DataFrame
        df = pd.DataFrame(self.data)

    # Save to CSV (append if file exists, else create new)
        if os.path.exists(self.file_path):
            df.to_csv(self.file_path, mode="a", header=False, index=False, na_rep="NaN")
        else:
            df.to_csv(self.file_path, mode="w", header=True, index=False, na_rep="NaN")

    # Clear data after saving
        for key in self.data.keys():
            self.data[key] = []

