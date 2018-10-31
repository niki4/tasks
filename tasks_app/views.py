from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.response import Response

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

            task_result = "test result"
            result_rec = Result.objects.create(result=task_result)
            # result_ser = ResultSerializer(data=result_rec)
            # result_ser.is_valid()

            serializer.save(result=result_rec)

            # headers = self.get_success_headers(serializer.data)
            # return Response(result_ser.validated_data, status=status.HTTP_201_CREATED, headers=headers)
            return HttpResponseRedirect(
                redirect_to=reverse('tasks_app:result-detail', args=(result_rec.pk, )))
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows view and list results of the tasks
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
