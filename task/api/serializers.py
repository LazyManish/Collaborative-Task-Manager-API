from rest_framework import serializers
from task.models import TaskModel

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = '__all__'

