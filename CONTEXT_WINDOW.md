# MASTER CONTEXT & AI SESSION HANDOVER
> **CRITICAL INSTRUCTION FOR INCOMING AI MODEL:**  
> Read this file first. It contains the complete state, technical constraints, data schemas, user preferences, and pending decisions for this repository. Do NOT hallucinate new requirements, do NOT introduce forbidden libraries (no Pandas in Phase 1), and follow `/ponytail` mode (build the smallest working diff, avoid extra code, and ask the user before making architectural decisions).

---

## 1. User & Course Metadata

| Key | Value |
| :--- | :--- |
| **Student Name** | HOSSAIN, MD. RAFID |
| **Student ID** | `23-54787-3` |
| **University** | American International University–Bangladesh (AIUB) |
| **Department** | Faculty of Science & Technology (FST) \| Department of Computer Science |
| **Course Code & Title**| **CSC 4162 / BSE 4112: Programming in Python** |
| **Semester** | Fall 2026–27 |
| **Course Instructor** | Md Kamrul Islam (Lecturer & AI Researcher, Room: 9210K) |
| **Active Mode** | `/ponytail` (Lazy senior dev mode: least code, zero bloat, ask user for decisions) |

---

## 2. Project Identity: AIUB-PathFinder

* **What it does:** Standalone Python academic performance auditor & degree intelligence system for AIUB BScCSE students.
* **Input Architecture:**
  * **In-System Data (Built-in):** `data/aiub_curriculum.csv` (101 courses: Core 309 + Electives 338 with prerequisite mappings). The user NEVER supplies this file; it is internal.
  * **User Input (Single File):** The user ONLY inputs their AIUB Grade Report (`.pdf` or `.txt`). A pre-extracted sample report (`data/sample_grade_report.txt`) is bundled as default.
* **Current Student State Parsed:**
  * Completed Credits: $118.0 / 148.0$ ($79.7\%$ degree completed).
  * Current CGPA: $3.81 / 4.00$ (*Magna Cum Laude* track).
  * 46 completed courses across 8 semesters ($2023\text{--}2024\text{ Fall}$ to $2025\text{--}2026\text{ Summer}$).
  * **Current Ongoing Semester:** $2026\text{--}2027\text{ Fall}$ with 5 courses ($15.0\text{ Cr}$):
    1. `MGT3202` — Engineering Management (3.0 Cr)
    2. `CSC4180` — Introduction to Data Science (3.0 Cr)
    3. `CSC4232` — Machine Learning (3.0 Cr)
    4. `CSC4162` — Programming in Python (3.0 Cr)
    5. `COE3103` — Data Communication (3.0 Cr)

---

## 3. Strict Syllabus Boundaries (Non-Negotiable)

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             TWO-PHASE ARCHITECTURE                               │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│          PHASE 1: MID-TERM (CURRENT)   │           PHASE 2: FINAL TERM           │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • Pure Python OOP (classes, inherit,   │ • Pandas (DataFrames, Series, cleaning, │
│   encapsulation, polymorphism)         │   missing data imputation, groupby)     │
│ • Raw Data Structures:                 │ • Matplotlib & Seaborn visual charts    │
│   list, tuple, set, dict               │ • Advanced statistical hypothesis tests │
│ • File Handling: csv, json, txt        │ • Live Web Dashboard (connecting the    │
│ • Exception Handling: try-except       │   Stitch UI prototype in `ui_prototype`)│
│ • Approved Library: **NumPy ONLY**     │                                         │
│ • Approved GUI: **Tkinter Canvas**     │                                         │
│ • **STRICTLY FORBIDDEN IN MIDTERM:**   │                                         │
│   NO Pandas, NO Scikit-Learn, NO heavy │                                         │
│   web frameworks (Django/Flask), NO    │                                         │
│   database ORMs.                       │                                         │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 4. Current Codebase Map & Status

* **Status:** Phase 1 is **100% complete and verified**. All 9 unit tests pass in $0.04\text{s}$. Git commits are clean on `main`.

| File Path | Purpose | Key Details |
| :--- | :--- | :--- |
| [`main.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/main.py) | Application Entry Point | Interactive menu (Opts 0–8), error-resilient input loop (`EOFError` safe). |
| [`src/models.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/models.py) | OOP Domain Classes | `AcademicCourse` (Base) $\rightarrow$ `CompletedCourse` & `CurriculumCourse`; `SemesterRecord`, `StudentAcademicProfile`. Encapsulation with `@property` and validation setters. |
| [`src/curriculum_engine.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/curriculum_engine.py) | Prerequisite & Track Matcher | Uses **Python Sets** (`prereqs.issubset(completed)`). Ranks 4 AIUB tracks (#1 Intelligent Systems: 90.3% match). |
| [`src/analytics.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/analytics.py) | NumPy Analytical Engine | Mean ($3.799$), Median ($3.760$), Std Dev ($\sigma = 0.117$), `np.polyfit()` linear regression slope, and "What-If" simulator. |
| [`src/report_parser.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/report_parser.py) | PDF / TXT Ingestion | Reads PDF (via `pypdf`) or TXT, regex course matching, title alias resolution (51/51 courses matched). |
| [`src/chart_viewer.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/chart_viewer.py) | Visual 2D Plot | Terminal 2D Cartesian ASCII graph + Tkinter Canvas GUI popup window plotting CGPA & SGPA dual curves. |
| [`src/ui.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/ui.py) | Presentation Layer | Formatted ASCII tables, horizontal bar diagrams, degree completion bars. |
| [`tests/test_core.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/tests/test_core.py) | Unit Test Suite | 9 unit tests verifying models, validation, sets, NumPy, parser, and ASCII plotting. |
| [`data/aiub_curriculum.csv`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/aiub_curriculum.csv) | In-System Curriculum | 101 AIUB courses with credit splits, lecture/lab hours, and prerequisites. |
| [`data/sample_grade_report.txt`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/sample_grade_report.txt) | Default Student Transcript | Full transcript of MD. RAFID HOSSAIN (118 credits completed + 15 ongoing). |
| [`data/student_audit_export.json`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/student_audit_export.json) | Exported Audit | Serialized persistent audit ledger generated by Option 8. |
| [`data/sample_run_output.txt`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/sample_run_output.txt) | Verification Log | 246-line captured console transcript of all 8 menu operations executing cleanly. |
| [`ui_prototype/`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/ui_prototype/) | Stitch Web UI Export | User's generated Stitch UI prototype: `code.html`, `screen.png`, `DESIGN.md`. |
| [`MIDTERM_PROJECT_REPORT.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/MIDTERM_PROJECT_REPORT.md) | Official Report | 10-point formal report strictly following Section 13 of the AIUB Midterm syllabus. |
| [`VIVA_DEFENSE_GUIDE.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/VIVA_DEFENSE_GUIDE.md) | Viva Preparation | 3-minute demo script + model answers for likely viva questions (OOP, Sets, NumPy). |
| [`README.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/README.md) | Project Overview | Installation, run commands, feature list, and architecture summary. |
| [`PROGRESS_TRACKER.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/PROGRESS_TRACKER.md) | Milestone Checklist | Milestones 1–10 all marked complete. |

---

## 5. Active Ponytail Decisions on Deck

When the user gives their next prompt, resolve these **two decisions**:

1. **Architecture Decision:**
   * Option A (Consolidated / Lean — Ponytail default): Merge `src/` into 3 concise files (`core.py`, `analytics.py`, `main.py`) reducing codebase size from ~1,200 lines to ~350 lines with zero bloat.
   * Option B (Keep Current): Retain the existing 6-file structure in `src/`.

2. **Interface Delivery Decision:**
   * Option A (Terminal + Tkinter Canvas — Midterm safe): Retain CLI menu + Tkinter Canvas popup (100% compliant with Midterm syllabus).
   * Option B (Serve Stitch Web Dashboard): Connect `ui_prototype/code.html` via a minimal built-in Python `http.server`.

---

## 6. How to Run & Verify Immediately

```powershell
# Run unit tests (All 9 pass in 0.04s)
python -m unittest tests/test_core.py

# Run application
python main.py
```
