#!/usr/bin/env python3
"""
Tractor Beam Command Line Interface

This script provides command-line access to tractor-beam functionality,
including launching the GUI and running configurations.
"""

import sys
import argparse
import asyncio
from pathlib import Path


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(
        description="Tractor Beam - High-efficiency text & file scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s gui                          # Launch the GUI interface
  %(prog)s run config.json              # Run a configuration file
  %(prog)s validate config.json         # Validate a configuration file
  %(prog)s examples                     # List available example configurations
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # GUI command
    gui_parser = subparsers.add_parser('gui', help='Launch the graphical user interface')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run a configuration file')
    run_parser.add_argument('config', help='Path to configuration file')
    run_parser.add_argument('--no-parallel', action='store_true', 
                           help='Disable parallel processing')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate a configuration file')
    validate_parser.add_argument('config', help='Path to configuration file')
    
    # Examples command
    examples_parser = subparsers.add_parser('examples', help='List example configurations')
    examples_parser.add_argument('--copy', help='Copy an example to a new file')
    
    # Version command
    version_parser = subparsers.add_parser('version', help='Show version information')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
        
    return handle_command(args)


def handle_command(args):
    """Handle the parsed command"""
    try:
        if args.command == 'gui':
            return launch_gui()
        elif args.command == 'run':
            return run_config(args.config, parallel=not args.no_parallel)
        elif args.command == 'validate':
            return validate_config(args.config)
        elif args.command == 'examples':
            return handle_examples(args.copy)
        elif args.command == 'version':
            return show_version()
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


def launch_gui():
    """Launch the GUI interface"""
    try:
        from tractor_beam.gui import TractorBeamGUI
        print("Launching Tractor Beam GUI...")
        app = TractorBeamGUI()
        app.run()
        return 0
    except ImportError as e:
        if "tkinter" in str(e).lower():
            print("Error: GUI requires tkinter but it's not available.")
            print("Please install tkinter or use the command-line interface instead.")
        else:
            print(f"Error importing GUI: {e}")
        return 1


def run_config(config_path, parallel=True):
    """Run a configuration file"""
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1
        
    try:
        from tractor_beam import Beam
        
        print(f"Loading configuration from {config_path}...")
        beam = Beam(str(config_file))
        
        print("Starting tractor beam execution...")
        if parallel:
            print("Parallel processing enabled")
        else:
            print("Parallel processing disabled")
            
        async def run_async():
            async def progress_callback(runs):
                print(f"Progress: {len(runs)} job runs completed")
                
            await beam.go(cb=progress_callback)
            
        asyncio.run(run_async())
        print("Execution completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error running configuration: {e}")
        return 1


def validate_config(config_path):
    """Validate a configuration file"""
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Error: Configuration file not found: {config_path}")
        return 1
        
    try:
        from tractor_beam.utils.config import Config
        
        print(f"Validating configuration: {config_path}")
        config = Config(str(config_file))
        
        print("✅ Configuration is valid!")
        print(f"   Project: {config.conf.settings.name}")
        print(f"   Role: {config.conf.role}")
        print(f"   Jobs: {len(config.conf.settings.jobs)}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Configuration is invalid: {e}")
        return 1


def handle_examples(copy_to=None):
    """Handle examples command"""
    try:
        # Find examples directory
        from tractor_beam import __file__ as tb_file
        examples_dir = Path(tb_file).parent.parent / "examples" / "configs"
        
        if not examples_dir.exists():
            print("Examples directory not found")
            return 1
            
        # List examples
        examples = list(examples_dir.glob("*.json"))
        if not examples:
            print("No example configurations found")
            return 1
            
        print("Available example configurations:")
        for i, example in enumerate(examples, 1):
            print(f"  {i}. {example.name}")
            
        # Copy example if requested
        if copy_to:
            if copy_to.isdigit():
                # Copy by number
                index = int(copy_to) - 1
                if 0 <= index < len(examples):
                    source = examples[index]
                    dest = Path(source.name)
                    dest.write_text(source.read_text())
                    print(f"Copied {source.name} to {dest}")
                else:
                    print(f"Invalid example number: {copy_to}")
                    return 1
            else:
                # Copy by name
                source_name = copy_to if copy_to.endswith('.json') else f"{copy_to}.json"
                source = examples_dir / source_name
                if source.exists():
                    dest = Path(source.name)
                    dest.write_text(source.read_text())
                    print(f"Copied {source.name} to {dest}")
                else:
                    print(f"Example not found: {source_name}")
                    return 1
                    
        return 0
        
    except Exception as e:
        print(f"Error handling examples: {e}")
        return 1


def show_version():
    """Show version information"""
    try:
        from tractor_beam import __version__
        print(f"Tractor Beam version {__version__}")
        
        # Show optional features
        try:
            from tractor_beam.gui import TractorBeamGUI
            print("GUI support: Available")
        except ImportError:
            print("GUI support: Not available (tkinter required)")
            
        return 0
    except Exception as e:
        print(f"Error getting version: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())