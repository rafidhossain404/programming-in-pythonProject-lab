# AIUB-PathFinder: Viva Defense & Code Explanation Guide
> **CSC 4162 / BSE 4112: Programming in Python | Fall 2026–27**  
> **Examiner / Instructor:** Md Kamrul Islam | **Student:** HOSSAIN, MD. RAFID (`23-54787-3`)

This document prepares you for likely viva questions during your midterm project demonstration. Each question is paired with a clear, technically sound answer referencing your actual codebase.

---

## 🎯 1. Demonstration Walkthrough (How to Present Live in 3 Minutes)

1. **Step 1: Launch the Program**
   ```powershell
   python main.py
   ```
   *Explain to the teacher:* "The application immediately initializes the in-system AIUB BScCSE Curriculum database (101 courses). Then it prompts for an AIUB Grade Report PDF or text file. If I press Enter, it automatically ingests my real grade report."

2. **Step 2: Show Feature 1 (Profile & Ongoing Detection)**
   *Press `1`.*
   *Explain:* "Notice that it computed 79.7% degree completion (118/148 credits) and automatically isolated the 5 courses I am currently enrolled in for Fall 2026-27 (including this Python course, CSC 4162!)."

3. **Step 3: Show Feature 2 & 3 (NumPy Statistics & 2D Line Plot)**
   *Press `2` then `3`.*
   *Explain:* "Here, NumPy computes my descriptive statistics (Mean SGPA 3.80, Median 3.76, and consistency $\sigma = 0.117$). When I press 3, it renders a 2D Cartesian Coordinate Graph of my CGPA across all semesters. I can also press 'Y' to launch the interactive Tkinter Canvas window showing the visual curve with data point annotations and legend."

4. **Step 4: Show Feature 5 (Set-Theoretic Prerequisite Engine)**
   *Press `6` (Course Unlocks).*
   *Explain:* "This answers what courses are unlocked for me right now using Python set subset operations, and simulates what becomes unlocked after passing my 5 current courses—for example, passing Python unlocks Natural Language Processing (CSC 4233)!"

5. **Step 5: Show Feature 6 (Major Track Matcher)**
   *Press `7`.*
   *Explain:* "It evaluates my past foundation grades and ranks the 4 AIUB BScCSE elective specializations. It correctly identified Intelligent Systems & Data Science as my top match with a 90.3% compatibility score!"

6. **Step 6: Show File Persistence & Exit**
   *Press `8` then `0`.*
   *Explain:* "It exports a complete JSON audit file to `data/student_audit_export.json` and cleanly exits without crashing."

---

## 💬 2. Anticipated Viva Questions & Model Answers

### Question 1: "Where and why did you use Object-Oriented Programming (OOP)?"
> **Your Answer:**  
> "In [`src/models.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/models.py), I created a base class `AcademicCourse` and two derived subclasses: `CompletedCourse` and `CurriculumCourse`.
> - **Encapsulation:** All attributes (`__course_code`, `__course_name`, `__credits`, `__grade_point`) are private. I used Python `@property` getters and a `@credits.setter` that strictly validates that credits must be a float between $0.0$ and $10.0$.
> - **Inheritance:** `CompletedCourse` extends `AcademicCourse` by adding term grades (`mtg`, `ftg`, `final_grade`) and dynamic passed status checks. `CurriculumCourse` extends it by adding prerequisite sets and domain categories.
> - **Polymorphism:** The base class defines `is_passed()`, `calculate_weighted_points()`, and `get_summary()`. Both subclasses override these methods to provide specialized behavior."

---

### Question 2: "Where did you use Python Sets, and why is a Set better than a List there?"
> **Your Answer:**  
> "In [`src/curriculum_engine.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/curriculum_engine.py), I modeled all course prerequisites as **Python Sets** (`__prerequisites: Set[str]`).
> - To check if a student is eligible to take a course, I execute:
>   ```python
>   course.prerequisites.issubset(completed_courses_set)
>   ```
> - If a student hasn't met the prerequisites, I compute the missing courses using **Set Difference**:
>   ```python
>   missing = course.prerequisites.difference(completed_courses_set)
>   ```
> - In track matching, I compute the overlap between track foundation courses and completed courses using **Set Intersection**:
>   ```python
>   taken = track_foundations.intersection(completed_courses_set)
>   ```
> - **Why a Set?** A set guarantees no duplicate course codes and provides $O(1)$ average time complexity for lookups, whereas a list requires $O(n)$ linear traversal."

---

### Question 3: "How does your project use NumPy, and why is importing it justified?"
> **Your Answer:**  
> "In [`src/analytics.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/analytics.py), I didn't just use NumPy for a simple average; I used it for multi-semester numerical computing:
> 1. Converted SGPA history into a NumPy `ndarray` (`np.array(...)`).
> 2. Computed descriptive dispersion metrics: `np.mean()`, `np.median()`, `np.std()`, `np.var()`, and distribution quartiles via `np.percentile([25, 50, 75])`.
> 3. Used sample standard deviation ($\sigma = 0.117$) to classify performance consistency.
> 4. Computed a 1st-order polynomial linear regression fit:
>    ```python
>    slope, intercept = np.polyfit(semesters_x, sgpa_y, 1)
>    ```
>    This calculates the linear slope ($m$) of my semester momentum to project next semester's expected GPA mathematically."

---

### Question 4: "Why are Pandas and Scikit-learn not used in this project?"
> **Your Answer:**  
> "Because Section 10 of the Midterm Requirements strictly forbids third-party libraries that replace or hide students' implementation of core Python logic. In the midterm syllabus (Lectures 1–10), the approved numerical library is **NumPy**, while Pandas and Matplotlib belong to the **Final Term syllabus**. Our project strictly complies with midterm guidelines, but is architected to feed directly into Pandas DataFrames and Matplotlib charts for Phase 2."

---

### Question 5: "How does your code handle errors and prevent crashes?"
> **Your Answer:**  
> "I followed the Defensive Programming principle and FR-7:
> 1. In `src/models.py`, setting credits to a negative number or a string raises `ValueError` or `TypeError`.
> 2. In `src/report_parser.py`, opening missing files catches `FileNotFoundError` and corrupted lines are skipped cleanly.
> 3. In `main.py`, the interactive input loop catches `(EOFError, KeyboardInterrupt)` and invalid menu inputs, allowing the program to prompt the user again without terminating unexpectedly."

---

### Question 6: "How did you implement the 2D Line Graph feature?"
> **Your Answer:**  
> "In [`src/chart_viewer.py`](file:///D:/GITHUB_PROJECT/programming-in-pythonProject-lab/src/chart_viewer.py):
> 1. **Terminal 2D Coordinate Graph:** I initialized a 2D matrix grid, mapped each semester and CGPA value to discrete coordinate rows and columns, plotted vertex markers (`●`), and drew connecting line vectors (`╲`, `╱`, `─`).
> 2. **Tkinter GUI Canvas Window:** Using Python's standard `tkinter` library (approved in Section 6), I built a window that draws the Cartesian coordinate system, grid tick marks, a cumulative CGPA line, a dashed SGPA line, and interactive data bubbles on a Tkinter `Canvas`."

---

## 🛠️ Quick Verification Commands for the Viva
Before presenting, run these two commands in PowerShell:
```powershell
# 1. Run unit test suite (should report 'Ran 9 tests ... OK')
python -m unittest tests/test_core.py

# 2. Run the main program
python main.py
```
*(All 9 tests pass, and `main.py` is ready for immediate live execution).*
