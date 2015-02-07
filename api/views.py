from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from task.models import Task
from api.serializers import TaskSerializer,EmployeeSerializer


@api_view(['GET', 'POST'])
def task_list(request):
    """
    List all tasks, or create a new task.
    """
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response({'results': serializer.data})

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response({'results': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    """
    Get, udpate, or delete a specific task
    """
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        print"templateeeeeeeeeeeeeeeeeeeeeeeeee"
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print"geeeeeeeeeeet"
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    elif request.method == 'PUT':
        print"this is puttttt"
        serializer = TaskSerializer(task, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serilizer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['PUT', 'POST'])
def add_task(request):
    """
    List all tasks, or create a new task.
    """
    print"ddddddddddd"
    if request.method == 'PUT':
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'POST'])           
def add_employee(request):
    status1={}
    errors={}
    print"ddddddddddd"
    if request.method == 'PUT':
        serializer = EmployeeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            print"1111111"
            message="successfully created"
            status1['message']="successfully created"
            return Response(status1, status=status.HTTP_201_CREATED)
        else:
            print"2222222222"
            for err in serializer.errors:
                errors['error']=err
                
            return Response(
                errors, status=status.HTTP_400_BAD_REQUEST)
    