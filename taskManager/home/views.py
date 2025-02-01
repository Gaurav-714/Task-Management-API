from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q
import uuid
from .serializers import TaskModelSerializer
from .models import TaskModel


class CreateListTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = TaskModel.objects.filter(user=request.user).order_by('?')
            search_query = request.GET.get('search')
            if search_query:
                tasks = TaskModel.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

            paginator = Paginator(tasks, 5)
            page_number = request.GET.get('page', 1)

            try:
                page_tasks = paginator.page(page_number)
            except:
                page_tasks = []

            serializer = TaskModelSerializer(page_tasks, many=True)
            return Response({
                'success': True,
                'message': 'Tasks fetched successfully.',
                'number_of_tasks': tasks.count(),
                'tasks': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({
                'success': False,
                'message': 'Something went wrong.',
                #'error': str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data
        if 'status' in data:
            data['status'] = data['status'].lower()
        if 'priority' in data:
            data['priority'] = data['priority'].lower()

        serializer = TaskModelSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'success': True,
                'message': 'Task created successfully.',
                'task': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': 'Error occurred while task creation.',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UpdateRetrieveTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def validate_task_id(self, request, task_id):
        try:
            task_uuid = uuid.UUID(str(task_id))
        except ValueError:
            return Response({
                'success': False,
                'error': 'Invalid UUID format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        task = TaskModel.objects.filter(task_id=task_id).first()
        if not task:
            return Response({
                'success': False,
                'message': 'Task does not exist with this UUID.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if task.user != request.user:
            return Response({
                'success': False,
                'message': 'You are not authorized for this.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        return task 

    def get(self, request, task_id):
        task = self.validate_task_id(request, task_id)
        if isinstance(task, Response):
            return task
        
        serializer = TaskModelSerializer(task)
        return Response({
            'success': True,
            'message': 'Task fetched successfully.',
            'task': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, task_id):
        task = self.validate_task_id(request, task_id)
        if isinstance(task, Response):
            return task
        
        data = request.data
        if 'status' in data:
            data['status'] = data['status'].lower()
        if 'priority' in data:
            data['priority'] = data['priority'].lower()
        
        serializer = TaskModelSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Task updated successfully.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, task_id):
        task = self.validate_task_id(request, task_id)
        if isinstance(task, Response):
            return task 
        
        task.delete()
        return Response({
            'success': True,
            'message': 'Task deleted successfully.'
        }, status=status.HTTP_200_OK)
