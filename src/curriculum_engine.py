"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: curriculum_engine.py
Purpose: Curriculum Management, Set-Theoretic Prerequisite Analysis,
         Course Unlock Engine, and Major Specialization Track Matcher.
"""

import csv
import os
import sys
from typing import Dict, Set, List, Tuple, Any

# Ensure project root is in sys.path when running this script directly
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

try:
    from src.models import CurriculumCourse, CompletedCourse, ACADEMIC_DOMAINS
except ModuleNotFoundError:
    from models import CurriculumCourse, CompletedCourse, ACADEMIC_DOMAINS


# =====================================================================
# SPECIALIZATION TRACK CONFIGURATIONS (AIUB BScCSE Tracks)
# =====================================================================

SPECIALIZATION_TRACKS: Dict[str, Dict[str, Any]] = {
    "DATA_SCIENCE_AI": {
        "title": "Intelligent Systems & Data Science",
        "description": "Focus on Machine Learning, NLP, Data Mining, Computer Vision, and AI.",
        "foundation_codes": ["CSC2108", "CSC2211", "MAT3103", "CSC3217"],  # DB, Algo, Stats, AI
        "elective_codes": [
            "CSC4180",  # Intro to Data Science
            "CSC4232",  # Machine Learning
            "CSC4233",  # NLP
            "CSC4285",  # Data Warehouse & Mining
            "COE4234",  # Computer Vision & Pattern Recognition
            "COE4231",  # Image Processing
            "CSC4230",  # Bioinformatics
        ],
    },
    "SOFTWARE_ENGINEERING": {
        "title": "Software Engineering & Enterprise Systems",
        "description": "Focus on Architecture, Testing, Project Management, and Web/Mobile Dev.",
        "foundation_codes": ["CSC1205", "CSC2108", "CSC2210", "CSC3112", "CSC3215"],  # OOP1, DB, OOP2, SE, WebTech
        "elective_codes": [
            "CSC4160",  # Software Requirement Engg
            "CSC4271",  # Software Quality & Testing
            "CSC4270",  # Software Dev Project Management
            "CSC4273",  # Software Architecture & Design Patterns
            "CSC4272",  # Mobile App Development
            "CSC4161",  # Advanced Web Tech
            "CSC4163",  # Advanced Java
            "CSC4164",  # Advanced .NET
        ],
    },
    "NETWORKS_SECURITY": {
        "title": "Networks, Systems & Cyber Security",
        "description": "Focus on Advanced Networks, Cyber Laws, Wireless Sensors, and Security.",
        "foundation_codes": ["COE3103", "COE3104", "COE3206", "CSC3214"],  # Data Comm, Microprocessor, Networks, OS
        "elective_codes": [
            "COE4126",  # Advanced Computer Networks
            "COE4232",  # Network Security
            "COE4127",  # Network Resource Management
            "COE4233",  # Wireless Sensor Networks
            "CSC4183",  # Cyber Laws & Info Security
            "COE4125",  # Advanced OS
        ],
    },
    "HARDWARE_ROBOTICS": {
        "title": "Hardware, Embedded Systems & Robotics",
        "description": "Focus on Digital Design, VLSI, Telecom, and Robotics Engineering.",
        "foundation_codes": ["EEE2103", "EEE3101", "COE3104", "COE3205"],  # Devices, DLC, Microprocessor, Architecture
        "elective_codes": [
            "COE4128",  # Digital System Design
            "COE4235",  # Robotics Engineering
            "EEE4209",  # Telecommunications Engg
            "EEE4217",  # VLSI Circuit Design
            "EEE4233",  # Digital Design with Verilog/VHDL
            "EEE3103",  # Digital Signal Processing
        ],
    },
}


class CurriculumEngine:
    """
    Core curriculum repository and set-theoretic prerequisite solver.
    Uses pure Python Sets for prerequisite satisfaction tests.
    """
    def __init__(self, curriculum_csv_path: str):
        self.__csv_path = curriculum_csv_path
        self.__catalog: Dict[str, CurriculumCourse] = {}
        self.__course_domain_map: Dict[str, str] = {}
        self._load_curriculum()

    @property
    def catalog(self) -> Dict[str, CurriculumCourse]:
        return dict(self.__catalog)

    @property
    def domain_map(self) -> Dict[str, str]:
        return dict(self.__course_domain_map)

    # -------------------------------------------------------------------------
    # CSV INGESTION & DOMAIN CLASSIFICATION
    # -------------------------------------------------------------------------
    def _load_curriculum(self) -> None:
        """Parses the AIUB Curriculum CSV and builds the course catalog."""
        if not os.path.exists(self.__csv_path):
            raise FileNotFoundError(f"Curriculum CSV not found at: {self.__csv_path}")

        with open(self.__csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                code = row["Course Code"].strip().upper()
                name = row["Course Name"].strip()
                curr_no = int(row.get("Curriculum No", 309))
                curr_name = row.get("Curriculum", "BSc in CSE")
                sem_slot = row.get("Semester", "")
                cr = float(row.get("Total Credits", 3.0))
                prereqs = row.get("Prerequisites", "")

                domain = self._determine_domain(code, name)
                self.__course_domain_map[code] = domain

                course_obj = CurriculumCourse(
                    curriculum_no=curr_no,
                    curriculum_name=curr_name,
                    semester_slot=sem_slot,
                    course_code=code,
                    course_name=name,
                    credits=cr,
                    prerequisites_raw=prereqs,
                    domain=domain
                )
                self.__catalog[code] = course_obj

    @staticmethod
    def _determine_domain(course_code: str, course_name: str) -> str:
        """Categorizes course into one of the 6 recognized academic domains."""
        prefix = course_code[:3].upper()
        if prefix in ("MAT",):
            return "MATH_STAT"
        elif prefix in ("PHY", "CHE"):
            return "BASIC_SCI"
        elif prefix in ("COE", "EEE"):
            return "HARDWARE"
        elif prefix in ("BBA", "ECO", "MGT", "MIS"):
            return "BUSINESS"
        elif prefix in ("ENG", "BAS", "BAE"):
            return "HUMANITIES"
        elif prefix in ("CSC",):
            # Special exceptions
            if "STATISTICS" in course_name.upper():
                return "MATH_STAT"
            return "CS_CORE"
        return "CS_CORE"

    # -------------------------------------------------------------------------
    # SET-THEORETIC PREREQUISITE & COURSE UNLOCK LOGIC
    # -------------------------------------------------------------------------
    def get_remaining_core_courses(self, completed_codes: Set[str]) -> List[CurriculumCourse]:
        """Returns all Curriculum 309 Core courses not yet taken."""
        remaining = []
        for code, course in self.__catalog.items():
            if not course.is_elective and code not in completed_codes:
                remaining.append(course)
        return sorted(remaining, key=lambda c: (c.semester_slot, c.course_code))

    def get_unlocked_core_courses(self, completed_codes: Set[str]) -> List[CurriculumCourse]:
        """
        Returns remaining core courses whose prerequisites are completely satisfied.
        Uses Python Set operation: course.is_unlocked(completed_codes) -> prereqs.issubset(completed)
        """
        remaining = self.get_remaining_core_courses(completed_codes)
        unlocked = [c for c in remaining if c.is_unlocked(completed_codes)]
        return sorted(unlocked, key=lambda c: (c.semester_slot, c.course_code))

    def get_unlocked_electives(self, completed_codes: Set[str]) -> List[CurriculumCourse]:
        """
        Returns all Curriculum 338 Electives whose prerequisites are satisfied and not yet taken.
        """
        unlocked = []
        for code, course in self.__catalog.items():
            if course.is_elective and code not in completed_codes:
                if course.is_unlocked(completed_codes):
                    unlocked.append(course)
        return sorted(unlocked, key=lambda c: c.course_code)

    def simulate_post_current_unlocks(
        self,
        completed_codes: Set[str],
        current_enrolled_codes: Set[str]
    ) -> Dict[str, Any]:
        """
        Simulates what newly becomes unlocked once the student passes their current enrolled courses.
        newly_unlocked = unlocked(completed | current) - unlocked(completed)
        """
        currently_unlocked_all = {
            c.course_code for c in self.get_unlocked_core_courses(completed_codes) + self.get_unlocked_electives(completed_codes)
        }

        future_completed = completed_codes.union(current_enrolled_codes)
        future_unlocked_core = self.get_unlocked_core_courses(future_completed)
        future_unlocked_electives = self.get_unlocked_electives(future_completed)

        newly_unlocked_core = [
            c for c in future_unlocked_core if c.course_code not in currently_unlocked_all and c.course_code not in future_completed
        ]
        newly_unlocked_electives = [
            c for c in future_unlocked_electives if c.course_code not in currently_unlocked_all and c.course_code not in future_completed
        ]

        return {
            "newly_unlocked_core": newly_unlocked_core,
            "newly_unlocked_electives": newly_unlocked_electives,
            "total_newly_unlocked": len(newly_unlocked_core) + len(newly_unlocked_electives),
        }

    # -------------------------------------------------------------------------
    # MAJOR SPECIALIZATION TRACK MATCHER
    # -------------------------------------------------------------------------
    def evaluate_specialization_tracks(
        self,
        completed_courses: List[CompletedCourse],
        completed_codes: Set[str],
        current_codes: Optional[Set[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluates the student's foundation performance to recommend the optimal Major Specialization.
        Uses Set intersections (track_foundation & completed_codes) and computes an Aptitude Score.
        """
        current_codes = current_codes or set()
        course_grade_map = {c.course_code: c.grade_point for c in completed_courses}
        rankings = []

        for track_key, track_info in SPECIALIZATION_TRACKS.items():
            foundations: Set[str] = set(track_info["foundation_codes"])
            taken_foundations = foundations.intersection(completed_codes)

            # Calculate Foundation Average GPA
            if taken_foundations:
                points = [course_grade_map[c] for c in taken_foundations if c in course_grade_map]
                foundation_gpa = sum(points) / len(points) if points else 0.0
            else:
                foundation_gpa = 0.0

            # Find electives for this track
            track_electives: Set[str] = set(track_info["elective_codes"])
            unlocked_in_track = []
            total_accessible_count = 0

            for code in track_electives:
                if code in self.__catalog:
                    course_obj = self.__catalog[code]
                    # Accessible if prerequisites are met (including completed or currently enrolled)
                    if course_obj.is_unlocked(completed_codes) or code in completed_codes or code in current_codes:
                        total_accessible_count += 1
                    
                    # Available for FUTURE registration (not already completed, not currently ongoing)
                    if (
                        code not in completed_codes
                        and code not in current_codes
                        and course_obj.is_unlocked(completed_codes)
                    ):
                        unlocked_in_track.append(course_obj)

            # Match Score (0 - 100%)
            # Weight: 70% foundation performance + 30% unlocked/demonstrated track readiness
            perf_factor = (foundation_gpa / 4.0) * 70.0
            readiness_factor = (total_accessible_count / max(1, len(track_electives))) * 30.0
            match_score = round(perf_factor + readiness_factor, 1)

            if match_score >= 85.0:
                fit_label = "Prime Alignment / Highly Recommended"
            elif match_score >= 70.0:
                fit_label = "Strong Compatibility"
            else:
                fit_label = "Viable Alternative"

            rankings.append({
                "track_key": track_key,
                "title": track_info["title"],
                "description": track_info["description"],
                "match_score": match_score,
                "foundation_gpa": round(foundation_gpa, 2),
                "taken_foundations_count": f"{len(taken_foundations)}/{len(foundations)}",
                "unlocked_electives_count": len(unlocked_in_track),
                "unlocked_electives": unlocked_in_track,
                "fit_label": fit_label,
            })

        # Sort by match score descending
        return sorted(rankings, key=lambda r: r["match_score"], reverse=True)


if __name__ == "__main__":
    print("[AIUB-PathFinder] CurriculumEngine loaded successfully.")
