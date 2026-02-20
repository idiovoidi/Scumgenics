# Scumgenics - Mewgenics Save Manager

Python (PyQt6) 

Backup, and restore your game save files through a simple graphical interface.


## Installation

### Option 1: Standalone Executable (Recommended for Users)

1. **Download** `Scumgenics.exe` from the releases page
2. **Place it** in a permanent location (e.g., `C:\Games\Scumgenics\`)
3. **Run it** - no Python installation required!

The exe will create `logs/` and `backups/` folders in the same directory.

### Option 2: Run from Source (For Developers)

1. **Download or clone this repository** to your local machine

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - PyQt6 (GUI framework)
   - pytest, pytest-qt, pytest-mock (testing frameworks)
   - hypothesis (property-based testing)
   - coverage (code coverage)

