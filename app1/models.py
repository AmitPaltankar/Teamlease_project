from django.db import models


class File(models.Model):
    file = models.FileField(upload_to="files")

    def __str__(self):
        return str(self.file)

class FileError(models.Model):
    file_error = models.CharField(max_length=10000)

    def __str__(self):
        return self.file_error

class Employee(models.Model):
    emp_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    date_of_join = models.DateTimeField(null=True, auto_now_add=True)

    

    def __str__(self):
        return self.name


