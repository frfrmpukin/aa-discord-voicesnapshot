import csv
import requests

from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from authservices.discord.models import DiscordUser
from .models import VoiceSnapshot


def get_voice_channels():
    url = f"https://discord.com/api/v10/guilds/{settings.VOICESNAPSHOT_GUILD_ID}/channels"
    headers = {"Authorization": f"Bot {settings.DISCORD_TOKEN}"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    return [c for c in data if c.get("type") == 2]


@permission_required("aa_discord_voicesnapshot.take_snapshot")
def snapshot(request):
    channels = get_voice_channels()
    results = []
    selected_channel_id = None
    selected_channel_name = None
    timestamp = None
    snapshot_taken_by = None

    if request.method == "POST":
        selected_channel_id = request.POST.get("channel_id")
        selected_channel_name = next(
            (c["name"] for c in channels if str(c["id"]) == selected_channel_id),
            "Unknown"
        )

        timestamp = timezone.now()
        snapshot_taken_by = request.user

        url = f"https://discord.com/api/v10/guilds/{settings.VOICESNAPSHOT_GUILD_ID}/voice-states"
        headers = {"Authorization": f"Bot {settings.DISCORD_TOKEN}"}

        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()

        raw_occupants = [
            vs for vs in data
            if vs.get("channel_id") == selected_channel_id
        ]

        for o in raw_occupants:
            du = DiscordUser.objects.filter(uid=o["user_id"]).first()
            results.append({
                "user_id": o["user_id"],
                "username": du.user.username if du else "Unknown",
            })

        VoiceSnapshot.objects.create(
            taken_by=snapshot_taken_by,
            timestamp=timestamp,
            channel_id=int(selected_channel_id),
            channel_name=selected_channel_name,
            occupants=results,
        )

    return render(request, "aa_discord_voicesnapshot/snapshot.html", {
        "channels": channels,
        "results": results,
        "selected_channel_id": selected_channel_id,
        "selected_channel_name": selected_channel_name,
        "timestamp": timestamp,
        "snapshot_taken_by": snapshot_taken_by.username if snapshot_taken_by else None,
    })


@permission_required("aa_discord_voicesnapshot.view_snapshot_history")
def history(request):
    snapshots = VoiceSnapshot.objects.all().order_by("-timestamp")

    channel_filter = request.GET.get("channel")
    user_filter = request.GET.get("user")

    if channel_filter:
        snapshots = snapshots.filter(channel_name__icontains=channel_filter)

    if user_filter:
        snapshots = snapshots.filter(taken_by__username__icontains=user_filter)

    paginator = Paginator(snapshots, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "aa_discord_voicesnapshot/history.html", {
        "page_obj": page_obj,
        "channel_filter": channel_filter,
        "user_filter": user_filter,
    })


@permission_required("aa_discord_voicesnapshot.view_snapshot_history")
def snapshot_detail(request, snapshot_id):
    snapshot = get_object_or_404(VoiceSnapshot, id=snapshot_id)

    return render(request, "aa_discord_voicesnapshot/detail.html", {
        "snapshot": snapshot,
    })


@permission_required("aa_discord_voicesnapshot.edit_snapshot")
def snapshot_edit(request, snapshot_id):
    snapshot = get_object_or_404(VoiceSnapshot, id=snapshot_id)
    occupants = snapshot.occupants.copy()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "remove":
            user_id = request.POST.get("user_id")
            occupants = [o for o in occupants if str(o["user_id"]) != str(user_id)]

        elif action == "add":
            new_user_id = request.POST.get("new_user_id")
            new_username = request.POST.get("new_username")

            if new_user_id and new_username:
                occupants.append({
                    "user_id": int(new_user_id),
                    "username": new_username,
                })

        snapshot.occupants = occupants
        snapshot.save()

    return render(request, "aa_discord_voicesnapshot/edit.html", {
        "snapshot": snapshot,
        "occupants": occupants,
    })


@permission_required("aa_discord_voicesnapshot.delete_snapshot")
def snapshot_delete(request, snapshot_id):
    snapshot = get_object_or_404(VoiceSnapshot, id=snapshot_id)
    snapshot.delete()
    return redirect("aa_discord_voicesnapshot:history")


@permission_required("aa_discord_voicesnapshot.view_snapshot_history")
def snapshot_export_csv(request):
    snapshots = VoiceSnapshot.objects.order_by("-timestamp")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=snapshot_history.csv"

    writer = csv.writer(response)
    writer.writerow(["ID", "Timestamp", "Channel", "Taken By", "Occupants"])

    for s in snapshots:
        occupant_list = ", ".join(
            [f"{o['username']} ({o['user_id']})" for o in s.occupants]
        )
        writer.writerow([
            s.id,
            s.timestamp,
            s.channel_name,
            s.taken_by.username if s.taken_by else "",
            occupant_list,
        ])

    return response
