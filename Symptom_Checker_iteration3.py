import tkinter as tk
from tkinter import messagebox, ttk

class SymptomChecker:
    def __init__(self):
        self.entered_symptoms = set()

    # Symptom list dictionary 
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

    def remove_symptom(self, symptom):
        # Remove the symptom if it exists in the entered symptoms
        if symptom in self.entered_symptoms:
            self.entered_symptoms.remove(symptom)
            return True
        return False

    def show_log(self):
        log_text = "\n".join([", ".join(entry) for entry in self.log])
        return log_text


class SymptomCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Symptom Checker")
        
        # Create an instruction page 
        self.instructions_page()

        # Symptom descriptions dictionary
        self.symptom_descriptions = {
            "fever": "A rise in body temperature above the normal range.",
            "cough": "A sudden, forceful expulsion of air from the lungs.",
            "headache": "Pain or discomfort in the head, face, or neck area.",
            "fatigue": "A feeling of tiredness or lack of energy.",
            "sore throat": "Pain or irritation in the throat.",
            "nausea": "The feeling of wanting to vomit, usually associated with an upset stomach.",
            "vomiting": "The involuntary, forceful expulsion of stomach contents through the mouth.",
            "shortness of breath": "A feeling of being unable to take a full breath or a sense of breathlessness.",
            "stomach pain": "Discomfort or pain in the stomach area.",
            "diarrhea": "Frequent, loose, or watery bowel movements.",
            "loss of taste": "The inability to perceive flavors.",
            "runny nose": "Excess mucus production in the nasal passages.",
            "sensitivity to light": "Discomfort or pain in the eyes when exposed to light."
        }

    def instructions_page(self):
        self.instruction_frame = tk.Frame(self.root)
        self.instruction_frame.pack(padx=20, pady=20)

        # Information of the instructions
        instruction_label = tk.Label(self.instruction_frame, text=
        "Welcome to the Symptom Checker!\n\n"
         "This app helps you identify potential conditions by giving you a prognosis based on the symptoms you enter.\n\n"
        "1. Select or type a symptom from the list.\n"
        "2. Click 'Add Symptom' to log it.\n"
        "3. If you want to remove a symptom click on it and click 'Remove Symptom'.\n "
        "4. Double click entered symptom to view defenition'.\n "
        "5. The app will show possible conditions based on your symptoms.\n\n"
        "Click 'OK' to start.", font=("Arial", 14))
        instruction_label.pack(padx=10, pady=20)

        ok_button = tk.Button(self.instruction_frame, text="OK", font=("Arial", 12), command=self.show_main_app)
        ok_button.pack()

    def show_main_app(self):
        # Remove the instruction page
        self.instruction_frame.destroy()

        # Now create the main symptom checker interface
        self.checker = LoggedSymptomChecker()

        # List of symptoms to choose from (autocomplete suggestion)
        self.all_symptoms = [
            "fever", "cough", "headache", "fatigue", "sore throat", "nausea", "vomiting", 
            "shortness of breath", "stomach pain", "diarrhea", "loss of taste", 
            "runny nose", "sensitivity to light"
        ]
        
        # Sort the symptoms alphabetically before setting them in the Combobox
        self.all_symptoms = sorted(self.all_symptoms)

        # GUI Elements
        self.symptom_label = tk.Label(self.root, text="Enter a Symptom:", font=("Arial", 12))
        self.symptom_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        # Create a Combobox for symptom input with autocomplete
        self.symptom_combobox = ttk.Combobox(self.root, width=30, font=("Arial", 12), state="normal")
        self.symptom_combobox['values'] = self.all_symptoms
        self.symptom_combobox.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.symptom_combobox.set("")  # Start with an empty value

        self.enter_button = tk.Button(self.root, text="Add Symptom", font=("Arial", 12), command=self.add_symptom)
        self.enter_button.grid(row=0, column=2, padx=10, pady=10)

        # Listbox to display added symptoms
        self.symptom_listbox = tk.Listbox(self.root, width=40, height=6, font=("Arial", 12))
        self.symptom_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # The program for the listbox for selecting a symptom and showing its definition
        self.symptom_listbox.bind("<Double-1>", self.show_symptom_definition)

        self.remove_button = tk.Button(self.root, text="Remove Symptom", font=("Arial", 12), command=self.remove_symptom)
        self.remove_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.result_label = tk.Label(self.root, text="Results will appear here.", width=60, height=6, relief="solid", font=("Arial", 11), anchor="nw", justify="left", wraplength=450)
        self.result_label.grid(row=3, column=0, columnspan=3, padx=15, pady=15)

        self.log_button = tk.Button(self.root, text="Show Symptom Log", font=("Arial", 12), command=self.show_log)
        self.log_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", font=("Arial", 12), command=self.root.quit)
        self.exit_button.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    #Adds Symptom chosen by the user
    def add_symptom(self):
        symptom = self.symptom_combobox.get().strip().lower()
        if symptom and symptom in self.all_symptoms:
            self.checker.entered_symptoms.add(symptom)
            self.symptom_listbox.insert(tk.END, symptom)
            self.symptom_combobox.set("")  # Clear the combobox after adding the symptom
            self.checker.get_symptoms()
        else:
            messagebox.showwarning("Input Error", "Please select a valid symptom from the list.")

        self.show_results()

    def remove_symptom(self):
        # Get the selected symptom from the listbox
        selected_symptom_index = self.symptom_listbox.curselection()
        if selected_symptom_index:
            symptom_to_remove = self.symptom_listbox.get(selected_symptom_index)
            if self.checker.remove_symptom(symptom_to_remove):
                self.symptom_listbox.delete(selected_symptom_index)
                self.show_results()
            else:
                messagebox.showwarning("Error", "Symptom not found.")
        else:
            messagebox.showwarning("Selection Error", "Please select a symptom to remove.")

    def show_results(self):
        result = self.checker.check_symptoms()
        self.result_label.config(text=result)

    def show_log(self):
        log_text = self.checker.show_log()
        if not log_text:
            log_text = "No symptoms logged yet."
        messagebox.showinfo("Symptom Log", log_text)

    def show_symptom_definition(self, event):
        selected_symptom_index = self.symptom_listbox.curselection()
        if selected_symptom_index:
            selected_symptom = self.symptom_listbox.get(selected_symptom_index)
            definition = self.symptom_descriptions.get(selected_symptom, "No definition available.")
            messagebox.showinfo(f"Definition of {selected_symptom.capitalize()}", definition)
        else:
            messagebox.showinfo("No Selection", "Please select a symptom from the list.")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SymptomCheckerApp(root)
    root.mainloop()
