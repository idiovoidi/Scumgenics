I am making a Python based PyQT6 app that I plan to deploy as a save loader for the game Mewgenics, the app title is a parody of the name with Scumgenics to reflect the save scum nature.

The save for my game resides here
"C:\Users\Mitchell\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves\steamcampaign01.sav"

There are additional backup saves here
"C:\Users\Mitchell\AppData\Roaming\Glaiel Games\Mewgenics\76561197960287930\saves\backups"

I want this app to be able to select the backup saves and replace them with the main game saves "steamcampaign01_2026-02-20_02-07.savbackup" needs to be converted into "steamcampaign01.sav" and placed into the save folder.

The code should account for additional users so I can distribute it to the community on Reddit So [USERNAME] instead of "Mitchell" 

The app should have the additional option to double backup saves in a sub-folder within the codebase.