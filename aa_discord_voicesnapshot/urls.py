from django.urls import path
from . import views

app_name = "aa_discord_voicesnapshot"

urlpatterns = [
    path("snapshot/", views.snapshot, name="snapshot"),
    path("history/", views.history, name="history"),
    path("history/export/csv/", views.snapshot_export_csv, name="snapshot_export_csv"),
    path("history/<int:snapshot_id>/", views.snapshot_detail, name="snapshot_detail"),
    path("history/<int:snapshot_id>/edit/", views.snapshot_edit, name="snapshot_edit"),
    path("history/<int:snapshot_id>/delete/", views.snapshot_delete, name="snapshot_delete"),
]
