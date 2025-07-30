"""
Main GUI Window for Tractor Beam

This module implements the main graphical interface for tractor-beam operations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import threading
import asyncio
from pathlib import Path
import sys
import os

# Add the parent directory to sys.path to import tractor_beam
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tractor_beam.tractor import Beam
from tractor_beam.utils.config import Config
from .config_editor import ConfigEditor
from .job_manager import JobManager
from .monitor import ProgressMonitor
from .file_viewer import FileViewer


class TractorBeamGUI:
    """Main GUI application for Tractor Beam"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tractor Beam - Data Scraping GUI")
        self.root.geometry("1200x800")
        
        # Current configuration and beam instance
        self.current_config = None
        self.beam = None
        self.config_file_path = None
        
        # Threading for async operations
        self.loop = None
        self.thread = None
        
        self.setup_ui()
        self.setup_menu()
        
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Configuration and Jobs
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        # Right panel - Monitoring and Results
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        self.setup_left_panel(left_frame)
        self.setup_right_panel(right_frame)
        
    def setup_left_panel(self, parent):
        """Setup the left panel with config and job management"""
        # Configuration section
        config_frame = ttk.LabelFrame(parent, text="Configuration", padding=10)
        config_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Config file info
        self.config_info_frame = ttk.Frame(config_frame)
        self.config_info_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(self.config_info_frame, text="Config File:").pack(anchor=tk.W)
        self.config_file_label = ttk.Label(self.config_info_frame, text="No file loaded", foreground="gray")
        self.config_file_label.pack(anchor=tk.W)
        
        # Config buttons
        config_buttons_frame = ttk.Frame(config_frame)
        config_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(config_buttons_frame, text="New Config", command=self.new_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons_frame, text="Load Config", command=self.load_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons_frame, text="Save Config", command=self.save_config).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(config_buttons_frame, text="Edit Config", command=self.edit_config).pack(side=tk.LEFT)
        
        # Job management section
        job_frame = ttk.LabelFrame(config_frame, text="Jobs", padding=10)
        job_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Job list
        self.job_listbox = tk.Listbox(job_frame, height=8)
        job_scrollbar = ttk.Scrollbar(job_frame, orient=tk.VERTICAL, command=self.job_listbox.yview)
        self.job_listbox.configure(yscrollcommand=job_scrollbar.set)
        
        self.job_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        job_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Job buttons
        job_buttons_frame = ttk.Frame(config_frame)
        job_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(job_buttons_frame, text="Add Job", command=self.add_job).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(job_buttons_frame, text="Edit Job", command=self.edit_job).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(job_buttons_frame, text="Remove Job", command=self.remove_job).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(job_buttons_frame, text="Run Jobs", command=self.run_jobs, style="Accent.TButton").pack(side=tk.RIGHT)
        
    def setup_right_panel(self, parent):
        """Setup the right panel with monitoring and results"""
        # Create notebook for tabs
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Progress monitoring tab
        monitor_frame = ttk.Frame(notebook)
        notebook.add(monitor_frame, text="Progress Monitor")
        self.progress_monitor = ProgressMonitor(monitor_frame)
        
        # File viewer tab
        files_frame = ttk.Frame(notebook)
        notebook.add(files_frame, text="Files & Results")
        self.file_viewer = FileViewer(files_frame)
        
        # Tutorial tab
        tutorial_frame = ttk.Frame(notebook)
        notebook.add(tutorial_frame, text="Tutorial")
        self.setup_tutorial_tab(tutorial_frame)
        
    def setup_tutorial_tab(self, parent):
        """Setup the tutorial tab"""
        # Tutorial content
        tutorial_text = tk.Text(parent, wrap=tk.WORD, padx=10, pady=10)
        tutorial_scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tutorial_text.yview)
        tutorial_text.configure(yscrollcommand=tutorial_scrollbar.set)
        
        tutorial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tutorial_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load tutorial content
        tutorial_content = self.get_tutorial_content()
        tutorial_text.insert(tk.END, tutorial_content)
        tutorial_text.configure(state=tk.DISABLED)
        
    def setup_menu(self):
        """Setup the application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Config", command=self.new_config)
        file_menu.add_command(label="Open Config", command=self.load_config)
        file_menu.add_command(label="Save Config", command=self.save_config)
        file_menu.add_command(label="Save Config As...", command=self.save_config_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Load Examples", command=self.load_examples)
        tools_menu.add_command(label="Validate Config", command=self.validate_config)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Tutorial", command=self.show_tutorial)
        help_menu.add_command(label="About", command=self.show_about)
        
    def new_config(self):
        """Create a new configuration"""
        self.current_config = {
            "role": "server",
            "settings": {
                "name": "new_project",
                "proj_dir": ".",
                "jobs": []
            }
        }
        self.config_file_path = None
        self.config_file_label.config(text="New configuration", foreground="blue")
        self.update_job_list()
        self.progress_monitor.log("Created new configuration")
        
    def load_config(self):
        """Load a configuration file"""
        file_path = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.current_config = json.load(f)
                self.config_file_path = file_path
                self.config_file_label.config(text=Path(file_path).name, foreground="green")
                self.update_job_list()
                self.progress_monitor.log(f"Loaded configuration from {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load configuration:\n{str(e)}")
                
    def save_config(self):
        """Save the current configuration"""
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration to save")
            return
            
        if not self.config_file_path:
            self.save_config_as()
            return
            
        try:
            with open(self.config_file_path, 'w') as f:
                json.dump(self.current_config, f, indent=4)
            self.progress_monitor.log(f"Saved configuration to {Path(self.config_file_path).name}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
            
    def save_config_as(self):
        """Save the configuration with a new filename"""
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Configuration As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(self.current_config, f, indent=4)
                self.config_file_path = file_path
                self.config_file_label.config(text=Path(file_path).name, foreground="green")
                self.progress_monitor.log(f"Saved configuration to {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
                
    def edit_config(self):
        """Open the configuration editor"""
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration loaded")
            return
            
        editor = ConfigEditor(self.root, self.current_config)
        if editor.result:
            self.current_config = editor.result
            self.update_job_list()
            self.progress_monitor.log("Configuration updated")
            
    def validate_config(self):
        """Validate the current configuration"""
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration to validate")
            return
            
        try:
            # Create a temporary Config object to validate
            temp_config = Config(self.current_config)
            messagebox.showinfo("Validation", "Configuration is valid!")
            self.progress_monitor.log("Configuration validation successful")
        except Exception as e:
            messagebox.showerror("Validation Error", f"Configuration is invalid:\n{str(e)}")
            self.progress_monitor.log(f"Configuration validation failed: {str(e)}")
            
    def add_job(self):
        """Add a new job"""
        if not self.current_config:
            messagebox.showwarning("Warning", "Please create or load a configuration first")
            return
            
        job_manager = JobManager(self.root)
        if job_manager.result:
            self.current_config["settings"]["jobs"].append(job_manager.result)
            self.update_job_list()
            self.progress_monitor.log("Added new job")
            
    def edit_job(self):
        """Edit the selected job"""
        selection = self.job_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a job to edit")
            return
            
        job_index = selection[0]
        job = self.current_config["settings"]["jobs"][job_index]
        
        job_manager = JobManager(self.root, job)
        if job_manager.result:
            self.current_config["settings"]["jobs"][job_index] = job_manager.result
            self.update_job_list()
            self.progress_monitor.log(f"Updated job {job_index + 1}")
            
    def remove_job(self):
        """Remove the selected job"""
        selection = self.job_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a job to remove")
            return
            
        job_index = selection[0]
        if messagebox.askyesno("Confirm", "Are you sure you want to remove this job?"):
            del self.current_config["settings"]["jobs"][job_index]
            self.update_job_list()
            self.progress_monitor.log(f"Removed job {job_index + 1}")
            
    def update_job_list(self):
        """Update the job list display"""
        self.job_listbox.delete(0, tk.END)
        if self.current_config and "settings" in self.current_config:
            for i, job in enumerate(self.current_config["settings"]["jobs"]):
                url = job.get("url", "No URL")
                types = ", ".join(job.get("types", []))
                if not types:
                    types = "All types"
                self.job_listbox.insert(tk.END, f"{i+1}. {url} ({types})")
                
    def run_jobs(self):
        """Run all configured jobs"""
        if not self.current_config:
            messagebox.showwarning("Warning", "No configuration loaded")
            return
            
        if not self.current_config["settings"]["jobs"]:
            messagebox.showwarning("Warning", "No jobs configured")
            return
            
        # Run jobs in a separate thread
        self.progress_monitor.clear()
        self.progress_monitor.log("Starting job execution...")
        
        def run_async():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                beam = Beam(self.current_config)
                
                async def progress_callback(runs):
                    self.progress_monitor.log(f"Completed job run: {len(runs)} total runs")
                    
                loop.run_until_complete(beam.go(cb=progress_callback))
                
                self.progress_monitor.log("All jobs completed successfully!")
                
                # Update file viewer with results
                if hasattr(beam, 'runs') and beam.runs:
                    self.file_viewer.update_results(beam.runs)
                    
            except Exception as e:
                self.progress_monitor.log(f"Error running jobs: {str(e)}")
                
        threading.Thread(target=run_async, daemon=True).start()
        
    def load_examples(self):
        """Load example configurations"""
        examples_dir = Path(__file__).parent.parent.parent / "examples" / "configs"
        if not examples_dir.exists():
            messagebox.showwarning("Warning", "Examples directory not found")
            return
            
        file_path = filedialog.askopenfilename(
            title="Load Example Configuration",
            initialdir=str(examples_dir),
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    self.current_config = json.load(f)
                self.config_file_path = None  # Mark as unsaved
                self.config_file_label.config(text=f"Example: {Path(file_path).name}", foreground="orange")
                self.update_job_list()
                self.progress_monitor.log(f"Loaded example configuration: {Path(file_path).name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load example:\n{str(e)}")
                
    def show_tutorial(self):
        """Show the tutorial window"""
        tutorial_window = tk.Toplevel(self.root)
        tutorial_window.title("Tractor Beam Tutorial")
        tutorial_window.geometry("800x600")
        
        # Tutorial content
        tutorial_text = tk.Text(tutorial_window, wrap=tk.WORD, padx=20, pady=20)
        tutorial_scrollbar = ttk.Scrollbar(tutorial_window, orient=tk.VERTICAL, command=tutorial_text.yview)
        tutorial_text.configure(yscrollcommand=tutorial_scrollbar.set)
        
        tutorial_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tutorial_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load tutorial content
        tutorial_content = self.get_tutorial_content()
        tutorial_text.insert(tk.END, tutorial_content)
        tutorial_text.configure(state=tk.DISABLED)
        
    def show_about(self):
        """Show the about dialog"""
        about_text = """Tractor Beam GUI v1.0

A graphical interface for the high-efficiency text & file scraper with smart tracking.

Features:
• Visual configuration management
• Job creation and editing
• Progress monitoring
• File and results viewing
• Built-in tutorials and examples

Built with Python and tkinter."""
        
        messagebox.showinfo("About Tractor Beam GUI", about_text)
        
    def get_tutorial_content(self):
        """Get the tutorial content"""
        return """TRACTOR BEAM TUTORIAL

Welcome to Tractor Beam! This tutorial will guide you through using the graphical interface to create and manage data scraping projects.

1. GETTING STARTED

First, you'll need to create or load a configuration. A configuration defines:
- Project settings (name, directory)
- Jobs (what to scrape, where from)
- Processing options

2. CREATING A NEW CONFIGURATION

Click "New Config" to create a fresh configuration. This will give you a basic structure to work with.

3. ADDING JOBS

Jobs define what data to scrape. Each job can specify:
- URL: The web address to scrape from
- Types: File types to download (pdf, html, etc.)
- Beacon: Special processing module
- Delay: Time between operations (for watching)
- Custom: Additional processing options

4. RUNNING JOBS

Once your configuration is set up with jobs, click "Run Jobs" to start the scraping process. You can monitor progress in the Progress Monitor tab.

5. VIEWING RESULTS

After jobs complete, check the Files & Results tab to see what was downloaded and processed.

6. EXAMPLE CONFIGURATIONS

Use "Tools -> Load Examples" to explore pre-built configurations for common scenarios like:
- Web scraping
- Document downloading
- RSS feed monitoring
- Financial data extraction

7. ADVANCED FEATURES

Tractor Beam supports many advanced features:
- Parallel processing
- Custom beacons for specific data sources
- File processing and text extraction
- CSV record management
- Recursive URL discovery

For more detailed information, see the project documentation and example notebooks.

Happy scraping!"""
        
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()


def main():
    """Main entry point for the GUI application"""
    app = TractorBeamGUI()
    app.run()


if __name__ == "__main__":
    main()