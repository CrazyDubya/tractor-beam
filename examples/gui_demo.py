#!/usr/bin/env python3
"""
Tractor Beam GUI Demo

This script demonstrates the graphical interface for tractor-beam operations.
Run this script to open the GUI application.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from tractor_beam.gui import TractorBeamGUI


def main():
    """Main entry point for the GUI demo"""
    print("Starting Tractor Beam GUI...")
    print("This is a demonstration of the graphical interface for tractor-beam operations.")
    print("Use the GUI to:")
    print("  - Create and edit configurations")
    print("  - Manage scraping jobs")
    print("  - Monitor progress")
    print("  - View results and files")
    print()
    
    try:
        app = TractorBeamGUI()
        app.run()
    except KeyboardInterrupt:
        print("\nGUI closed by user.")
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    sys.exit(main())