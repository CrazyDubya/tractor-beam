"""
Configuration Editor Dialog

This module provides a dialog for editing tractor-beam configurations.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json


class ConfigEditor:
    """Dialog for editing configuration settings"""
    
    def __init__(self, parent, config):
        self.result = None
        self.config = config.copy()
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Configuration")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
    def setup_ui(self):
        """Setup the configuration editor interface"""
        # Main frame
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuration sections
        self.setup_general_settings(main_frame)
        self.setup_project_settings(main_frame)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.RIGHT)
        
    def setup_general_settings(self, parent):
        """Setup general configuration settings"""
        general_frame = ttk.LabelFrame(parent, text="General Settings", padding=10)
        general_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Role
        ttk.Label(general_frame, text="Role:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.role_var = tk.StringVar(value=self.config.get("role", "server"))
        role_combo = ttk.Combobox(general_frame, textvariable=self.role_var, 
                                 values=["server", "client", "watcher"], state="readonly")
        role_combo.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 5))
        
        general_frame.columnconfigure(1, weight=1)
        
    def setup_project_settings(self, parent):
        """Setup project-specific settings"""
        project_frame = ttk.LabelFrame(parent, text="Project Settings", padding=10)
        project_frame.pack(fill=tk.BOTH, expand=True)
        
        settings = self.config.get("settings", {})
        
        # Project name
        ttk.Label(project_frame, text="Project Name:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.name_var = tk.StringVar(value=settings.get("name", ""))
        name_entry = ttk.Entry(project_frame, textvariable=self.name_var)
        name_entry.grid(row=0, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 5))
        
        # Project directory
        ttk.Label(project_frame, text="Project Directory:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        self.proj_dir_var = tk.StringVar(value=settings.get("proj_dir", "."))
        proj_dir_entry = ttk.Entry(project_frame, textvariable=self.proj_dir_var)
        proj_dir_entry.grid(row=1, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 5))
        
        # JSON editor for advanced settings
        ttk.Label(project_frame, text="Advanced (JSON):").grid(row=2, column=0, sticky=tk.NW, pady=(10, 0))
        
        # Text widget for JSON editing
        json_frame = ttk.Frame(project_frame)
        json_frame.grid(row=2, column=1, sticky=tk.NSEW, padx=(10, 0), pady=(10, 0))
        
        self.json_text = tk.Text(json_frame, height=15, wrap=tk.NONE)
        json_scrollbar_v = ttk.Scrollbar(json_frame, orient=tk.VERTICAL, command=self.json_text.yview)
        json_scrollbar_h = ttk.Scrollbar(json_frame, orient=tk.HORIZONTAL, command=self.json_text.xview)
        self.json_text.configure(yscrollcommand=json_scrollbar_v.set, xscrollcommand=json_scrollbar_h.set)
        
        self.json_text.grid(row=0, column=0, sticky=tk.NSEW)
        json_scrollbar_v.grid(row=0, column=1, sticky=tk.NS)
        json_scrollbar_h.grid(row=1, column=0, sticky=tk.EW)
        
        json_frame.columnconfigure(0, weight=1)
        json_frame.rowconfigure(0, weight=1)
        
        # Load current config into JSON editor
        self.json_text.insert(tk.END, json.dumps(self.config, indent=4))
        
        project_frame.columnconfigure(1, weight=1)
        project_frame.rowconfigure(2, weight=1)
        
    def save(self):
        """Save the configuration changes"""
        try:
            # Try to parse the JSON from the text editor
            json_content = self.json_text.get(1.0, tk.END).strip()
            config_from_json = json.loads(json_content)
            
            # Update basic fields
            config_from_json["role"] = self.role_var.get()
            if "settings" not in config_from_json:
                config_from_json["settings"] = {}
            config_from_json["settings"]["name"] = self.name_var.get()
            config_from_json["settings"]["proj_dir"] = self.proj_dir_var.get()
            
            self.result = config_from_json
            self.dialog.destroy()
            
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"Invalid JSON syntax:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration:\n{str(e)}")
            
    def cancel(self):
        """Cancel editing and close dialog"""
        self.dialog.destroy()