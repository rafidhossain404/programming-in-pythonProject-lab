"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Main Application Entry Point | CSC 4162 Midterm Project
American International University-Bangladesh (AIUB) | Fall 2026-27
"""

import os
import sys
from src.curriculum_engine import CurriculumEngine
from src.report_parser import GradeReportParser
from src.analytics import AcademicAnalyticsEngine
from src.ui import TerminalUI


def main():
    if "--gui" in sys.argv or "-g" in sys.argv:
        from desktop_app import main as run_gui
        run_gui()
        return

    TerminalUI.print_banner()

    # Base paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
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
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1].strip('"\'')):
        report_file = sys.argv[1].strip('"\'')
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
            from desktop_app import main as run_gui
            print("Launching Native Desktop GUI Window...")
            run_gui()

        elif choice == "1":
            # Profile & Summary
            TerminalUI.display_profile_summary(profile)

        elif choice == "2":
            # Statistical Overview & Progression
            stats = analytics.compute_statistical_overview()
            progression = analytics.generate_sgpa_progression_table()
            TerminalUI.display_statistical_overview(stats, progression)

        elif choice == "3":
            # Visual Line Plot (CGPA vs Semesters)
            TerminalUI.display_cgpa_line_chart(profile)

        elif choice == "4":
            # Subject Domain Strengths
            domain_results = analytics.compute_domain_strengths(curr_engine.domain_map)
            TerminalUI.display_domain_strengths(domain_results)

        elif choice == "5":
            # Forecaster & What-If Simulator
            forecast = analytics.forecast_next_semester_sgpa()
            TerminalUI.display_forecaster_and_simulation(forecast, analytics, profile)

        elif choice == "6":
            # Course Unlocks & Prerequisites
            TerminalUI.display_course_unlocks(curr_engine, completed_codes, current_codes)

        elif choice == "7":
            # Major Track Matcher
            rankings = curr_engine.evaluate_specialization_tracks(
                profile.get_completed_courses_list(),
                completed_codes
            )
            TerminalUI.display_specialization_tracks(rankings)

        elif choice == "8":
            # Export Audit
            stats = analytics.compute_statistical_overview()
            domain_results = analytics.compute_domain_strengths(curr_engine.domain_map)
            TerminalUI.export_audit_report(profile, stats, domain_results, export_path)

        else:
            print("\n[!] Invalid selection. Please enter a number between 0 and 8.")

        try:
            input("\nPress [Enter] to return to menu...")
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()
