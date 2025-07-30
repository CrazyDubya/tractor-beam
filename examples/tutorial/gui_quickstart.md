# GUI Quick Start Guide

This guide will get you up and running with the Tractor Beam GUI in just a few minutes.

## Step 1: Launch the GUI

```bash
cd examples
python gui_demo.py
```

Or in your Python code:
```python
from tractor_beam.gui import TractorBeamGUI
app = TractorBeamGUI()
app.run()
```

## Step 2: Create Your First Project

1. **New Configuration**: Click "New Config" to create a fresh project
2. **Project Settings**: The default settings are fine for getting started
3. **Save Location**: Choose "Save Config As..." to save your project

## Step 3: Add a Simple Job

1. **Add Job**: Click "Add Job" in the left panel
2. **Basic Settings Tab**:
   - **URL**: Enter `https://httpbin.org/` (a safe testing site)
   - **File Types**: Check "html" and "json"
   - **Description**: Enter "Test job for learning"

3. **Tasks Tab**:
   - Keep "Abduct" and "Visits" checked
   - Optionally check "Process" to extract text content

4. **Save**: Click "Save Job"

## Step 4: Run Your First Job

1. **Review**: Check that your job appears in the job list
2. **Execute**: Click "Run Jobs" 
3. **Monitor**: Watch the progress in the "Progress Monitor" tab
4. **Results**: View downloaded files in the "Files & Results" tab

## Step 5: Explore the Interface

### Left Panel - Configuration & Jobs
- **Configuration section**: Manage your project settings
- **Jobs section**: Add, edit, and remove scraping jobs

### Right Panel - Monitoring & Results
- **Progress Monitor**: Real-time logging and progress tracking
- **Files & Results**: Browse downloaded files and view results
- **Tutorial**: Built-in help and documentation

## Step 6: Try Advanced Features

1. **Load Examples**: Use "Tools -> Load Examples" to explore pre-built configurations
2. **Edit Configuration**: Click "Edit Config" for advanced JSON editing  
3. **Add Complex Jobs**: Try jobs with delays, recursion, or custom processing

## Common Tasks

### Loading Example Configurations
- Menu: Tools -> Load Examples
- Navigate to the examples/configs folder
- Try: example.json, example.youtube.json, example.edgar.json

### Saving Your Work
- Use "Save Config" to save current project
- Use "Save Config As..." to create a new file
- Configurations are saved as JSON files

### Monitoring Progress
- The Progress Monitor shows real-time logs
- Progress bar indicates current operation status
- Logs can be saved to files for later review

### Viewing Results
- Files & Results tab shows downloaded content
- Text content can be previewed and saved
- Results summary shows job statistics

## Tips for Success

1. **Start Small**: Begin with simple single-page scraping jobs
2. **Test URLs**: Use the built-in validation to check your configurations
3. **Monitor Resources**: Watch system performance during large jobs
4. **Save Often**: Save your configurations frequently
5. **Read Logs**: The progress monitor provides valuable debugging information

## Next Steps

Once you're comfortable with the basics:

1. Read the complete tutorial: `examples/tutorial/complete_tutorial.md`
2. Explore advanced job settings (recursion, delays, custom processing)
3. Try different beacons for specialized data sources
4. Experiment with parallel processing for multiple jobs

## Getting Help

- **Built-in Tutorial**: Available in the GUI's Tutorial tab
- **Examples**: Pre-built configurations for common scenarios  
- **Validation**: Use "Tools -> Validate Config" to check your settings
- **Logs**: Monitor the Progress tab for detailed operation information

Happy scraping!