from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from tasks_app.models import Task, TaskParam, Result


class ParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskParam
        fields = ('msg', 'count')


class TaskSerializer(WritableNestedModelSerializer):
    params = ParamsSerializer()

    class Meta:
        model = Task
        fields = ('task_name', 'params')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('result', )
