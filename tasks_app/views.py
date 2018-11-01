import subprocess

from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.response import Response

import tasks
from tasks_app.models import Task, Result
from tasks_app.serializers import TaskSerializer, ResultSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be created or viewed.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def create(self, request, *args, **kwargs):

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():

            task_result, err = self.order_task(serializer)
            if err:
                return Response(
                    {
                        "status": "ERROR",
                        "error_code": 500,
                        "error_msg": err
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result_rec = Result.objects.create(result=task_result)

            serializer.save(result=result_rec)

            return HttpResponseRedirect(
                redirect_to=reverse('tasks_app:result-detail', args=(result_rec.pk, )))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def order_task(self, serializer):
        task_name = serializer.validated_data["task_name"]
        request_params = str(dict(serializer.validated_data["params"]))
        task_params = tasks.parse_user_params(request_params)

        cmdline = ['./example_tasks.py', task_name, '--params', str(task_params)]
        p = subprocess.Popen(cmdline, stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            return None, err

        return out.decode("utf-8"), None


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows view and list results of the tasks
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
