# SYSTEM CONTEXT & COURSE KNOWLEDGE BASE
> **Mandatory AI Instruction:** Any AI model interacting with this project MUST read this file in full before proposing, writing, or modifying any code or documentation. This document establishes the non-negotiable boundaries, constraints, syllabus scopes, and project architecture for CSC 4162 / BSE 4112.

---

## 1. Course Information & Metadata

- **Institution:** American International University–Bangladesh (AIUB)
- **Faculty:** Faculty of Science and Technology (FST) | Department of Computer Science (CS)
- **Course Code & Title:** CSC 4162 / BSE 4112: Programming in Python
- **Credits & Contact:** 3 Credit Hours (2 hrs Theory + 2 hrs 20 mins Lab per week)
- **Prerequisite:** CSC 3215 / BSE 1201 (Web Technologies)
- **Curriculum Role:** Elective for CSE; Core for Data Science (DS) and Computer Networks & Cyber Security (CNCS)
- **Course Instructor:** Md Kamrul Islam (Lecturer & AI Researcher, Room: 9210K, Email: `mdkamrul.islam@aiub.edu`)
- **Student / Author:** Mohsin Ibna Hossain

---

## 2. Project Architecture: The Two-Phase Strategy

The project is structured in **two consecutive phases** that form a continuous, cohesive software lifecycle:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             TWO-PHASE PROJECT ROADMAP                            │
├────────────────────────────────────────┬─────────────────────────────────────────┤
│          PHASE 1: MID-TERM             │           PHASE 2: FINAL TERM           │
├────────────────────────────────────────┼─────────────────────────────────────────┤
│ • Focus: Core Python Fundamentals      │ • Focus: Data Science & Analytics       │
│ • Raw Data Structures (List, Tuple,    │ • High-Level Data Science Stack         │
│   Set, Dictionary)                     │ • Pandas (DataFrames, Series, Cleaning, │
│ • Object-Oriented Programming (OOP):   │   Grouping, Merging, Filtering)         │
│   Encapsulation, Inheritance, Poly.    │ • Matplotlib (Visualizations, Trends,   │
│ • Custom File I/O (CSV / JSON / TXT)   │   Distribution Plots, Multi-plots)      │
│ • Exception Handling & Data Validation │ • Advanced NumPy (Matrix/Vector Ops)    │
│ • Approved Numerical Lib: NumPy only   │ • Statistical Inference & Predictive    │
│ • Menu-driven CLI / Clean Interface    │   Analytics / Dashboard Integration     │
└────────────────────────────────────────┴─────────────────────────────────────────┘
```

---

## 3. Midterm Project Requirements & Evaluation Criteria

### 3.1 Key Parameters
- **Assessment Type:** Group Project (Total: 40 Marks)
- **Target Goal:** Build a working Python application addressing a practical, societal problem with persistent storage, structured logic, and numerical calculations.
- **Evaluation Principle:** Marks are based on correctness, clean code modularity, robust data structures, and the ability to explain implementation during viva — **not visual flashiness alone**.

### 3.2 Required Python Concepts (Checklist)
| Concept | Mandatory Implementation Requirement |
| :--- | :--- |
| **Variables & Types** | Meaningful storage of identifiers, records, numerical values, categories, flags |
| **Operators** | Arithmetic calculations, comparison checks, logical conditions, running aggregates |
| **Control Flow** | `if`, `elif`, `else` for validation, branch navigation, record filtering |
| **Loops** | `while` for interactive runtime menus; `for` for traversing collections/records |
| **Functions** | Modularity: Input parsing, validation, CRUD operations, calculation, file ops |
| **Lists** | Primary collections for records, transaction history, metric sequences |
| **Tuples** | Immutable configurations, fixed categories, status enumeration, coordinate pairs |
| **Sets** | Unique ID tracking, duplicate prevention, category membership validation |
| **Dictionaries** | Key-value record representations, category lookup tables, index maps |
| **File Handling** | Persistent storage using `.csv` or `.json` (min 10 sample records, create on missing) |
| **Exception Handling** | Robust `try-except-else-finally` catching `ValueError`, `FileNotFoundError`, `KeyError` |
| **OOP** | Minimum 1-2 rich domain classes (Encapsulation with private attrs, Inheritance, Polymorphism) |
| **Approved Library** | **NumPy ONLY** for statistical computations (mean, median, std, min, max, percentiles) |

### 3.3 Functional Requirements (FR-1 through FR-7)
1. **FR-1: User Interaction:** Clear, error-resilient menu-driven interface with structured prompts and feedback.
2. **FR-2: Minimum 5 Operations:** Add record, View all records, Search/Filter, Update record, Delete record, Numerical summary calculation, Save/Export data.
3. **FR-3: Persistent Data:** Records must be persisted in CSV/JSON. Restarting the program must retain data.
4. **FR-4: Validation:** Reject negative numbers, empty required strings, duplicate IDs (using `set`), invalid categories.
5. **FR-5: Analysis & Calculation:** Compute descriptive metrics (mean, median, standard deviation, extremes) using NumPy arrays.
6. **FR-6: Structured Architecture:** Separation of concerns: Data Model Classes $\rightarrow$ Service/Manager Class $\rightarrow$ I/O Utility $\rightarrow$ Menu Interface.
7. **FR-7: Error Recovery:** The application must never crash on user typos or missing files.

### 3.4 Official Mark Distribution (40 Marks Total)
- **Problem Overview & Design:** 4 Marks
- **User Interaction & Interface:** 5 Marks
- **Variables, Operators, Conditionals & Loops:** 4 Marks
- **Functions & Modularity:** 4 Marks
- **Data Structures (List, Tuple, Set, Dict):** 5 Marks
- **File Handling & Persistence:** 4 Marks
- **Exception Handling & Validation:** 3 Marks
- **Object-Oriented Programming (OOP):** 5 Marks
- **Library/Module Use & Analysis (NumPy):** 4 Marks
- **Code Quality, Report & Viva Readiness:** 2 Marks

---

## 4. Strict Boundaries & FORBIDDEN Topics

> [!CAUTION]
> **STRICT COMPLIANCE RULES (DO NOT VIOLATE):**
> 1. **FORBIDDEN IN MIDTERM:**
>    - **NO Pandas** (DataFrames, Series, `pd.read_csv` are strictly reserved for Final Term).
>    - **NO Scikit-Learn / Machine Learning models**.
>    - **NO Heavy Web Frameworks** (Django, FastAPI, Flask).
>    - **NO Database ORMs / SQL engines** (SQLAlchemy, SQLite) unless purely optional file exports.
>    - **NO External non-standard libraries** without approval (e.g., requests, beautifulsoup, seaborn).
> 2. **PERMITTED IN MIDTERM:**
>    - Standard library: `math`, `random`, `datetime`, `os`, `sys`, `csv`, `json`, `re`.
>    - Course-approved numerical library: **`numpy`**.
>    - Built-in GUI module: `tkinter` (optional, but clean CLI is preferred for core evaluation).
> 3. **ACADEMIC INTEGRITY:**
>    - Code must be clear, idiomatic Python with no obfuscation or AI hallucinations.
>    - Every function, method, and data structure must be easily defendable in viva.

---

## 5. Course Syllabus Reference

### Midterm Syllabus (Lectures 01–09, Labs 02–07, Notes Ch 1–15)
- **Ch 1:** Python Introduction, Character set, Variables, Data Types, Operators, Casting, Input/Output.
- **Ch 2:** Strings, Indexing, Slicing, String Methods (`upper`, `lower`, `strip`, `replace`, `find`, `count`).
- **Ch 3:** Conditionals (`if`, `if-else`, `if-elif-else`, nested conditions, logical operators).
- **Ch 4:** Loops (`for`, `while`, `range`, iteration, summation patterns).
- **Ch 5:** Loop Control (`break`, `continue`, `pass`, single-line print with `end=`).
- **Ch 6:** Lists (indexing, slicing, `append`, `insert`, `extend`, `remove`, `pop`, `sort`, `reverse`, copy).
- **Ch 7:** Tuples (immutability, single-item comma rule, `count`, `index`, conversion).
- **Ch 8:** Dictionaries (`keys`, `values`, `items`, `get`, `pop`, nested dictionaries).
- **Ch 9:** Sets (uniqueness, duplicate elimination, `add`, `remove`, `discard`, union `|`, intersection `&`, difference `-`).
- **Ch 10:** Functions (parameters, default arguments, return values, docstrings).
- **Ch 11:** Recursion (base case, recursive step, call stack).
- **Ch 12:** Object-Oriented Programming (Classes, Objects, `__init__`, `self`, Encapsulation with private `__attr`, Getters/Setters, Inheritance: Single/Multilevel/Multiple, `super()`, Abstraction with `abc`, Polymorphism, `@staticmethod`, `@classmethod`).
- **Ch 13:** File I/O (`open`, modes `r/w/a/x`, `with` statement, `read`, `readline`, `readlines`, `write`, `writelines`, `os.remove`).
- **Ch 14:** Modules & Imports (`math`, `random`, `datetime`, `os`, `sys`).
- **Ch 15:** Virtual Environments (`venv`, `activate`, `requirements.txt`).
- **Introductory NumPy (Lecture 10):** `ndarray`, shape, dimensions, slicing, vector operations, `sum`, `mean`, `min`, `max`, `std`.

### Final Term Syllabus (Notes & Advanced Lectures)
- **Pandas:** Series & DataFrame creation, CSV/Excel/JSON loading (`read_csv`, `read_excel`, `read_json`), Data Inspection (`head`, `tail`, `info`, `describe`, `shape`, `columns`, `nunique`), Indexing (`loc`, `iloc`), Filtering & Boolean Masking, Missing Data Cleaning (`isna`, `dropna`, `fillna`), Deduplication (`drop_duplicates`), Feature Engineering & Column Transformations.
- **NumPy Advanced:** Multi-dimensional manipulations, broadcasting, boolean indexing, mathematical transformations.
- **Matplotlib / Visualization:** Line charts, bar graphs, histograms, scatter plots, subplots, titles, labels, legends, exporting visual figures.

---

## 6. Official Selected Project: "AIUB-PathFinder"
**Domain:** Higher Education & Academic Performance Analytics (High University & Societal Impact)

### Why this project?
1. **Midterm Phase (Phase 1) - Fully Built & Verified:**
   - Ingests real AIUB Grade Report PDFs and the AIUB BScCSE Curriculum (Core 309 & Electives 338, 101 courses).
   - **OOP Design:** Base class `AcademicCourse`, derived classes `CompletedCourse` (encapsulating term grades and grade points) and `CurriculumCourse` (encapsulating prerequisite sets and domain classifications), aggregated by `SemesterRecord` and `StudentAcademicProfile`.
   - **Data Structures:**
     - `list`: Chronological semester progression list and unlocked course queues.
     - `tuple`: Fixed AIUB grading scale `((90, 4.0, "A+"), ...)` and academic domains.
     - `set`: Set-theoretic prerequisite satisfaction (`prereqs.issubset(completed)`), set difference for missing prerequisites, and set intersections for track matching.
     - `dict`: Course code lookup dictionary, normalized name aliases, and domain strength aggregates.
   - **NumPy Numerical Engine:** Computes descriptive statistics (Mean SGPA, Median, Std Dev, Variance, Percentiles) and 1st-order linear regression (`np.polyfit`) for next-semester SGPA projection.
   - **Interactive What-If Simulator:** Dynamically computes how grades in current enrolled courses impact the graduating CGPA.
   - **Major Specialization Track Matcher:** Evaluates foundation course performance across 4 AIUB tracks (Intelligent Systems & Data Science, Software Engineering, Networks & Security, Hardware & Robotics).
   - **Interface:** Terminal UI with ASCII horizontal bar charts and error recovery.

2. **Final Term Phase (Phase 2 Roadmap):**
   - Ingest the saved `student_audit_export.json` and curriculum CSV directly into Pandas DataFrames.
   - Advanced exploratory data analysis (EDA): Course difficulty clustering, correlation between credit load and semester GPA.
   - Generate Matplotlib figures: Time-series SGPA vs CGPA curves, colored department strength bar charts, and prerequisite dependency graphs.

---

## 7. Rules for AI Collaborators
1. **Always check `PROGRESS_TRACKER.md`** before suggesting changes or taking actions.
2. **Never skip validation** or leave unhandled exceptions.
3. **Never introduce forbidden libraries** (especially Pandas or Sklearn) during Phase 1.
4. **Ensure 100% testability:** Write clean, modular, runnable code with zero syntax or runtime errors.
5. **Update `PROGRESS_TRACKER.md`** at the conclusion of every meaningful milestone.
