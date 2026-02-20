# Requirements Document

## Introduction

Scumgenics is a desktop save manager application for the game Mewgenics. The application enables players to manage, backup, and restore game save files through a PyQt6-based graphical interface. The system supports multiple Windows user accounts and provides backup management capabilities for the Mewgenics save file system.

## Glossary

- **Save_Manager**: The Scumgenics desktop application
- **Main_Save**: The active game save file (steamcampaign01.sav)
- **Backup_Save**: A timestamped backup copy of the main save (steamcampaign01_YYYY-MM-DD_HH-MM.savbackup)
- **Game_Directory**: The Mewgenics save directory at C:\Users\[USERNAME]\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves
- **Backup_Directory**: The backups subdirectory within the Game_Directory
- **Local_Backup_Directory**: A backup storage directory within the application codebase
- **User_Profile**: The Windows username of the current system user

## Requirements

### Requirement 1: Display Application Window

**User Story:** As a player, I want to see a desktop application window titled "Scumgenics", so that I can access save management features.

#### Acceptance Criteria

1. THE Save_Manager SHALL display a window with the title "Scumgenics"
2. THE Save_Manager SHALL use PyQt6 as the GUI framework
3. THE Save_Manager SHALL render the window on Windows operating systems

### Requirement 2: Detect User Profile

**User Story:** As a player on a shared computer, I want the application to automatically detect my Windows username, so that it accesses my save files correctly.

#### Acceptance Criteria

1. WHEN the Save_Manager starts, THE Save_Manager SHALL detect the current User_Profile
2. THE Save_Manager SHALL construct file paths using the detected User_Profile
3. THE Save_Manager SHALL NOT use hardcoded usernames in file paths

### Requirement 3: Locate Main Save File

**User Story:** As a player, I want the application to find my main save file, so that I can manage it.

#### Acceptance Criteria

1. THE Save_Manager SHALL locate the Main_Save at C:\Users\[USERNAME]\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves\steamcampaign01.sav
2. WHEN the Main_Save does not exist, THE Save_Manager SHALL display an error message indicating the file was not found
3. THE Save_Manager SHALL verify the Main_Save file exists before performing operations on it

### Requirement 4: List Available Backup Saves

**User Story:** As a player, I want to see all available backup saves, so that I can choose which one to restore.

#### Acceptance Criteria

1. THE Save_Manager SHALL scan the Backup_Directory for files matching the pattern steamcampaign01_YYYY-MM-DD_HH-MM.savbackup
2. THE Save_Manager SHALL display the list of Backup_Save files in the user interface
3. THE Save_Manager SHALL sort Backup_Save files by timestamp in descending order
4. WHEN the Backup_Directory contains no Backup_Save files, THE Save_Manager SHALL display a message indicating no backups are available

### Requirement 5: Select Backup Save for Restoration

**User Story:** As a player, I want to select a backup save from the list, so that I can restore it as my main save.

#### Acceptance Criteria

1. THE Save_Manager SHALL allow the user to select one Backup_Save from the displayed list
2. WHEN a Backup_Save is selected, THE Save_Manager SHALL enable the restore action
3. WHEN no Backup_Save is selected, THE Save_Manager SHALL disable the restore action

### Requirement 6: Restore Backup Save as Main Save

**User Story:** As a player, I want to restore a selected backup save as my main save, so that I can return to a previous game state.

#### Acceptance Criteria

1. WHEN the user initiates a restore operation, THE Save_Manager SHALL delete the existing Main_Save file
2. WHEN the Main_Save is deleted, THE Save_Manager SHALL copy the selected Backup_Save to the Game_Directory
3. WHEN the Backup_Save is copied, THE Save_Manager SHALL rename it to steamcampaign01.sav
4. WHEN the restore operation succeeds, THE Save_Manager SHALL display a success message
5. IF the restore operation fails at any step, THEN THE Save_Manager SHALL display an error message with the failure reason
6. THE Save_Manager SHALL perform the delete and copy operations as a two-step process to ensure the game reads the restored save correctly

### Requirement 7: Create Local Backup Copy

**User Story:** As a player, I want to create additional backup copies within the application directory, so that I have extra protection for my save files.

#### Acceptance Criteria

1. THE Save_Manager SHALL provide an option to create a backup copy in the Local_Backup_Directory
2. WHEN the user creates a local backup, THE Save_Manager SHALL copy the Main_Save to the Local_Backup_Directory with a timestamp
3. THE Save_Manager SHALL create the Local_Backup_Directory if it does not exist
4. THE Save_Manager SHALL use the format steamcampaign01_YYYY-MM-DD_HH-MM.savbackup for local backup filenames
5. WHEN the local backup operation succeeds, THE Save_Manager SHALL display a success message
6. IF the local backup operation fails, THEN THE Save_Manager SHALL display an error message with the failure reason

### Requirement 8: Handle File System Errors

**User Story:** As a player, I want to be notified when file operations fail, so that I understand what went wrong.

#### Acceptance Criteria

1. IF a file read operation fails, THEN THE Save_Manager SHALL display an error message indicating the file could not be read
2. IF a file write operation fails, THEN THE Save_Manager SHALL display an error message indicating the file could not be written
3. IF a directory access operation fails, THEN THE Save_Manager SHALL display an error message indicating the directory could not be accessed
4. THE Save_Manager SHALL include the specific file path in error messages

### Requirement 9: Support Distribution to Community

**User Story:** As a developer, I want the application to be distributable to the Reddit community, so that other players can use it.

#### Acceptance Criteria

1. THE Save_Manager SHALL run as a standalone Python application
2. THE Save_Manager SHALL NOT require hardcoded configuration specific to a single user
3. THE Save_Manager SHALL include all necessary dependencies in the distribution package
4. THE Save_Manager SHALL function correctly on different Windows user accounts without modification
