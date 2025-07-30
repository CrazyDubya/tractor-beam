# Tractor Beam Complete Tutorial

This comprehensive tutorial will guide you through all aspects of using tractor-beam, from basic configuration to advanced features and the new graphical interface.

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Basic Concepts](#basic-concepts)
4. [Configuration](#configuration)
5. [Using the GUI](#using-the-gui)
6. [Command Line Usage](#command-line-usage)
7. [Job Types and Examples](#job-types-and-examples)
8. [Advanced Features](#advanced-features)
9. [Troubleshooting](#troubleshooting)
10. [Real-World Examples](#real-world-examples)

## Introduction

Tractor Beam is a high-efficiency text & file scraper with smart tracking, designed for building language model datasets quickly and efficiently. It provides both programmatic and graphical interfaces for configuring and running data collection jobs.

### Key Features

- **Parallel Processing**: Leverage multiple CPU cores for efficient scraping
- **Modular Design**: Extensible beacon system for different data sources
- **Smart Tracking**: Avoid duplicate downloads and track progress
- **Multiple Formats**: Support for various file types (PDF, HTML, XML, etc.)
- **Monitoring**: Real-time progress tracking and logging
- **GUI Interface**: User-friendly graphical interface for all operations

## Installation

### From PyPI
```bash
pip install llm-tractor-beam
```

### From Source
```bash
git clone https://github.com/CrazyDubya/tractor-beam.git
cd tractor-beam
pip install -e .
```

## Basic Concepts

### Core Components

1. **Beam**: The main orchestrator that manages all operations
2. **Config**: Handles configuration loading and validation
3. **Jobs**: Individual scraping tasks with specific parameters
4. **Beacons**: Specialized modules for different data sources
5. **Abduct**: Downloads files from URLs
6. **Visit**: Creates CSV records of operations
7. **Focus**: Processes and extracts text content

### Workflow

1. **Configuration**: Define project settings and jobs
2. **Execution**: Run the beam to execute all jobs
3. **Processing**: Extract and process downloaded content
4. **Recording**: Track results in CSV format
5. **Monitoring**: View progress and results

## Configuration

### Basic Configuration Structure

A tractor-beam configuration is a JSON file with the following structure:

```json
{
    "role": "server",
    "settings": {
        "name": "my_project",
        "proj_dir": "./my_project",
        "jobs": [
            {
                "url": "https://example.com",
                "types": ["pdf", "html"],
                "beacon": null,
                "delay": null,
                "tasks": ["abduct", "visits"],
                "custom": []
            }
        ]
    }
}
```

### Configuration Fields

- **role**: Operation mode (`server`, `client`, `watcher`)
- **name**: Project name
- **proj_dir**: Directory for storing project files
- **jobs**: Array of scraping jobs

### Job Fields

- **url**: Target URL to scrape
- **types**: File types to download (empty array = all types)
- **beacon**: Specialized processing module
- **delay**: Delay between operations (for watching mode)
- **tasks**: Tasks to perform (`abduct`, `visits`, `process`)
- **custom**: Custom processing options

## Using the GUI

### Starting the GUI

```bash
# From the examples directory
python gui_demo.py

# Or import in your code
from tractor_beam.gui import TractorBeamGUI
app = TractorBeamGUI()
app.run()
```

### GUI Components

#### 1. Configuration Management

- **New Config**: Create a fresh configuration
- **Load Config**: Open existing configuration files
- **Save Config**: Save current configuration
- **Edit Config**: Advanced configuration editing

#### 2. Job Management

- **Add Job**: Create new scraping jobs
- **Edit Job**: Modify existing jobs
- **Remove Job**: Delete jobs from configuration
- **Job List**: View all configured jobs

#### 3. Progress Monitoring

- **Progress Bar**: Visual progress indication
- **Log Window**: Real-time operation logging
- **Status Updates**: Current operation status

#### 4. File Viewer

- **File Browser**: Navigate downloaded files
- **Content Viewer**: Preview file contents
- **Results Summary**: Overview of job results

### Step-by-Step GUI Tutorial

#### Step 1: Create a New Project

1. Click "New Config" to create a fresh configuration
2. The configuration will be initialized with default settings
3. You can immediately start adding jobs or modify settings

#### Step 2: Add Your First Job

1. Click "Add Job" in the job management section
2. Fill in the basic settings:
   - **URL**: Enter the website you want to scrape
   - **File Types**: Select the types of files to download
   - **Tasks**: Choose what operations to perform

3. Optionally configure advanced settings:
   - **Delay**: For periodic scraping
   - **Recursion**: For following links
   - **Custom Processing**: For specialized handling

4. Click "Save Job" to add it to your configuration

#### Step 3: Run Your Jobs

1. Review your jobs in the job list
2. Click "Run Jobs" to start execution
3. Monitor progress in the Progress Monitor tab
4. View results in the Files & Results tab

## Command Line Usage

### Basic Usage

```python
from tractor_beam import tractor

# Load configuration and run
beam = tractor.Beam('config.json')
results = await beam.go()
```

### With Callback

```python
async def progress_callback(runs):
    print(f"Completed {len(runs)} job runs")

beam = tractor.Beam('config.json')
await beam.go(cb=progress_callback)
```

### Configuration in Code

```python
config = {
    "role": "server",
    "settings": {
        "name": "my_project",
        "proj_dir": "./output",
        "jobs": [
            {
                "url": "https://example.com",
                "types": ["pdf"],
                "beacon": None,
                "delay": None,
                "tasks": ["abduct", "visits"]
            }
        ]
    }
}

beam = tractor.Beam(config)
await beam.go()
```

## Job Types and Examples

### 1. Simple File Download

Download all PDF files from a website:

```json
{
    "url": "https://example.com/documents",
    "types": ["pdf"],
    "beacon": null,
    "delay": null,
    "tasks": ["abduct", "visits"]
}
```

### 2. Recursive Web Scraping

Scrape multiple pages following links:

```json
{
    "url": "https://example.com",
    "types": ["html", "pdf"],
    "beacon": null,
    "delay": null,
    "tasks": ["abduct", "visits", "process"],
    "recursive": true,
    "max_depth": 2
}
```

### 3. Periodic Monitoring

Watch for new content periodically:

```json
{
    "url": "https://news.example.com",
    "types": ["html"],
    "beacon": null,
    "delay": 3600,
    "tasks": ["abduct", "visits", "process"]
}
```

### 4. Specialized Sources

Use beacons for specific data sources:

```json
{
    "url": "https://www.sec.gov/edgar/search/",
    "types": ["html", "xml"],
    "beacon": "edgar",
    "delay": null,
    "tasks": ["abduct", "visits", "process"]
}
```

## Advanced Features

### Custom Beacons

Create specialized processing modules for specific data sources:

```python
# In tractor_beam/abducts/beacons/my_beacon/
class Stream:
    def __init__(self, conf, job):
        self.conf = conf
        self.job = job
    
    def fetch(self):
        # Custom fetching logic
        pass

class Helpers:
    def process_data(self, data):
        # Custom data processing
        pass
```

### Custom Processing

Add custom headers and processing functions:

```json
{
    "url": "https://api.example.com/data",
    "types": ["json"],
    "beacon": null,
    "delay": null,
    "tasks": ["abduct", "visits"],
    "custom": [
        {
            "func": "custom_json_processor",
            "headers": {
                "Authorization": "Bearer TOKEN",
                "User-Agent": "TractorBeam/1.0"
            }
        }
    ]
}
```

### Parallel Processing

Configure parallel execution:

```python
# Automatically uses optimal number of CPU cores
beam = tractor.Beam(config)
await beam.go()  # Will use multiprocessing for parallel jobs
```

## Troubleshooting

### Common Issues

#### 1. Configuration Validation Errors

**Problem**: "Configuration is invalid" error
**Solution**: 
- Use the GUI's "Tools -> Validate Config" feature
- Check JSON syntax in the configuration editor
- Ensure all required fields are present

#### 2. Permission Errors

**Problem**: Can't write to project directory
**Solution**:
- Check directory permissions
- Use a different project directory
- Run with appropriate privileges

#### 3. Network Issues

**Problem**: Downloads fail or timeout
**Solution**:
- Check internet connection
- Verify URL accessibility
- Add appropriate headers for authentication
- Increase timeout values

#### 4. Memory Issues

**Problem**: Out of memory during large downloads
**Solution**:
- Process files in smaller batches
- Increase system memory
- Use streaming processing for large files

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

beam = tractor.Beam(config)
await beam.go()
```

## Real-World Examples

### Example 1: Research Paper Collection

Collect academic papers from a research website:

```json
{
    "role": "server",
    "settings": {
        "name": "research_papers",
        "proj_dir": "./research_data",
        "jobs": [
            {
                "url": "https://arxiv.org/list/cs.AI/recent",
                "types": ["pdf"],
                "beacon": null,
                "delay": null,
                "tasks": ["abduct", "visits", "process"],
                "description": "Collect recent AI papers from arXiv"
            }
        ]
    }
}
```

### Example 2: News Monitoring

Monitor news websites for new articles:

```json
{
    "role": "watcher",
    "settings": {
        "name": "news_monitor",
        "proj_dir": "./news_data",
        "jobs": [
            {
                "url": "https://news.example.com/tech",
                "types": ["html"],
                "beacon": null,
                "delay": 1800,
                "tasks": ["abduct", "visits", "process"],
                "description": "Monitor tech news every 30 minutes"
            }
        ]
    }
}
```

### Example 3: Financial Data Collection

Collect financial filings using the EDGAR beacon:

```json
{
    "role": "server",
    "settings": {
        "name": "financial_filings",
        "proj_dir": "./financial_data",
        "jobs": [
            {
                "url": "https://www.sec.gov/edgar/search/",
                "types": ["html", "xml", "txt"],
                "beacon": "edgar",
                "delay": null,
                "tasks": ["abduct", "visits", "process"],
                "custom": [
                    {
                        "func": "edgar_processor",
                        "headers": {
                            "User-Agent": "Your Company Name your@email.com"
                        }
                    }
                ]
            }
        ]
    }
}
```

### Example 4: Documentation Scraping

Scrape technical documentation:

```json
{
    "role": "server",
    "settings": {
        "name": "tech_docs",
        "proj_dir": "./documentation",
        "jobs": [
            {
                "url": "https://docs.example.com",
                "types": ["html", "pdf"],
                "beacon": null,
                "delay": null,
                "tasks": ["abduct", "visits", "process"],
                "recursive": true,
                "max_depth": 3,
                "description": "Scrape complete documentation site"
            }
        ]
    }
}
```

## Best Practices

### 1. Configuration Management

- Use descriptive project names
- Organize configurations by purpose
- Version control your configurations
- Test configurations with small datasets first

### 2. Respectful Scraping

- Always check robots.txt
- Use appropriate delays between requests
- Include proper User-Agent headers
- Respect rate limits and terms of service

### 3. Data Organization

- Use meaningful project directories
- Regularly clean up temporary files
- Archive completed projects
- Document your data collection process

### 4. Performance Optimization

- Start with single jobs, then parallelize
- Monitor system resources during execution
- Use appropriate file type filters
- Consider storage space requirements

## Conclusion

Tractor Beam provides a powerful and flexible platform for data collection and scraping operations. Whether you prefer the graphical interface for interactive work or the programmatic interface for automation, tractor-beam can adapt to your workflow.

The combination of modular design, parallel processing, and specialized beacons makes it suitable for a wide range of data collection tasks, from academic research to business intelligence.

For additional help and examples, explore the example configurations included with the project and don't hesitate to experiment with different settings to find what works best for your specific use case.

Happy scraping!