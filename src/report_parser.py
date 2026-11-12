"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: report_parser.py
Purpose: Ingests and parses AIUB Grade Report from PDF or text file,
         extracts student profile, semester records, completed & ongoing courses.
"""

import os
import re
from typing import Dict, Optional, Tuple
from pypdf import PdfReader
from src.models import (
    StudentAcademicProfile,
    SemesterRecord,
    CompletedCourse,
    GRADE_POINT_MAP,
)


# Known alias mapping for slight discrepancies between Grade Report text & Curriculum titles
NAME_ALIASES: Dict[str, str] = {
    "DIFFCALCULUSANDCOORDINATEGEOMETRY": "MAT1102",
    "DIFFERENTIALCALCULUSCOORDINATEGEOMETRY": "MAT1102",
    "ENGLISHWRITINGSKILLSCOMMUNICATIONSCSENGG": "ENG1202",
    "ENGLISHWRITINGSKILLSCOMMUNICATION": "ENG1202",
    "INTEGRALCALCULUSORDDIFFEQUATION": "MAT1205",
    "INTEGRALCALCULUSORDINARYDIFFERENTIALEQUATIONS": "MAT1205",
    "OBJECTORIENTEDPROGRAMMING1JAVA": "CSC1205",
    "OBJECTORIENTEDPROGRAMMING1": "CSC1205",
    "BUSINESSCOMMUNICATIONCSENGG": "ENG2103",
    "BUSINESSCOMMUNICATION": "ENG2103",
    "ARTIFICIALINTELLIGENCEANDEXPERTSYSTEM": "CSC3217",
    "ARTIFICIALINTELLIGENCEANDEXPERTSYS": "CSC3217",
    "MICROPROCESSORANDEMBEDDEDSYSTEMS": "COE3104",
    "MICROPROCESSORANDEMBEDDEDSYSTEM": "COE3104",
}


class GradeReportParser:
    """
    Parser for AIUB Grade Reports.
    Supports both native PDF files and plain text extracts with robust error handling.
    """
    def __init__(self, curriculum_lookup_map: Optional[Dict[str, str]] = None):
        # Maps normalized course name -> Course Code (e.g., 'INTRODUCTIONTOPROGRAMMING' -> 'CSC1102')
        self.__name_to_code: Dict[str, str] = dict(NAME_ALIASES)
        
        # If no custom lookup is passed, automatically load from data/aiub_curriculum.csv if it exists
        if curriculum_lookup_map is None:
            curriculum_lookup_map = self._load_default_curriculum_map()

        if curriculum_lookup_map:
            for k, v in curriculum_lookup_map.items():
                norm = re.sub(r'[^A-Z0-9]', '', k.upper())
                if norm not in self.__name_to_code:
                    self.__name_to_code[norm] = v

    @staticmethod
    def _load_default_curriculum_map() -> Dict[str, str]:
        """Loads default course name to code mapping from data/aiub_curriculum.csv."""
        import csv
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "aiub_curriculum.csv")
        mapping = {}
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    mapping[row["Course Name"]] = row["Course Code"]
        return mapping

    def parse_file(self, file_path: str) -> StudentAcademicProfile:
        """
        Main entry point: detects whether input is PDF or TXT and parses accordingly.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Grade report file not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            text = self._extract_text_from_pdf(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()

        return self.parse_text(text)

    def parse_curriculum_file(self, file_path: str) -> dict:
        """
        Parses an AIUB Grade Report by Curriculum PDF.
        Extracts student metadata, completed courses, ongoing courses, and remaining degree requirements.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Curriculum report file not found: {file_path}")

        reader = PdfReader(file_path)
        full_text = "\n".join([p.extract_text() or "" for p in reader.pages])
        lines = [l.strip() for l in full_text.splitlines() if l.strip()]

        student_id = ""
        student_name = ""
        credits = 0.0
        cgpa = 0.0
        degree = "Bachelor of Science in Computer Science & Engineering"

        m_id = re.search(r'\b(\d{2}-\d{5}-\d)\b', full_text)
        if m_id:
            student_id = m_id.group(1).strip()

        for i, l in enumerate(lines):
            if l == 'Student ID' and i + 10 < len(lines):
                for j in range(i, min(i + 35, len(lines))):
                    if re.match(r'^[A-Z\s]+,\s*[A-Z\.\s]+$', lines[j]) and not student_name:
                        student_name = lines[j].strip()
                    if re.match(r'^\d+\.\d{2}$', lines[j]) and cgpa == 0.0:
                        try:
                            cgpa = float(lines[j])
                        except ValueError:
                            pass
                    if re.match(r'^\d+$', lines[j]) and int(lines[j]) > 30 and credits == 0.0:
                        try:
                            credits = float(lines[j])
                        except ValueError:
                            pass

        courses = []
        i = 0
        while i < len(lines):
            line = lines[i]
            code_match = re.match(r'^([A-Z]{3,4}\d{4}|[A-Z]{3}\*{4}|[A-Z]{3}\#{4})$', line)
            if code_match:
                code = code_match.group(1).strip()
                name = lines[i + 1].strip() if i + 1 < len(lines) else ""
                status = "remaining"
                grade = ""
                term = ""
                offset = 2
                if i + 2 < len(lines):
                    st_match = re.match(r'^\((.*?)\)\s*\[(.*?)\]$', lines[i + 2])
                    if st_match:
                        term = st_match.group(1).strip()
                        grade = st_match.group(2).strip()
                        status = "ongoing" if grade in ("-", "") else "completed"
                        offset = 3
                courses.append({
                    "course_code": code,
                    "course_name": name,
                    "term": term,
                    "grade": grade,
                    "status": status
                })
                i += offset
            else:
                i += 1

        return {
            "student_id": student_id,
            "student_name": student_name,
            "completed_credits": credits,
            "cgpa": cgpa,
            "degree": degree,
            "total_courses": len(courses),
            "completed": [c for c in courses if c["status"] == "completed"],
            "ongoing": [c for c in courses if c["status"] == "ongoing"],
            "remaining": [c for c in courses if c["status"] == "remaining"],
        }

    def parse_dual_reports(self, semester_path: str, curriculum_path: str) -> StudentAcademicProfile:
        """
        Parses both Grade Report by Semester and Grade Report by Curriculum.
        Combines chronological progress with curriculum requirement audit.
        """
        profile = self.parse_file(semester_path)
        curr_data = self.parse_curriculum_file(curriculum_path)

        # Reconcile metadata if semester report had placeholders or reversed names
        if (profile.student_id == "Unknown ID" or not profile.student_id) and curr_data.get("student_id"):
            profile._StudentAcademicProfile__student_id = curr_data["student_id"]

        if (profile.student_name == "AIUB Student" or not profile.student_name) and curr_data.get("student_name"):
            profile._StudentAcademicProfile__student_name = curr_data["student_name"]

        if curr_data.get("completed_credits") and profile.completed_credits == 0.0:
            profile._StudentAcademicProfile__completed_credits = curr_data["completed_credits"]

        if curr_data.get("cgpa") and profile.cgpa == 0.0:
            profile._StudentAcademicProfile__cgpa = curr_data["cgpa"]

        # Store remaining curriculum courses in profile
        profile.set_curriculum_remaining(curr_data.get("remaining", []))

        return profile

    @staticmethod
    def _extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extracts all text pages from an AIUB Grade Report PDF and reconstitutes
        multi-line course tables into standard single-line formats.
        """
        reader = PdfReader(pdf_path)
        raw_lines = [l.strip() for page in reader.pages for l in (page.extract_text() or "").splitlines() if l.strip()]

        cleaned_lines = []
        i = 0
        while i < len(raw_lines):
            line = raw_lines[i]
            if line.startswith('***'):
                cleaned_lines.append(line)
                i += 1
            elif re.match(r'^\d{5}$', line) and i + 6 < len(raw_lines):
                # 5-digit class ID followed by fields on separate lines
                cid = line
                cname = raw_lines[i + 1]
                credits = raw_lines[i + 2]
                mtg = raw_lines[i + 3]
                ftg = raw_lines[i + 4]
                fg = raw_lines[i + 5]
                tgp = raw_lines[i + 6]
                val = "VAL"
                prn = "Y"
                offset = 7
                if i + offset < len(raw_lines) and raw_lines[i + offset] in ("Y", "N"):
                    prn = raw_lines[i + offset]
                    offset += 1
                if i + offset < len(raw_lines) and raw_lines[i + offset] == "VAL":
                    val = raw_lines[i + offset]
                    offset += 1
                cleaned_lines.append(f"{cid} {cname} {credits} {mtg} {ftg} {fg} {tgp} {val} {prn}")
                i += offset
            elif (
                re.match(r'^\d+\.\d{2}$', line)
                and i + 3 < len(raw_lines)
                and all(re.match(r'^\d+\.\d{2}$', raw_lines[i + k]) for k in range(1, 4))
            ):
                # 4 summary numbers at bottom of semester (TGP, ECR, SGPA, CGPA)
                cleaned_lines.append(f"{line} {raw_lines[i+1]} {raw_lines[i+2]} {raw_lines[i+3]}")
                i += 4
            else:
                if line == 'ID Number' and i + 5 < len(raw_lines) and raw_lines[i + 1] == 'Student Name':
                    # Parse column-stacked header
                    id_num = raw_lines[i + 5]
                    name = raw_lines[i + 6]
                    cr = raw_lines[i + 7]
                    cgpa = raw_lines[i + 9] if i + 9 < len(raw_lines) else "0.00"
                    cleaned_lines.append(f"ID Number : {id_num}")
                    cleaned_lines.append(f"Student Name : {name}")
                    cleaned_lines.append(f"Credit Completed : {cr}")
                    cleaned_lines.append(f"CGPA : {cgpa}")
                cleaned_lines.append(line)
                i += 1

        return "\n".join(cleaned_lines)

    def parse_text(self, text: str) -> StudentAcademicProfile:
        """
        Parses the full text of an AIUB Grade Report into a StudentAcademicProfile.
        """
        # 1. Extract Student Metadata
        student_id = "Unknown ID"
        id_match = re.search(r'ID Number\s*:\s*([0-9\-]+)', text)
        if id_match:
            student_id = id_match.group(1).strip()

        student_name = "AIUB Student"
        name_match = re.search(r'Student Name\s*:\s*([^\n\r]+)', text)
        if name_match:
            student_name = name_match.group(1).strip()

        credits_completed = 0.0
        cr_match = re.search(r'Credit Completed\s*:\s*([0-9\.]+)', text)
        if cr_match:
            credits_completed = float(cr_match.group(1).strip())

        cgpa = 0.0
        cgpa_match = re.search(r'CGPA\s*:\s*([0-9\.]+)', text)
        if cgpa_match:
            cgpa = float(cgpa_match.group(1).strip())

        degree = "Bachelor of Science in Computer Science & Engineering"
        course_match = re.search(r'Course\s*:\s*([^\n\r]+)', text)
        if course_match:
            degree = course_match.group(1).strip()

        profile = StudentAcademicProfile(
            student_id=student_id,
            student_name=student_name,
            degree=degree,
            completed_credits=credits_completed,
            cgpa=cgpa
        )

        # 2. Split by Semesters (Pattern: '*** YYYY-YYYY, Term')
        sem_blocks = re.split(r'\*\*\*\s*(\d{4}-\d{4},\s*[A-Za-z]+)', text)
        if len(sem_blocks) < 2:
            raise ValueError("No semester records found in the grade report. Please verify format.")

        for i in range(1, len(sem_blocks), 2):
            sem_title = sem_blocks[i].strip()
            sem_content = sem_blocks[i + 1]

            sem_record = SemesterRecord(sem_title)
            self._parse_semester_courses(sem_record, sem_content)

            # Look for semester summary line (e.g. '63.25 16.00 3.95 3.95' or '0.00 0.00 0.00 3.81')
            summary_match = re.search(r'(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})\s+(\d+\.\d{2})', sem_content)
            if summary_match:
                tgp_str, ecr_str, sgpa_str, cgpa_str = summary_match.groups()
                sem_record.sgpa = float(sgpa_str)
                sem_record.cgpa = float(cgpa_str)

            # Ongoing semester check: if SGPA is 0.0 and courses have '-' grades
            if sem_record.sgpa == 0.0 and any(c.is_in_progress for c in sem_record.courses):
                sem_record.is_current = True

            profile.add_semester(sem_record)

        return profile

    def _parse_semester_courses(self, sem_record: SemesterRecord, content: str) -> None:
        """
        Parses all course lines within a single semester text block.
        """
        for line in content.split("\n"):
            line = line.strip()
            # Course line regex matching:
            # ClassID (5 digits) | Course Name | Credits | MTG | FTG | FG | TGP | STS | PRN
            # e.g.: 02334 PHYSICS 1 3.00 A A+ A+ 12.00 VAL Y
            # e.g.: 00820 ENGINEERING MANAGEMENT 3.00 - - - 0.00 VAL Y
            m = re.match(
                r'^\d{5}\s+(.*?)\s+(\d+\.\d{2})\s+([A-Za-z\+\-]+)\s+([A-Za-z\+\-]+)\s+([A-Za-z\+\-]+)\s+(\d+\.\d{2})\s+([A-Za-z]+)\s+([A-Za-z]+)',
                line
            )
            if m:
                cname = m.group(1).strip()
                credits = float(m.group(2))
                mtg = m.group(3).strip()
                ftg = m.group(4).strip()
                fg = m.group(5).strip()
                tgp = float(m.group(6))
                status = m.group(7).strip()

                norm_name = re.sub(r'[^A-Z0-9]', '', cname.upper())
                course_code = self.__name_to_code.get(norm_name, "GEN0000")

                grade_point = GRADE_POINT_MAP.get(fg, 0.0)
                earned_cr = credits if fg != "F" and fg != "-" else 0.0

                course = CompletedCourse(
                    course_code=course_code,
                    course_name=cname,
                    credits=credits,
                    mtg=mtg,
                    ftg=ftg,
                    final_grade=fg,
                    grade_point=grade_point,
                    earned_credits=earned_cr,
                    status=status,
                    semester_name=sem_record.semester_name
                )
                sem_record.add_course(course)
