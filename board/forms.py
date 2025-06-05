from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from board.models import Task, Worker


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = Task
        fields = "__all__"


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position", )


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "position")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if Worker.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
