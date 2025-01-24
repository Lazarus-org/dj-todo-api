from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Todo, TodoUserAssignment

class TodoUserAssignmentInline(admin.TabularInline):
    """
    Inline admin for TodoUserAssignment to allow assigning users to a Todo directly from the Todo admin page.
    """
    model = TodoUserAssignment
    autocomplete_fields = ('user',)  # Enable autocomplete for the user field
    extra = 1  # Show one extra empty form by default
    verbose_name = _('User Assignment')
    verbose_name_plural = _('User Assignments')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Todo model.
    """
    list_display = ('title', 'completed', 'due_date', 'priority', 'created_at', 'updated_at')
    list_editable = ('priority',)  # Allow editing these fields directly from the list view
    list_filter = ('completed', 'priority', 'created_at', 'updated_at')  # Add more filters for better usability
    search_fields = ('title', 'description')  # Enable search by title and description
    list_per_page = 20  # Show 20 items per page
    date_hierarchy = 'created_at'  # Add a date hierarchy for easy navigation by creation date
    inlines = [TodoUserAssignmentInline]  # Include the inline for assigning users
    readonly_fields = ('created_at', 'updated_at')  # Make these fields read-only in the detail view
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'completed', 'due_date', 'priority')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Collapse this section by default
        }),
    )

    def get_queryset(self, request):
        """
        Optimize the queryset by prefetching related users.
        """
        return super().get_queryset(request).prefetch_related('assigned_users')


@admin.register(TodoUserAssignment)
class TodoUserAssignmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the TodoUserAssignment model.
    """
    list_display = ('todo', 'user', 'role', 'assigned_at')
    list_select_related = ('todo', 'user')  # Optimize database queries by selecting related objects
    list_filter = ('role', 'assigned_at')  # Add more filters for better usability
    search_fields = ('todo__title',)  # Enable search by todo title and user details
    autocomplete_fields = ('user', 'todo')  # Enable autocomplete for user and todo fields
    list_per_page = 20  # Show 20 items per page
    date_hierarchy = 'assigned_at'  # Add a date hierarchy for easy navigation by assignment date
    readonly_fields = ('assigned_at',)  # Make this field read-only in the detail view
    fieldsets = (
        (None, {
            'fields': ('todo', 'user', 'role')
        }),
        (_('Metadata'), {
            'fields': ('assigned_at',),
            'classes': ('collapse',)  # Collapse this section by default
        }),
    )

    def get_queryset(self, request):
        """
        Optimize the queryset by selecting related objects.
        """
        return super().get_queryset(request).select_related('todo', 'user')