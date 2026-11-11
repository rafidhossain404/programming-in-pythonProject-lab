"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: server.py
Purpose: Lightweight HTTP Server using Python standard library (http.server).
         Serves Stitch web dashboard and provides JSON API for live calculations.
         Strictly complies with Midterm rules (No external web frameworks).
"""

import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.curriculum_engine import CurriculumEngine
from src.report_parser import GradeReportParser
from src.analytics import AcademicAnalyticsEngine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRICULUM_PATH = os.path.join(BASE_DIR, "data", "aiub_curriculum.csv")
DEFAULT_REPORT_PATH = os.path.join(BASE_DIR, "data", "sample_grade_report.txt")
UI_HTML_PATH = os.path.join(BASE_DIR, "ui_prototype", "code.html")

# Initialize in-system curriculum & parser
curr_engine = CurriculumEngine(CURRICULUM_PATH)
name_lookup = {c.course_name: c.course_code for c in curr_engine.catalog.values()}
parser = GradeReportParser(name_lookup)
current_profile = parser.parse_file(DEFAULT_REPORT_PATH)
analytics = AcademicAnalyticsEngine(current_profile)


def get_dashboard_payload():
    """Generates complete JSON payload for the web dashboard."""
    completed_codes = current_profile.get_completed_course_codes()
    in_progress = current_profile.get_in_progress_courses()
    current_codes = {c.course_code for c in in_progress}

    stats = analytics.compute_statistical_overview()
    progression = analytics.generate_sgpa_progression_table()
    domain_results = analytics.compute_domain_strengths(curr_engine.domain_map)
    forecast = analytics.forecast_next_semester_sgpa()
    rankings = curr_engine.evaluate_specialization_tracks(
        current_profile.get_completed_courses_list(),
        completed_codes
    )
    unlocked_core = curr_engine.get_unlocked_core_courses(completed_codes)
    unlocked_electives = curr_engine.get_unlocked_electives(completed_codes)
    post_unlocks = curr_engine.simulate_post_current_unlocks(completed_codes, current_codes)

    return {
        "student": {
            "name": current_profile.student_name,
            "id": current_profile.student_id,
            "degree": current_profile.degree,
            "completed_credits": current_profile.completed_credits,
            "cgpa": current_profile.cgpa,
            "degree_pct": round((current_profile.completed_credits / 148.0) * 100, 1),
        },
        "stats": stats,
        "progression": progression,
        "domains": [
            {
                "key": k,
                "name": v["domain_name"],
                "gpa": v["domain_gpa"],
                "credits": v["total_credits"],
                "eval": v["evaluation"],
            }
            for k, v in domain_results.items()
        ],
        "forecast": forecast,
        "tracks": [
            {
                "title": r["title"],
                "match_score": r["match_score"],
                "gpa": r["foundation_gpa"],
                "fit_label": r["fit_label"],
                "cleared": r["taken_foundations_count"],
                "unlocked_count": r["unlocked_electives_count"],
            }
            for r in rankings
        ],
        "enrolled_courses": [
            {"code": c.course_code, "name": c.course_name, "credits": c.credits}
            for c in in_progress
        ],
        "unlocked_core": [{"code": c.course_code, "name": c.course_name, "credits": c.credits} for c in unlocked_core],
        "unlocked_electives": [{"code": c.course_code, "name": c.course_name, "credits": c.credits} for c in unlocked_electives],
        "post_unlocks": {
            "core": [{"code": c.course_code, "name": c.course_name} for c in post_unlocks["newly_unlocked_core"]],
            "electives": [{"code": c.course_code, "name": c.course_name} for c in post_unlocks["newly_unlocked_electives"]],
        }
    }


class DashboardHandler(BaseHTTPRequestHandler):
    """Handles static UI requests and JSON API routes."""

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._serve_file(UI_HTML_PATH, "text/html; charset=utf-8")
        elif self.path == "/api/data":
            self._send_json(get_dashboard_payload())
        elif self.path.startswith("/screen.png"):
            png_path = os.path.join(BASE_DIR, "ui_prototype", "screen.png")
            self._serve_file(png_path, "image/png")
        else:
            self.send_error(404, "Route not found")

    def do_POST(self):
        global current_profile, analytics
        if self.path == "/api/simulate":
            # What-If calculation endpoint
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            try:
                data = json.loads(body)
                grades = data.get("grades", {})
                result = analytics.simulate_current_semester_scenarios(grades)
                self._send_json(result)
            except Exception as e:
                self.send_error(400, f"Simulation error: {e}")

        elif self.path == "/api/upload":
            # Grade report upload endpoint
            content_len = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(content_len)
            try:
                # Save uploaded bytes to temp file and parse
                temp_upload = os.path.join(BASE_DIR, "data", "latest_uploaded_report.txt")
                with open(temp_upload, "wb") as f:
                    f.write(raw_data)
                current_profile = parser.parse_file(temp_upload)
                analytics = AcademicAnalyticsEngine(current_profile)
                self._send_json({"status": "success", "data": get_dashboard_payload()})
            except Exception as e:
                self.send_error(400, f"Upload parsing error: {e}")
        else:
            self.send_error(404, "Endpoint not found")

    def _serve_file(self, filepath: str, content_type: str):
        if not os.path.exists(filepath):
            self.send_error(404, "File not found")
            return
        with open(filepath, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _send_json(self, data: dict):
        raw = json.dumps(data).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, format, *args):
        # Quiet standard HTTP logging for clean terminal
        pass


def run_server(port: int = 8000):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print("=" * 80)
    print(f"  AIUB-PathFinder Web Dashboard Live at: http://127.0.0.1:{port}/")
    print("  Serving Stitch UI connected to Python backend API.")
    print("  Press Ctrl+C to stop the server.")
    print("=" * 80)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  Dashboard server stopped.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
