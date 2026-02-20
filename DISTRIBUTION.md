# Distribution Guide for Scumgenics

## Building the Executable

### Quick Build
Simply run:
```bash
build_exe.bat
```

This will:
1. Install PyInstaller if needed
2. Clean previous builds
3. Create `dist/Scumgenics.exe`

### Manual Build
If you prefer to build manually:
```bash
pip install pyinstaller
pyinstaller Scumgenics.spec
```

## What Gets Created

After building, you'll find:
- `dist/Scumgenics.exe` - The standalone executable (~50-150MB)
- `build/` - Temporary build files (can be deleted)

## Distributing to Users

### What to Share
Upload `Scumgenics.exe` from the `dist/` folder to:
- GitHub Releases
- Itch.io
- Google Drive / Dropbox
- Your preferred file sharing platform

### User Instructions
Users should:
1. Download `Scumgenics.exe`
2. Place it in a permanent location (e.g., `C:\Games\Scumgenics\`)
3. Run it - no Python installation required!

### Important Notes for Users
- The exe creates `logs/` and `backups/` folders in the same directory
- Don't run from Downloads or Temp folders (files may be lost)
- Mewgenics must be installed and run at least once
- Windows may show a SmartScreen warning (click "More info" → "Run anyway")

## File Size
The exe will be 50-150MB because it includes:
- Python runtime
- PyQt6 GUI framework
- All application code

This is normal for Python GUI applications.

## Troubleshooting Build Issues

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "Module not found" errors
The spec file includes all necessary modules. If you added new dependencies:
1. Update `requirements.txt`
2. Add to `hiddenimports` in `Scumgenics.spec`

### Exe crashes on startup
1. Build with console enabled to see errors:
   - In `Scumgenics.spec`, change `console=False` to `console=True`
   - Rebuild and check console output
2. Check if all data files are included in the `datas` section

### Large file size
To reduce size:
- Remove unused dependencies from `requirements.txt`
- Add more modules to `excludes` in the spec file
- Use UPX compression (already enabled)

## Testing the Exe

Before distributing:
1. Test on a clean Windows machine without Python
2. Verify all features work (backup, restore, launch game)
3. Check that logs and backups are created properly
4. Test with and without Mewgenics installed

## Version Updates

When releasing a new version:
1. Update version number in your code
2. Rebuild the exe: `build_exe.bat`
3. Test thoroughly
4. Upload to distribution platform
5. Update release notes

## Optional: Add an Icon

To add a custom icon:
1. Create or download an `.ico` file
2. Save it as `icon.ico` in the project root
3. In `Scumgenics.spec`, change:
   ```python
   icon=None,  # Change to:
   icon='icon.ico',
   ```
4. Rebuild

## Optional: Code Signing

For professional distribution (removes SmartScreen warnings):
1. Purchase a code signing certificate
2. Use `signtool.exe` to sign the exe
3. This costs money but improves user trust

## Support

If users report issues:
1. Ask them to check the `logs/` folder
2. Request the log file for debugging
3. Verify they're using the latest version
