from .pagination import TaskPagination
from .models import TaskManager
from rest_framework.views import APIView
from .serializers import TaskManagerSerializer
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import IsAdminOrOwner

#view to get all the tasks
class TaskManagerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        # Filtering
        completed = request.query_params.get('completed', None)
        tasks = TaskManager.objects.all()

        # Regular user can only see their own tasks
        if not request.user.is_staff:
            tasks = tasks.filter(user=request.user)

        if completed is not None:
            tasks = tasks.filter(completed=(completed.lower() == 'true'))
        # Pagination
        paginator = TaskPagination()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskManagerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    
# view to post a task
    def post(self, request):    
        data = request.data
        serializer = TaskManagerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)

# to get the specfic task update the data and delete the data
class TaskManagerDetailsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    def get(self, request):
        task_id = request.query_params.get('task_id')
        task = TaskManager.objects.filter(id = task_id).first()
        if not task:
            return Response({'error': 'Task not found'}, status=404)
        self.check_object_permissions(request, task) 
        serializer = TaskManagerSerializer(task)
        return Response(serializer.data, status = 200)
    
    # update the task
    def put(self, request):
        task_id = request.query_params.get('task_id')
        task = TaskManager.objects.filter(id = task_id).first()
        if not task:
            return Response({'error': 'Task not found'}, status=404)
        self.check_object_permissions(request, task) 
        serializer = TaskManagerSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    # delete the task
    def delete(self, request):
        task_id = request.query_params.get('task_id', None)
        if not task_id:
            return Response({'error':'Please provide task id'}, status = 400)
        task = TaskManager.objects.filter(id = task_id).first()
        self.check_object_permissions(request, task) 
        if task:
            task.delete()
            return Response({'message': 'Task deleted successfully'}, status=204)
        return Response({'error': 'Task not found'}, status=404)
        