from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name','password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if user:
            raise serializers.ValidationError("Account with this email already exists.")
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
            raise serializers.ValidationError("Account with this email does not exist.")
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError("Incorrect password.")
        return attrs
    
    def get_jwt_token(self, validated_data):
        user = User.objects.filter(email=validated_data['email']).first()
        if user.check_password(validated_data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'success': True,
                'message': 'Logged in successfully.',
                'data': {
                    'token': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }
                }
            }
        else:
            return {
                'success': False,
                'message': 'Invalid credentials, please try again.',
                'data': {}
            }