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

DISCORD_TOKEN = "your bot token"
VOICESNAPSHOT_GUILD_ID = 123456789012345678  # your Discord guild ID
```
3. In your root urls.py:
```
from django.urls import include, path

urlpatterns += [
    path("voicesnapshot/", include("aa_discord_voicesnapshot.urls")),
]
```
4. Run migrations:
```
python manage.py makemigrations aa_discord_voicesnapshot
python manage.py migrate
```
5. Assign permissions to groups via Alliance Auth admin:
_ `aa_discord_voicesnapshot.take_snapshot`
_ `aa_discord_voicesnapshot.view_snapshot_history`
_ `aa_discord_voicesnapshot.edit_snapshot`
_ `aa_discord_voicesnapshot.delete_snapshot`
