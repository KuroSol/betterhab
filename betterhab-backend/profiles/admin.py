from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'has_teacher_role', 'has_student_role')
    list_filter = ('has_teacher_role', 'has_student_role')

admin.site.register(Profile, ProfileAdmin)
