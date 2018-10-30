from django.conf.urls import include, url
from rest_framework import routers

from tasks_app import views

router = routers.DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

app_name = 'tasks_app'

urlpatterns = [
    url(r'^', include(router.urls))
]