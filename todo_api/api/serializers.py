from rest_framework import serializers
from .models import Task, TelegramUser


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=TelegramUser.objects.all())

    class Meta:
        model = Task
        fields = '__all__'


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ('id', 'user_id')
