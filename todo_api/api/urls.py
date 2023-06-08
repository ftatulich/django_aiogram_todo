from django.urls import path
from .views import TaskListAPIView, TaskDetailAPIView, TelegramUserView, CompleteTaskView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('telegram-users/<int:user_id>/', TelegramUserView.as_view()),
    path('tasks/<int:task_id>/complete/', CompleteTaskView.as_view(), name='complete-task'),
    path('telegram-users/', TelegramUserView.as_view(), name='telegram-users'),
]
