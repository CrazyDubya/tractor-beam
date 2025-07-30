from .tractor import Beam
from .utils.config import Config

try:
    from .gui import TractorBeamGUI
    __all__ = ["Beam", "Config", "TractorBeamGUI"]
except ImportError:
    # GUI not available (e.g., no tkinter)
    __all__ = ["Beam", "Config"]
    
__version__ = "0.1.2"
