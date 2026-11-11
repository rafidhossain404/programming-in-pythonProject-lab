# AIUB-PathFinder: Academic Performance & Degree Intelligence System
> **CSC 4162 / BSE 4112: Programming in Python | Midterm Project (Fall 2026–27)**  
> **American International University–Bangladesh (AIUB)**  
> **Student:** HOSSAIN, MD. RAFID (ID: `23-54787-3`) | **Instructor:** Md Kamrul Islam  

---

## 📌 Project Overview
**AIUB-PathFinder** is an intelligent academic performance analytics and degree audit application designed specifically for AIUB students and academic advisors. The system ingests official AIUB Grade Reports (PDF/TXT), analyzes historical academic trajectories across semesters using **NumPy**, maps performance against the **AIUB BScCSE Curriculum (Core 309 & Electives 338)**, and solves course unlock dependencies using pure **Python Set Theory**.

The project is built in strict accordance with the **Fall 2026–27 Midterm Project Requirements**, demonstrating core Python fundamentals, Object-Oriented Programming (OOP), all four primary data structures (`list`, `tuple`, `set`, `dict`), robust exception handling, and NumPy numerical computing without relying on forbidden high-level frameworks (no Pandas or Scikit-learn in Phase 1).

---

## 🚀 Key Features

1. **Automated Grade Report Ingestion & Ongoing Semester Detection**
   - Automatically parses AIUB Grade Reports (PDF or TXT) extracting 51 courses across 9 terms.
   - Detects the current in-progress semester (**2026-2027 Fall**) and isolates the 5 currently enrolled courses (15.0 Credits).

2. **NumPy Statistical Overview & Progression Engine**
   - Calculates central tendency and variance: Mean SGPA ($3.799$), Median ($3.760$), Standard Deviation ($\sigma = 0.117$), Variance, and Quartiles ($Q_1=3.75, Q_2=3.76, Q_3=3.91$).
   - Computes an **Academic Stability Index** and tracks chronological grade momentum (`+0.20`, `-0.22`, etc.).

3. **Visual 2D Coordinate Line Plot (CGPA vs. Semesters)**
   - High-resolution **2D Cartesian Terminal Graph** matching hand-drawn progression sketches.
   - Interactive **Tkinter Canvas GUI Window** displaying smooth dual-trace curves (Cumulative CGPA in blue, Semester SGPA in green dashed) with data point annotations and legend.

4. **Subject Domain Strength Analysis (ASCII Bar Diagram)**
   - Aggregates courses across 6 university departments: *CS & Software Engineering (3.88), Mathematics & Statistics (3.82), Basic Natural Sciences (3.79), Humanities & Languages (3.78), Hardware & Circuits (3.65), and Business & Management (3.63)*.
   - Generates horizontal ASCII visual progress bars and qualitative mastery ratings.

5. **Next-Semester Predictive Forecaster & Interactive "What-If" Simulator**
   - Uses **NumPy 1st-order linear regression** (`np.polyfit`) to project next-semester SGPA based on historical momentum.
   - Simulates custom grade scenarios for current enrolled courses to project graduating CGPA in real-time.

6. **Set-Theoretic Prerequisite & Course Unlock Engine**
   - Models curriculum prerequisites as Python sets and tests unlock conditions via `prereqs.issubset(completed_courses)`.
   - Identifies remaining core courses, eligible electives, and previews newly unlocked courses after passing the current term.

7. **Major Specialization Track Matcher**
   - Ranks 4 AIUB BScCSE elective specializations based on foundation grade point averages and unlocked course counts:
     - **#1 Intelligent Systems & Data Science** (90.3% Match — *Prime Alignment*)
     - **#2 Software Engineering & Enterprise Systems** (82.6% Match)
     - **#3 Hardware, Embedded Systems & Robotics** (75.6% Match)
     - **#4 Networks, Systems & Cyber Security** (73.4% Match)

8. **Persistent Academic Audit Export**
   - Exports complete profile, statistical metrics, domain GPAs, and course states to structured JSON (`data/student_audit_export.json`).

---

## 📂 Project Structure

```
programming-in-pythonProject-lab/
├── CONTEXT_WINDOW.md             # Master course guidelines & syllabus boundaries
├── PROGRESS_TRACKER.md           # Anti-hallucination state ledger & milestone checklist
├── MIDTERM_PROJECT_REPORT.md     # Official formal project report (AIUB Section 13 format)
├── VIVA_DEFENSE_GUIDE.md         # Comprehensive viva preparation & concept QA guide
├── main.py                       # Application master entry point & interactive CLI
├── data/
│   ├── aiub_curriculum.csv       # In-system curriculum database (101 courses, Core 309 + Elective 338)
│   ├── sample_grade_report.txt   # Official sample AIUB Grade Report (46 completed + 5 enrolled)
│   ├── student_audit_export.json # Exported academic audit ledger
│   └── sample_run_output.txt     # Complete 246-line captured verification log
├── src/
│   ├── __init__.py
│   ├── models.py                 # Core OOP domain models (Encapsulation, Inheritance, Polymorphism)
│   ├── curriculum_engine.py      # Set-theoretic prerequisite engine & major track matcher
│   ├── analytics.py              # NumPy statistical calculations, linear regression & simulation
│   ├── report_parser.py          # PDF/TXT grade report parser with name alias resolution
│   ├── ui.py                     # Terminal UI, ASCII horizontal bar charts & formatted tables
│   └── chart_viewer.py           # 2D ASCII coordinate plot & Tkinter Canvas graphical window
├── tests/
│   ├── __init__.py
│   └── test_core.py              # 9 automated unit tests verifying OOP, Sets, NumPy & Parsing
└── ui_prototype/                 # Stitch-generated UI mockup assets (HTML, PNG, Design spec)
    ├── code.html
    ├── screen.png
    └── DESIGN.md
```

---

## ⚙️ Installation & Requirements

### System Requirements:
- Python 3.10+ (Tested on Python 3.14)
- Windows / Linux / macOS

### Dependencies:
```bash
pip install numpy pypdf
```
*(Tkinter is built into standard Python distributions on Windows).*

---

## 🎮 How to Run

### 1. Launch Interactive CLI:
```bash
python main.py
```
*(Press Enter when prompted to immediately analyze the bundled AIUB sample report, or type the path to any custom `.pdf` or `.txt` grade report).*

### 2. Launch Web Dashboard (Stitch UI):
```bash
python server.py
```
*(Opens the interactive web dashboard at `http://127.0.0.1:8000/` connected live to the Python backend).*

### 3. Pass a Custom Grade Report directly to CLI:
```bash
python main.py "path/to/GradeReport.pdf"
```

### 4. Run Automated Unit Tests:
```bash
python -m unittest tests/test_core.py
```
*(All 9 unit tests pass in under 0.05 seconds).*

---

## 📊 Two-Phase Architecture Roadmap

| Milestone | Phase 1 (Midterm) — COMPLETED | Phase 2 (Final Term) — UPCOMING |
|:---|:---|:---|
| **Data Engine** | Pure Python OOP + Custom Sets/Dicts/Lists | **Pandas** DataFrames & Series |
| **Persistence** | CSV Ingestion & JSON Audit Export | Parquet / SQLite / Multi-format exports |
| **Analytics** | **NumPy** (`ndarray`, `std`, `percentile`, `polyfit`) | Advanced NumPy + Statistical Hypothesis Testing |
| **Visualization**| 2D ASCII Plots + **Tkinter Canvas** Window | **Matplotlib** & Seaborn High-Res Charts |
| **Interface** | Terminal CLI Menu + Tkinter Popups | **Web Dashboard** (Integrating Stitch prototype) |

---

## 📄 License & Academic Integrity
Developed as part of the **CSC 4162 / BSE 4112 Programming in Python** coursework at American International University–Bangladesh (AIUB). Code is strictly original and adheres to the university academic integrity policy.
