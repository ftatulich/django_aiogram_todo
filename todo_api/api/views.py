from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404

from .db_utils import select_user_tasks, select_user, select_task_by_id
from .models import Task, TelegramUser
from .serializers import TaskSerializer, TelegramUserSerializer
from .utils import get_user_id_from_request


class TaskListAPIView(APIView):
    def get(self, request):
        tasks = select_user_tasks(get_user_id_from_request(request))
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            user = select_user(get_user_id_from_request(request))

            data = request.data.copy()
            data['user'] = user.id

            serializer = TaskSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except TelegramUser.DoesNotExist:
            return Response("Invalid user ID.", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("")


class TaskDetailAPIView(APIView):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        user = select_user(get_user_id_from_request(request))
        if task.user != user:
            return Response('', status.HTTP_406_NOT_ACCEPTABLE)

        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            user = select_user(get_user_id_from_request(request))
            if task.user != user:
                return Response('', status.HTTP_406_NOT_ACCEPTABLE)

            data = request.data.copy()
            data['user'] = user.id

            serializer = TaskSerializer(task, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'e'}, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        user = select_user(get_user_id_from_request(request))

        if task.user != user:
            return Response('', status.HTTP_406_NOT_ACCEPTABLE)

        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompleteTaskView(APIView):
    def put(self, request, task_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            user = select_user(get_user_id_from_request(request))
            if task.user != user:
                return Response('', status.HTTP_406_NOT_ACCEPTABLE)

            task = select_task_by_id(task_id)
            task.completed = True
            task.save()
            return Response({'message': 'Task completed successfully.'}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'message': 'Task not found.'}, status=status.HTTP_404_NOT_FOUND)


class TelegramUserView(APIView):
    def get(self, request, user_id):
        try:
            user = select_user(user_id)
            serializer = TelegramUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except TelegramUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
