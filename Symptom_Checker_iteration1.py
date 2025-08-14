# Create a symptom checker whick gets symptoms from a user and presents a prognosis 
class SymptomChecker:
    def __init__(self):
        self.entered_symptoms = set()

#This fucntion gets 
    def get_symptoms(self):
        print("Welcome to Symptom Checker")
        print("Please enter your symptoms (press Enter when done):\n")
        while True:
            symptom = input("Enter a symptom: ").strip().lower()
            if symptom == "":
                break
            self.entered_symptoms.add(symptom)
            print("Got it. Any other symptoms? If you are done press enter")

    def check_symptoms(self):
        if {"fever", "cough", "shortness of breath"}.issubset(self.entered_symptoms):
            return "You may have the flu."
        elif {"headache", "fatigue"}.issubset(self.entered_symptoms):
            return "You might have a migraine."
        elif "sore throat" in self.entered_symptoms:
            return "You may have a cold."
        else:
            return "Your symptoms don't match anything specific. Please see a doctor if you feel unwell."

    def run(self):
        self.get_symptoms()
        print("\nResults")
        if not self.entered_symptoms:
            print("You didn't enter any symptoms. Please talk to a healthcare provider if you feel unwell.")
            return
        result = self.check_symptoms()
        print(result)
        print("\nThanks for using the Symptom Checker")


class LoggedSymptomChecker(SymptomChecker):
    def __init__(self):
        super().__init__()
        self.log = []

    def get_symptoms(self):
        super().get_symptoms()
        # Log the entered symptoms after collection
        self.log.append(self.entered_symptoms.copy())
        print(f"[LOG] Symptoms recorded: {self.entered_symptoms}")

    def show_log(self):
        print("\nSymptom Log:")
        for entry in self.log:
            print(entry)



# Create a LoggedSymptomChecker instance and run it
checker = LoggedSymptomChecker()
checker.run()

# Show the log of entered symptoms
checker.show_log()
