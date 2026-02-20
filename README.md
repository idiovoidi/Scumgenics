# Scumgenics - Mewgenics Save Manager

A desktop save manager application for the game Mewgenics. Manage, backup, and restore your game save files through a simple graphical interface.

## Features

- **Automatic Save Detection**: Automatically finds your Mewgenics save files based on your Windows username
- **Backup Management**: View and restore timestamped backup saves
- **Local Backups**: Create additional backup copies within the application directory
- **Game Launcher**: Quick launch Mewgenics after swapping saves
- **Custom Save Paths**: Configure custom save folder locations
- **Cross-User Support**: Works on any Windows user account without configuration

## Requirements

- **Python**: Version 3.8 or higher
- **Operating System**: Windows 10 or Windows 11
- **Mewgenics**: Must be installed and run at least once to create initial save files

## Installation

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

## Usage

### Running the Application

To start Scumgenics, run:

```bash
python main.py
```

The application window will open showing your available backup saves.

### Managing Saves

1. **View Backups**: The main window displays all available backup saves sorted by date (newest first)

2. **Restore a Backup**:
   - Select a backup from the list
   - Click the "Restore" button
   - The selected backup will replace your current save file

3. **Create Local Backup**:
   - Click the "Create External Backup" button
   - A timestamped copy of your current save will be created in the `backups/` directory

4. **Launch Game**:
   - Click the "Launch Game" button to start Mewgenics
   - Note: You must configure the game executable path first (see Options below)

### Options

Access the Options tab to configure:

1. **Custom Save Folder**:
   - Click "Browse..." to select a custom save folder location
   - Useful if your saves are in a non-standard location
   - Leave empty to use automatic detection

2. **Game Executable Path**:
   - Click "Browse..." next to "Game Executable Path"
   - Select your Mewgenics.exe file
   - Once configured, you can use the "Launch Game" button on the Backups tab
   - The Launch Game button will be disabled until you set this path

3. **Open Backup Folder**:
   - Quickly open the local backup directory in Windows Explorer

### Backup Directory Locations

The application manages backups in two locations:

1. **Game Backup Directory** (created by Mewgenics):
   ```
   C:\Users\[YOUR_USERNAME]\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves\backups\
   ```
   - Contains backups created by the game
   - Format: `steamcampaign01_YYYY-MM-DD_HH-MM.savbackup`

2. **Local Backup Directory** (created by Scumgenics):
   ```
   [Application Directory]\backups\
   ```
   - Contains backups you create using the "Create Local Backup" button
   - Same filename format as game backups
   - Provides extra protection for your save files

### Main Save File Location

Your active save file is located at:
```
C:\Users\[YOUR_USERNAME]\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves\steamcampaign01.sav
```

## Troubleshooting

### "Main save file not found!"

**Problem**: The application cannot find your Mewgenics save file.

**Solutions**:
- Ensure Mewgenics has been run at least once to create a save file
- Verify the game is installed correctly
- Check that the save file exists at the expected location (see above)
- Make sure you're running the application on the same Windows user account where you play Mewgenics

### "Failed to detect Windows username!"

**Problem**: The application cannot determine your Windows username.

**Solutions**:
- Ensure you're running on a Windows operating system
- Check that your user account is properly configured
- Try running the application as administrator

### "Access denied" or "Permission error"

**Problem**: The application doesn't have permission to read or write files.

**Solutions**:
- Run the application as administrator
- Check that the Mewgenics save directory is not read-only
- Ensure no other application (including Mewgenics) has the save file open
- Verify you have write permissions in the application directory

### "I/O error" during restore operation

**Problem**: File operations failed during backup restoration.

**Solutions**:
- Close Mewgenics if it's running
- Check available disk space
- Verify the backup file is not corrupted
- Try creating a new local backup before attempting restore

### Restore failed after deleting main save

**Problem**: The restore operation deleted your main save but failed to copy the backup.

**Solutions**:
- Don't panic! Your backup file is still intact
- Manually copy the backup file from the backup directory to the saves directory
- Rename the copied file to `steamcampaign01.sav`
- Check the log file (`logs/scumgenics_YYYYMMDD.log`) for detailed error information

### Application crashes on startup

**Problem**: The application closes immediately or shows an error.

**Solutions**:
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (must be 3.8 or higher)
- Review the log file in the `logs/` directory for error details
- Ensure PyQt6 is properly installed

## Logs

The application creates detailed log files in the `logs/` directory:
- Filename format: `scumgenics_YYYYMMDD.log`
- Contains timestamps, operations, file paths, and error details
- Useful for troubleshooting issues

## Safety Notes

- **Always close Mewgenics before using this application** to avoid file conflicts
- The restore operation is destructive - it deletes your current save before restoring
- Create local backups regularly for extra protection
- Keep multiple backup copies before experimenting with save restoration

## Development

### Running Tests

To run the test suite:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=src --cov-report=html
```

View the coverage report by opening `htmlcov/index.html` in a browser.

## License

This is a community tool for Mewgenics players. Use at your own risk.

## Support

If you encounter issues not covered in the troubleshooting section:
1. Check the log files in the `logs/` directory
2. Verify your Python and dependency versions
3. Ensure Mewgenics is properly installed and has created save files

## Credits

Created for the Mewgenics community.
