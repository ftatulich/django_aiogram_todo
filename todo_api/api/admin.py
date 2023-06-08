from django.contrib import admin
from .models import Task, TelegramUser

admin.site.register(Task)
admin.site.register(TelegramUser)
