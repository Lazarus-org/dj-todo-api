from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

class Todo(models.Model):
    """
    Represents a Todo task with a title, description, priority, due date, and completion status.
    Tasks can be assigned to multiple users through the `TodoUserAssignment` intermediate model.
    """
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
    ]

    title = models.CharField(
        max_length=200,
        help_text=_('The title of the todo task.'),
        db_comment='The title of the todo task.'
    )
    description = models.TextField(
        blank=True, null=True,
        help_text=_('A detailed description of the todo task.'),
        db_comment='A detailed description of the todo task.'
    )
    completed = models.BooleanField(
        default=False,
        help_text=_('Indicates whether the todo task is completed.'),
        db_comment='Indicates whether the todo task is completed.'
    )
    due_date = models.DateField(
        blank=True, null=True,
        help_text=_('The due date for the todo task.'),
        db_comment='The due date for the todo task.'
    )
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text=_('The priority level of the todo task.'),
        db_comment='The priority level of the todo task.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The date and time when the todo task was created.'),
        db_comment='The date and time when the todo task was created.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_('The date and time when the todo task was last updated.'),
        db_comment='The date and time when the todo task was last updated.'
    )
    assigned_users = models.ManyToManyField(
        User,
        through='TodoUserAssignment',
        related_name='assigned_todos',
        help_text=_('The users assigned to this todo task.'),
        db_comment='The users assigned to this todo task.'
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Default ordering by creation date (newest first)
        db_table_comment = 'Stores todo tasks and their metadata.'
        verbose_name = _('Todo')
        verbose_name_plural = _('Todos')


class TodoUserAssignment(models.Model):
    """
    Represents the assignment of a user to a todo task with a specific role.
    This is an intermediate table for the Many-to-Many relationship between `Todo` and `User`.
    """
    ROLE_CHOICES = [
        ('assignee', _('Assignee')),
        ('reviewer', _('Reviewer')),
    ]

    todo = models.ForeignKey(
        Todo,
        on_delete=models.CASCADE,
        help_text=_('The todo task to which the user is assigned.'),
        db_comment='The todo task to which the user is assigned.'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('The user assigned to the todo task.'),
        db_comment='The user assigned to the todo task.'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='assignee',
        help_text=_('The role of the user in the todo task (e.g., assignee or reviewer).'),
        db_comment='The role of the user in the todo task (e.g., assignee or reviewer).'
    )
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_('The date and time when the user was assigned to the todo task.'),
        db_comment='The date and time when the user was assigned to the todo task.'
    )

    class Meta:
        unique_together = ('todo', 'user')  # Ensure a user is assigned to a todo only once
        db_table_comment = 'Stores the assignment of users to todo tasks with their roles.'
        verbose_name = _('Todo User Assignment')
        verbose_name_plural = _('Todo User Assignments')

    def __str__(self):
        return f"{self.user} - {self.todo.title} ({self.role})"