from InquirerPy  import inquirer
# Variables for the program

# Integer Variables
practice_exam_limit = 50 # The fixed number of questions for the Full Practice Exam Mode
Domain_quiz_limit = 20   # The fixed number of questions for a Domain-Based Practice Quiz.
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
        message="Select an option\n",
        choices= domains).execute()    # List of menu items
    if choice == "Back": # This if statement returns us to the main menu
        main_menu()


def main_menu():
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
            break
        if choice == "Exit":
            confirm = inquirer.confirm(message = "Are you sure you want to quit?").execute()
            if confirm:
                print ("Goodbye!")
                break
            continue
        handle_selection(choice)

if __name__ == "__main__":
    main_menu()

