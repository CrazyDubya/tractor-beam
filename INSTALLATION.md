# Tractor Beam Installation & Setup Guide

This guide covers installation and setup for all components of tractor-beam, including the new GUI interface.

## Basic Installation

### From PyPI (Recommended)
```bash
pip install llm-tractor-beam
```

### From Source
```bash
git clone https://github.com/CrazyDubya/tractor-beam.git
cd tractor-beam
pip install -e .
```

## GUI Requirements

The GUI interface requires `tkinter`, which is included with most Python installations but may need to be installed separately on some systems.

### Linux (Ubuntu/Debian)
```bash
sudo apt-get install python3-tkinter
```

### Linux (CentOS/RHEL/Fedora)
```bash
# CentOS/RHEL
sudo yum install tkinter
# or Fedora
sudo dnf install python3-tkinter
```

### macOS
Tkinter is included with Python from python.org. If using Homebrew:
```bash
brew install python-tk
```

### Windows
Tkinter is included with Python from python.org and Microsoft Store versions.

## Verification

Test your installation:

```bash
# Test basic functionality
python -c "import tractor_beam; print('✅ Tractor Beam installed')"

# Test GUI availability
python -c "from tractor_beam.gui import TractorBeamGUI; print('✅ GUI available')"

# Test CLI
python -m tractor_beam.cli version
```

## Quick Start

### Launch GUI
```bash
# Direct launch
python examples/gui_demo.py

# Via CLI
python -m tractor_beam.cli gui
```

### Command Line Usage
```bash
# Validate a configuration
python -m tractor_beam.cli validate config.json

# Run a configuration
python -m tractor_beam.cli run config.json

# List examples
python -m tractor_beam.cli examples
```

### Programmatic Usage
```python
from tractor_beam import Beam
import asyncio

async def main():
    beam = Beam('config.json')
    await beam.go()

asyncio.run(main())
```

## Optional Dependencies

Some features require additional packages:

### PDF Processing (Advanced)
```bash
pip install marker-pdf
```

### Additional File Types
Most file types are supported out of the box, but some specialized formats may require additional packages.

## Troubleshooting

### GUI Won't Start
- **Issue**: `No module named 'tkinter'`
- **Solution**: Install tkinter for your system (see GUI Requirements above)

### Import Errors
- **Issue**: Missing dependencies
- **Solution**: Install requirements: `pip install -r requirements.txt`

### Permission Errors
- **Issue**: Can't write to project directories
- **Solution**: Check permissions or use a different project directory

### Network Issues
- **Issue**: Downloads fail
- **Solution**: Check internet connection and firewall settings

## Development Setup

For development work:

```bash
git clone https://github.com/CrazyDubya/tractor-beam.git
cd tractor-beam
pip install -e .
pip install -r requirements.txt

# Run tests
python tests/test_Config.py

# Install development tools (optional)
pip install pytest black flake8
```

## Environment Variables

Tractor Beam respects these environment variables:

- `TRACTOR_BEAM_CONFIG_DIR`: Default directory for configurations
- `TRACTOR_BEAM_DATA_DIR`: Default directory for data output

## Support

- **Documentation**: See `examples/tutorial/` for comprehensive guides
- **Examples**: Check `examples/configs/` for sample configurations
- **Issues**: Report bugs and request features on GitHub

Happy scraping! 🛸