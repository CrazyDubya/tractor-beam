"""
Job Manager Dialog

This module provides a dialog for creating and editing individual jobs.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class JobManager:
    """Dialog for creating and editing jobs"""
    
    def __init__(self, parent, job=None):
        self.result = None
        self.job = job.copy() if job else self.get_default_job()
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Job Manager" if job else "Add New Job")
        self.dialog.geometry("700x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        # Wait for dialog to close
        self.dialog.wait_window()
        
    def get_default_job(self):
        """Get default job structure"""
        return {
            "url": "",
            "types": [],
            "beacon": None,
            "delay": None,
            "tasks": ["abduct", "visits"],
            "custom": []
        }
        
    def setup_ui(self):
        """Setup the job manager interface"""
        # Main frame with notebook
        main_frame = ttk.Frame(self.dialog, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Basic settings tab
        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Basic Settings")
        self.setup_basic_settings(basic_frame)
        
        # Advanced settings tab
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced Settings")
        self.setup_advanced_settings(advanced_frame)
        
        # Tasks tab
        tasks_frame = ttk.Frame(notebook)
        notebook.add(tasks_frame, text="Tasks")
        self.setup_tasks_settings(tasks_frame)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Save Job", command=self.save).pack(side=tk.RIGHT)
        
    def setup_basic_settings(self, parent):
        """Setup basic job settings"""
        # URL
        ttk.Label(parent, text="URL:").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.url_var = tk.StringVar(value=self.job.get("url", ""))
        url_entry = ttk.Entry(parent, textvariable=self.url_var, width=60)
        url_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, padx=(10, 0), pady=(10, 5))
        
        # File types
        ttk.Label(parent, text="File Types:").grid(row=1, column=0, sticky=tk.W, pady=(0, 5))
        types_frame = ttk.Frame(parent)
        types_frame.grid(row=1, column=1, columnspan=2, sticky=tk.EW, padx=(10, 0), pady=(0, 5))
        
        self.types_vars = {}
        common_types = ["pdf", "html", "txt", "doc", "docx", "xml", "json", "csv"]
        current_types = self.job.get("types", [])
        
        for i, file_type in enumerate(common_types):
            var = tk.BooleanVar(value=file_type in current_types)
            self.types_vars[file_type] = var
            cb = ttk.Checkbutton(types_frame, text=file_type, variable=var)
            cb.grid(row=i//4, column=i%4, sticky=tk.W, padx=(0, 10))
            
        # Custom types
        ttk.Label(parent, text="Custom Types:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.custom_types_var = tk.StringVar()
        custom_types_entry = ttk.Entry(parent, textvariable=self.custom_types_var, width=40)
        custom_types_entry.grid(row=2, column=1, sticky=tk.EW, padx=(10, 0), pady=(10, 5))
        ttk.Label(parent, text="(comma separated)").grid(row=2, column=2, sticky=tk.W, padx=(5, 0), pady=(10, 5))
        
        # Set custom types from job
        custom_in_job = [t for t in current_types if t not in common_types]
        if custom_in_job:
            self.custom_types_var.set(", ".join(custom_in_job))
            
        # Beacon
        ttk.Label(parent, text="Beacon:").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.beacon_var = tk.StringVar(value=self.job.get("beacon") or "")
        beacon_combo = ttk.Combobox(parent, textvariable=self.beacon_var,
                                   values=["", "edgar", "youtube", "google", "generic"])
        beacon_combo.grid(row=3, column=1, sticky=tk.EW, padx=(10, 0), pady=(0, 5))
        ttk.Label(parent, text="(optional)").grid(row=3, column=2, sticky=tk.W, padx=(5, 0), pady=(0, 5))
        
        # Description/Notes
        ttk.Label(parent, text="Description:").grid(row=4, column=0, sticky=tk.NW, pady=(10, 5))
        self.description_text = tk.Text(parent, height=4, width=50)
        self.description_text.grid(row=4, column=1, columnspan=2, sticky=tk.EW, padx=(10, 0), pady=(10, 5))
        
        # Load description if it exists
        description = self.job.get("description", "")
        if description:
            self.description_text.insert(tk.END, description)
            
        parent.columnconfigure(1, weight=1)
        
    def setup_advanced_settings(self, parent):
        """Setup advanced job settings"""
        # Delay
        ttk.Label(parent, text="Delay (seconds):").grid(row=0, column=0, sticky=tk.W, pady=(10, 5))
        self.delay_var = tk.StringVar(value=str(self.job.get("delay") or ""))
        delay_entry = ttk.Entry(parent, textvariable=self.delay_var, width=20)
        delay_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 5))
        ttk.Label(parent, text="(for periodic execution)").grid(row=0, column=2, sticky=tk.W, padx=(5, 0), pady=(10, 5))
        
        # Recursion settings
        recursion_frame = ttk.LabelFrame(parent, text="Recursion Settings", padding=10)
        recursion_frame.grid(row=1, column=0, columnspan=3, sticky=tk.EW, pady=(10, 0))
        
        self.recursive_var = tk.BooleanVar(value=self.job.get("recursive", False))
        ttk.Checkbutton(recursion_frame, text="Enable recursive crawling", 
                       variable=self.recursive_var).pack(anchor=tk.W, pady=(0, 5))
        
        ttk.Label(recursion_frame, text="Max depth:").pack(anchor=tk.W)
        self.max_depth_var = tk.StringVar(value=str(self.job.get("max_depth", 1)))
        depth_entry = ttk.Entry(recursion_frame, textvariable=self.max_depth_var, width=10)
        depth_entry.pack(anchor=tk.W, pady=(0, 5))
        
        # Output settings
        output_frame = ttk.LabelFrame(parent, text="Output Settings", padding=10)
        output_frame.grid(row=2, column=0, columnspan=3, sticky=tk.EW, pady=(10, 0))
        
        ttk.Label(output_frame, text="Output directory:").pack(anchor=tk.W)
        self.output_dir_var = tk.StringVar(value=self.job.get("output_dir", ""))
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var, width=50)
        output_entry.pack(fill=tk.X, pady=(0, 5))
        
        self.overwrite_var = tk.BooleanVar(value=self.job.get("overwrite", False))
        ttk.Checkbutton(output_frame, text="Overwrite existing files", 
                       variable=self.overwrite_var).pack(anchor=tk.W)
        
        parent.columnconfigure(1, weight=1)
        
    def setup_tasks_settings(self, parent):
        """Setup task configuration"""
        ttk.Label(parent, text="Select tasks to perform for this job:").pack(anchor=tk.W, pady=(10, 10))
        
        # Task checkboxes
        self.task_vars = {}
        tasks = ["abduct", "visits", "process"]
        task_descriptions = {
            "abduct": "Download files from URL",
            "visits": "Create CSV records",
            "process": "Process and extract text content"
        }
        
        current_tasks = self.job.get("tasks", ["abduct", "visits"])
        
        for task in tasks:
            var = tk.BooleanVar(value=task in current_tasks)
            self.task_vars[task] = var
            
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, pady=2)
            
            cb = ttk.Checkbutton(frame, text=task.title(), variable=var)
            cb.pack(side=tk.LEFT)
            
            desc_label = ttk.Label(frame, text=task_descriptions[task], foreground="gray")
            desc_label.pack(side=tk.LEFT, padx=(10, 0))
            
        # Custom processing
        custom_frame = ttk.LabelFrame(parent, text="Custom Processing", padding=10)
        custom_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        ttk.Label(custom_frame, text="Custom function:").pack(anchor=tk.W)
        self.custom_func_var = tk.StringVar()
        custom_func_entry = ttk.Entry(custom_frame, textvariable=self.custom_func_var, width=50)
        custom_func_entry.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(custom_frame, text="Custom headers (JSON):").pack(anchor=tk.W)
        self.custom_headers_text = tk.Text(custom_frame, height=6)
        self.custom_headers_text.pack(fill=tk.BOTH, expand=True)
        
        # Load custom settings
        custom = self.job.get("custom", [])
        if custom and len(custom) > 0:
            first_custom = custom[0]
            self.custom_func_var.set(first_custom.get("func", ""))
            headers = first_custom.get("headers")
            if headers:
                import json
                self.custom_headers_text.insert(tk.END, json.dumps(headers, indent=2))
                
    def save(self):
        """Save the job configuration"""
        try:
            # Build job from form data
            job = {}
            
            # Basic settings
            job["url"] = self.url_var.get().strip()
            if not job["url"]:
                messagebox.showerror("Error", "URL is required")
                return
                
            # File types
            types = []
            for file_type, var in self.types_vars.items():
                if var.get():
                    types.append(file_type)
                    
            # Add custom types
            custom_types = self.custom_types_var.get().strip()
            if custom_types:
                custom_types_list = [t.strip() for t in custom_types.split(",") if t.strip()]
                types.extend(custom_types_list)
                
            job["types"] = types
            
            # Beacon
            beacon = self.beacon_var.get().strip()
            job["beacon"] = beacon if beacon else None
            
            # Delay
            delay = self.delay_var.get().strip()
            if delay:
                try:
                    job["delay"] = float(delay)
                except ValueError:
                    messagebox.showerror("Error", "Delay must be a number")
                    return
            else:
                job["delay"] = None
                
            # Tasks
            tasks = []
            for task, var in self.task_vars.items():
                if var.get():
                    tasks.append(task)
            job["tasks"] = tasks
            
            # Description
            description = self.description_text.get(1.0, tk.END).strip()
            if description:
                job["description"] = description
                
            # Advanced settings
            if self.recursive_var.get():
                job["recursive"] = True
                try:
                    job["max_depth"] = int(self.max_depth_var.get())
                except ValueError:
                    job["max_depth"] = 1
                    
            output_dir = self.output_dir_var.get().strip()
            if output_dir:
                job["output_dir"] = output_dir
                
            if self.overwrite_var.get():
                job["overwrite"] = True
                
            # Custom processing
            custom_func = self.custom_func_var.get().strip()
            custom_headers = self.custom_headers_text.get(1.0, tk.END).strip()
            
            if custom_func or custom_headers:
                custom_obj = {"func": custom_func}
                
                if custom_headers:
                    try:
                        import json
                        headers = json.loads(custom_headers)
                        custom_obj["headers"] = headers
                    except json.JSONDecodeError:
                        messagebox.showerror("Error", "Invalid JSON in custom headers")
                        return
                        
                job["custom"] = [custom_obj]
            else:
                job["custom"] = []
                
            self.result = job
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save job:\n{str(e)}")
            
    def cancel(self):
        """Cancel job editing and close dialog"""
        self.dialog.destroy()