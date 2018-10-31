from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from tasks_app import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)
router.register(r'results', views.ResultViewSet)

app_name = 'tasks_app'

urlpatterns = [
    url(r'^', include(router.urls))
]
