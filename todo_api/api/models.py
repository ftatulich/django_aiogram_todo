from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    user = models.ForeignKey("TelegramUser", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.user_id)
