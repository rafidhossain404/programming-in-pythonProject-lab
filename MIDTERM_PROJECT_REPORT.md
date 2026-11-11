# AMERICAN INTERNATIONAL UNIVERSITY–BANGLADESH (AIUB)
## FACULTY OF SCIENCE & TECHNOLOGY | DEPARTMENT OF COMPUTER SCIENCE
### CSC 4162 / BSE 4112: PROGRAMMING IN PYTHON | FALL 2026–27
---
# MID-TERM PROJECT REPORT
## **AIUB-PathFinder: Academic Performance & Degree Intelligence System**

---

### **1. Project Title & Student/Group Information**
- **Project Title:** AIUB-PathFinder: Academic Performance & Degree Intelligence System
- **Course Code & Title:** CSC 4162 / BSE 4112: Programming in Python
- **Semester:** Fall 2026–27
- **Course Instructor:** Md Kamrul Islam (Lecturer, Department of Computer Science)
- **Student Name:** HOSSAIN, MD. RAFID
- **Student ID:** 23-54787-3
- **Degree Program:** Bachelor of Science in Computer Science & Engineering (BSc in CSE)
- **Primary Source Code Repository:** `https://github.com/rafidhossain/programming-in-pythonProject-lab`

---

### **2. Problem Statement, Objectives, and Intended Users**

#### 2.1 Problem Statement
In undergraduate engineering programs at AIUB, students must navigate a complex curriculum comprising 148 credits across 8+ semesters. Each semester involves multiple assessment components across foundational sciences, theoretical computer science, engineering hardware, mathematics, and electives. Students and academic advisors frequently face challenges:
1. **Prerequisite Blindspots:** Students struggle to identify which core or major elective courses are currently unlocked versus which prerequisites act as academic bottlenecks.
2. **Lack of Early Trend Forecasting:** Students lack predictive tools to project how performance in ongoing courses affects their graduating CGPA and Latin Honors standing (*Magna Cum Laude* vs. *Summa Cum Laude*).
3. **Domain Strengths Uncertainty:** Transcripts present raw course grades without highlighting subject-matter strengths (e.g., Software Engineering vs. Mathematics vs. Hardware).
4. **Major Specialization Dilemma:** Near Semester 7/8, students must declare their Major Track without an objective quantitative match to their foundational performance.

#### 2.2 Objectives
The primary objective of **AIUB-PathFinder** is to develop a robust, standalone Python application that:
- Ingests official AIUB Grade Reports (PDF or TXT) and parses historical academic trajectories.
- Evaluates semester performance using **NumPy** descriptive statistics and linear regression forecasting.
- Builds a set-theoretic directed dependency engine to evaluate course unlock conditions against the official **AIUB BScCSE Curriculum (Core 309 & Electives 338)**.
- Ranks major specialization tracks and visualizes performance trends via ASCII coordinate graphs and interactive Tkinter GUI windows.

#### 2.3 Intended Users
- **AIUB Undergraduate Students:** To self-audit degree completion, plan course registration, and simulate what-if grade scenarios.
- **Academic Mentors & Faculty Advisors:** To evaluate student academic trajectories, detect performance dips, and provide data-backed pre-advising recommendations.

---

### **3. Feature List and Application Workflow/Design**

#### 3.1 Feature List
1. **Automated Grade Report Ingestion & Current Semester Detection:** Automatically reads AIUB Grade Reports, extracts student metadata, 46 completed courses across 8 semesters, and isolates the 5 ongoing enrolled courses in Fall 2026–2027.
2. **Statistical Overview & SGPA/CGPA Progression (NumPy Engine):** Computes Mean SGPA, Median, Variance, Standard Deviation ($\sigma = 0.117$), and Quartiles ($Q_1, Q_2, Q_3$). Builds a chronological progression ledger with momentum tracking.
3. **2D Coordinate Visual Line Plot (CGPA vs. Semesters):** Renders a 2D Cartesian coordinate ASCII plot in the terminal and launches an interactive **Tkinter Canvas GUI Window** plotting dual-trace curves (Cumulative CGPA in blue, Semester SGPA in dashed green).
4. **Subject Domain Strength Analysis:** Categorizes courses across 6 university departments (*CS Core, Math/Stats, Basic Science, Humanities, Hardware, Business*), computes credit-weighted domain GPAs, and renders horizontal ASCII bar diagrams.
5. **Next-Semester Predictive Forecaster & Interactive "What-If" Simulator:** Employs NumPy 1st-order polynomial linear fit (`np.polyfit`) to project next-term GPA and lets users simulate grade outcomes for currently enrolled courses.
6. **Set-Theoretic Prerequisite & Course Unlock Engine:** Evaluates prerequisite satisfaction via Python sets (`prereqs.issubset(completed)`) to show unlocked core courses, eligible electives, and preview post-current unlocks.
7. **Major Specialization Track Matcher:** Evaluates foundational grades to compute match percentages for 4 AIUB tracks (*Intelligent Systems & Data Science, Software Engineering, Hardware & Embedded Systems, Networks & Cyber Security*).
8. **Persistent Academic Audit Export:** Saves full student profiles, statistical metrics, and course states to structured JSON (`data/student_audit_export.json`).

#### 3.2 Application Architecture & Workflow Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   APPLICATION WORKFLOW                                 │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│   [AIUB Curriculum CSV] (In-System)         [AIUB Grade Report PDF / TXT] (User Input) │
│               │                                              │                         │
│               ▼                                              ▼                         │
│     CurriculumEngine (src)                        GradeReportParser (src)              │
│     • Loads 101 Courses                           • Regex Token Extraction             │
│     • Parses Prerequisite Sets                    • Ingests Semesters & Terms          │
│     • Maps Academic Domains                       • Detects Current Enrolled Load      │
│               │                                              │                         │
│               └──────────────────────┬───────────────────────┘                         │
│                                      ▼                                                 │
│                        StudentAcademicProfile (models.py)                              │
│                        • Encapsulated Courses & Semesters                              │
│                        • Credit-weighted GPAs & History                                │
│                                      │                                                 │
│               ┌──────────────────────┴──────────────────────┐                          │
│               ▼                                             ▼                          │
│    AcademicAnalyticsEngine (NumPy)               AcademicChartViewer (Tkinter)         │
│    • Mean, Std Dev, Variance, Percentiles        • 2D ASCII Terminal Cartesian Plot    │
│    • Linear Regression (np.polyfit)              • Interactive Tkinter Canvas Window   │
│    • "What-If" CGPA Simulator                    • Dual Trace: CGPA & SGPA             │
│               │                                             │                          │
│               └──────────────────────┬──────────────────────┘                          │
│                                      ▼                                                 │
│                            TerminalUI & main.py                                        │
│                            • Interactive Menu Loop (FR-1 to FR-7)                      │
│                            • JSON Persistence Export (`data/student_audit_export.json`)│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### **4. Explanation of Python Concepts Used**

1. **Variables and Data Types:** Primitive types (`int`, `float`, `str`, `bool`) represent credits, grade points, student identifiers, and completion flags with strong typing conventions.
2. **Operators:** Arithmetic operators compute weighted grade point totals (`credits * grade_point`), division computes semester SGPAs, comparison operators evaluate honors thresholds, and logical operators validate multi-condition inputs.
3. **Conditional Statements (`if-elif-else`):** Direct menu routing, validate credit boundaries ($0.0 \le \text{credits} \le 10.0$), evaluate passing grades, and assign academic stability labels based on standard deviation thresholds.
4. **Loops (`for` and `while`):** 
   - `while` loops maintain the continuous interactive menu loop with error resilience (FR-7).
   - `for` loops traverse parsed PDF text lines, iterate over course collections, compute domain aggregates, and construct 2D coordinate ASCII grid matrices.
5. **Functions and Modularity:** Application logic is partitioned into dedicated functions and class methods across 6 modules, avoiding monolithic procedural code (FR-6).

---

### **5. Data Structure Explanation: List, Tuple, Set, and Dictionary**

The application makes purposeful, non-trivial use of all four primary Python data structures:

| Data Structure | Implementation in AIUB-PathFinder | Purpose & Technical Justification |
|:---|:---|:---|
| **Tuple** | `AIUB_GRADE_POINTS = (("A+", 4.00), ("A", 3.75), ...)`<br>`ACADEMIC_DOMAINS = ("CS_CORE", "MATH_STAT", ...)` | **Immutability:** Guarantees that university grade point mappings, grade boundaries, and department categories cannot be modified or corrupted at runtime. |
| **Set** | `completed_codes = {"CSC1102", "MAT1102", ...}`<br>`course.is_unlocked() -> prereqs.issubset(completed_codes)` | **Set Theory & Deduplication:** Ensures $O(1)$ membership checks, guarantees uniqueness of course codes, and enables mathematical subset operations (`issubset`) to solve prerequisite dependencies. Also uses set difference (`difference`) to identify missing prerequisites. |
| **Dictionary** | `self.__catalog: Dict[str, CurriculumCourse]`<br>`self.__course_domain_map: Dict[str, str]` | **Key-Value Mapping:** Provides $O(1)$ associative lookup mapping course codes to object instances, normalized course title aliases, and domain aggregations. |
| **List** | `self.__courses: List[CompletedCourse]`<br>`self.__semesters: List[SemesterRecord]` | **Sequential Ordering:** Preserves the exact chronological sequence of completed semesters, maintains student grade histories, and stores output queues for table rendering. |

---

### **6. Object-Oriented Design: Class Names, Attributes, and Methods**

The software architecture implements strict Object-Oriented Programming (OOP) including Encapsulation, Inheritance, and Polymorphism:

```
                    ┌───────────────────────────┐
                    │      AcademicCourse       │ (Base Class)
                    ├───────────────────────────┤
                    │ - __course_code: str      │
                    │ - __course_name: str      │
                    │ - __credits: float        │
                    ├───────────────────────────┤
                    │ + is_passed(): bool       │
                    │ + calculate_weighted_pts()│
                    │ + get_summary(): str      │
                    └─────────────┬─────────────┘
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
   ┌───────────────────────────┐     ┌───────────────────────────┐
   │      CompletedCourse      │     │     CurriculumCourse      │
   ├───────────────────────────┤     ├───────────────────────────┤
   │ - __mtg, __ftg, __final:str│    │ - __curriculum_no: int    │
   │ - __grade_point: float    │     │ - __semester_slot: str    │
   │ - __is_in_progress: bool  │     │ - __prerequisites: Set[str│
   │ - __semester_name: str    │     │ - __domain: str           │
   ├───────────────────────────┤     ├───────────────────────────┤
   │ + simulate_grade(letter)  │     │ + is_unlocked(comp_set)   │
   │ + is_passed() [Override]  │     │ + missing_prereqs()       │
   │ + calculate_weighted_pts()│     │ + get_summary() [Override]│
   └───────────────────────────┘     └───────────────────────────┘
```

#### 6.1 `AcademicCourse` (Base Class)
- **Attributes:** Private `__course_code` (str), `__course_name` (str), `__credits` (float).
- **Encapsulation:** Uses `@property` getters and a `@credits.setter` enforcing $0.0 \le \text{credits} \le 10.0$ and type checks.
- **Polymorphism:** Defines virtual methods `is_passed()`, `calculate_weighted_points()`, and `get_summary()`.

#### 6.2 `CompletedCourse(AcademicCourse)` (Inheritance)
- **Attributes:** Adds private `__mtg`, `__ftg`, `__final_grade`, `__grade_point`, `__earned_credits`, `__is_in_progress`, `__semester_name`.
- **Methods:** Overrides `is_passed()` (checks passing status and non-in-progress state), overrides `calculate_weighted_points()` (`credits * grade_point`), and implements `simulate_grade()` for what-if scenarios.

#### 6.3 `CurriculumCourse(AcademicCourse)` (Inheritance)
- **Attributes:** Adds private `__curriculum_no`, `__curriculum_name`, `__semester_slot`, `__domain`, `__prerequisites` (Set[str]).
- **Methods:** `is_unlocked(completed_set)` tests `__prerequisites.issubset(completed_set)`; `missing_prerequisites()` returns the set difference; overrides `get_summary()`.

#### 6.4 `SemesterRecord` & `StudentAcademicProfile` (Aggregation)
- `SemesterRecord`: Encapsulates semester name, `List[CompletedCourse]`, `sgpa`, `cgpa`, and `is_current` status. Computes dynamic semester GPA.
- `StudentAcademicProfile`: Encapsulates student ID, name, degree, completed credits, CGPA, and `List[SemesterRecord]`. Provides filter methods (`get_completed_course_codes()`, `get_in_progress_courses()`, `get_sgpa_history()`).

---

### **7. File Handling and Exception Handling Explanation**

#### 7.1 File Handling
- **Curriculum Database (`data/aiub_curriculum.csv`):** Ingested using Python's built-in `csv.DictReader` to populate 101 course objects with zero third-party dependencies.
- **Grade Report Parsing (`data/sample_grade_report.txt` / `.pdf`):** Ingests native PDF grade reports using `pypdf.PdfReader` or structured text files, parsing student metadata, semesters, and course lines via compiled regular expressions.
- **Audit Persistence Export (`data/student_audit_export.json`):** Serializes the evaluated student profile, descriptive statistics, and domain analytics into indented JSON via `json.dump()`.

#### 7.2 Exception Handling & Input Validation
The application adheres strictly to FR-4 and FR-7, ensuring it never crashes on unexpected inputs:
- `FileNotFoundError`: Caught when loading curriculum or grade report files, displaying descriptive diagnostics.
- `ValueError` & `TypeError`: Raised and caught within model setters if credit values are non-numeric or out of range ($< 0.0$ or $> 10.0$).
- `(EOFError, KeyboardInterrupt)`: Handled across all interactive prompts (`input()`) so piped or interrupted CLI runs terminate cleanly.
- Menu Validation: Unrecognized menu numbers or non-numeric inputs prompt an advisory message without terminating the application.

---

### **8. Library/Module Use and Justification**

#### 8.1 Approved Library: NumPy
In strict compliance with Section 6 of the Midterm Requirements, **NumPy is used genuinely for numerical computing and statistical modeling**:
1. **Array Conversion:** Vectors of semester GPAs and earned credits are loaded into `np.ndarray` structures.
2. **Descriptive Statistics:** `np.mean()`, `np.median()`, `np.std()`, `np.var()`, and `np.percentile([25, 50, 75])` compute central tendency, variance, and distribution quartiles.
3. **Academic Stability Rating:** Uses the sample standard deviation ($\sigma = 0.117$) to classify performance consistency.
4. **Polynomial Linear Regression (`np.polyfit`):** Computes 1st-order linear regression coefficients ($y = mx + c$) across historical semester indices to project next-semester SGPA based on actual academic momentum.

#### 8.2 Standard Library Modules
- `tkinter`: Built-in GUI toolkit used to render the visual 2D line graph canvas window with axes, ticks, grid, markers, and legend.
- `csv` & `json`: Standard persistence format serialization.
- `re`: Regular expressions for pattern-matching student IDs (`XX-XXXXX-X`) and semester course rows.
- `os` & `sys`: Path resolution and command-line argument handling.

#### 8.3 External Helper: PyPDF
- `pypdf`: Lightweight PDF reader used strictly to extract raw text strings from uploaded Grade Report PDF documents.

---

### **9. Screenshots and Sample Input/Output**

*(A complete 246-line execution transcript is recorded in `data/sample_run_output.txt` and UI prototype screenshots are stored in `ui_prototype/screen.png`).*

#### 9.1 Startup & Ingestion Sample Output
```text
================================================================================
  AIUB-PathFinder | Academic Performance & Degree Intelligence System
  American International University-Bangladesh (AIUB) | Fall 2026-27
================================================================================
  [IN-SYSTEM DATA] Initializing AIUB BScCSE Curriculum Knowledge Base... DONE (101 courses registered)

  [USER INPUT REQUIRED]
  Please provide your AIUB Grade Report (Supports PDF or TXT).
  Enter file path [or press ENTER for default 'sample_grade_report.txt']: 
  Ingesting Grade Report from: 'sample_grade_report.txt'... DONE
  • Student    : HOSSAIN, MD. RAFID (ID: 23-54787-3)
  • Progress   : 46 Completed Courses (118.0 Cr) | CGPA: 3.81
  • In-Progress: 5 Ongoing Courses (15.0 Cr)
```

#### 9.2 2D Coordinate Visual Line Plot Sample Output (Option 3)
```text
  CGPA
  4.00 ┤                                                 
  3.97 ┤                                                 
  3.94 ┤  ●╲                                             
  3.91 ┤    ╲                                            
  3.88 ┤     ╲╲╲   ╱╱╱●╲╲╲                               
  3.85 ┤        ●╱╱       ╲╲●─────●─────●╲╲              
  3.81 ┤                                   ╲╲╲●─────●    
  3.78 ┤                                                 
  3.75 ┤                                                 
       └──────────────────────────────────────────────────▶
         S1    S2    S3    S4    S5    S6    S7    S8    
                        semesters
```

#### 9.3 Subject Domain Strengths Sample Output (Option 4)
```text
  CS & Software Engineering        [3.88 / 4.00]  ███████████████████░  [Outstanding Mastery] (50.0 Cr)
  Mathematics & Statistics         [3.82 / 4.00]  ██████████████████░░  [High Proficiency]    (21.0 Cr)
  Basic Natural Sciences (Phy/Chm) [3.79 / 4.00]  █████████████████░░░  [High Proficiency]    (14.0 Cr)
  Humanities, Languages & Ethics   [3.78 / 4.00]  █████████████████░░░  [High Proficiency]    (18.0 Cr)
  Hardware, Circuits & Arch        [3.65 / 4.00]  ████████████████░░░░  [High Proficiency]    (22.0 Cr)
  Business, Economics & Management [3.63 / 4.00]  ████████████████░░░░  [Solid Competence]    ( 8.0 Cr)
```

#### 9.4 Major Specialization Track Matcher Sample Output (Option 7)
```text
  #1 Intelligent Systems & Data S  [90.30 / 100.00]  ████████████████░░ % | GPA: 3.94 [Prime Alignment / Highly Recommended]
     Description: Focus on Machine Learning, NLP, Data Mining, Computer Vision, and AI.
     Foundations Cleared: 4/4 | Unlocked Electives: 5
     Top Unlocked Options: COE4231 (IMAGE PROCESSING), CSC4230 (BIOINFORMATICS), CSC4180 (INTRODUCTION TO DATA SCIENCE)
```

---

### **10. Limitations, Societal Benefit, and Future Improvements**

#### 10.1 Societal & Educational Benefit
- **Academic Retention:** Provides early academic risk awareness, reducing unexpected probation risks by highlighting cumulative GPA momentum.
- **Empowered Advising:** Helps students make informed, strategic choices during pre-advising rather than registering for random electives.
- **Optimized Graduation Runway:** Clarifies exactly what 15 credits are needed to complete the 148-credit degree.

#### 10.2 Current Limitations (Phase 1)
- **Single Curriculum Scope:** Currently models Curriculum 309 (Core) and 338 (Electives) for BScCSE; other AIUB departments (BBA, EEE) require their own curriculum CSV mappings.
- **No Direct Web Interface in Phase 1:** Operates via terminal CLI and Tkinter GUI popups rather than a full browser web application (reserved for Phase 2).

#### 10.3 Phase 2 (Final Term) Future Roadmap
1. **Pandas Integration:** Ingest persistent JSON/CSV logs into Pandas DataFrames for advanced filtering, missing grade imputation (`fillna`), and cross-semester pivot tables.
2. **Matplotlib & Seaborn Visualizations:** Replace terminal ASCII charts with high-resolution exportable graphics (CGPA curves with confidence intervals, department radar charts, and grade distribution histograms).
3. **Web Dashboard Integration:** Connect the newly created **Stitch UI Prototype** (`ui_prototype/code.html`) with a lightweight Python backend for interactive browser-based grade report auditing.
4. **Cohort Analytics:** Extend the engine to analyze multi-student cohorts, generating bell-curve grade distributions and course difficulty analytics for faculty members.

---
**End of Midterm Project Report.**
