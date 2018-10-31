from django.db import models


class TaskParam(models.Model):
    msg = models.CharField(max_length=200)
    count = models.IntegerField()

    def __str__(self):
        return '{"msg": "%s", "count": "%s"}' % (self.msg, self.count)


class Result(models.Model):
    result = models.CharField(max_length=100)

    def __str__(self):
        return self.result


class Task(models.Model):
    task_name = models.CharField(max_length=100)
    params = models.ForeignKey(TaskParam, blank=False, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
