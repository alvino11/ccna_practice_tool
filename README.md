# CCNA CLI Practice Tool

A lightweight, offline, command-line application designed to help students prepare for the **Cisco CCNA (200-301)** exam through structured quizzes, performance analytics, and targeted review of weak areas.

This tool simulates exam-style practice in a distraction-free terminal environment while tracking learning progress across official CCNA domains.

---

## 🚀 Project Overview

The CCNA CLI Practice Tool is a Python-based interactive quiz system that allows users to practice domain-specific questions or take a full-length mixed practice exam. It includes scoring, analytics, and persistent settings, with planned database-backed historical tracking.

---

## ✨ Key Features

### 🧠 Interactive CLI Quiz Engine

* **Menu-Driven Navigation** using `InquirerPy` with arrow-key selection.
* **Two Study Modes**:

  * **Topic-Based Mode**: Practice questions filtered by CCNA exam domains.
  * **Full Practice Mode**: A mixed-domain mock exam for realistic exam simulation.
* **Robust Input Validation**: Ensures only valid multiple-choice answers (A–D) are accepted.

---

### 📊 Scoring & Performance Analytics

* **Automatic Scoring** with real-time score and percentage calculation.
* **Pass/Fail Feedback** after each quiz session.
* **Domain-Level Performance Breakdown** to identify weak knowledge areas.
* **Proficiency Ranking** per domain:

  * **Strong**
  * **Moderate**
  * **Weak**
* **Incorrect Answer Review Mode**: Displays missed questions with correct answers.

---

### 💾 Data Persistence

* **Local Settings Storage (`settings.json`)**
  Remembers user-defined question limits across sessions.
* **Offline Question Bank (`questions.json`)**
  Fully offline operation with no internet dependency.
* **Planned SQLite3 Database** for long-term performance tracking.

---

## 📚 Supported CCNA Domains (200-301)

* Network Fundamentals
* Network Access
* IP Connectivity
* IP Services
* Security Fundamentals
* Automation and Programmability

---

## 🛠 Tech Stack

* **Language**: Python 3.x
* **Libraries**:

  * `InquirerPy`
  * `json`
  * `random`
  * `os`
  * *(Planned)* `sqlite3`, `pandas`
* **Data Formats**: JSON (questions and settings)
* **Planned Storage**: SQLite database for historical results

---

## 📂 Project Structure

```
ccna-cli-practice-tool/
│
├── main.py            # Core CLI application and quiz engine
├── questions.json     # Local CCNA question repository
├── settings.json      # User-configurable settings (auto-generated)
├── README.md           # Project documentation
└── (planned) ccna_history.db # SQLite database for performance tracking
```

---

## ⚙️ Installation & Usage

### 1. Install Dependencies

```bash
pip install InquirerPy
```

### 2. Run the Application

```bash
python main.py
```

### 3. Configure Settings

* Open the **Settings** menu to set:

  * Number of questions per topic quiz
  * Number of questions in full practice exam

### 4. Start Practicing

* Choose **Topic-Based Quiz** or **Full Practice Exam**
* Answer multiple-choice questions (A–D)
* Receive instant scoring and feedback

### 5. Analyze Results

* View domain-level performance summaries
* Review incorrect answers
* Track improvement over time (planned persistent history)

---

## 🛡️ Error Handling & Robustness

The application includes a centralized validation layer to ensure a crash-free experience:

* **Input Guard**: A dedicated validation engine (`get_validated_input`) prevents the application from crashing when users enter non-numeric characters or values outside the 1–100 range.
* **File Integrity Protection**: The `safe_load_json` utility provides a safety net for configuration and question files. If a file is missing or corrupted, the tool automatically reverts to stable default values instead of terminating.
* **Persistent Logic**: Refactored settings management ensures that user preferences are validated before being committed to `settings.json`, preventing "dirty data" from affecting future sessions.

## 🧪 How It Works

1. Launch the CLI tool
2. Select a study mode
3. Answer multiple-choice questions
4. Receive score and pass/fail status
5. Review incorrect answers
6. View domain performance breakdown
7. Track progress across attempts

---

## 🧭 Development Roadmap

### 🔜 Short-Term

- [x] Implement SQLite3 result storage (`save_results_to_database`)
* [ ] Add performance history viewer using `pandas`
* [x] Add database cleanup/reset option in Settings

### 🧠 Planned Enhancements

* Flashcard-style revision mode
* Timed exam simulation mode
* Difficulty-based question weighting
* Export results to CSV
* Graphical performance trend visualization

---

## 🎯 Project Goals

* Provide an offline, exam-focused CCNA practice environment
* Help learners identify weak domains early
* Encourage structured and measurable exam preparation
* Serve as a foundation for advanced networking learning tools

## 🗄️ Databases
SQLite was selected because it suits a local, single user desktop application. It requires no installation and stores all data in a single file, making the project easy to move or share. It integrates directly with Python through the built-in sqlite3 library and handles values like None as NULL without extra work. For this use case, it is fast and reliable since it avoids network overhead and protects data with ACID compliance. It also supports future data analysis since tools like Pandas can read SQLite data directly.


---


