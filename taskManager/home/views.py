from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskModelSerializer
from .models import TaskModel


class CreateListTaskView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = TaskModel.objects.filter(user=request.user).order_by('-createdAt')
            serializer = TaskModelSerializer(tasks, many=True)
            return Response({
                'success': True,
                'message': 'Tasks fetched successfully.',
                'number of tasks': tasks.count(),
                'tasks': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as ex:
            return Response({
                'success': False,
                'message': 'Something went wrong.',
                'error' : str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            request.data['status'] = request.data['status'].lower()
            request.data['priority'] = request.data['priority'].lower()

            serializer = TaskModelSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                #serializer.save()
                task = serializer.save(user=request.user)
                return Response({
                    'success': True,
                    'message': 'Task created successfully.',
                    'task': TaskModelSerializer(task).data #serializer.validated_data
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'success': False,
                'message': 'Error occurred while task creation.',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return Response({
                'success': False,
                'message': 'Something went wrong.',
                'error' : str(ex)
            }, status=status.HTTP_400_BAD_REQUEST)

