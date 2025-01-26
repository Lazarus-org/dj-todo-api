from django.shortcuts import render
from .models import Todo

def todo_list(request):
    todos = Todo.objects.prefetch_related('assigned_users').all()
    return render(request, 'todo_list.html', {'todos': todos})