"""
AIUB-PathFinder: Unit Test Suite
Module: test_core.py
Tests: Verification of OOP Models, Set-Theoretic Prerequisite Logic,
       NumPy Analytics, and Grade Report Parsing.
"""

import os
import unittest
import numpy as np

from src.models import (
    AcademicCourse,
    CompletedCourse,
    CurriculumCourse,
    SemesterRecord,
    StudentAcademicProfile,
)
from src.curriculum_engine import CurriculumEngine
from src.report_parser import GradeReportParser
from src.analytics import AcademicAnalyticsEngine


class TestAcademicModels(unittest.TestCase):
    def test_course_encapsulation_and_validation(self):
        c = AcademicCourse("CSC1102", "Introduction to Programming", 3.0)
        self.assertEqual(c.course_code, "CSC1102")
        self.assertEqual(c.credits, 3.0)

        # Validation test: negative credits should raise ValueError
        with self.assertRaises(ValueError):
            c.credits = -1.0

        # Non-numeric credit should raise TypeError
        with self.assertRaises(TypeError):
            c.credits = "three"

    def test_completed_course_calculations(self):
        # A+ (4.00) in 3-credit course -> 12.0 points
        c1 = CompletedCourse("CSC1102", "Intro to Programming", 3.0, "A+", "A+", "A+", 4.00, 3.0)
        self.assertTrue(c1.is_passed())
        self.assertEqual(c1.calculate_weighted_points(), 12.0)

        # Ongoing course with '-' grade
        c2 = CompletedCourse("CSC4162", "Programming in Python", 3.0, "-", "-", "-", 0.0, 0.0)
        self.assertTrue(c2.is_in_progress)
        self.assertFalse(c2.is_passed())
        self.assertEqual(c2.calculate_weighted_points(), 0.0)

    def test_curriculum_course_set_prerequisites(self):
        # Discrete Math requires MAT1102 and CSC1102
        c = CurriculumCourse(309, "BSc in CSE", "Semester 2", "CSC1204", "Discrete Math", 3.0, "MAT1102; CSC1102")
        self.assertEqual(c.prerequisites, {"MAT1102", "CSC1102"})

        # Not unlocked if only MAT1102 is completed
        self.assertFalse(c.is_unlocked({"MAT1102"}))
        self.assertEqual(c.missing_prerequisites({"MAT1102"}), {"CSC1102"})

        # Unlocked when both are completed (set subset operation)
        self.assertTrue(c.is_unlocked({"MAT1102", "CSC1102"}))
        self.assertEqual(c.missing_prerequisites({"MAT1102", "CSC1102"}), set())


class TestCurriculumEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, "data", "aiub_curriculum.csv")
        cls.engine = CurriculumEngine(csv_path)

    def test_catalog_loaded(self):
        self.assertGreater(len(self.engine.catalog), 50)
        self.assertIn("CSC1102", self.engine.catalog)
        self.assertIn("CSC4162", self.engine.catalog)

    def test_unlocked_courses(self):
        completed = {"CSC1102", "CSC1103", "PHY1101", "PHY1102", "MAT1102", "ENG1101", "CSC1101"}
        unlocked = self.engine.get_unlocked_core_courses(completed)
        unlocked_codes = {c.course_code for c in unlocked}

        # CSC1205 (OOP1) requires CSC1102; CSC1103 -> Should be unlocked
        self.assertIn("CSC1205", unlocked_codes)
        # CSC1204 (Discrete Math) requires MAT1102; CSC1102 -> Should be unlocked
        self.assertIn("CSC1204", unlocked_codes)

    def test_specialization_track_matcher(self):
        completed_codes = {"CSC2108", "CSC2211", "MAT3103", "CSC3217"}
        completed_courses = [
            CompletedCourse("CSC2108", "Database", 3.0, "A+", "A+", "A+", 4.00, 3.0),
            CompletedCourse("CSC2211", "Algorithms", 3.0, "A+", "A+", "A+", 4.00, 3.0),
            CompletedCourse("MAT3103", "Statistics", 3.0, "A", "A", "A", 3.75, 3.0),
            CompletedCourse("CSC3217", "AI", 3.0, "A+", "A+", "A+", 4.00, 3.0),
        ]
        rankings = self.engine.evaluate_specialization_tracks(completed_courses, completed_codes)
        self.assertGreater(len(rankings), 0)
        # Data Science & AI track should score at the top
        self.assertEqual(rankings[0]["track_key"], "DATA_SCIENCE_AI")
        self.assertGreaterEqual(rankings[0]["match_score"], 80.0)


class TestAnalyticsEngine(unittest.TestCase):
    def test_numpy_statistics_and_regression(self):
        profile = StudentAcademicProfile("23-54787-3", "MD. RAFID HOSSAIN", completed_credits=48.0, cgpa=3.85)
        # Add 3 mock semesters
        for sem_name, sgpa in [("Sem 1", 3.80), ("Sem 2", 3.85), ("Sem 3", 3.90)]:
            s = SemesterRecord(sem_name)
            s.sgpa = sgpa
            s.add_course(CompletedCourse("MOCK", "Mock Course", 3.0, "A", "A", "A", sgpa, 3.0))
            profile.add_semester(s)

        analytics = AcademicAnalyticsEngine(profile)
        stats = analytics.compute_statistical_overview()

        self.assertEqual(stats["count"], 3)
        self.assertAlmostEqual(stats["mean"], 3.85, places=2)
        self.assertEqual(stats["min_sgpa"], 3.80)
        self.assertEqual(stats["max_sgpa"], 3.90)

        # Regression slope should be positive (improving from 3.80 -> 3.85 -> 3.90)
        forecast = analytics.forecast_next_semester_sgpa()
        self.assertGreater(forecast["linear_slope"], 0.0)


class TestReportParser(unittest.TestCase):
    def test_parse_sample_report(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        txt_path = os.path.join(base_dir, "data", "sample_grade_report.txt")
        parser = GradeReportParser()
        profile = parser.parse_file(txt_path)

        self.assertEqual(profile.student_id, "23-54787-3")
        self.assertIn("RAFID", profile.student_name.upper())
        self.assertEqual(profile.completed_credits, 118.0)
        self.assertEqual(profile.cgpa, 3.81)

        # In-progress detection test: should have 5 ongoing courses in 2026-2027 Fall
        in_progress = profile.get_in_progress_courses()
        self.assertEqual(len(in_progress), 5)
        in_progress_codes = {c.course_code for c in in_progress}
        self.assertIn("CSC4162", in_progress_codes)  # Programming in Python!


class TestChartViewer(unittest.TestCase):
    def test_ascii_line_plot_generation(self):
        from src.chart_viewer import AcademicChartViewer
        semesters = ["S1", "S2", "S3", "S4"]
        cgpas = [3.95, 3.85, 3.89, 3.81]
        plot_str = AcademicChartViewer.render_ascii_line_plot(semesters, cgpas, "CGPA", 3.70, 4.00, 10)
        self.assertIn("CGPA", plot_str)
        self.assertIn("semesters", plot_str)
        self.assertIn("●", plot_str)
        self.assertIn("S1", plot_str)
        self.assertIn("S4", plot_str)


if __name__ == "__main__":
    unittest.main()
