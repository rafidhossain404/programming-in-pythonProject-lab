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

* **Status:** Phase 1 is **100% complete and verified**. All 10 unit tests pass. Git commits are clean on `main`.
* **GUI Architecture:** Dual-mode — Stitch HTML Dashboard (primary, via `pywebview` Edge WebView2) + Tkinter Canvas (fallback). `main.py` defaults to GUI; `--cli` for terminal.

| File Path | Purpose | Key Details |
| :--- | :--- | :--- |
| [`main.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/main.py) | Application Entry Point | `python main.py` → launches GUI (Stitch dashboard). `--cli` / `-c` → terminal menu. `--tkinter` → Tkinter fallback GUI. |
| [`desktop_app.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/desktop_app.py) | Desktop GUI Layer | `PathFinderDesktopApp` (Tkinter 60fps animated GUI) + `PathFinderBridge` (pywebview JS↔Python IPC bridge) + `launch_stitch_gui()`. |
| [`src/models.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/models.py) | OOP Domain Classes | `AcademicCourse` (Base) $\rightarrow$ `CompletedCourse` & `CurriculumCourse`; `SemesterRecord`, `StudentAcademicProfile`. Encapsulation with `@property` and validation setters. |
| [`src/curriculum_engine.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/curriculum_engine.py) | Prerequisite & Track Matcher | Uses **Python Sets** (`prereqs.issubset(completed)`). Ranks 4 AIUB tracks (#1 Intelligent Systems: 90.3% match). |
| [`src/analytics.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/analytics.py) | NumPy Analytical Engine | Mean ($3.799$), Median ($3.760$), Std Dev ($\sigma = 0.117$), `np.polyfit()` linear regression slope, and "What-If" simulator. |
| [`src/report_parser.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/report_parser.py) | PDF / TXT Ingestion | Reads PDF (via `pypdf`) or TXT, regex course matching, title alias resolution (51/51 courses matched). |
| [`src/chart_viewer.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/chart_viewer.py) | Visual 2D Plot | Terminal 2D Cartesian ASCII graph + Tkinter Canvas GUI popup window plotting CGPA & SGPA dual curves. |
| [`src/ui.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/ui.py) | Presentation Layer | Formatted ASCII tables, horizontal bar diagrams, degree completion bars. |
| [`tests/test_core.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/tests/test_core.py) | Unit Test Suite | 10 unit tests verifying models, validation, sets, NumPy, parser, and ASCII plotting. |
| [`data/aiub_curriculum.csv`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/aiub_curriculum.csv) | In-System Curriculum | 101 AIUB courses with credit splits, lecture/lab hours, and prerequisites. |
| [`data/sample_grade_report.txt`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/sample_grade_report.txt) | Default Student Transcript | Full transcript of MD. RAFID HOSSAIN (118 credits completed + 15 ongoing). |
| [`data/student_audit_export.json`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/student_audit_export.json) | Exported Audit | Serialized persistent audit ledger generated by Option 8. |
| [`data/sample_run_output.txt`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/data/sample_run_output.txt) | Verification Log | 246-line captured console transcript of all 8 menu operations executing cleanly. |
| [`stitch_dashboard/`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/stitch_dashboard/) | Stitch Desktop Dashboard | `code.html` (1325-line interactive HTML dashboard), `tailwind.min.js` (local Tailwind bundle), `DESIGN.md`, `screen.png`. Loaded by `pywebview` as native desktop window. |
| [`ui_prototype/`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/ui_prototype/) | UI Prototype Copy | Mirror of `stitch_dashboard/` for archival. |
| [`MIDTERM_PROJECT_REPORT.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/MIDTERM_PROJECT_REPORT.md) | Official Report | 10-point formal report strictly following Section 13 of the AIUB Midterm syllabus. |
| [`VIVA_DEFENSE_GUIDE.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/VIVA_DEFENSE_GUIDE.md) | Viva Preparation | 3-minute demo script + model answers for likely viva questions (OOP, Sets, NumPy). |
| [`README.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/README.md) | Project Overview | Installation, run commands, feature list, and architecture summary. |
| [`PROGRESS_TRACKER.md`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/PROGRESS_TRACKER.md) | Milestone Checklist | Milestones 1–10 all marked complete. |

---

## 5. Dependencies

| Package | Version | Purpose |
| :--- | :--- | :--- |
| `numpy` | 2.5.4 | Statistical analysis (mean, median, std dev, polyfit) |
| `pypdf` | 7.0.1 | PDF grade report parsing |
| `pywebview` | 6.2.1 | Native desktop window wrapping Stitch HTML (Edge WebView2 on Windows) |
| `pillow` | 13.0.0 | Image support (optional) |

---

## 6. Architectural Decisions (Resolved)

| Decision ID | Decision Made | Rationale |
| :--- | :--- | :--- |
| **DEC-001** | Selected **AIUB-PathFinder** (Academic Performance & Degree Intelligence System) | Directly models AIUB student degree progression, grade report auditing, and curriculum prerequisite resolution. |
| **DEC-002** | Exclude Pandas and ML frameworks completely from Phase 1 | Strictly required by course guidelines (Section 10). Preserves evaluation integrity and demonstrates fundamental Python mastery. |
| **DEC-003** | Use standard library `csv` & `json` with NumPy for Phase 1 calculations | Satisfies FR-3 (Persistent data) and FR-5 (NumPy analysis) without masking core logic. |
| **DEC-004** | **Stitch HTML Dashboard via `pywebview`** as primary GUI; Tkinter Canvas as fallback | User requested "I want the UI exactly like this" (Stitch prototype). `pywebview` wraps HTML in a native Edge WebView2 desktop window — no web server, no browser tab. Desktop app, NOT web app. Tkinter preserved as `--tkinter` fallback for midterm compliance. |
| **DEC-005** | Keep existing 6-file `src/` structure (not consolidated) | User chose Option B. Retains clear separation of concerns for viva defense. |
| **DEC-006** | All dashboard features on one scrollable page (not tabbed) | User explicitly requested "all function in one page". Stitch HTML has: KPI Cards, CGPA Chart (SVG), Domain Strengths, Track Matcher, What-If Simulator, Prerequisite Engine — all visible without navigation. |
| **DEC-007** | **Zero-Hardcoding Live Dynamic Hydration** | Dashboard automatically binds to `window.pywebview.api.get_dashboard_data()` on launch. Updates student metadata, KPIs, What-If courses, Domain Strengths, and Track Matcher dynamically from the active parsed file. |
| **DEC-008** | **Native PDF Layout Reconstitution** | `GradeReportParser._extract_text_from_pdf()` reconstitutes AIUB's multi-line columnar PDF tokens into single-line course structures, enabling seamless ingestion of official PDF grade reports with 100% course recovery. |

---

## 7. Stitch Dashboard Architecture (Primary GUI)

* **Entry**: `python main.py` → `desktop_app.launch_stitch_gui()` → `pywebview.create_window(url='stitch_dashboard/code.html', js_api=bridge)`
* **Bridge**: `PathFinderBridge` class exposes Python OOP backend to JavaScript via `window.pywebview.api`:
  * `get_dashboard_data()` — Serializes profile, analytics, domains, tracks, unlocked courses, enrolled courses
  * `simulate_grades(grades)` — What-If CGPA simulator
  * `upload_grade_report()` — Native file dialog for new PDF/TXT ingestion
  * `export_audit()` — Exports audit JSON via `TerminalUI.export_audit_report()`
* **HTML Features** (all interactive, IDs wired in `<script>` block):
  * 4 KPI cards (CGPA, Degree %, Enrolled Load, Consistency σ)
  * SVG CGPA chart with hover tooltips (`chart-tooltip`, `chart-node` class)
  * Domain strength horizontal bars
  * Track matcher with match % and fit labels
  * What-If simulator with grade dropdowns + preset buttons (`preset-all-aplus`, `preset-expected`, `preset-conservative`)
  * Prerequisite engine with 3 tab switcher: Core / Electives / Unlocks After Passing
  * Upload / Audit / Download buttons with toast notifications

---

## 8. How to Run & Verify

```powershell
# Install dependencies (first time)
pip install numpy pypdf pywebview pillow

# Run unit tests (All 10 pass)
python -m unittest tests/test_core.py

# Launch application (Stitch Desktop Dashboard — default)
python main.py

# Launch CLI terminal mode
python main.py --cli

# Launch Tkinter fallback GUI
python main.py --tkinter
```

---

## 9. Known Issues & Notes

* `pywebview` WebView2 may emit `E_ABORT` during `window.destroy()` — cosmetic, no functional impact.
* Stitch HTML uses Google Fonts CDN (Inter, JetBrains Mono) and Material Symbols. Offline-only environments will get fallback system fonts.
* Tailwind CSS loads from local `tailwind.min.js` first, CDN fallback if missing.

---

## 10. Phase 2 (Final Term) Future Roadmap
*(Locked until Phase 1 submission and approval)*
- [ ] Ingest curriculum and grade history into Pandas DataFrames
- [ ] Handle missing and noisy grade telemetry data (`isna`, `dropna`, `fillna`)
- [ ] Exploratory Data Analysis (EDA) using Pandas groupby, pivot tables, and aggregations
- [ ] Matplotlib visualizations: Time-series grade trends, category bar charts, cohort analysis
- [ ] Connect live Python data to Stitch Dashboard via `PathFinderBridge` for real-time updates
