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
- websocket-client

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

AND
# Create or Add to
PLUGINS += [
    "aa_discord_voicesnapshot",
]

```

3. Run migrations:
```
python manage.py migrate
```
4. Create the runner file in your AA project directory:

This file is NOT installed automatically by pip. You must either:
- create it manually, or
- download voicesnapshot_runner.py from this GitHub repo.
- place it here:
```
    /home/allianceserver/myauth/voicesnapshot_runner.py
```
- file contents for voicesnapshot_runner.py
```
from aa_discord_voicesnapshot.gateway import VoiceGatewayClient

if __name__ == "__main__":
    client = VoiceGatewayClient()
    client.start()
    client.join()
```
  
5. Edit myauth.conf or supervisor.conf
  - `You will add this block at the bottom, BEFORE the [group:myauth] line:`
```
[program:voicesnapshot]
command=/home/allianceserver/venv/auth/bin/python /home/allianceserver/myauth/voicesnapshot_runner.py
directory=/home/allianceserver/myauth
user=allianceserver
autostart=true
autorestart=true
stdout_logfile=/home/allianceserver/myauth/log/voicesnapshot.out.log
stderr_logfile=/home/allianceserver/myauth/log/voicesnapshot.err.log
priority=998
```
  - `Then update the group:`
```
[group:myauth]
programs=beat,worker,worker_services,gunicorn,voicesnapshot
priority=999
```
- `Update supervisor and restart myauth`
```
supervisorctl reread
supervisorctl update
```
```
# Restart only the voicesnapshot program
supervisorctl restart voicesnapshot
```
```
# Or restart the entire myauth group
supervisorctl restart myauth:
```

6. Assign permissions to groups via Alliance Auth admin:
   - `aa_discord_voicesnapshot.take_snapshot`
   - `aa_discord_voicesnapshot.view_snapshot_history`
   - `aa_discord_voicesnapshot.edit_snapshot`
   - `aa_discord_voicesnapshot.delete_snapshot`

7. Access the plugin at:
```
/voicesnapshot/
```

## Important
The Discord Gateway does not run inside Django or gunicorn.
It must be started by Supervisor using the runner script above.
- Note: The runner file is kept outside the plugin package because Alliance Auth
Supervisor services must run from the project directory, not from site-packages.

## Troubleshooting
Common Issue
- voicesnapshot: ERROR (spawn error)  
  - Supervisor cannot find the runner file.

Fix
- Make sure the below exists.
```
/home/allianceserver/myauth/voicesnapshot_runner.py
```
