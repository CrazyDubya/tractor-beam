"""
File Viewer

This module provides file and results viewing functionality.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import json


class FileViewer:
    """File and results viewing widget"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_results = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the file viewer interface"""
        # Create paned window for file tree and content
        paned_window = ttk.PanedWindow(self.parent, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - File tree
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        
        # Right panel - File content
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=2)
        
        self.setup_file_tree(left_frame)
        self.setup_content_viewer(right_frame)
        
    def setup_file_tree(self, parent):
        """Setup the file tree browser"""
        # File tree controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(controls_frame, text="Browse Folder", command=self.browse_folder).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="Refresh", command=self.refresh_tree).pack(side=tk.LEFT, padx=(5, 0))
        
        # File tree
        tree_frame = ttk.LabelFrame(parent, text="Files", padding=5)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for files
        self.file_tree = ttk.Treeview(tree_frame, columns=("size", "modified"), show="tree headings")
        self.file_tree.heading("#0", text="Name")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("modified", text="Modified")
        
        self.file_tree.column("#0", width=200)
        self.file_tree.column("size", width=80)
        self.file_tree.column("modified", width=120)
        
        # Scrollbars for tree
        tree_scroll_v = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.file_tree.yview)
        tree_scroll_h = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.file_tree.xview)
        self.file_tree.configure(yscrollcommand=tree_scroll_v.set, xscrollcommand=tree_scroll_h.set)
        
        self.file_tree.grid(row=0, column=0, sticky=tk.NSEW)
        tree_scroll_v.grid(row=0, column=1, sticky=tk.NS)
        tree_scroll_h.grid(row=1, column=0, sticky=tk.EW)
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        # Bind tree selection
        self.file_tree.bind("<<TreeviewSelect>>", self.on_file_select)
        
        # Context menu for tree
        self.tree_menu = tk.Menu(self.file_tree, tearoff=0)
        self.tree_menu.add_command(label="Open", command=self.open_selected_file)
        self.tree_menu.add_command(label="Open in System", command=self.open_in_system)
        self.tree_menu.add_separator()
        self.tree_menu.add_command(label="Copy Path", command=self.copy_path)
        self.tree_menu.add_command(label="Show in Explorer", command=self.show_in_explorer)
        
        self.file_tree.bind("<Button-3>", self.show_tree_menu)
        
    def setup_content_viewer(self, parent):
        """Setup the content viewer"""
        # Content viewer controls
        controls_frame = ttk.Frame(parent)
        controls_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.file_path_var = tk.StringVar(value="No file selected")
        ttk.Label(controls_frame, textvariable=self.file_path_var, foreground="gray").pack(side=tk.LEFT)
        
        ttk.Button(controls_frame, text="Save Content", command=self.save_content).pack(side=tk.RIGHT)
        
        # Notebook for different content types
        content_notebook = ttk.Notebook(parent)
        content_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Text content tab
        text_frame = ttk.Frame(content_notebook)
        content_notebook.add(text_frame, text="Text Content")
        
        self.text_content = tk.Text(text_frame, wrap=tk.WORD, state=tk.DISABLED)
        text_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_content.yview)
        self.text_content.configure(yscrollcommand=text_scroll.set)
        
        self.text_content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Results summary tab
        results_frame = ttk.Frame(content_notebook)
        content_notebook.add(results_frame, text="Results Summary")
        
        self.results_tree = ttk.Treeview(results_frame, columns=("status", "files", "data"), show="tree headings")
        self.results_tree.heading("#0", text="Job")
        self.results_tree.heading("status", text="Status")
        self.results_tree.heading("files", text="Files")
        self.results_tree.heading("data", text="Data")
        
        results_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=results_scroll.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        results_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_folder(self):
        """Browse for a folder to display"""
        folder_path = filedialog.askdirectory(title="Select Folder to Browse")
        if folder_path:
            self.load_folder(folder_path)
            
    def load_folder(self, folder_path):
        """Load a folder into the file tree"""
        try:
            # Clear existing items
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
                
            # Add folder contents
            self._add_folder_to_tree("", folder_path)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load folder:\n{str(e)}")
            
    def _add_folder_to_tree(self, parent, folder_path):
        """Recursively add folder contents to tree"""
        try:
            folder = Path(folder_path)
            
            # Add files first
            for item in sorted(folder.iterdir()):
                if item.is_file():
                    size = self._format_size(item.stat().st_size)
                    modified = self._format_time(item.stat().st_mtime)
                    
                    self.file_tree.insert(parent, tk.END, text=item.name, 
                                        values=(size, modified), tags=("file",))
                    
            # Then add directories
            for item in sorted(folder.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    dir_item = self.file_tree.insert(parent, tk.END, text=item.name, 
                                                   values=("", ""), tags=("folder",))
                    
                    # Add a dummy child to make it expandable
                    self.file_tree.insert(dir_item, tk.END, text="Loading...")
                    
        except PermissionError:
            pass  # Skip folders we can't access
            
    def _format_size(self, size_bytes):
        """Format file size for display"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes/(1024**2):.1f} MB"
        else:
            return f"{size_bytes/(1024**3):.1f} GB"
            
    def _format_time(self, timestamp):
        """Format timestamp for display"""
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime("%m/%d/%Y %H:%M")
        
    def refresh_tree(self):
        """Refresh the current tree view"""
        # Get the current root path if any
        if hasattr(self, '_current_folder'):
            self.load_folder(self._current_folder)
            
    def on_file_select(self, event):
        """Handle file selection in tree"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            file_path = self._get_item_path(item)
            
            if file_path and os.path.isfile(file_path):
                self.load_file_content(file_path)
                
    def _get_item_path(self, item):
        """Get the full path for a tree item"""
        # This is a simplified version - in a real implementation,
        # you'd need to track the full paths properly
        return None
        
    def load_file_content(self, file_path):
        """Load and display file content"""
        try:
            self.file_path_var.set(f"Loading: {Path(file_path).name}")
            
            # Try to read as text
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Enable text widget and update content
            self.text_content.configure(state=tk.NORMAL)
            self.text_content.delete(1.0, tk.END)
            self.text_content.insert(tk.END, content)
            self.text_content.configure(state=tk.DISABLED)
            
            self.file_path_var.set(str(file_path))
            
        except Exception as e:
            self.text_content.configure(state=tk.NORMAL)
            self.text_content.delete(1.0, tk.END)
            self.text_content.insert(tk.END, f"Error loading file: {str(e)}")
            self.text_content.configure(state=tk.DISABLED)
            
    def save_content(self):
        """Save the current content to a file"""
        content = self.text_content.get(1.0, tk.END)
        if not content.strip():
            messagebox.showwarning("Warning", "No content to save")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Save Content",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(content)
                messagebox.showinfo("Success", f"Content saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save content:\n{str(e)}")
                
    def update_results(self, results):
        """Update the results display"""
        self.current_results = results
        
        # Clear existing results
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
            
        # Add new results
        for i, run in enumerate(results):
            status = run.get("status", "unknown")
            
            # Count files and data
            file_count = 0
            data_count = 0
            
            if "Abduct" in run and hasattr(run["Abduct"], "state") and run["Abduct"].state:
                file_count = len(run["Abduct"].state.data)
                
            if "data" in run:
                data_count = len(run["data"])
                
            self.results_tree.insert("", tk.END, text=f"Run {i+1}", 
                                   values=(status, file_count, data_count))
                                   
    def show_tree_menu(self, event):
        """Show context menu for tree"""
        item = self.file_tree.identify_row(event.y)
        if item:
            self.file_tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)
            
    def open_selected_file(self):
        """Open the selected file in the content viewer"""
        selection = self.file_tree.selection()
        if selection:
            # Implementation would depend on how paths are tracked
            pass
            
    def open_in_system(self):
        """Open file with system default application"""
        selection = self.file_tree.selection()
        if selection:
            # Implementation would depend on how paths are tracked
            pass
            
    def copy_path(self):
        """Copy file path to clipboard"""
        selection = self.file_tree.selection()
        if selection:
            # Implementation would depend on how paths are tracked
            pass
            
    def show_in_explorer(self):
        """Show file in system file manager"""
        selection = self.file_tree.selection()
        if selection:
            # Implementation would depend on how paths are tracked
            pass