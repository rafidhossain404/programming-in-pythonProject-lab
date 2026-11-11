# PROJECT PROGRESS TRACKER & STATE LEDGER
> **AI Anti-Hallucination Protocol:** Any AI model resuming work on this repository MUST first read this file alongside `CONTEXT_WINDOW.md`. Check the **Current State**, verify what has already been built, and proceed directly from the **Immediate Next Task**. Do not duplicate completed work, rewrite established architectures, or introduce forbidden libraries.

---

## 1. Project Overview & Status

| Attribute | Details |
| :--- | :--- |
| **Project Title** | **AIUB-PathFinder**: Academic Performance & Degree Intelligence System |
| **Course** | CSC 4162 / BSE 4112: Programming in Python (AIUB) |
| **Current Phase** | **Phase 1: Midterm Project Complete & Submission-Ready** |
| **Midterm Target Marks** | 40 / 40 Marks (Rubric Audit Score: 40/40) |
| **Current Milestone** | **Milestones 1 through 10 Fully Completed** $\rightarrow$ Ready for Live Demo & Submission |
| **Last Updated** | 2026-11-11 |

---

## 2. Phase 1 (Midterm) Milestone Checklist

### Milestone 1: Knowledge Ingestion & Scope Audit
- [x] Extract and read all lecture slides (Lectures 01 to 10)
- [x] Extract and read Lab Manual (Labs 02 to 07)
- [x] Read Mid-Term Notes (15 Chapters, 87 pages)
- [x] Read Final-Term Notes (Pandas, DataFrames, Data Cleaning)
- [x] Analyze Project Requirements document (`Python_Midterm_Project_Requirements_Fall_26_27.pdf`)
- [x] Identify course constraints, forbidden libraries, and grading criteria

### Milestone 2: Context Window & State System
- [x] Formulate Two-Phase Data Science roadmap (Midterm pure Python + NumPy $\rightarrow$ Final Term Pandas + Matplotlib)
- [x] Create persistent master context file (`CONTEXT_WINDOW.md`)
- [x] Create persistent state tracking ledger (`PROGRESS_TRACKER.md`)

### Milestone 3: Domain Architecture & Project Specification
- [x] Finalized AIUB Academic Performance & Degree Intelligence System (**AIUB-PathFinder**)
- [x] Ingested AIUB BScCSE Curriculum (Curriculum 309 Core + 338 Electives, 101 courses)
- [x] Mapped real AIUB Grade Report (MD. RAFID HOSSAIN, 23-54787-3, 118 Cr completed, 5 current enrolled courses)

### Milestone 4: Core Domain OOP Models (`src/models.py`)
- [x] Base class `AcademicCourse` with encapsulation (`__course_code`, `__course_name`, `__credits` property validation)
- [x] Subclass `CompletedCourse` with term grades (`mtg`, `ftg`, `final_grade`, `grade_point`, `is_in_progress`)
- [x] Subclass `CurriculumCourse` with set-theoretic prerequisite parsing and domain tags
- [x] `SemesterRecord` and `StudentAcademicProfile` aggregate models with credit-weighted calculations

### Milestone 5: In-Memory Data Management & Data Structures (`src/curriculum_engine.py`)
- [x] `tuple`: Immutable AIUB grade points and academic domain classifications
- [x] `set`: Set-theoretic prerequisite fulfillment (`prereqs.issubset(completed)`), set difference for missing prerequisites
- [x] `dict`: Course code to course details lookup, normalized name aliases, domain mappings
- [x] `list`: Chronological semester progression list and unlocked course queues
- [x] Major Specialization Track Matcher (Intelligent Systems & Data Science vs Software vs Networks vs Hardware)

### Milestone 6: File Persistence & Ingestion (`src/report_parser.py`)
- [x] Ingests AIUB Grade Report from PDF (via `pypdf`) or formatted text
- [x] Auto-detects in-progress semester (2026-2027 Fall with 5 courses)
- [x] Auto-exports complete academic audit to `data/student_audit_export.json`

### Milestone 7: NumPy Numerical & Statistical Engine (`src/analytics.py`)
- [x] Statistical Overview: Mean SGPA (3.799), Median (3.760), Std Dev (0.117), Variance, Percentiles (25, 50, 75)
- [x] Linear Regression Trend: `np.polyfit(semesters, sgpas, 1)` for next-semester SGPA projection
- [x] Interactive "What-If" simulator for current enrolled courses
- [x] Domain strength vector aggregations across 6 university subject departments

### Milestone 8: Interactive User Interface (`src/ui.py` & `main.py`)
- [x] Clean, error-resilient menu system (Options 0 through 8)
- [x] ASCII horizontal bar chart visualizer for domain strengths and degree completion progress
- [x] 2D Cartesian Coordinate Plot for CGPA vs Semesters (Terminal ASCII graph matching user's sketch)
- [x] Interactive Graphical Tkinter Window popup (`src/chart_viewer.py`) plotting CGPA & SGPA curves on Canvas
- [x] Chronological progression table with momentum tracking (+0.20, -0.22, etc.)

### Milestone 9: Code Quality, Verification & Unit Testing (`tests/test_core.py`)
- [x] 10/10 comprehensive unit tests passing cleanly in 0.75s
- [x] Zero runtime crashes on unexpected inputs or piped executions
- [x] Native Desktop GUI with 60 FPS Canvas animations (dynamic line drawing, ease-out progress bars, hover tooltips)

### Milestone 10: Midterm Documentation & Viva Preparation
- [x] Formal Project Report conforming 100% to Section 13 format (`MIDTERM_PROJECT_REPORT.md`)
- [x] Viva Defense Guide with exact code line references and model answers (`VIVA_DEFENSE_GUIDE.md`)
- [x] Professional project README (`README.md`)
- [x] Verified full execution log recorded in `data/sample_run_output.txt`

---

## 3. Phase 2 (Final Term) Future Roadmap
*(Locked until Phase 1 submission and approval)*
- [ ] Ingest curriculum and grade history into Pandas DataFrames
- [ ] Handle missing and noisy grade telemetry data (`isna`, `dropna`, `fillna`)
- [ ] Exploratory Data Analysis (EDA) using Pandas groupby, pivot tables, and aggregations
- [ ] Matplotlib visualizations: Time-series grade trends, category bar charts, cohort analysis
- [ ] Predictive consumption/performance estimation and final dashboard

---

## 4. Key Architectural Decisions Log

| Decision ID | Decision Made | Rationale |
| :--- | :--- | :--- |
| **DEC-001** | Selected **AIUB-PathFinder** (Academic Performance & Degree Intelligence System) | Directly models AIUB student degree progression, grade report auditing, and curriculum prerequisite resolution. |
| **DEC-002** | Exclude Pandas and ML frameworks completely from Phase 1 | Strictly required by course guidelines (Section 10). Preserves evaluation integrity and demonstrates fundamental Python mastery. |
| **DEC-003** | Use standard library `csv` & `json` with NumPy for Phase 1 calculations | Satisfies FR-3 (Persistent data) and FR-5 (NumPy analysis) without masking core logic. |
| **DEC-004** | Pure Tkinter Desktop GUI with 60 FPS Canvas Animation Loop | Zero external dependencies; 100% syllabus safe; delivers responsive animated line graphs and progress bars. |

---

## 5. Immediate Next Task
👉 **Review with User & Final Packaging:**
1. Present the animated Desktop GUI (`desktop_app.py`) features.
2. Confirm if the user wants to package a clean submission `.zip` archive or review viva questions.
