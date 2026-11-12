"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: ui.py
Purpose: Interactive Console Interface, ASCII Horizontal Bar Charts,
         Formatted Metric Tables, and Error-Resilient User Input Loops.
"""

import os
import sys
from typing import Dict, List, Any
import json
import csv

# Ensure project root is in sys.path when running this script directly
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


class TerminalUI:
    """
    Console presentation layer for AIUB-PathFinder.
    Uses ANSI borders, ASCII bar charts, and robust validation loops.
    """

    @staticmethod
    def print_banner() -> None:
        print("\n" + "=" * 80)
        print("  AIUB-PathFinder | Academic Performance & Degree Intelligence System")
        print("  American International University-Bangladesh (AIUB) | Fall 2026-27")
        print("=" * 80)

    @staticmethod
    def print_menu() -> None:
        print("\n--- MASTER OPERATIONS MENU ---")
        print("  [G] Launch Full Native Desktop GUI Application")
        print("  [1] Student Profile & Degree Progress Summary")
        print("  [2] Statistical Overview & SGPA/CGPA Progression (NumPy Engine)")
        print("  [3] Visual Line Plot: CGPA vs Semesters Chart (Terminal 2D & Tkinter GUI)")
        print("  [4] Subject Domain Strength Analysis (ASCII Bar Diagram)")
        print("  [5] Next-Semester Predictive Forecaster & Interactive What-If Simulator")
        print("  [6] Prerequisite & Course Unlock Engine (Set-Theoretic Analysis)")
        print("  [7] Major Specialization Track Matcher (AI/DS vs SE vs Networks)")
        print("  [8] Export Complete Academic Audit (JSON & Summary Text)")
        print("  [0] Exit Application")
        print("-" * 80)

    @staticmethod
    def draw_bar_chart(label: str, value: float, max_val: float = 4.0, bar_length: int = 20) -> str:
        """
        Draws an ASCII horizontal bar chart representing scores or percentages.
        e.g., [3.81 / 4.00] ███████████████████░
        """
        ratio = max(0.0, min(1.0, value / max_val if max_val > 0 else 0.0))
        filled_len = int(round(ratio * bar_length))
        empty_len = bar_length - filled_len
        bar = "█" * filled_len + "░" * empty_len
        return f"{label:<32} [{value:4.2f} / {max_val:.2f}]  {bar}"

    # -------------------------------------------------------------------------
    # OPERATION VIEWS
    # -------------------------------------------------------------------------

    @classmethod
    def display_profile_summary(cls, profile) -> None:
        print("\n" + "=" * 80)
        print("  1. STUDENT PROFILE & DEGREE COMPLETION STATUS")
        print("=" * 80)
        print(f"  Student Name     : {profile.student_name}")
        print(f"  Student ID       : {profile.student_id}")
        print(f"  Degree Program   : {profile.degree}")
        print(f"  Completed Credits: {profile.completed_credits:.1f} / 148.0 Credits")
        print(f"  Current CGPA     : {profile.cgpa:.2f} / 4.00")

        # Degree Completion Bar
        pct = (profile.completed_credits / 148.0) * 100.0
        bar = cls.draw_bar_chart("Degree Completion", pct, 100.0, 25)
        print(f"\n  {bar} ({pct:.1f}%)")

        in_progress = profile.get_in_progress_courses()
        print(f"\n  Currently Enrolled Courses (2026-2027 Fall): [{len(in_progress)} Courses | {sum(c.credits for c in in_progress):.1f} Credits]")
        for c in in_progress:
            print(f"    • [{c.course_code:<7}] {c.course_name:<40} ({c.credits:.1f} Cr)")

    @classmethod
    def display_cgpa_line_chart(cls, profile) -> None:
        """
        Renders the 2D Coordinate Graph of CGPA vs Semesters matching user's sketch,
        with an option to open the graphical Tkinter popup window.
        """
        try:
            from src.chart_viewer import AcademicChartViewer
        except ModuleNotFoundError:
            from chart_viewer import AcademicChartViewer

        completed_sems = [s for s in profile.semesters if not s.is_current and s.cgpa > 0.0]
        if not completed_sems:
            print("\n  No completed semester records available to plot.")
            return

        sem_names = [s.semester_name for s in completed_sems]
        cgpa_vals = [s.cgpa for s in completed_sems]
        sgpa_vals = [s.sgpa for s in completed_sems]

        print("\n" + "=" * 80)
        print("  3. 2D COORDINATE VISUAL PLOT: CGPA vs SEMESTERS")
        print("=" * 80)
        print("  Cartesian coordinate plot rendering historical cumulative performance:\n")

        # Determine dynamic y-axis range
        min_c = min(cgpa_vals)
        max_c = max(cgpa_vals)
        plot_min = max(2.0, round(min_c - 0.15, 2))
        plot_max = min(4.0, round(max_c + 0.10, 2))

        ascii_plot = AcademicChartViewer.render_ascii_line_plot(
            sem_names,
            cgpa_vals,
            y_label="CGPA",
            min_val=plot_min,
            max_val=plot_max,
            height=12
        )
        print(ascii_plot)

        print("\n  [SEMESTER LEGEND]")
        for i, (name, c_val, s_val) in enumerate(zip(sem_names, cgpa_vals, sgpa_vals), 1):
            print(f"    S{i}: {name:<22} | CGPA: {c_val:.2f} | SGPA: {s_val:.2f}")

        # Offer GUI window launch
        gui_choice = input("\n  Launch interactive Graphical Tkinter Window? [Y/n]: ").strip().lower()
        if gui_choice in ("", "y", "yes"):
            try:
                print("  Opening Tkinter graphical chart window (close window to return to console)...")
                AcademicChartViewer.show_graphical_window(
                    sem_names,
                    cgpa_vals,
                    sgpa_vals,
                    profile.student_name,
                    profile.student_id
                )
            except Exception as e:
                print(f"  [Notice] Graphical window could not be opened: {e}")

    @classmethod
    def display_statistical_overview(cls, stats: Dict[str, Any], progression: List[Dict[str, Any]]) -> None:
        print("\n" + "=" * 80)
        print("  2. STATISTICAL OVERVIEW & SGPA/CGPA PROGRESSION (NUMPY ENGINE)")
        print("=" * 80)

        if not stats:
            print("  No completed semester data available.")
            return

        print("  [DESCRIPTIVE STATISTICS SUMMARY]")
        print(f"  • Total Semesters Evaluated : {stats['count']}")
        print(f"  • Mean SGPA                 : {stats['mean']:.3f}")
        print(f"  • Median SGPA               : {stats['median']:.3f}")
        print(f"  • Standard Deviation (σ)    : {stats['std_dev']:.3f}  ({stats['stability_rating']})")
        print(f"  • Variance                  : {stats['variance']:.4f}")
        print(f"  • Min SGPA / Max SGPA       : {stats['min_sgpa']:.2f} / {stats['max_sgpa']:.2f}")
        print(f"  • Percentiles (Q1, Q2, Q3)  : 25% = {stats['percentile_25']:.2f} | 50% = {stats['percentile_50']:.2f} | 75% = {stats['percentile_75']:.2f}")
        print(f"  • Peak Semester             : {stats['best_semester'][0]} (SGPA: {stats['best_semester'][1]:.2f})")
        print(f"  • Toughest Semester         : {stats['lowest_semester'][0]} (SGPA: {stats['lowest_semester'][1]:.2f})")

        print("\n  [SEMESTER-BY-SEMESTER CHRONOLOGICAL PROGRESSION TABLE]")
        print("  " + "-" * 76)
        print(f"  {'Semester':<22} | {'Credits':<7} | {'SGPA':<6} | {'CGPA':<6} | {'Momentum':<24}")
        print("  " + "-" * 76)
        for row in progression:
            print(f"  {row['semester']:<22} | {row['credits']:<7} | {row['sgpa']:<6} | {row['cgpa']:<6} | {row['momentum']:<24}")
        print("  " + "-" * 76)

        # ASCII Sparkline Trend
        print("\n  [SGPA TREND VISUALIZATION]")
        for row in progression:
            if row['status'] == 'Completed':
                val = float(row['sgpa'])
                bar = cls.draw_bar_chart(row['semester'], val, 4.0, 18)
                print(f"  {bar}")

    @classmethod
    def display_domain_strengths(cls, domain_results: Dict[str, Dict[str, Any]]) -> None:
        print("\n" + "=" * 80)
        print("  3. SUBJECT DOMAIN STRENGTH ANALYSIS (HORIZONTAL BAR DIAGRAM)")
        print("=" * 80)
        print("  Evaluates academic performance across university subject departments:\n")

        # Sort domains by GPA descending
        sorted_domains = sorted(domain_results.values(), key=lambda d: d["domain_gpa"], reverse=True)
        for d in sorted_domains:
            bar_line = cls.draw_bar_chart(d["domain_name"], d["domain_gpa"], 4.0, 22)
            print(f"  {bar_line}  [{d['evaluation']}] ({d['total_credits']:.1f} Cr)")

        print("\n  [DOMAIN DETAILS & SAMPLE COURSES]")
        for d in sorted_domains:
            if d["course_count"] > 0:
                courses_sample = ", ".join(d["sample_courses"])
                print(f"  • {d['domain_name']} ({d['total_credits']:.1f} Cr, {d['course_count']} courses):")
                print(f"    Sample: {courses_sample}")

    @classmethod
    def display_forecaster_and_simulation(cls, forecast: Dict[str, Any], analytics_engine, profile) -> None:
        print("\n" + "=" * 80)
        print("  4. NEXT-SEMESTER PREDICTIVE FORECASTER & WHAT-IF SIMULATOR")
        print("=" * 80)

        if "error" in forecast:
            print(f"  [NOTE] {forecast['error']}")
            return

        print("  [NUMPY LINEAR TREND EXTRAPOLATION]")
        print(f"  • Linear Regression Slope (m): {forecast['linear_slope']:+.4f} per semester ({forecast['trend_direction']})")
        print(f"  • Trend-Projected SGPA       : {forecast['forecasted_sgpa']:.2f} / 4.00")
        print(f"  • 3-Semester Weighted Average: {forecast['weighted_recent_avg']:.2f} / 4.00")
        print(f"  • Projected Graduating CGPA  : {forecast['projected_cgpa_after_current']:.3f} (After current semester)")

        # What-If Simulator
        enrolled = profile.get_in_progress_courses()
        if not enrolled:
            print("\n  No currently enrolled courses detected to simulate.")
            return

        print(f"\n  [INTERACTIVE 'WHAT-IF' SIMULATION FOR CURRENT 5 COURSES]")
        print(f"  Current baseline CGPA: {profile.cgpa:.2f}")

        # Benchmark preset 1: All A+
        all_a_plus = {c.course_code: "A+" for c in enrolled}
        res_a_plus = analytics_engine.simulate_current_semester_scenarios(all_a_plus)
        print(f"\n  Scenario A: If you earn all A+ (4.00 in all 5 courses):")
        print(f"    -> Semester SGPA: {res_a_plus['simulated_sgpa']:.2f} | New CGPA: {res_a_plus['new_projected_cgpa']:.3f} ({res_a_plus['cgpa_delta']})")

        # Benchmark preset 2: All A
        all_a = {c.course_code: "A" for c in enrolled}
        res_a = analytics_engine.simulate_current_semester_scenarios(all_a)
        print(f"  Scenario B: If you earn all A (3.75 in all 5 courses):")
        print(f"    -> Semester SGPA: {res_a['simulated_sgpa']:.2f} | New CGPA: {res_a['new_projected_cgpa']:.3f} ({res_a['cgpa_delta']})")

        # Benchmark preset 3: Expected Historical Trend
        trend_letter = "A" if forecast['forecasted_sgpa'] >= 3.75 else "B+"
        trend_sim = {c.course_code: trend_letter for c in enrolled}
        res_trend = analytics_engine.simulate_current_semester_scenarios(trend_sim)
        print(f"  Scenario C: Based on linear trend ({trend_letter} average):")
        print(f"    -> Semester SGPA: {res_trend['simulated_sgpa']:.2f} | New CGPA: {res_trend['new_projected_cgpa']:.3f} ({res_trend['cgpa_delta']})")

    @classmethod
    def display_course_unlocks(cls, curr_engine, completed_codes: set, current_codes: set) -> None:
        print("\n" + "=" * 80)
        print("  5. PREREQUISITE & COURSE UNLOCK ENGINE (SET-THEORETIC ANALYSIS)")
        print("=" * 80)

        unlocked_core = [c for c in curr_engine.get_unlocked_core_courses(completed_codes) if c.course_code not in current_codes]
        unlocked_electives = [c for c in curr_engine.get_unlocked_electives(completed_codes) if c.course_code not in current_codes]

        print(f"  [1. REMAINING CORE COURSES UNLOCKED RIGHT NOW: {len(unlocked_core)} Courses]")
        for c in unlocked_core:
            print(f"    • {c.get_summary()}")

        print(f"\n  [2. ELIGIBLE ELECTIVES UNLOCKED RIGHT NOW: {len(unlocked_electives)} Courses]")
        for c in unlocked_electives[:12]:  # Show first 12 for clean viewing
            print(f"    • {c.get_summary()}")
        if len(unlocked_electives) > 12:
            print(f"      ... and {len(unlocked_electives) - 12} more eligible electives.")

        # Post-current unlock simulation
        post_unlock = curr_engine.simulate_post_current_unlocks(completed_codes, current_codes)
        print(f"\n  [3. NEW COURSES UNLOCKED ONCE CURRENT SEMESTER IS PASSED: {post_unlock['total_newly_unlocked']} Courses]")
        for c in post_unlock["newly_unlocked_core"]:
            print(f"    ★ CORE:     [{c.course_code}] {c.course_name} (Prereqs: {', '.join(c.prerequisites)})")
        for c in post_unlock["newly_unlocked_electives"]:
            print(f"    ★ ELECTIVE: [{c.course_code}] {c.course_name} (Prereqs: {', '.join(c.prerequisites)})")

    @classmethod
    def display_specialization_tracks(cls, rankings: List[Dict[str, Any]]) -> None:
        print("\n" + "=" * 80)
        print("  6. MAJOR SPECIALIZATION TRACK MATCHER")
        print("=" * 80)
        print("  Evaluates foundation performance to match optimal BScCSE Major Specialization:\n")

        for idx, r in enumerate(rankings, 1):
            bar = cls.draw_bar_chart(f"#{idx} {r['title'][:28]}", r['match_score'], 100.0, 18)
            print(f"  {bar} % | GPA: {r['foundation_gpa']:.2f} [{r['fit_label']}]")
            print(f"     Description: {r['description']}")
            print(f"     Foundations Cleared: {r['taken_foundations_count']} | Unlocked Electives: {r['unlocked_electives_count']}")
            unlocked_names = [f"{c.course_code} ({c.course_name})" for c in r['unlocked_electives'][:3]]
            print(f"     Top Unlocked Options: {', '.join(unlocked_names)}")
            print("  " + "-" * 76)

    @classmethod
    def export_audit_report(cls, profile, stats: Dict[str, Any], domain_results: Dict[str, Any], output_path: str) -> None:
        """
        Exports a complete, structured JSON and text audit report to disk.
        """
        data = {
            "student_profile": {
                "name": profile.student_name,
                "id": profile.student_id,
                "degree": profile.degree,
                "completed_credits": profile.completed_credits,
                "cgpa": profile.cgpa,
            },
            "statistics": stats,
            "domain_strengths": {k: {"gpa": v["domain_gpa"], "credits": v["total_credits"]} for k, v in domain_results.items()},
            "completed_courses_count": len(profile.get_completed_courses_list()),
            "in_progress_courses": [
                {"code": c.course_code, "name": c.course_name, "credits": c.credits} for c in profile.get_in_progress_courses()
            ],
        }

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"\n  [SUCCESS] Academic Audit successfully exported to: {output_path}")


def run_cli():
    """Runs the terminal-based command line interface."""
    from src.curriculum_engine import CurriculumEngine
    from src.report_parser import GradeReportParser
    from src.analytics import AcademicAnalyticsEngine
    from desktop_app import main as launch_desktop_gui

    TerminalUI.print_banner()

    # Base paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    curriculum_path = os.path.join(base_dir, "data", "aiub_curriculum.csv")
    default_report_path = os.path.join(base_dir, "data", "sample_grade_report.txt")
    export_path = os.path.join(base_dir, "data", "student_audit_export.json")

    # In-System Data: AIUB Curriculum Database (Core 309 + Elective 338)
    print("  [IN-SYSTEM DATA] Initializing AIUB BScCSE Curriculum Knowledge Base...", end=" ")
    try:
        curr_engine = CurriculumEngine(curriculum_path)
        print(f"DONE ({len(curr_engine.catalog)} courses registered)")
    except Exception as e:
        print(f"\n[ERROR] In-system curriculum database missing: {e}")
        return

    name_lookup = {c.course_name: c.course_code for c in curr_engine.catalog.values()}
    parser = GradeReportParser(name_lookup)

    # User Input: ONLY the Grade Report is required
    report_file = None
    args = [a for a in sys.argv[1:] if a not in ("--cli", "-c")]
    if len(args) > 0 and os.path.exists(args[0].strip('"\'')):
        report_file = args[0].strip('"\'')
    else:
        print("\n  [USER INPUT REQUIRED]")
        print("  Please provide your AIUB Grade Report (Supports PDF or TXT).")
        try:
            user_input = input(f"  Enter file path [or press ENTER for default '{os.path.basename(default_report_path)}']: ").strip().strip('"\'')
            if user_input and os.path.exists(user_input):
                report_file = user_input
            else:
                report_file = default_report_path
        except (EOFError, KeyboardInterrupt):
            report_file = default_report_path

    print(f"\n  Ingesting Grade Report from: '{os.path.basename(report_file)}'...", end=" ")
    try:
        profile = parser.parse_file(report_file)
        completed_codes = profile.get_completed_course_codes()
        in_progress = profile.get_in_progress_courses()
        current_codes = {c.course_code for c in in_progress}
        print("DONE")
        print(f"  • Student    : {profile.student_name} (ID: {profile.student_id})")
        print(f"  • Progress   : {len(completed_codes)} Completed Courses ({profile.completed_credits:.1f} Cr) | CGPA: {profile.cgpa:.2f}")
        print(f"  • In-Progress: {len(in_progress)} Ongoing Courses ({sum(c.credits for c in in_progress):.1f} Cr)")
    except Exception as e:
        print(f"\n[ERROR] Failed to parse grade report '{report_file}': {e}")
        return

    analytics = AcademicAnalyticsEngine(profile)

    # Interactive Menu Loop (Error Resilient - FR-7)
    while True:
        TerminalUI.print_menu()
        try:
            choice = input("Enter option [0-8] (or 'q' to quit): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting AIUB-PathFinder...")
            break

        if choice in ("0", "q", "exit"):
            print("\nThank you for using AIUB-PathFinder. Best wishes for your semester!")
            break

        elif choice == "g":
            print("Launching Native Desktop GUI Window...")
            launch_desktop_gui()

        elif choice == "1":
            TerminalUI.display_profile_summary(profile)

        elif choice == "2":
            stats = analytics.compute_statistical_overview()
            progression = analytics.generate_sgpa_progression_table()
            TerminalUI.display_statistical_overview(stats, progression)

        elif choice == "3":
            TerminalUI.display_cgpa_line_chart(profile)

        elif choice == "4":
            domain_results = analytics.compute_domain_strengths(curr_engine.domain_map)
            TerminalUI.display_domain_strengths(domain_results)

        elif choice == "5":
            forecast = analytics.forecast_next_semester_sgpa()
            TerminalUI.display_forecaster_and_simulation(forecast, analytics, profile)

        elif choice == "6":
            TerminalUI.display_course_unlocks(curr_engine, completed_codes, current_codes)

        elif choice == "7":
            in_progress_codes = {c.course_code for c in profile.get_in_progress_courses()}
            rankings = curr_engine.evaluate_specialization_tracks(
                profile.get_completed_courses_list(),
                completed_codes,
                in_progress_codes
            )
            TerminalUI.display_specialization_tracks(rankings)

        elif choice == "8":
            stats = analytics.compute_statistical_overview()
            domain_results = analytics.compute_domain_strengths(curr_engine.domain_map)
            TerminalUI.export_audit_report(profile, stats, domain_results, export_path)

        else:
            print("\n[!] Invalid selection. Please enter a number between 0 and 8.")

        try:
            input("\nPress [Enter] to return to menu...")
        except (EOFError, KeyboardInterrupt):
            break
