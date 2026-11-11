"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Native Desktop Application (Tkinter GUI)
American International University-Bangladesh (AIUB) | Fall 2026-27
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json

from src.curriculum_engine import CurriculumEngine
from src.report_parser import GradeReportParser
from src.analytics import AcademicAnalyticsEngine
from src.models import GRADE_POINT_MAP


class PathFinderDesktopApp:
    """
    Native Desktop GUI for AIUB-PathFinder using Python standard library (tkinter + ttk).
    Strictly complies with Midterm Project Requirements (Section 6 approved GUI).
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("AIUB-PathFinder | Academic Performance & Degree Intelligence System")
        self.root.geometry("1060x720")
        self.root.minsize(920, 620)
        self.root.configure(bg="#0F172A")

        # Paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        curr_path = os.path.join(self.base_dir, "data", "aiub_curriculum.csv")
        self.default_report = os.path.join(self.base_dir, "data", "sample_grade_report.txt")

        # In-System Curriculum Engine
        self.curr_engine = CurriculumEngine(curr_path)
        name_lookup = {c.course_name: c.course_code for c in self.curr_engine.catalog.values()}
        self.parser = GradeReportParser(name_lookup)

        # State
        self.profile = None
        self.analytics = None
        self.sim_vars = {}

        self._load_report(self.default_report)
        self._build_ui()
        self._refresh_all_views()

    def _load_report(self, filepath: str):
        try:
            self.profile = self.parser.parse_file(filepath)
            self.analytics = AcademicAnalyticsEngine(self.profile)
        except Exception as e:
            messagebox.showerror("Error Opening Report", f"Failed to parse report:\n{e}")

    # =========================================================================
    # UI CONSTRUCTION
    # =========================================================================

    def _build_ui(self):
        # 1. Top Bar
        top_bar = tk.Frame(self.root, bg="#1E293B", height=60)
        top_bar.pack(fill="x", padx=15, pady=(12, 6))

        title_frame = tk.Frame(top_bar, bg="#1E293B")
        title_frame.pack(side="left", padx=15, pady=8)

        tk.Label(
            title_frame,
            text="AIUB-PathFinder",
            font=("Segoe UI", 15, "bold"),
            fg="#38BDF8",
            bg="#1E293B"
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="BScCSE Degree Intelligence System | Fall 2026-27",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#1E293B"
        ).pack(anchor="w")

        btn_frame = tk.Frame(top_bar, bg="#1E293B")
        btn_frame.pack(side="right", padx=15, pady=8)

        tk.Button(
            btn_frame,
            text="📁 Open Grade Report (PDF/TXT)",
            command=self._on_open_file,
            bg="#0284C7",
            fg="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=5,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="💾 Export Audit (.JSON)",
            command=self._on_export_audit,
            bg="#334155",
            fg="#F8FAFC",
            font=("Segoe UI", 9),
            padx=12,
            pady=5,
            relief="flat",
            cursor="hand2"
        ).pack(side="left", padx=5)

        # 2. KPI Cards Row
        self.kpi_frame = tk.Frame(self.root, bg="#0F172A")
        self.kpi_frame.pack(fill="x", padx=15, pady=4)

        # 3. Main Tabs (ttk.Notebook)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#0F172A", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1E293B", foreground="#CBD5E1", padding=[16, 7], font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#0284C7")], foreground=[("selected", "#FFFFFF")])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=(6, 12))

        # Tabs
        self.tab_chart = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_domains = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_whatif = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_unlocks = tk.Frame(self.notebook, bg="#1E293B")
        self.tab_tracks = tk.Frame(self.notebook, bg="#1E293B")

        self.notebook.add(self.tab_chart, text="📈 CGPA vs Semesters Chart")
        self.notebook.add(self.tab_domains, text="🏛️ Domain Strengths")
        self.notebook.add(self.tab_whatif, text="🎯 What-If Simulator")
        self.notebook.add(self.tab_unlocks, text="🔓 Course Unlocks")
        self.notebook.add(self.tab_tracks, text="🏆 Major Specializations")

    # =========================================================================
    # REFRESH VIEWS
    # =========================================================================

    def _refresh_all_views(self):
        self._refresh_kpis()
        self._render_chart_tab()
        self._render_domain_tab()
        self._render_whatif_tab()
        self._render_unlocks_tab()
        self._render_tracks_tab()

    def _refresh_kpis(self):
        for w in self.kpi_frame.winfo_children():
            w.destroy()

        stats = self.analytics.compute_statistical_overview()
        pct = (self.profile.completed_credits / 148.0) * 100.0
        enrolled_cr = sum(c.credits for c in self.profile.get_in_progress_courses())

        kpis = [
            ("Current CGPA", f"{self.profile.cgpa:.2f} / 4.00", "Magna Cum Laude Track", "#38BDF8"),
            ("Degree Completion", f"{self.profile.completed_credits:.1f} / 148.0 Cr", f"{pct:.1f}% Completed", "#34D399"),
            ("Enrolled Load", f"{len(self.profile.get_in_progress_courses())} Courses ({enrolled_cr:.1f} Cr)", "Fall 2026-27 Active", "#F59E0B"),
            ("Academic Consistency", f"σ = {stats.get('std_dev', 0.117):.3f}", stats.get("stability_rating", "Consistent"), "#A855F7"),
        ]

        for title, val, sub, color in kpis:
            card = tk.Frame(self.kpi_frame, bg="#1E293B", padx=14, pady=10)
            card.pack(side="left", fill="both", expand=True, padx=4)
            tk.Label(card, text=title, font=("Segoe UI", 9), fg="#94A3B8", bg="#1E293B").pack(anchor="w")
            tk.Label(card, text=val, font=("Segoe UI", 14, "bold"), fg=color, bg="#1E293B").pack(anchor="w")
            tk.Label(card, text=sub, font=("Segoe UI", 8), fg="#CBD5E1", bg="#1E293B").pack(anchor="w")

    # -------------------------------------------------------------------------
    # TAB 1: CGPA vs Semesters Chart (Canvas Line Plot)
    # -------------------------------------------------------------------------
    def _render_chart_tab(self):
        for w in self.tab_chart.winfo_children():
            w.destroy()

        canvas = tk.Canvas(self.tab_chart, bg="#1E293B", highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=20, pady=15)

        sems = [s for s in self.profile.semesters if not s.is_current and s.cgpa > 0.0]
        if not sems:
            return

        names = [s.semester_name.replace("20", "").replace(",", "") for s in sems]
        cgpas = [s.cgpa for s in sems]
        sgpas = [s.sgpa for s in sems]

        # Canvas Dimensions
        origin_x = 80
        origin_y = 360
        chart_w = 780
        chart_h = 260
        top_y = origin_y - chart_h

        min_y, max_y = 2.50, 4.00

        # Title & Legend
        canvas.create_text(origin_x, 20, text="Academic Progression: CGPA & SGPA vs Semesters", font=("Segoe UI", 12, "bold"), fill="#F8FAFC", anchor="w")
        canvas.create_line(620, 20, 650, 20, fill="#38BDF8", width=3)
        canvas.create_text(655, 20, text="CGPA", font=("Segoe UI", 9, "bold"), fill="#F8FAFC", anchor="w")
        canvas.create_line(720, 20, 750, 20, fill="#34D399", width=2, dash=(3, 3))
        canvas.create_text(755, 20, text="SGPA", font=("Segoe UI", 9, "bold"), fill="#F8FAFC", anchor="w")

        # Grid lines & Y ticks
        for tick in [2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00]:
            ratio = (tick - min_y) / (max_y - min_y)
            ty = origin_y - (ratio * chart_h)
            canvas.create_line(origin_x - 5, ty, origin_x, ty, fill="#94A3B8")
            canvas.create_line(origin_x, ty, origin_x + chart_w, ty, fill="#334155", dash=(2, 4))
            canvas.create_text(origin_x - 12, ty, text=f"{tick:.2f}", font=("Segoe UI", 8), fill="#94A3B8", anchor="e")

        # Axes
        canvas.create_line(origin_x, origin_y, origin_x + chart_w + 15, origin_y, fill="#CBD5E1", width=2)
        canvas.create_line(origin_x, origin_y, origin_x, top_y - 15, fill="#CBD5E1", width=2)
        canvas.create_text(origin_x + (chart_w // 2), origin_y + 35, text="semesters", font=("Segoe UI", 11, "bold"), fill="#F8FAFC")
        canvas.create_text(25, top_y + (chart_h // 2), text="CGPA", font=("Segoe UI", 11, "bold"), fill="#F8FAFC", angle=90)

        step = chart_w / max(1, len(names) - 1)
        cgpa_pts, sgpa_pts = [], []

        for i, sem in enumerate(names):
            cx = origin_x + (i * step)
            canvas.create_line(cx, origin_y, cx, origin_y + 5, fill="#94A3B8")
            canvas.create_text(cx, origin_y + 16, text=sem, font=("Segoe UI", 8), fill="#94A3B8")

            cy = origin_y - (((cgpas[i] - min_y) / (max_y - min_y)) * chart_h)
            sy = origin_y - (((sgpas[i] - min_y) / (max_y - min_y)) * chart_h)
            cgpa_pts.append((cx, cy))
            sgpa_pts.append((cx, sy))

        # Draw Lines
        for i in range(len(sgpa_pts) - 1):
            canvas.create_line(sgpa_pts[i][0], sgpa_pts[i][1], sgpa_pts[i+1][0], sgpa_pts[i+1][1], fill="#34D399", width=2, dash=(3, 3))
        for i in range(len(cgpa_pts) - 1):
            canvas.create_line(cgpa_pts[i][0], cgpa_pts[i][1], cgpa_pts[i+1][0], cgpa_pts[i+1][1], fill="#38BDF8", width=3)

        # Draw Points
        for i, (cx, cy) in enumerate(cgpa_pts):
            canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#0284C7", outline="#FFFFFF", width=2)
            canvas.create_text(cx, cy - 12, text=f"{cgpas[i]:.2f}", font=("Segoe UI", 8, "bold"), fill="#BAE6FD")

    # -------------------------------------------------------------------------
    # TAB 2: Domain Strengths
    # -------------------------------------------------------------------------
    def _render_domain_tab(self):
        for w in self.tab_domains.winfo_children():
            w.destroy()

        results = self.analytics.compute_domain_strengths(self.curr_engine.domain_map)
        sorted_d = sorted(results.values(), key=lambda d: d["domain_gpa"], reverse=True)

        lbl = tk.Label(self.tab_domains, text="Academic Subject Domain Performance Ranking", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#1E293B")
        lbl.pack(anchor="w", padx=25, pady=(15, 10))

        for d in sorted_d:
            f = tk.Frame(self.tab_domains, bg="#1E293B")
            f.pack(fill="x", padx=25, pady=6)

            tk.Label(f, text=f"{d['domain_name']} ({d['total_credits']:.1f} Cr)", font=("Segoe UI", 9, "bold"), fg="#F8FAFC", bg="#1E293B", width=36, anchor="w").pack(side="left")
            
            # Bar Canvas
            c = tk.Canvas(f, width=280, height=18, bg="#334155", highlightthickness=0)
            c.pack(side="left", padx=10)
            fill_w = int((d["domain_gpa"] / 4.0) * 280)
            c.create_rectangle(0, 0, fill_w, 18, fill="#0284C7", outline="")

            tk.Label(f, text=f"{d['domain_gpa']:.2f} / 4.00  [{d['evaluation']}]", font=("Segoe UI", 9), fg="#38BDF8", bg="#1E293B").pack(side="left")

    # -------------------------------------------------------------------------
    # TAB 3: What-If Simulator
    # -------------------------------------------------------------------------
    def _render_whatif_tab(self):
        for w in self.tab_whatif.winfo_children():
            w.destroy()

        enrolled = self.profile.get_in_progress_courses()
        self.sim_vars = {}

        header = tk.Frame(self.tab_whatif, bg="#1E293B")
        header.pack(fill="x", padx=25, pady=(15, 10))

        tk.Label(header, text="Interactive Simulation for 2026-2027 Fall Courses", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#1E293B").pack(side="left")

        # Quick Preset Buttons
        tk.Button(header, text="All A+", command=lambda: self._set_all_grades("A+"), bg="#334155", fg="#FFFFFF", padx=8, pady=2, relief="flat").pack(side="right", padx=3)
        tk.Button(header, text="All A", command=lambda: self._set_all_grades("A"), bg="#334155", fg="#FFFFFF", padx=8, pady=2, relief="flat").pack(side="right", padx=3)
        tk.Button(header, text="Conservative (B+)", command=lambda: self._set_all_grades("B+"), bg="#334155", fg="#FFFFFF", padx=8, pady=2, relief="flat").pack(side="right", padx=3)

        # Course Rows
        for c in enrolled:
            row = tk.Frame(self.tab_whatif, bg="#1E293B")
            row.pack(fill="x", padx=25, pady=5)

            tk.Label(row, text=f"[{c.course_code}] {c.course_name} ({c.credits:.1f} Cr)", font=("Segoe UI", 9, "bold"), fg="#CBD5E1", bg="#1E293B", width=48, anchor="w").pack(side="left")

            var = tk.StringVar(value="A+")
            self.sim_vars[c.course_code] = var
            combo = ttk.Combobox(row, textvariable=var, values=["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"], state="readonly", width=8)
            combo.pack(side="left", padx=10)
            combo.bind("<<ComboboxSelected>>", lambda e: self._recalculate_simulation())

        # Result Banner
        self.sim_result_lbl = tk.Label(self.tab_whatif, text="", font=("Segoe UI", 12, "bold"), fg="#34D399", bg="#1E293B")
        self.sim_result_lbl.pack(pady=20)
        self._recalculate_simulation()

    def _set_all_grades(self, grade: str):
        for var in self.sim_vars.values():
            var.set(grade)
        self._recalculate_simulation()

    def _recalculate_simulation(self):
        grades = {code: var.get() for code, var in self.sim_vars.items()}
        res = self.analytics.simulate_current_semester_scenarios(grades)
        self.sim_result_lbl.config(
            text=f"Projected CGPA: {res['new_projected_cgpa']:.3f}  ({res['cgpa_delta']})  |  Simulated Semester SGPA: {res['simulated_sgpa']:.2f}"
        )

    # -------------------------------------------------------------------------
    # TAB 4: Course Unlocks
    # -------------------------------------------------------------------------
    def _render_unlocks_tab(self):
        for w in self.tab_unlocks.winfo_children():
            w.destroy()

        completed = self.profile.get_completed_course_codes()
        unlocked_core = self.curr_engine.get_unlocked_core_courses(completed)
        unlocked_elec = self.curr_engine.get_unlocked_electives(completed)

        tk.Label(self.tab_unlocks, text=f"Unlocked Core Courses ({len(unlocked_core)} Remaining)", font=("Segoe UI", 11, "bold"), fg="#38BDF8", bg="#1E293B").pack(anchor="w", padx=25, pady=(12, 4))
        for c in unlocked_core:
            tk.Label(self.tab_unlocks, text=f"  • [{c.course_code}] {c.course_name} ({c.credits:.1f} Cr)  |  Prereqs: {', '.join(c.prerequisites) or 'None'}", font=("Segoe UI", 8), fg="#CBD5E1", bg="#1E293B").pack(anchor="w", padx=25)

        tk.Label(self.tab_unlocks, text=f"Top Eligible Electives ({len(unlocked_elec)} Available)", font=("Segoe UI", 11, "bold"), fg="#34D399", bg="#1E293B").pack(anchor="w", padx=25, pady=(15, 4))
        for c in unlocked_elec[:8]:
            tk.Label(self.tab_unlocks, text=f"  • [{c.course_code}] {c.course_name} ({c.credits:.1f} Cr)  |  Prereqs: {', '.join(c.prerequisites) or 'None'}", font=("Segoe UI", 8), fg="#CBD5E1", bg="#1E293B").pack(anchor="w", padx=25)

    # -------------------------------------------------------------------------
    # TAB 5: Major Specialization Track Matcher
    # -------------------------------------------------------------------------
    def _render_tracks_tab(self):
        for w in self.tab_tracks.winfo_children():
            w.destroy()

        rankings = self.curr_engine.evaluate_specialization_tracks(
            self.profile.get_completed_courses_list(),
            self.profile.get_completed_course_codes()
        )

        tk.Label(self.tab_tracks, text="AIUB BScCSE Specialization Track Alignment", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#1E293B").pack(anchor="w", padx=25, pady=(12, 8))

        for idx, r in enumerate(rankings, 1):
            card = tk.Frame(self.tab_tracks, bg="#334155", padx=12, pady=8)
            card.pack(fill="x", padx=25, pady=4)

            tk.Label(card, text=f"#{idx} {r['title']} — {r['match_score']:.1f}% Match [{r['fit_label']}]", font=("Segoe UI", 9, "bold"), fg="#38BDF8", bg="#334155").pack(anchor="w")
            tk.Label(card, text=f"{r['description']} | Foundation GPA: {r['foundation_gpa']:.2f}", font=("Segoe UI", 8), fg="#E2E8F0", bg="#334155").pack(anchor="w")

    # =========================================================================
    # DIALOG ACTIONS
    # =========================================================================

    def _on_open_file(self):
        path = filedialog.askopenfilename(
            title="Select AIUB Grade Report",
            filetypes=[("Grade Reports", "*.txt;*.pdf"), ("All Files", "*.*")]
        )
        if path:
            self._load_report(path)
            self._refresh_all_views()
            messagebox.showinfo("Report Loaded", f"Successfully parsed grade report for {self.profile.student_name}!")

    def _on_export_audit(self):
        path = filedialog.asksaveasfilename(
            title="Export Academic Audit",
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")]
        )
        if path:
            from src.ui import TerminalUI
            stats = self.analytics.compute_statistical_overview()
            domains = self.analytics.compute_domain_strengths(self.curr_engine.domain_map)
            TerminalUI.export_audit_report(self.profile, stats, domains, path)
            messagebox.showinfo("Export Successful", f"Audit report exported to:\n{path}")


def main():
    root = tk.Tk()
    app = PathFinderDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
