from rest_framework import serializers
from datetime import date
from .models import TaskModel

class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['task_id','title','description','status','priority','due_date']
        read_only_fields = ['user']

    def validate(self, data):     
        # Validate 'due_date' field
        if 'due_date' in data:
            if data['due_date'] < date.today():
                raise serializers.ValidationError("Due date cannot be in past.")
        return data
    
    def create(self, validated_data):
        #user = self.context['request'].user
        task = TaskModel.objects.create(**validated_data)
        return task