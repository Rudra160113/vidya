# File location: vidya/ci/pre_commit_hooks.py

import sys
import os
import subprocess
import logging

# This is a simple placeholder to demonstrate the concept.
# In a real project, this would be integrated with a tool like `pre-commit`.

def check_for_print_statements(files):
    """Checks if any 'print(' statements are left in the code."""
    logging.info("Running pre-commit hook: Checking for print statements...")
    
    for filename in files:
        with open(filename, 'r') as f:
            for line_number, line in enumerate(f, 1):
                if 'print(' in line:
                    logging.error(f"Error: Found 'print(' statement in {filename} on line {line_number}.")
                    return False
    return True

def run_formatter(files):
    """Runs a code formatter (like Black) on the staged files."""
    logging.info("Running pre-commit hook: Formatting code with Black...")
    
    try:
        # A real implementation would use the `black` library
        # subprocess.run(["black", *files], check=True, capture_output=True)
        logging.warning("Skipping actual formatting (placeholder).")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Code formatting failed: {e.stderr}")
        return False

if __name__ == "__main__":
    staged_files = sys.argv[1:]
    
    if not staged_files:
        logging.info("No files staged. Skipping pre-commit hooks.")
        sys.exit(0)
        
    if not check_for_print_statements(staged_files):
        sys.exit(1) # Fail the commit

    if not run_formatter(staged_files):
        sys.exit(1) # Fail the commit
        
    logging.info("Pre-commit hooks passed. Ready to commit.")
    sys.exit(0)
