from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from board.models import Task, Worker

def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
    }
    return render(request, "board/index.html", context=context)

class TasksListView(generic.ListView):
    model = Task
    template_name = "board/tasks_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["urgent_tasks"] = Task.objects.filter(priority=Task.Priority.URGENT)
        context["high_tasks"] = Task.objects.filter(priority=Task.Priority.HIGH)
        context["medium_tasks"] = Task.objects.filter(priority=Task.Priority.MEDIUM)
        context["low_tasks"] = Task.objects.filter(priority=Task.Priority.LOW)
        return context


class WorkersListView(generic.ListView):
    model = Worker
    template_name = "board/workers_list.html"
    context_object_name = "workers"
