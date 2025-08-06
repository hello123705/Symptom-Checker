def Symptomchecker():
    print("=== Welcome to Symptom Checker ===")
    print("Please enter your symptoms.\n")

    entered_symptoms = set()

    while True:
        symptom = input("Enter a symptom: ").strip().lower()
        if symptom == "":
            break
        entered_symptoms.add(symptom)
        print("Got it. Any other symptoms and if you are done press enter?")

    print("\n--- Results ---")

    if not entered_symptoms:
        print("You didn’t enter any symptoms. If you feel unwell, please talk to a healthcare provider.")
        return

    # Simple pattern matching
    if {"fever", "cough", "shortness of breath"}.issubset(entered_symptoms):
        print("You may have the flu.")
    elif {"headache", "fatigue"}.issubset(entered_symptoms):        
        print("You might have a mild bug.")
    elif "sore throat" in entered_symptoms:
        print("you might have the cold cold.")
    else:
        print("Your symptoms don't match anything specific . If your not feeling well, it's best to see a doctor.")

    print("\nThanks for using the Symptom Checker!")

if __name__ == "__main__":
    Symptomchecker()
