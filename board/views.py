from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from board.models import Task, Worker
from board.forms import TaskCreateForm

def index(request: HttpRequest) -> HttpResponse:
    num_tasks = Task.objects.count()
    num_workers = Worker.objects.count()
    user = request.user if request.user.is_authenticated else None

    context = {
        "num_tasks": num_tasks,
        "num_workers": num_workers,
        "user": user,
    }
    return render(request, "board/index.html", context=context)

class TasksListView(LoginRequiredMixin, generic.ListView):
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


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    template_name = "board/task_delete.html"
    success_url = reverse_lazy("board:task-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("board:task-list")


class WorkersListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    template_name = "board/workers_list.html"
    context_object_name = "workers"


class WorkerProfileDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
