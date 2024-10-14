from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
#from django.db.models import Q
#from django.core.paginator import Paginator
from .models import *
from .serializers import *


class RegisterView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = RegisterSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                        'success' : True,
                        'message' : 'Your account is created.',
                        'data' : serializer.data
                    }, status = status.HTTP_201_CREATED)
            
            return Response({
                        'success' : False,
                        'message' : 'Error occurred while registration.',
                        'data' : serializer.errors
                    }, status = status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            return Response({
                    'success' : False,
                    'message' : 'Something went wrong.',
                    'error' : str(ex)
                }, status = status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)

            if serializer.is_valid():
                response = serializer.get_jwt_token(serializer.validated_data)
                if response:
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'success': False,
                        'message': 'Invalid login credentials.',
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'success': False,
                    'message': 'Error occurred while authentication.',
                    'errors': serializer.errors,
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            return Response({
                    'success' : False,
                    'message' : 'Something went wrong.',
                    'error' : str(ex)
                }, status = status.HTTP_400_BAD_REQUEST)