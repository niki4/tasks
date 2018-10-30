from rest_framework import viewsets

from tasks_app.models import Task
from tasks_app.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """ Handles creating CRUD instance set for Task """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
