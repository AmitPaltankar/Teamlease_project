from django.contrib import admin
from .models import Employee, File, FileError

class Employee_Admin(admin.ModelAdmin):
    list_display = ['emp_id', 'name', 'email', 'mobile','date_of_join']
admin.site.register(Employee, Employee_Admin)

admin.site.register(File)

admin.site.register(FileError)
