from InquirerPy  import inquirer
import random
import json
import os

# Variables for the program

# Integer Variables
practice_exam_limit = 50 # The fixed number of questions for the Full Practice Exam Mode
domain_quiz_limit = 20   # The fixed number of questions for a Domain-Based Practice Quiz.
current_score = 0        # The raw count of correct answers during an active session.
passing_threshold = 80   # The configurable percentage required to receive a "Pass" indication.

# Boolean Variables
is_running = True # A flag that keeps the main menu loop active until the user chooses to exit.
# is_full_exam = False # A toggle used to switch between full exam and single-domain question fetching.
is_input_valid = True # A flag used to validate users input during answer choices.

# String Variable
# user_answer = "c" # Captures the user's multiple-choice selection (A–D).
selected_domain = "network access" # Stores the specific CCNA domain currently being assessed.
performance_rank = "moderate" # Stores the classification (Weak, Moderate, Strong) based on historical data.

# Dictionary Variable
domain_scores_counter = {} # A dictionary that tracks correct answers per domain example: {"network access": 5}
domain_totals = {}  # A dictionary that tracks the total number of questions encountered per domain in
# the current pool (used to calculate accurate percentages)
SETTINGS_FILE = "settings.json" # file containing settings config of the program

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
        message=f"Select a domain for your {domain_quiz_limit}-question quiz:\n",
        choices= domains).execute()    # List of menu items
    if choice == "Back": # This if statement returns us to the main menu
        return

    run_quiz_engine("domain", domain_name=choice)

def run_quiz_engine(mode, domain_name=None):
    # global variable access for session scoring
    global current_score, domain_scores_counter

    # initialize counters for domain-level performance tracking
    domain_list = []
    for domain in domains:
        if domain != "Back":
            domain_list.append(domain.lower())

    # domain_scores_counter = {}
    # domain_totals = {}
    for domain in domain_list:
        domain_scores_counter[domain] = 0
        domain_totals[domain] = 0

    # load JSON question bank from local data storage
    try:
        with open('questions.json', 'r') as questions_file:
            questions_data = json.load(questions_file)
            all_questions = questions_data['questions']
    except FileNotFoundError:
        print("error: questions.json not found.")
        return

    # filter questions based on mode using standard for loops
    questions_pool = []
    if mode == "domain":
        # generate fixed set of questions from a selected ccna domain
        for questions in all_questions:
            if questions['domain'].lower() == domain_name.lower():
                questions_pool.append(questions)
        limit = domain_quiz_limit  # set to 20
    else:
        # generate mixed exam randomly selected across all ccna domains
        for questions in all_questions:
            questions_pool.append(questions)
        limit = practice_exam_limit  # set to 50

    # shuffling questions present in pool and selecting number needed
    random.shuffle(questions_pool)
    session_pool = questions_pool[:limit]

    for num, question in enumerate(session_pool, start=1):
        domain_key = question['domain'].lower()
        domain_totals[domain_key] += 1

        # Numbered question
        print(f"\nQuestion {num} - Domain: {question['domain']}")
        print(question['question_text'])

        # display multiple-choice answers (a–d)
        for key in question['options']:
            print(f"{key}) {question['options'][key]}")

        # Input validation loop: only a-d allowed
        while is_input_valid:
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


def display_summary(limit, domain_scores_counter, domain_totals):
    # Calculate overall percentage of quiz
    # current_score is accessed as a global variable
    overall_percentage = (current_score / limit) * 100

    print("=" * 50)
    print("                QUIZ RESULTS                ")
    print("=" * 50)

    # Display raw score and percentage
    print(f"Overall Score: {current_score}/{limit}")
    print(f"Percentage:    {overall_percentage:.1f}%")

    # Pass/Fail indication (using your 80% passing_threshold)
    if overall_percentage >= passing_threshold:
        print("Final Grade:  PASS")
    else:
        print("Final Grade:  FAIL")

    print("-" * 50)
    # Domain-level performance tracking
    print("Performance by CCNA Domain:")

    # Iterate through the dictionary to calculate domain-specific metrics
    for domain_name in domain_scores_counter:
        count_asked = domain_totals[domain_name]

        # Only display domains that appeared in the current quiz session
        if count_asked > 0:
            correct_count = domain_scores_counter[domain_name]
            domain_pct = (correct_count / count_asked) * 100

            # Identify strengths and weaknesses (Classification)
            if domain_pct >= 80:
                performance_rank = "Strong"
            elif domain_pct >= 60:
                performance_rank = "Moderate"
            else:
                performance_rank = "Weak"

            # Formatting the output for a clean CLI look
            # ensures the domain names align vertically
            print(f"- {domain_name.ljust(30)}: {domain_pct:.1f}% ({performance_rank})")

    print("=" * 50)
    print("Press ENTER to return to the Main Menu...")
    input()  # Pauses so the user can review results


def save_results_to_database(overall_score, total_questions, domain_scores_dict):
    pass
    global current_score, domain_totals, domain_scores_counter
#     Establish Connection
    with sqlite3.connect("ccna_history.db") as conn:
#     OPEN a connection to the local file "ccna_history.db"
#     CREATE a "cursor" object to execute commands
        cur = conn.cursor()
#     # Make sure Table Exists
#     IF the table "quiz_attempts" does not exist:
#         CREATE TABLE "quiz_attempts" with these columns:
#             - id: (Unique ID, auto-incrementing)
#             - date_time: (current date)
#             - total_score
#             - total_question
#             - percentage
#             - network_fundamentals_pct
#             - network_access_pct
#             - ip_connectivity_pct
#             - ip_services_pct
#             - security_fundamentals_pct
#             - automation_programmability_pct

#     # Prepare the Data
#     CALCULATE the overall percentage (score / total * 100)
#     GET the current date

#     FOR each domain in the official CCNA list:
#         CALCULATE that specific domain's percentage from domain_scores_dict
#         IF the domain wasn't in the quiz, set its value to NULL or 0

#     # Execute the Insertion
#     INSERT a new row into "quiz_attempts" using the calculated values

#     # Finalize
#     COMMIT the changes (save them to the disk)
#     CLOSE the database connection
#     PRINT "Results saved to performance history."

def display_history():
    pass
# This function will aid us in viewing Performance History
# Load ccna_history.db using Pandas Library
# Display performance history using Pandas Library

def display_settings():
    global practice_exam_limit,domain_quiz_limit
    # Generate and select option from the Settings menu
    while True:
        choice = inquirer.select(
            message="                   SETTINGS\n                 ===============                    ",
            choices=["Change Full Practice Exam Questions Limit",
                     "Change Domain Exams Questions Limit",
                     "Clear Performance History",
                     "Back to Main Menu",
                     ],
        ).execute()
        if choice == "Change Full Practice Exam Questions Limit":
            while True:
                # Check if input falls between 1 and 100 and is an integer
                try:
                    value = int(input("Enter the maximum number of questions you want to exam: "))
                    if not 1 <= value <= 100:
                        raise ValueError
                    practice_exam_limit = value
                    save_settings()
                    print(f"Number of questions set to {practice_exam_limit}")
                    break
                except ValueError:
                    print("Please enter a number between 1 and 100.")
        elif choice == "Change Domain Exams Questions Limit":
            while True:
                try:
                    value = int(input("Enter the maximum number of questions you want to exam: "))
                    if not 1 <= value <= 100:
                        raise ValueError
                    domain_quiz_limit = value
                    save_settings()
                    print(f"Number of questions set to {domain_quiz_limit}")
                    break
                except ValueError:
                    print("Please enter a number between 1 and 100.")
        elif choice == "Clear Performance History":
            pass # This will include code to delete table from database
        elif choice == "Back to Main Menu":
            return


def save_settings():
    data = {
        "practice_exam_limit": practice_exam_limit,
        "domain_quiz_limit": domain_quiz_limit
    }
    with open(SETTINGS_FILE, "w") as output_file:
        json.dump(data, output_file, indent=4)


def load_settings():
    global practice_exam_limit, domain_quiz_limit

    # Check if file exists first
    if not os.path.exists(SETTINGS_FILE):
        return  # Do nothing, use the initial values above

    try:
        with open(SETTINGS_FILE, "r") as settings_file:
            data = json.load(settings_file)
            practice_exam_limit = data.get("practice_exam_limit", practice_exam_limit)
            domain_quiz_limit = data.get("domain_quiz_limit", domain_quiz_limit)
    except (json.JSONDecodeError, IOError):
        print("Settings file corrupted. Using default values.")




def main_menu():
    global is_running
    while is_running:
        print("\n" + "=" * 50)
        print("                CCNA PRACTICE TOOL                ")
        print("=" * 50)
        choice=inquirer.select(
            message = "Use the up and down arrow keys to select and press ENTER to confirm\n",
            choices = [f"Topic-based Exam Mode ({domain_quiz_limit} questions)",
                    f"Full Practice Exam Mode ({practice_exam_limit} questions)",
                    "View Performance History",
                    "Settings",
                    "Exit"
                       ],
        ).execute()
        if choice == f"Topic-based Exam Mode ({domain_quiz_limit} questions)":
            topic_exam()    # starts 20-question domain exam
        elif choice == f"Full Practice Exam Mode ({practice_exam_limit} questions)":
            run_quiz_engine("full")  # starts 50-question mixed exam
        elif choice == "View Performance History":
            pass
        elif choice == "Settings":
            display_settings()
        elif choice == "Exit":
            confirm = inquirer.confirm(message = "Are you sure you want to quit?").execute()
            if confirm:
                print ("Goodbye!")
                is_running = False

if __name__ == "__main__":
    load_settings()
    main_menu()

