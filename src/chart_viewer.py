"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Module: chart_viewer.py
Purpose: Graphical Tkinter Canvas Line Chart Window and High-Resolution
         Terminal 2D Coordinate Graph matching the user's sketched CGPA vs Semesters plot.
"""

from typing import List, Tuple, Optional
import tkinter as tk
from tkinter import ttk


class AcademicChartViewer:
    """
    Renders 2D visual line plots of CGPA & SGPA vs Semesters.
    Supports both graphical Tkinter Canvas popup and high-fidelity Terminal ASCII plotting.
    """

    # =========================================================================
    # 1. GRAPHICAL TKINTER CANVAS WINDOW (Matches User Hand-Drawn Sketch)
    # =========================================================================

    @staticmethod
    def show_graphical_window(
        semesters: List[str],
        cgpas: List[float],
        sgpas: List[float],
        student_name: str = "HOSSAIN, MD. RAFID",
        student_id: str = "23-54787-3"
    ) -> None:
        """
        Launches an interactive graphical Tkinter window plotting CGPA vs Semesters
        on a custom 2D Canvas with axes, ticks, grid, markers, and legend.
        """
        root = tk.Toplevel() if tk._default_root else tk.Tk()
        root.title(f"AIUB-PathFinder | CGPA & SGPA vs Semesters — {student_id}")
        root.geometry("860x580")
        root.configure(bg="#0F172A")  # Deep Slate Dark Theme

        # Header Frame
        hdr = tk.Frame(root, bg="#0F172A")
        hdr.pack(fill="x", padx=25, pady=(15, 5))

        tk.Label(
            hdr,
            text="ACADEMIC PROGRESSION: CGPA vs SEMESTERS",
            font=("Segoe UI", 14, "bold"),
            fg="#F8FAFC",
            bg="#0F172A"
        ).pack(anchor="w")

        tk.Label(
            hdr,
            text=f"Student: {student_name} | ID: {student_id} | American International University-Bangladesh",
            font=("Segoe UI", 9),
            fg="#94A3B8",
            bg="#0F172A"
        ).pack(anchor="w")

        # Canvas for 2D Cartesian Graph
        canvas = tk.Canvas(root, width=800, height=440, bg="#1E293B", highlightthickness=1, highlightbackground="#334155")
        canvas.pack(padx=25, pady=10)

        # Plot Dimensions
        origin_x = 80
        origin_y = 370
        chart_w = 660
        chart_h = 280
        top_y = origin_y - chart_h

        # Y-Axis Range: 2.50 to 4.00
        min_y = 2.50
        max_y = 4.00

        # Draw Grid & Y-Ticks
        for tick in [2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00]:
            ratio = (tick - min_y) / (max_y - min_y)
            ty = origin_y - (ratio * chart_h)
            canvas.create_line(origin_x - 6, ty, origin_x, ty, fill="#94A3B8", width=1)
            canvas.create_line(origin_x, ty, origin_x + chart_w, ty, fill="#334155", width=1, dash=(2, 4))
            canvas.create_text(origin_x - 18, ty, text=f"{tick:.2f}", font=("Segoe UI", 8), fill="#94A3B8")

        # Draw Axes
        canvas.create_line(origin_x, origin_y, origin_x + chart_w + 20, origin_y, fill="#CBD5E1", width=2) # X Axis
        canvas.create_line(origin_x, origin_y, origin_x, top_y - 20, fill="#CBD5E1", width=2)            # Y Axis

        # Axis Labels (Matching user sketch: Y='CGPA', X='semesters')
        canvas.create_text(origin_x + (chart_w // 2), origin_y + 40, text="semesters", font=("Segoe UI", 12, "bold"), fill="#F8FAFC")
        canvas.create_text(25, top_y + (chart_h // 2), text="CGPA", font=("Segoe UI", 12, "bold"), fill="#F8FAFC", angle=90)

        # X-Axis Ticks & Coordinates
        n_pts = len(semesters)
        x_step = chart_w / max(1, n_pts - 1)

        cgpa_pts: List[Tuple[float, float]] = []
        sgpa_pts: List[Tuple[float, float]] = []

        for i, sem_name in enumerate(semesters):
            cx = origin_x + (i * x_step)
            canvas.create_line(cx, origin_y, cx, origin_y + 6, fill="#94A3B8", width=1)

            # Abbreviated semester label
            short_sem = sem_name.replace("20", "").replace(",", "")
            canvas.create_text(cx, origin_y + 18, text=short_sem, font=("Segoe UI", 8), fill="#94A3B8")

            # CGPA Coordinate
            c_val = cgpas[i]
            c_ratio = (c_val - min_y) / (max_y - min_y)
            cy = origin_y - (c_ratio * chart_h)
            cgpa_pts.append((cx, cy))

            # SGPA Coordinate
            s_val = sgpas[i]
            s_ratio = (s_val - min_y) / (max_y - min_y)
            sy = origin_y - (s_ratio * chart_h)
            sgpa_pts.append((cx, sy))

        # 1. Draw SGPA Line (Emerald / Dashed)
        for i in range(len(sgpa_pts) - 1):
            x1, y1 = sgpa_pts[i]
            x2, y2 = sgpa_pts[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill="#34D399", width=2, dash=(3, 3))

        # 2. Draw CGPA Line (Vibrant Blue Solid - Exactly like user's sketch)
        for i in range(len(cgpa_pts) - 1):
            x1, y1 = cgpa_pts[i]
            x2, y2 = cgpa_pts[i + 1]
            canvas.create_line(x1, y1, x2, y2, fill="#38BDF8", width=3)

        # 3. Draw Points & Tooltip Labels for CGPA
        for i, (cx, cy) in enumerate(cgpa_pts):
            val = cgpas[i]
            canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#0284C7", outline="#FFFFFF", width=2)
            canvas.create_text(cx, cy - 14, text=f"{val:.2f}", font=("Segoe UI", 8, "bold"), fill="#BAE6FD")

        # Legend Box
        leg_x = origin_x + chart_w - 240
        leg_y = top_y + 10
        canvas.create_rectangle(leg_x - 10, leg_y - 8, leg_x + 230, leg_y + 35, fill="#0F172A", outline="#475569")
        canvas.create_line(leg_x, leg_y + 5, leg_x + 30, leg_y + 5, fill="#38BDF8", width=3)
        canvas.create_text(leg_x + 85, leg_y + 5, text="CGPA (Cumulative)", font=("Segoe UI", 8, "bold"), fill="#F8FAFC")
        canvas.create_line(leg_x, leg_y + 22, leg_x + 30, leg_y + 22, fill="#34D399", width=2, dash=(3, 3))
        canvas.create_text(leg_x + 85, leg_y + 22, text="SGPA (Semester)", font=("Segoe UI", 8, "bold"), fill="#F8FAFC")

        # Close Button
        btn_frame = tk.Frame(root, bg="#0F172A")
        btn_frame.pack(fill="x", padx=25, pady=(5, 15))
        tk.Button(
            btn_frame,
            text="Close Chart Window",
            command=root.destroy,
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            relief="flat",
            padx=15,
            pady=5
        ).pack(side="right")

        root.mainloop()

    # =========================================================================
    # 2. TERMINAL 2D COORDINATE PLOT (Pure ASCII for CLI environments)
    # =========================================================================

    @staticmethod
    def render_ascii_line_plot(
        semesters: List[str],
        values: List[float],
        y_label: str = "CGPA",
        min_val: float = 3.50,
        max_val: float = 4.00,
        height: int = 12
    ) -> str:
        """
        Draws a 2D Cartesian ASCII graph with Y-axis labeled 'CGPA' and X-axis labeled 'semesters',
        matching the exact layout of the user's hand-drawn image.
        """
        n_points = len(values)
        if n_points < 2:
            return "Need at least 2 semester points to plot graph."

        # Grid matrix initialized with spaces
        width = n_points * 6
        grid = [[" " for _ in range(width)] for _ in range(height)]

        # Map each value to (x, y) grid coordinates
        x_coords = [i * 6 + 1 for i in range(n_points)]
        y_coords = []
        for v in values:
            norm = (v - min_val) / max(0.01, (max_val - min_val))
            row = int(round((1.0 - norm) * (height - 1)))
            row = max(0, min(height - 1, row))
            y_coords.append(row)

        # Plot line segments between points
        for i in range(n_points - 1):
            x1, y1 = x_coords[i], y_coords[i]
            x2, y2 = x_coords[i + 1], y_coords[i + 1]

            # Place marker at vertex
            grid[y1][x1] = "●"

            # Connect with line characters
            dx = x2 - x1
            dy = y2 - y1
            for step in range(1, dx):
                inter_x = x1 + step
                inter_y = int(round(y1 + (dy / dx) * step))
                if 0 <= inter_y < height:
                    grid[inter_y][inter_x] = "─" if dy == 0 else ("╲" if dy > 0 else "╱")

        # Place final marker
        grid[y_coords[-1]][x_coords[-1]] = "●"

        # Build formatted output string with Y-Axis ticks
        lines = []
        lines.append(f"  {y_label}")
        for r in range(height):
            # Calculate tick value for this row
            tick_val = max_val - (r / (height - 1)) * (max_val - min_val)
            row_str = "".join(grid[r])
            lines.append(f"  {tick_val:4.2f} ┤ {row_str}")

        # X-Axis base
        axis_line = "  " + " " * 5 + "└" + "─" * (width + 2) + "▶"
        lines.append(axis_line)

        # X-Axis ticks
        tick_line = "  " + " " * 7
        for i in range(n_points):
            tick_line += f"S{i+1:<5}"
        lines.append(tick_line)

        # X-Axis label centered
        sem_label_line = "  " + " " * (width // 2 - 2) + "semesters"
        lines.append(sem_label_line)

        return "\n".join(lines)
