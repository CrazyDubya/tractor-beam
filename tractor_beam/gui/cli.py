"""
Tractor Beam GUI Entry Point

This module provides a command-line entry point for launching the GUI.
"""

def main():
    """Main entry point for the GUI application"""
    try:
        from .main_window import TractorBeamGUI
        app = TractorBeamGUI()
        app.run()
    except ImportError as e:
        if "tkinter" in str(e).lower():
            print("Error: tkinter is required for the GUI but is not available.")
            print("Please install tkinter or use the programmatic interface instead.")
            print("\nAlternatively, you can use tractor-beam without the GUI:")
            print("  from tractor_beam import tractor")
            print("  beam = tractor.Beam('config.json')")
            print("  await beam.go()")
        else:
            print(f"Error importing GUI components: {e}")
        return 1
    except Exception as e:
        print(f"Error starting GUI: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())