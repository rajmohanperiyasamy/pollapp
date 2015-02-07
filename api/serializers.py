from rest_framework import serializers

from task.models import Task,Employees


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'completed')
        

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employees
        fields = ('EmpId', 'first_name', 'last_name','mobile','email','country')

  
class AddTaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    completed = serializers.BooleanField(default=True)
    
    class Meta:
        model = Task
        fields = ('title', 'description', 'completed')