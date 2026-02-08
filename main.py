from InquirerPy  import inquirer
import random
import json

# Variables for the program

# Integer Variables
practice_exam_limit = 50 # The fixed number of questions for the Full Practice Exam Mode
domain_quiz_limit = 20   # The fixed number of questions for a Domain-Based Practice Quiz.
current_score = 0        # The raw count of correct answers during an active session.
passing_threshold = 80   # The configurable percentage required to receive a "Pass" indication.

# Boolean Variables
is_running = True # A flag that keeps the main menu loop active until the user chooses to exit.
is_full_exam = False # A toggle used to switch between full exam and single-domain question fetching.
is_input_valid = True # A flag used to validate users input during answer choices.

# String Variable
user_answer = "c" # Captures the user's multiple-choice selection (A–D).
selected_domain = "network access" # Stores the specific CCNA domain currently being assessed.
performance_rank = "moderate" # Stores the classification (Weak, Moderate, Strong) based on historical data.

# Dictionary Variable
domain_scores_counter = {} # A dictionary that tracks correct answers per domain example: {"network access": 5}
domain_totals = {}  # A dictionary that tracks the total number of questions encountered per domain in
# the current pool (used to calculate accurate percentages)

# List variable
domains =["Network Fundamentals",
          "Network Access",
          "IP Connectivity",
          "IP Services",
          "Security Fundamentals",
          "Automation and Programmability",
          "Back"
           ]


def topic_exam():
# Domain or topic-based exams CLI Menu. Function generates a menu which can be navigated with arrow keys.
    choice = inquirer.select(
        message="Select a domain for your 20-question quiz:\n",
        choices= domains).execute()    # List of menu items
    if choice == "Back": # This if statement returns us to the main menu
        return

    run_quiz_engine("domain", domain_name=choice)

def run_quiz_engine(mode, domain_name=None):
    # global variable access for session scoring
    global current_score
    current_score = 0

    # initialize counters for domain-level performance tracking
    domain_list = []
    for d in domains:
        if d != "Back":
            domain_list.append(d.lower())

    domain_scores_counter = {}
    domain_totals = {}
    for d in domain_list:
        domain_scores_counter[d] = 0
        domain_totals[d] = 0

    # load json question bank from local data storage
    try:
        with open('questions.json', 'r') as file:
            data = json.load(file)
            all_questions = data['questions']
    except FileNotFoundError:
        print("error: questions.json not found.")
        return

    # filter questions based on mode using standard for loops
    pool = []
    if mode == "domain":
        # generate fixed set of questions from a selected ccna domain
        for q in all_questions:
            if q['domain'].lower() == domain_name.lower():
                pool.append(q)
        limit = domain_quiz_limit  # set to 20
    else:
        # generate mixed exam randomly selected across all ccna domains
        for q in all_questions:
            pool.append(q)
        limit = practice_exam_limit  # set to 50

    # shuffling questions present in pool and selecting number needed
    random.shuffle(pool)
    session_pool = pool[:limit]

    for idx, question in enumerate(session_pool, start=1):
        domain_key = question['domain'].lower()
        domain_totals[domain_key] += 1

        # Numbered question
        print(f"\nQuestion {idx} - Domain: {question['domain']}")
        print(question['question_text'])

        # display multiple-choice answers (a–d)
        for key in question['options']:
            print(f"{key}) {question['options'][key]}")

        # Input validation loop: only a-d allowed
        while True:
            ans = input("Your answer (a-d): ").strip().lower()
            if ans in ['a', 'b', 'c', 'd']:
                break
            else:
                print("Invalid input! Please enter a, b, c, or d.")


        # automatic scoring
        if ans == question['correct_answer']:
            current_score += 1
            domain_scores_counter[domain_key] += 1
            print("correct!")
        else:
            print(f"incorrect. the correct answer was {question['correct_answer']}.")
            # optional explanation for review & feedback
            if 'explanation' in question:
                print(f"explanation: {question['explanation']}")

    # immediate feedback summary logic
    display_summary(limit, domain_scores_counter, domain_totals)


def main_menu():
    global is_running
    while is_running:
        choice=inquirer.select(
            message = "Use the up and down arrow keys to select and press ENTER to confirm\n",
            choices = ["Topic-based Exam Mode (20 questions)",
                    "Full Practice Exam Mode (50 questions)",
                    "View Performance History",
                    "Exit"
                       ],
        ).execute()
        if choice == "Topic-based Exam Mode (20 questions)":
            topic_exam()
        elif choice == "Full Practice Exam Mode (50 questions)":
            run_quiz_engine("full")  # starts 50-question mixed exam
        elif choice == "View Performance History":
            pass
        elif choice == "Exit":
            confirm = inquirer.confirm(message = "Are you sure you want to quit?").execute()
            if confirm:
                print ("Goodbye!")
                is_running = False

if __name__ == "__main__":
    main_menu()

