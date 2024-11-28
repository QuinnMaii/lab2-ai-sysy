import re
from pyswip import Prolog

# Initialize Prolog and load the knowledge base
prolog = Prolog()
prolog.consult("database-lab2.pl")  # Ensure the Prolog file is in the same directory

def extract_age(description):
    age_match = re.search(r"I am (\d+) years old", description, re.IGNORECASE)
    if age_match:
        try:
            return int(age_match.group(1))
        except ValueError:
            print("Error: Could not convert age to an integer.")
    return None

def extract_traits(description):
    traits_match = re.search(r"I think I am (.+)", description, re.IGNORECASE)
    if traits_match:
        traits = traits_match.group(1).lower().split("and")
        traits = [re.sub(r"[^\w\s]", "", trait.strip()) for trait in traits]
        return traits
    return []

def classify_house(traits):
    traits = [trait.strip().lower() for trait in traits]
    result = list(prolog.query(f"classify_by_traits({traits}, House)"))
    if result:
        houses = {r["House"] for r in result}
        return list(houses)
    return []

def get_required_subjects(career):
    result = list(prolog.query(f"career({career}, Subjects)"))
    if result:
        return result[0]["Subjects"]
    return []

def suggest_career(subjects):
    subjects = [subject.rstrip().lower() for subject in subjects]
    subjects_str = "[" + ", ".join(f"'{subject}'" for subject in subjects) + "]"
    result = list(prolog.query(f"suggest_career({subjects_str}, Career)"))
    if result:
        careers = list(set(r["Career"] for r in result))
        return careers
    return []

def main():
    print("Welcome to the Hogwarts Decision Support System!")
    print("Type 'exit' to quit the program.")
    
    while True:
        print("Please enter one of the following formats:")
        print("1. I am <age> years old and I think I am <traits>.")
        print("2. I love <subjects>.")
        print("3. I want to become a <career>.")
        print("4. exit")
        
        description = input("Enter your description: ").strip()
        
        if description.lower() == "exit":
            print("Exiting the program. Goodbye!")
            break
        
        age = extract_age(description)
        if age is not None:
            if 11 <= age <= 18:
                print(f"Welcome to Hogwarts! Your age is perfect for enrollment: {age} years old.")
                traits = extract_traits(description)
                if traits:
                    houses = classify_house(traits)
                    if houses:
                        print(f"Based on your traits, you belong to: {', '.join([house.capitalize() for house in houses])}.")
                    else:
                        print("Could not determine your House based on the given traits.")
                continue
            else:
                print(f"Sorry, your age ({age}) does not qualify for Hogwarts enrollment.")
                continue
        
        subjects_pattern = r"I love ([\w\s,]+)\."
        match = re.match(subjects_pattern, description, re.IGNORECASE)
        if match:
            subjects_part = description.lower().replace("i love ", "").strip()
            subjects = [subject.strip().rstrip('.').strip() for subject in subjects_part.split("and")]
            careers = suggest_career(subjects)
            if careers:
                print(f"Based on your favorite subjects, you might enjoy these careers: {', '.join(careers)}.")
            else:
                print("Could not find any careers based on the given subjects.")
            continue

        career_pattern = r"I want to become a ([\w\s]+)\."
        match = re.match(career_pattern, description, re.IGNORECASE)
        if match:
            career = match.group(1).strip().lower()
            required_subjects = get_required_subjects(career)
            if required_subjects:
                print(f"To become a {career}, you need to study these subjects: {', '.join(required_subjects)}.")
            else:
                print(f"Could not find any information on the career '{career}'.")
            continue
        
        print("Sorry, your input did not match any of the expected formats.")

if __name__ == "__main__":
    main()