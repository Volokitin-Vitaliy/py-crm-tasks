from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from board.models import Task, Position, Worker, TaskType

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", )
    fieldsets = UserAdmin.fieldsets + (
        ("Additional information", {
            "fields": ("position", )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets +(
        ("Additional Information", {
            "fields": ("first_name", "last_name","position", )
        }),
    )

@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "deadline", "priority", "is_completed")
    list_filter = ("priority", "is_completed")
    search_fields = ("name", "description")
