import pandas as pd
import os

class Database:
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
    file_path = os.path.join(script_dir, "data.csv")
    def __init__(self):
        self.file_path = self.file_path
        self.data = {
            'Questions': [],
            'Correct_Answer': [],
            'Inputted_Answer': [],
            'Result': []
        }

    def store_question(self, questions, correct_ans):
        self.data['Questions'].append(questions)
        self.data['Correct_Answer'].append(correct_ans)

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

    def read(self):
        df = pd.read_csv(self.file_path)
        
        # ✅ Ensure the required columns exist before selection
        required_columns = ["Correct_Answer", "Inputted_Answer"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise KeyError(f"Missing columns in data.csv: {missing_columns}")

        return df[['Correct_Answer', 'Inputted_Answer']].dropna()