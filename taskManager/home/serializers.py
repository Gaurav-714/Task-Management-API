from rest_framework import serializers
from datetime import date
from .models import TaskModel

class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        exclude = ['user']
        extra_kwargs = {
            'createdAt': {'read_only': True},
            'updatedAt': {'read_only': True},
        }

    def validate(self, data):
        if 'due_date' in data and data['due_date']:
            if data['due_date'] < date.today():
                raise serializers.ValidationError("Due date cannot be in the past.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        task = TaskModel.objects.create(user=user, **validated_data)
        return task
