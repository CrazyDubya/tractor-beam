"""
Progress Monitor

This module provides progress monitoring and logging for tractor-beam operations.
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading


class ProgressMonitor:
    """Progress monitoring and logging widget"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the progress monitor interface"""
        # Progress section
        progress_frame = ttk.LabelFrame(self.parent, text="Progress", padding=10)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                          maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(progress_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)
        
        # Log section
        log_frame = ttk.LabelFrame(self.parent, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        # Log text widget
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, wrap=tk.WORD, state=tk.DISABLED)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Log controls
        log_controls = ttk.Frame(log_frame)
        log_controls.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(log_controls, text="Clear Log", command=self.clear).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Save Log", command=self.save_log).pack(side=tk.LEFT, padx=(5, 0))
        
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(log_controls, text="Auto-scroll", variable=self.auto_scroll_var).pack(side=tk.RIGHT)
        
        # Configure log text tags for different message types
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("timestamp", foreground="gray")
        
    def log(self, message, level="info"):
        """Add a message to the log"""
        def _add_to_log():
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Enable text widget for editing
            self.log_text.configure(state=tk.NORMAL)
            
            # Add timestamp
            self.log_text.insert(tk.END, f"[{timestamp}] ", "timestamp")
            
            # Add message with appropriate tag
            self.log_text.insert(tk.END, f"{message}\n", level)
            
            # Disable text widget
            self.log_text.configure(state=tk.DISABLED)
            
            # Auto-scroll to bottom if enabled
            if self.auto_scroll_var.get():
                self.log_text.see(tk.END)
                
            # Update status
            self.status_var.set(message[:50] + "..." if len(message) > 50 else message)
            
        # Ensure this runs on the main thread
        if threading.current_thread() == threading.main_thread():
            _add_to_log()
        else:
            self.parent.after(0, _add_to_log)
            
    def clear(self):
        """Clear the log"""
        self.log_text.configure(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state=tk.DISABLED)
        self.status_var.set("Log cleared")
        
    def save_log(self):
        """Save the log to a file"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            title="Save Log",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                log_content = self.log_text.get(1.0, tk.END)
                with open(file_path, 'w') as f:
                    f.write(log_content)
                self.log(f"Log saved to {file_path}", "success")
            except Exception as e:
                self.log(f"Failed to save log: {str(e)}", "error")
                
    def set_progress(self, value, maximum=100):
        """Set the progress bar value"""
        def _set_progress():
            self.progress_bar.configure(maximum=maximum)
            self.progress_var.set(value)
            
        # Ensure this runs on the main thread
        if threading.current_thread() == threading.main_thread():
            _set_progress()
        else:
            self.parent.after(0, _set_progress)
            
    def reset_progress(self):
        """Reset the progress bar"""
        self.set_progress(0)
        
    def pulse_progress(self):
        """Start indeterminate progress"""
        def _pulse():
            self.progress_bar.configure(mode='indeterminate')
            self.progress_bar.start()
            
        if threading.current_thread() == threading.main_thread():
            _pulse()
        else:
            self.parent.after(0, _pulse)
            
    def stop_pulse(self):
        """Stop indeterminate progress"""
        def _stop_pulse():
            self.progress_bar.stop()
            self.progress_bar.configure(mode='determinate')
            
        if threading.current_thread() == threading.main_thread():
            _stop_pulse()
        else:
            self.parent.after(0, _stop_pulse)