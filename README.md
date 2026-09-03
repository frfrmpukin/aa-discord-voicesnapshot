# aa-discord-voicesnapshot

Alliance Auth plugin that lets authorized users take on-demand snapshots of who is in a selected Discord voice channel, and keeps a full history.

## Features

- Select any Discord voice channel and take a snapshot
- Log snapshots to the database (timestamp, channel, occupants, taker)
- View snapshot history with pagination and filtering
- View snapshot details (occupants)
- Edit snapshot occupants (add/remove)
- Delete snapshots (with separate permission)
- Export snapshot history to CSV
- Alliance Auth navigation menu entry
- Full permission separation:
  - `take_snapshot`
  - `view_snapshot_history`
  - `edit_snapshot`
  - `delete_snapshot`

## Requirements

- allianceauth.services.modules.discord
- aadiscordbot

## Installation

1. Install the plugin:

```bash
pip install git+https://github.com/frfrmpukin/aa-discord-voicesnapshot.git
```

2. In local.py:
```
INSTALLED_APPS += [
    "aa_discord_voicesnapshot",
]
```

3. Run migrations:
```
python manage.py makemigrations aa_discord_voicesnapshot
python manage.py migrate
```
4. Assign permissions to groups via Alliance Auth admin:
   - `aa_discord_voicesnapshot.take_snapshot`
   - `aa_discord_voicesnapshot.view_snapshot_history`
   - `aa_discord_voicesnapshot.edit_snapshot`
   - `aa_discord_voicesnapshot.delete_snapshot`
5. Access the plugin at:
```
/voicesnapshot/
```
