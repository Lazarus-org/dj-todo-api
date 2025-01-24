from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo_api.api.views.todo import TodoViewSet

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')

urlpatterns = router.urls
