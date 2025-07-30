"""
Tractor Beam GUI Module

This module provides a graphical user interface for the tractor-beam library,
making it easier to configure, manage, and monitor data scraping operations.
"""

try:
    from .main_window import TractorBeamGUI
    __all__ = ['TractorBeamGUI']
except ImportError as e:
    if "tkinter" in str(e).lower():
        # tkinter not available - provide a fallback
        class TractorBeamGUI:
            def __init__(self):
                raise ImportError("tkinter is required for the GUI but is not available. "
                                "Please install tkinter or use the programmatic interface instead.")
            
            def run(self):
                pass
                
        __all__ = ['TractorBeamGUI']
    else:
        raise