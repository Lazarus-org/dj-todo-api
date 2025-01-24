from rest_framework import mixins, viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth import get_user_model
from todo_api.models import Todo, TodoUserAssignment
from todo_api.api.serializers.todo import TodoSerializer, TodoUserAssignmentSerializer
from typing import List, Dict, Any, Optional

User = get_user_model()

class TodoViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    A ViewSet for managing Todo tasks.

    Provides CRUD operations for Todo tasks and additional actions like assigning users to tasks.
    Supports filtering, ordering, and searching.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    filter_backends: List[Any] = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields: List[str] = ['title', 'created_at', 'updated_at', 'due_date', 'priority']
    search_fields: List[str] = ['title', 'description']

    @action(detail=True, methods=['post'], url_path='assign-user', serializer_class=TodoUserAssignmentSerializer)
    def assign_user(self, request: Request, pk: Optional[int] = None) -> Response:
        """
        Assign a user to the todo task with a specific role.

        Args:
            request (Request): The incoming HTTP request.
            pk (Optional[int]): The primary key of the todo task.

        Returns:
            Response: A DRF Response object with the assignment details or an error message.

        Raises:
            404 Not Found: If the user does not exist.
            400 Bad Request: If the request data is invalid.
        """
        todo = self.get_object()
        user_id: Optional[int] = request.data.get('user_id')
        role: str = request.data.get('role', 'assignee')

        # Validate user_id
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user: User = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create or update the assignment
        assignment, created = TodoUserAssignment.objects.get_or_create(
            todo=todo,
            user=user,
            defaults={'role': role}
        )

        # Update the role if the assignment already exists
        if not created:
            assignment.role = role
            assignment.save()

        # Serialize and return the assignment
        serializer = TodoUserAssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)