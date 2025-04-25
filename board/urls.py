from django.urls import path

from board.views import (
    index, TasksListView, WorkersListView,
    TaskCreateView, TaskDetailView, TaskUpdateView,
    TaskDeleteView, WorkerProfileDetailView
)

urlpatterns = [
    path("", index, name="index"),
    path("tasks/", TasksListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/create", TaskCreateView.as_view(), name="task-create"),
    path("workers/", WorkersListView.as_view(), name="worker-list"),
    path("workers/<int:pk>", WorkerProfileDetailView.as_view(), name="worker-profile-detail"),
]

app_name = "board"
