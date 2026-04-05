from InquirerPy  import inquirer
import random
import json
import os
import sqlite3
from datetime import datetime
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

    # load JSON question bank from local data storage safely
    default_questions = {'questions': []} # fallback structure to ensure the program doesn't crash if the file is missing
    questions_data = safe_load_json('questions.json', default_questions)
    all_questions = questions_data.get('questions', [])
    # Check if we actually have questions to proceed; if not, return to menu
    if not all_questions:
        print("\nError: No questions available to load. Please check questions.json.")
        return

    # Filter questions based on mode
    questions_pool = []
    if mode == "domain":
        # generate fixed set of questions from a selected ccna domain
        for questions in all_questions:
            if questions['domain'].lower() == domain_name.lower():
                questions_pool.append(questions)
        limit = domain_quiz_limit
        random.shuffle(questions_pool)
        session_pool = questions_pool[:limit]
    else:
        # generate mixed exam randomly selected across all ccna domains
        limit = practice_exam_limit
        session_pool = []

        # Group all questions by domain
        domain_buckets = {d.lower(): [] for d in domains if d != "Back"}
        for q in all_questions:
            d_name = q['domain'].lower()
            if d_name in domain_buckets:
                domain_buckets[d_name].append(q)

        # Pick one random question from every bucket to guarantee coverage
        leftover_questions = []
        for d_name in domain_buckets:
            if domain_buckets[d_name]:
                random.shuffle(domain_buckets[d_name])
                # Add the first one to our guaranteed list
                session_pool.append(domain_buckets[d_name].pop(0))
                # Put the rest in a "leftover" pile for later
                leftover_questions.extend(domain_buckets[d_name])

        # Fill the remaining spots from the leftover pile
        random.shuffle(leftover_questions)
        needed = limit - len(session_pool)
        session_pool.extend(leftover_questions[:needed])

        # Final shuffle so the guaranteed ones aren't always at the start
        random.shuffle(session_pool)

    for num, question in enumerate(session_pool, start=1):
        domain_key = question['domain'].lower()
        domain_totals[domain_key] += 1

        # Numbered question
        print(f"\nQuestion {num} - Domain: {domain_key}")
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

    # Trigger the database save using the session's active data
    save_results_to_database(mode, current_score, limit, domain_scores_counter, domain_totals)

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
        else:
            print(f"- {domain_name.ljust(30)}: Not Tested")

    print("=" * 50)
    print("Press ENTER to return to the Main Menu...")
    input()  # Pauses so the user can review results


# 1. Update the function signature to include the totals dictionary
def save_results_to_database(exam_mode, overall_score, total_questions, domain_scores_dict, domain_totals_dict):
    """Archives results including the exam mode (Full or Domain)."""
    overall_percentage = (overall_score / total_questions) * 100 if total_questions > 0 else 0
    date_stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    ccna_sections = [d.lower() for d in domains if d != "Back"]

    domain_pcts = {}
    for section in ccna_sections:
        asked = domain_totals_dict.get(section, 0)
        correct = domain_scores_dict.get(section, 0)
        if asked > 0:
            percentage = (correct / asked) * 100
        else:
            percentage = None

        domain_pcts[section] = percentage

    try:
        with sqlite3.connect("ccna_history.db") as conn:
            cur = conn.cursor()

            # Added 'exam_mode TEXT' to the table creation
            cur.execute("""
                CREATE TABLE IF NOT EXISTS quiz_attempts (
                                                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                             date_time TEXT,
                                                             exam_mode TEXT,
                                                             total_score INTEGER,
                                                             total_questions INTEGER,
                                                             overall_percentage REAL,
                                                             network_fundamentals REAL,
                                                             network_access REAL,
                                                             ip_connectivity REAL,
                                                             ip_services REAL,
                                                             security_fundamentals REAL,
                                                             automation_programmability REAL
                )
            """)


            sql_query = '''INSERT INTO quiz_attempts (
                date_time, exam_mode, total_score, total_questions, overall_percentage,
                network_fundamentals, network_access, ip_connectivity, 
                ip_services, security_fundamentals, automation_programmability
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

            data_values = (
                date_stamp, exam_mode, overall_score, total_questions, overall_percentage,
                domain_pcts.get("network fundamentals"),
                domain_pcts.get("network access"),
                domain_pcts.get("ip connectivity"),
                domain_pcts.get("ip services"),
                domain_pcts.get("security fundamentals"),
                domain_pcts.get("automation and programmability")
            )

            cur.execute(sql_query, data_values)
            conn.commit()
            print(f"\n[Database] {exam_mode} results archived successfully.")

    except sqlite3.Error as e:
        print(f"\n[Database Error] Could not save results: {e}")


def display_history():
    pass
# This function will aid us in viewing Performance History
# Load ccna_history.db using Pandas Library
# Display performance history using Pandas Library

def get_validated_input(prompt, min_value=1, max_value=100):
    # Handles the repetitive try/except logic for numeric user settings.
    while True:
        try:
            value = int(input(prompt))
            if min_value <= value <= max_value:
                return value
            print(f"Error: Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")


def safe_load_json(file_path, default_data):
    # Handles file-related errors for loading settings or questions.
    if not os.path.exists(file_path):
        return default_data
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read {file_path} ({e}). Using defaults.")
        return default_data


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
            msg = "Enter max questions for Full Exam (1-100): "
            practice_exam_limit = get_validated_input(msg)
            save_settings()
            print(f"Number of questions set to {practice_exam_limit}")

        elif choice == "Change Domain Exams Questions Limit":
            msg = "Enter max questions for Domain Quiz (1-100): "
            domain_quiz_limit = get_validated_input(msg)
            save_settings()
            print(f"Number of questions set to {domain_quiz_limit}")

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

    # Define defaults in case the settings file is missing or broken
    defaults = {
        "practice_exam_limit": practice_exam_limit,
        "domain_quiz_limit": domain_quiz_limit
    }

    data = safe_load_json(SETTINGS_FILE, defaults)

    # Update global variables from the loaded data
    practice_exam_limit = data.get("practice_exam_limit", defaults["practice_exam_limit"])
    domain_quiz_limit = data.get("domain_quiz_limit", defaults["domain_quiz_limit"])




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

