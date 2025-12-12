from django.contrib import admin
from .models import Organization, Project, Task

# Register models for admin interface
admin.site.register(Organization)
admin.site.register(Project)
admin.site.register(Task)
