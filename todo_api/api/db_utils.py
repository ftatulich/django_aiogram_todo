from .models import TelegramUser, Task


def select_user(user_id: int) -> TelegramUser:
    return TelegramUser.objects.get(user_id=user_id)


def select_user_tasks(user_id: int) -> list[Task]:
    user = select_user(user_id)
    return Task.objects.filter(user=user)


def select_task_by_id(task_id: int) -> Task:
    return Task.objects.get(pk=task_id)
