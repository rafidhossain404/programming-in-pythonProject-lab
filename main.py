"""
AIUB-PathFinder: Academic Performance & Degree Intelligence System
Main Application Entry Point | CSC 4162 Midterm Project
American International University-Bangladesh (AIUB) | Fall 2026-27
"""

import sys
from desktop_app import main as launch_desktop_gui


def main():
    """Main application entry point. Directly launches the Desktop GUI."""
    if "--cli" in sys.argv or "-c" in sys.argv:
        from src.ui import run_cli
        run_cli()
    else:
        launch_desktop_gui()


if __name__ == "__main__":
    main()
