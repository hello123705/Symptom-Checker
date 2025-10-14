import tkinter as tk
from tkinter import messagebox,ttk

class SymptomChecker:
    def __init__(self):
        self.entered_symptoms = set()

# symptom list 
    def check_symptoms(self):
        conditions = {
            "Flu": {"fever", "cough", "shortness of breath", "fatigue"},
            "Migraine": {"headache", "fatigue", "nausea", "sensitivity to light"},
            "Common Cold": {"sore throat", "runny nose", "cough"},
            "Stomach Bug": {"nausea", "vomiting", "diarrhea", "stomach pain"},
            "COVID-19": {"fever", "cough", "loss of taste", "shortness of breath", "fatigue"},
        }

        matches = []

        for condition, symptoms in conditions.items():
            match_count = len(symptoms.intersection(self.entered_symptoms))
            if match_count > 0:
                match_percentage = match_count / len(symptoms)
                matches.append((condition, match_count, match_percentage))

        if not matches:
            return "Your symptoms don't match anything specific. Please see a doctor if you feel unwell."

        # Sort by number of symptoms matched, then by percentage
        matches.sort(key=lambda x: (x[1], x[2]), reverse=True)

        result = "Possible conditions based on your symptoms:\n"
        for condition, count, percentage in matches:
            result += f"- {condition}: {count} matched ({int(percentage * 100)}%)\n"

        return result.strip()


class LoggedSymptomChecker(SymptomChecker):
    def __init__(self):
        super().__init__()
        self.log = []

    def get_symptoms(self):
        # Log the entered symptoms after they are entered
        self.log.append(self.entered_symptoms.copy())

    def show_log(self):
        log_text = "\n".join([", ".join(entry) for entry in self.log])
        return log_text


class SymptomCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symptom Checker")

        self.checker = LoggedSymptomChecker()

        # GUI Elements 
        self.symptom_label = tk.Label(root, text="Enter a Symptom:", font=("Arial", 12))
        self.symptom_label.grid(row=0, column=0, padx=10, pady=10)

        self.symptom_entry = tk.Entry(root, width=30, font=("Arial", 12))
        self.symptom_entry.grid(row=0, column=1, padx=10, pady=10)

        self.enter_button = tk.Button(root, text="Add Symptom", font=("Arial", 12), command=self.add_symptom)
        self.enter_button.grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(root, text="Results will appear here.", width=60, height=6, relief="solid", font=("Arial", 11), anchor="nw", justify="left", wraplength=450)
        self.result_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.symptom_listbox = tk.Listbox(root, height=6, width=50, font=("Arial", 10))
        self.symptom_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.log_button = tk.Button(root, text="Show Symptom Log", font=("Arial", 12), command=self.show_log)
        self.log_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
        self.exit_button.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

        # Optional: Symptom suggestion label
        self.suggestion_label = tk.Label(root, text="Try symptoms like: fever, cough, headache, sore throat, fatigue...", font=("Arial", 10), fg="gray")
        self.suggestion_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    def add_symptom(self):
        symptom = self.symptom_entry.get().strip().lower()
        if symptom:
            self.checker.entered_symptoms.add(symptom)
            self.symptom_listbox.insert(tk.END, symptom)
            self.symptom_entry.delete(0, tk.END)
            self.checker.get_symptoms()  # Log symptoms
        else:
            messagebox.showwarning("Input Error", "Please enter a valid symptom.")

        self.show_results()

    def show_results(self):
        result = self.checker.check_symptoms()
        self.result_label.config(text=result)

    def show_log(self):
        log_text = self.checker.show_log()
        if not log_text:
            log_text = "No symptoms logged yet."
        messagebox.showinfo("Symptom Log", log_text)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SymptomCheckerApp(root)
    root.mainloop()


