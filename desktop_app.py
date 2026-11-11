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
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _on_tab_changed(self, event):
        try:
            selected = self.notebook.select()
            if selected == str(self.tab_chart):
                self._render_chart_tab()
            elif selected == str(self.tab_domains):
                self._render_domain_tab()
        except tk.TclError:
            pass

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

            if title == "Degree Completion":
                deg_canvas = tk.Canvas(card, height=4, bg="#334155", highlightthickness=0)
                deg_canvas.pack(fill="x", pady=(4, 0))

                def _animate_degree_bar(frame=0, target_p=pct, c=deg_canvas):
                    try:
                        if not c.winfo_exists():
                            return
                        t = min(1.0, frame / 20.0)
                        ease = 1.0 - (1.0 - t) ** 2
                        w = c.winfo_width()
                        if w <= 1:
                            w = 180
                        c.delete("deg_bar")
                        fill_w = int(w * (target_p / 100.0) * ease)
                        c.create_rectangle(0, 0, fill_w, 4, fill="#34D399", outline="", tags="deg_bar")
                        if t < 1.0:
                            self.root.after(16, lambda: _animate_degree_bar(frame + 1, target_p, c))
                    except tk.TclError:
                        pass

                self.root.after(60, _animate_degree_bar)

    # -------------------------------------------------------------------------
    # TAB 1: CGPA vs Semesters Chart (Canvas Animated Line Plot & Tooltips)
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
        canvas.create_text(origin_x, 20, text="Academic Progression: CGPA & SGPA vs Semesters (Interactive Animation)", font=("Segoe UI", 12, "bold"), fill="#F8FAFC", anchor="w")
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

        def _draw_marker(pt, val):
            px, py = pt
            canvas.create_oval(px - 5, py - 5, px + 5, py + 5, fill="#0284C7", outline="#FFFFFF", width=2, tags="marker")
            canvas.create_text(px, py - 12, text=f"{val:.2f}", font=("Segoe UI", 8, "bold"), fill="#BAE6FD", tags="marker")

        # 60 FPS Progressive Line Drawing Animation
        def _animate_trace(idx=0, t=0.0):
            try:
                if not canvas.winfo_exists():
                    return
            except tk.TclError:
                return

            if idx >= len(cgpa_pts) - 1:
                _draw_marker(cgpa_pts[-1], cgpas[-1])
                return

            x0, y0 = cgpa_pts[idx]
            x1, y1 = cgpa_pts[idx + 1]
            sx0, sy0 = sgpa_pts[idx]
            sx1, sy1 = sgpa_pts[idx + 1]

            cur_x = x0 + (x1 - x0) * t
            cur_y = y0 + (y1 - y0) * t
            cur_sx = sx0 + (sx1 - sx0) * t
            cur_sy = sy0 + (sy1 - sy0) * t

            prev_t = max(0.0, t - 0.15)
            px0 = x0 + (x1 - x0) * prev_t
            py0 = y0 + (y1 - y0) * prev_t
            psx0 = sx0 + (sx1 - sx0) * prev_t
            psy0 = sy0 + (sy1 - sy0) * prev_t

            canvas.create_line(px0, py0, cur_x, cur_y, fill="#38BDF8", width=3, tags="anim_line")
            canvas.create_line(psx0, psy0, cur_sx, cur_sy, fill="#34D399", width=2, dash=(3, 3), tags="anim_line")

            if t == 0.0:
                _draw_marker((x0, y0), cgpas[idx])

            t += 0.15
            if t >= 1.0:
                canvas.create_line(cur_x, cur_y, x1, y1, fill="#38BDF8", width=3, tags="anim_line")
                canvas.create_line(cur_sx, cur_sy, sx1, sy1, fill="#34D399", width=2, dash=(3, 3), tags="anim_line")
                self.root.after(16, lambda: _animate_trace(idx + 1, 0.0))
            else:
                self.root.after(16, lambda: _animate_trace(idx, t))

        _animate_trace(0, 0.0)

        # Interactive Hover Tooltip
        def _on_hover(event):
            try:
                if not canvas.winfo_exists():
                    return
            except tk.TclError:
                return
            canvas.delete("tooltip")
            for i, (cx, cy) in enumerate(cgpa_pts):
                if abs(event.x - cx) < 22:
                    tx = min(cx + 10, chart_w - 40)
                    ty = max(cy - 50, 35)
                    canvas.create_rectangle(tx, ty, tx + 160, ty + 42, fill="#0F172A", outline="#38BDF8", width=1, tags="tooltip")
                    canvas.create_text(tx + 8, ty + 12, text=sems[i].semester_name, font=("Segoe UI", 8, "bold"), fill="#F8FAFC", anchor="w", tags="tooltip")
                    canvas.create_text(tx + 8, ty + 28, text=f"CGPA: {cgpas[i]:.2f} | SGPA: {sgpas[i]:.2f}", font=("Segoe UI", 8), fill="#34D399", anchor="w", tags="tooltip")
                    break

        canvas.bind("<Motion>", _on_hover)

    # -------------------------------------------------------------------------
    # TAB 2: Domain Strengths (Animated Bar Fill)
    # -------------------------------------------------------------------------
    def _render_domain_tab(self):
        for w in self.tab_domains.winfo_children():
            w.destroy()

        results = self.analytics.compute_domain_strengths(self.curr_engine.domain_map)
        sorted_d = sorted(results.values(), key=lambda d: d["domain_gpa"], reverse=True)

        lbl = tk.Label(self.tab_domains, text="Academic Subject Domain Performance Ranking", font=("Segoe UI", 12, "bold"), fg="#F8FAFC", bg="#1E293B")
        lbl.pack(anchor="w", padx=25, pady=(15, 10))

        bar_items = []
        for d in sorted_d:
            f = tk.Frame(self.tab_domains, bg="#1E293B")
            f.pack(fill="x", padx=25, pady=6)

            tk.Label(f, text=f"{d['domain_name']} ({d['total_credits']:.1f} Cr)", font=("Segoe UI", 9, "bold"), fg="#F8FAFC", bg="#1E293B", width=36, anchor="w").pack(side="left")

            c = tk.Canvas(f, width=280, height=18, bg="#334155", highlightthickness=0)
            c.pack(side="left", padx=10)
            target_w = int((d["domain_gpa"] / 4.0) * 280)
            bar_items.append((c, target_w))

            tk.Label(f, text=f"{d['domain_gpa']:.2f} / 4.00  [{d['evaluation']}]", font=("Segoe UI", 9), fg="#38BDF8", bg="#1E293B").pack(side="left")

        # Smooth Quadratic Ease-Out Progress Bar Animation
        def _animate_bars(frame=0):
            try:
                if not self.tab_domains.winfo_exists():
                    return
            except tk.TclError:
                return

            t = min(1.0, frame / 18.0)
            ease = 1.0 - (1.0 - t) ** 2  # ease-out quad
            for c_widget, target_w in bar_items:
                try:
                    if c_widget.winfo_exists():
                        c_widget.delete("bar")
                        cur_w = int(target_w * ease)
                        c_widget.create_rectangle(0, 0, cur_w, 18, fill="#0284C7", outline="", tags="bar")
                except tk.TclError:
                    pass

            if t < 1.0:
                self.root.after(16, lambda: _animate_bars(frame + 1))

        _animate_bars(0)

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


class PathFinderBridge:
    """Two-way IPC bridge between Python OOP backend and Stitch Desktop Dashboard."""

    def __init__(self, profile, analytics, curr_engine, parser, base_dir):
        self.profile = profile
        self.analytics = analytics
        self.curr_engine = curr_engine
        self.parser = parser
        self.base_dir = base_dir

    def get_dashboard_data(self):
        """Serializes current profile, analytics, domains, and tracks for the UI."""
        stats = self.analytics.compute_statistical_overview()
        prog = self.analytics.generate_sgpa_progression_table()
        domains = self.analytics.compute_domain_strengths(self.curr_engine.domain_map)
        completed_codes = self.profile.get_completed_course_codes()
        tracks = self.curr_engine.evaluate_specialization_tracks(self.profile.get_completed_courses_list(), completed_codes)
        unlocked_core = [{'course_code': c.course_code, 'course_name': c.course_name, 'credits': c.credits, 'prerequisites': sorted(c.prerequisites), 'domain': c.domain} for c in self.curr_engine.get_unlocked_core_courses(completed_codes)]
        unlocked_elec = [{'course_code': c.course_code, 'course_name': c.course_name, 'credits': c.credits, 'prerequisites': sorted(c.prerequisites), 'domain': c.domain} for c in self.curr_engine.get_unlocked_electives(completed_codes)]
        enrolled = [{'course_code': c.course_code, 'course_name': c.course_name, 'credits': c.credits, 'is_in_progress': c.is_in_progress} for c in self.profile.get_in_progress_courses()]

        return {
            "student_name": self.profile.student_name,
            "student_id": self.profile.student_id,
            "completed_credits": self.profile.completed_credits,
            "cgpa": self.profile.cgpa,
            "stats": stats,
            "progression": prog,
            "domains": domains,
            "tracks": tracks,
            "unlocked_core": unlocked_core,
            "unlocked_electives": unlocked_elec,
            "enrolled": enrolled,
        }

    def simulate_grades(self, grades: dict):
        """Simulate What-If grades for active enrolled courses."""
        return self.analytics.simulate_current_semester_scenarios(grades)

    def upload_grade_report(self):
        """Opens native file picker to ingest a new PDF or TXT grade report."""
        try:
            import webview
            window = webview.active_window()
            if not window:
                return {"status": "error", "message": "No active window"}

            file_types = ("Grade Reports (*.pdf;*.txt)", "PDF Files (*.pdf)", "Text Files (*.txt)", "All files (*.*)")
            result = window.create_file_dialog(webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types)
            if not result or len(result) == 0:
                return {"status": "cancelled"}

            file_path = result[0]
            self.profile = self.parser.parse_file(file_path)
            self.analytics = AcademicAnalyticsEngine(self.profile)
            return {
                "status": "ok",
                "student_name": self.profile.student_name,
                "student_id": self.profile.student_id,
                "courses_count": len(self.profile.get_completed_courses_list()),
                "cgpa": self.profile.cgpa,
                "completed_credits": self.profile.completed_credits,
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def export_audit(self):
        """Exports academic profile and audit to student_audit_export.json."""
        try:
            export_path = os.path.join(self.base_dir, "data", "student_audit_export.json")
            from src.ui import TerminalUI
            stats = self.analytics.compute_statistical_overview()
            domains = self.analytics.compute_domain_strengths(self.curr_engine.domain_map)
            TerminalUI.export_audit_report(self.profile, stats, domains, export_path)
            return {"status": "ok", "path": export_path}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def launch_stitch_gui():
    """Launches the Stitch Desktop Dashboard via native Edge WebView2 desktop window."""
    import webview

    base_dir = os.path.dirname(os.path.abspath(__file__))
    curriculum_path = os.path.join(base_dir, "data", "aiub_curriculum.csv")
    report_path = os.path.join(base_dir, "data", "sample_grade_report.txt")

    curr_engine = CurriculumEngine(curriculum_path)
    name_lookup = {c.course_name: c.course_code for c in curr_engine.catalog.values()}
    parser = GradeReportParser(name_lookup)
    profile = parser.parse_file(report_path)
    analytics = AcademicAnalyticsEngine(profile)

    bridge = PathFinderBridge(profile, analytics, curr_engine, parser, base_dir)
    html_path = os.path.join(base_dir, "stitch_dashboard", "code.html")

    window = webview.create_window(
        title="AIUB-PathFinder | Academic Intelligence & Degree Telemetry Console",
        url=html_path,
        js_api=bridge,
        width=1440,
        height=920,
        min_size=(1024, 720)
    )
    webview.start(debug=False)


def main():
    if "--tkinter" in sys.argv:
        root = tk.Tk()
        app = PathFinderDesktopApp(root)
        root.mainloop()
        return

    try:
        launch_stitch_gui()
    except Exception as e:
        print(f"[FALLBACK] Could not launch WebView GUI ({e}), falling back to Tkinter...")
        root = tk.Tk()
        app = PathFinderDesktopApp(root)
        root.mainloop()


if __name__ == "__main__":
    main()
