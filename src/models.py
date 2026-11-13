"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: models.py
Purpose: Core Domain Object-Oriented Models with Encapsulation, Inheritance,
         and Polymorphism as required by CSC 4162 Midterm Guidelines.
"""

from typing import List, Set, Tuple, Optional, Dict


# =====================================================================
# CONSTANT TUPLES (Required Python Concept: Tuples for immutable configs)
# =====================================================================

AIUB_GRADE_POINTS: Tuple[Tuple[str, float], ...] = (
    ("A+", 4.00),
    ("A",  3.75),
    ("B+", 3.50),
    ("B",  3.25),
    ("C+", 3.00),
    ("C",  2.75),
    ("D+", 2.50),
    ("D",  2.25),
    ("F",  0.00),
)

AIUB_GRADE_SCALE: Tuple[Tuple[float, float, str], ...] = (
    (90.0, 4.00, "A+"),
    (85.0, 3.75, "A"),
    (80.0, 3.50, "B+"),
    (75.0, 3.25, "B"),
    (70.0, 3.00, "C+"),
    (65.0, 2.75, "C"),
    (60.0, 2.50, "D+"),
    (50.0, 2.25, "D"),
    (0.0,  0.00, "F"),
)

ACADEMIC_DOMAINS: Tuple[str, ...] = (
    "CS_CORE",        # Programming, Data Structures, Algorithms, OOP, OS, AI, Compiler
    "MATH_STAT",      # Differential/Integral Calculus, Discrete Math, Linear Algebra, Stats
    "HARDWARE",       # Circuits, Electronics, DLC, Microprocessors, Architecture
    "BASIC_SCI",      # Physics 1 & 2, Labs, Chemistry
    "BUSINESS",       # Accounting, Economics, Engineering Management
    "HUMANITIES",     # English 1 & 2, Business Comm, Bangladesh Studies, Ethics
)

GRADE_POINT_MAP: Dict[str, float] = dict(AIUB_GRADE_POINTS)


# =====================================================================
# BASE CLASS: AcademicCourse (Demonstrating Encapsulation & OOP)
# =====================================================================

class AcademicCourse:
    """
    Base class representing any academic course at AIUB.
    Demonstrates strict encapsulation with private attributes and property getters/setters.
    """
    def __init__(self, course_code: str, course_name: str, credits: float):
        self.__course_code = course_code.strip().upper()
        self.__course_name = course_name.strip()
        self.credits = credits  # Uses setter for validation

    # --- Property Getters ---
    @property
    def course_code(self) -> str:
        return self.__course_code

    @property
    def course_name(self) -> str:
        return self.__course_name

    @property
    def credits(self) -> float:
        return self.__credits

    # --- Property Setter with Validation ---
    @credits.setter
    def credits(self, value: float) -> None:
        if not isinstance(value, (int, float)):
            raise TypeError("Course credits must be a numeric value.")
        if value < 0.0 or value > 10.0:
            raise ValueError(f"Invalid credit value: {value}. Must be between 0.0 and 10.0.")
        self.__credits = float(value)

    # --- Polymorphic Methods (Overridden in subclasses) ---
    def is_passed(self) -> bool:
        """Determines if the course is passed. Default implementation."""
        return False

    def calculate_weighted_points(self) -> float:
        """Calculates credits * grade_point. Overridden in CompletedCourse."""
        return 0.0

    def get_summary(self) -> str:
        """Polymorphic representation of course details."""
        return f"[{self.__course_code}] {self.__course_name} ({self.__credits:.1f} Cr)"

    def __repr__(self) -> str:
        return f"AcademicCourse({self.__course_code}, {self.__course_name}, {self.__credits})"


# =====================================================================
# SUBCLASS 1: CompletedCourse (Inheritance & Polymorphism)
# =====================================================================

class CompletedCourse(AcademicCourse):
    """
    Represents an enrolled or completed course from the student's Grade Report.
    Inherits from AcademicCourse and extends it with grade points and term grades.
    """
    def __init__(
        self,
        course_code: str,
        course_name: str,
        credits: float,
        mtg: str = "-",
        ftg: str = "-",
        final_grade: str = "-",
        grade_point: float = 0.0,
        earned_credits: float = 0.0,
        status: str = "VAL",
        semester_name: str = ""
    ):
        super().__init__(course_code, course_name, credits)
        self.__mtg = mtg.strip()
        self.__ftg = ftg.strip()
        self.__final_grade = final_grade.strip()
        self.__grade_point = float(grade_point)
        self.__earned_credits = float(earned_credits)
        self.__status = status.strip()
        self.__semester_name = semester_name.strip()
        # Automatically detect ongoing / in-progress courses
        self.__is_in_progress = (self.__final_grade == "-" or self.__final_grade == "")

    # --- Getters ---
    @property
    def mtg(self) -> str:
        return self.__mtg

    @property
    def ftg(self) -> str:
        return self.__ftg

    @property
    def final_grade(self) -> str:
        return self.__final_grade

    @property
    def grade_point(self) -> float:
        return self.__grade_point

    @property
    def earned_credits(self) -> float:
        return self.__earned_credits

    @property
    def status(self) -> str:
        return self.__status

    @property
    def semester_name(self) -> str:
        return self.__semester_name

    @property
    def is_in_progress(self) -> bool:
        return self.__is_in_progress

    # --- Setters for Simulation ---
    def simulate_grade(self, letter_grade: str) -> None:
        """Simulates what-if scenarios by updating the grade and grade point."""
        letter = letter_grade.strip().upper()
        if letter not in GRADE_POINT_MAP:
            raise ValueError(f"Invalid AIUB letter grade: {letter}")
        self.__final_grade = letter
        self.__grade_point = GRADE_POINT_MAP[letter]
        self.__earned_credits = self.credits if letter != "F" else 0.0
        self.__is_in_progress = False

    # --- Polymorphic Overrides ---
    def is_passed(self) -> bool:
        """Returns True if course is completed with a passing grade (non-F, non-in-progress)."""
        if self.__is_in_progress:
            return False
        return self.__final_grade != "F" and self.__earned_credits > 0.0

    def calculate_weighted_points(self) -> float:
        """Returns total grade points earned: credits * grade_point."""
        if self.__is_in_progress:
            return 0.0
        return self.credits * self.__grade_point

    def get_summary(self) -> str:
        if self.__is_in_progress:
            return f"[{self.course_code}] {self.course_name} ({self.credits:.1f} Cr) -> [CURRENT ENROLLED]"
        return (
            f"[{self.course_code}] {self.course_name:<36} | Cr: {self.credits:.1f} | "
            f"MT: {self.__mtg:<2} | FT: {self.__ftg:<2} | Final: {self.__final_grade:<2} | "
            f"GP: {self.__grade_point:.2f}"
        )


# =====================================================================
# SUBCLASS 2: CurriculumCourse (Inheritance & Domain Intelligence)
# =====================================================================

class CurriculumCourse(AcademicCourse):
    """
    Represents a course in the AIUB Curriculum (Curriculum 309 Core or 338 Electives).
    Contains prerequisite relationships modeled with Python Sets.
    """
    def __init__(
        self,
        curriculum_no: int,
        curriculum_name: str,
        semester_slot: str,
        course_code: str,
        course_name: str,
        credits: float,
        prerequisites_raw: str,
        domain: str = "CS_CORE"
    ):
        super().__init__(course_code, course_name, credits)
        self.__curriculum_no = int(curriculum_no)
        self.__curriculum_name = curriculum_name.strip()
        self.__semester_slot = semester_slot.strip()
        self.__domain = domain if domain in ACADEMIC_DOMAINS else "CS_CORE"
        # Parse prerequisites into a clean Python set of course codes
        self.__prerequisites: Set[str] = self._parse_prereqs(prerequisites_raw)

    @staticmethod
    def _parse_prereqs(raw: str) -> Set[str]:
        """Parses prerequisite string like 'CSC1204; CSC1205' into {'CSC1204', 'CSC1205'}."""
        if not raw or raw.strip().lower() in ("", "none", "nan"):
            return set()
        codes = [c.strip().upper() for c in raw.replace(",", ";").split(";")]
        return {c for c in codes if c}

    # --- Getters ---
    @property
    def curriculum_no(self) -> int:
        return self.__curriculum_no

    @property
    def semester_slot(self) -> str:
        return self.__semester_slot

    @property
    def is_elective(self) -> bool:
        return "Elective" in self.__semester_slot or self.__curriculum_no == 338

    @property
    def prerequisites(self) -> Set[str]:
        return set(self.__prerequisites)

    @property
    def domain(self) -> str:
        return self.__domain

    @domain.setter
    def domain(self, value: str) -> None:
        if value in ACADEMIC_DOMAINS:
            self.__domain = value

    def is_unlocked(self, completed_course_codes: Set[str]) -> bool:
        """
        Set-theoretic prerequisite check:
        Course is unlocked if all its prerequisites are a subset of completed courses.
        """
        if not self.__prerequisites:
            return True
        return self.__prerequisites.issubset(completed_course_codes)

    def missing_prerequisites(self, completed_course_codes: Set[str]) -> Set[str]:
        """Returns the set difference of prerequisites not yet satisfied."""
        return self.__prerequisites.difference(completed_course_codes)

    def get_summary(self) -> str:
        prereq_str = ", ".join(sorted(self.__prerequisites)) if self.__prerequisites else "None"
        tag = "[ELECTIVE]" if self.is_elective else f"[{self.__semester_slot}]"
        return f"{tag:<14} [{self.course_code}] {self.course_name:<36} ({self.credits:.1f} Cr) | Prereqs: {prereq_str}"


# =====================================================================
# AGGREGATE CLASS: SemesterRecord (Demonstrating List & Encapsulation)
# =====================================================================

class SemesterRecord:
    """
    Represents an individual academic semester with its collection of completed/enrolled courses.
    """
    def __init__(self, semester_name: str):
        self.__semester_name = semester_name.strip()
        self.__courses: List[CompletedCourse] = []
        self.__sgpa: float = 0.0
        self.__cgpa: float = 0.0
        self.__tgp: float = 0.0   # Total Grade Points from report summary
        self.__ecr: float = 0.0   # Earned Credits from report summary
        self.__is_current: bool = False

    @property
    def semester_name(self) -> str:
        return self.__semester_name

    @property
    def courses(self) -> List[CompletedCourse]:
        return list(self.__courses)

    @property
    def sgpa(self) -> float:
        return self.__sgpa

    @sgpa.setter
    def sgpa(self, value: float) -> None:
        self.__sgpa = max(0.0, min(4.0, float(value)))

    @property
    def cgpa(self) -> float:
        return self.__cgpa

    @cgpa.setter
    def cgpa(self, value: float) -> None:
        self.__cgpa = max(0.0, min(4.0, float(value)))

    @property
    def tgp(self) -> float:
        """Total Grade Points from report summary line."""
        return self.__tgp

    @tgp.setter
    def tgp(self, value: float) -> None:
        self.__tgp = max(0.0, float(value))

    @property
    def ecr(self) -> float:
        """Earned Credits from report summary line."""
        return self.__ecr

    @ecr.setter
    def ecr(self, value: float) -> None:
        self.__ecr = max(0.0, float(value))

    @property
    def is_current(self) -> bool:
        return self.__is_current

    @is_current.setter
    def is_current(self, value: bool) -> None:
        self.__is_current = bool(value)

    def add_course(self, course: CompletedCourse) -> None:
        self.__courses.append(course)
        if course.is_in_progress:
            self.__is_current = True

    def calculate_total_credits(self) -> float:
        """Returns sum of registered credits in this semester."""
        return sum(c.credits for c in self.__courses)

    def calculate_earned_credits(self) -> float:
        """Returns sum of earned credits from passed courses."""
        return sum(c.earned_credits for c in self.__courses if c.is_passed())

    def calculate_sgpa_dynamically(self) -> float:
        """Dynamically computes semester GPA based on credit weights."""
        passed_or_graded = [c for c in self.__courses if not c.is_in_progress]
        if not passed_or_graded:
            return 0.0
        total_points = sum(c.calculate_weighted_points() for c in passed_or_graded)
        total_credits = sum(c.credits for c in passed_or_graded)
        return total_points / total_credits if total_credits > 0 else 0.0


# =====================================================================
# STUDENT PROFILE CLASS: StudentAcademicProfile
# =====================================================================

class StudentAcademicProfile:
    """
    Encapsulates the complete academic record of an AIUB student.
    """
    def __init__(
        self,
        student_id: str,
        student_name: str,
        degree: str = "BSc in Computer Science & Engineering",
        completed_credits: float = 0.0,
        cgpa: float = 0.0
    ):
        self.__student_id = student_id.strip()
        self.__student_name = student_name.strip()
        self.__degree = degree.strip()
        self.__completed_credits = float(completed_credits)
        self.__cgpa = float(cgpa)
        self.__semesters: List[SemesterRecord] = []
        self.__curriculum_remaining: List[Dict[str, str]] = []

    @property
    def student_id(self) -> str:
        return self.__student_id

    @student_id.setter
    def student_id(self, value: str) -> None:
        self.__student_id = str(value).strip()

    @property
    def student_name(self) -> str:
        return self.__student_name

    @student_name.setter
    def student_name(self, value: str) -> None:
        self.__student_name = str(value).strip()

    @property
    def degree(self) -> str:
        return self.__degree

    @property
    def completed_credits(self) -> float:
        return self.__completed_credits

    @completed_credits.setter
    def completed_credits(self, value: float) -> None:
        self.__completed_credits = max(0.0, float(value))

    @property
    def cgpa(self) -> float:
        return self.__cgpa

    @cgpa.setter
    def cgpa(self, value: float) -> None:
        self.__cgpa = max(0.0, min(4.0, float(value)))

    @property
    def semesters(self) -> List[SemesterRecord]:
        return list(self.__semesters)

    @property
    def curriculum_remaining(self) -> List[Dict[str, str]]:
        return list(self.__curriculum_remaining)

    def set_curriculum_remaining(self, remaining: List[Dict[str, str]]) -> None:
        self.__curriculum_remaining = list(remaining)

    def add_semester(self, sem: SemesterRecord) -> None:
        self.__semesters.append(sem)

    def get_completed_course_codes(self) -> Set[str]:
        """Returns a Python Set of all course codes successfully passed."""
        passed: Set[str] = set()
        for s in self.__semesters:
            for c in s.courses:
                if c.is_passed():
                    passed.add(c.course_code)
        return passed

    def get_in_progress_courses(self) -> List[CompletedCourse]:
        """Returns all courses currently registered/in-progress."""
        in_progress: List[CompletedCourse] = []
        for s in self.__semesters:
            if s.is_current:
                for c in s.courses:
                    if c.is_in_progress:
                        in_progress.append(c)
        return in_progress

    def get_completed_courses_list(self) -> List[CompletedCourse]:
        """Returns a flat list of all completed courses."""
        return [c for s in self.__semesters for c in s.courses if c.is_passed()]

    def get_sgpa_history(self) -> List[Tuple[str, float, float]]:
        """Returns list of (semester_name, sgpa, earned_credits) for graded semesters."""
        history = []
        for s in self.__semesters:
            if not s.is_current and s.sgpa > 0.0:
                history.append((s.semester_name, s.sgpa, s.calculate_earned_credits()))
        return history
