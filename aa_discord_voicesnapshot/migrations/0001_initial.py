from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceSnapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('channel_id', models.BigIntegerField()),
                ('channel_name', models.CharField(max_length=255)),
                ('occupants', models.JSONField()),
                ('taken_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={
                'permissions': [
                    ('take_snapshot', 'Can take Discord voice snapshots'),
                    ('view_snapshot_history', 'Can view Discord snapshot history'),
                    ('edit_snapshot', 'Can edit Discord snapshots'),
                    ('delete_snapshot', 'Can delete Discord snapshots'),
                ],
            },
        ),
        migrations.CreateModel(
            name='VoiceState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(unique=True)),
                ('channel_id', models.BigIntegerField(blank=True, null=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
