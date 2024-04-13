from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Student(Person):
    student_id = models.CharField(max_length=10)

class Faculty(Person):
    faculty_id = models.CharField(max_length=10)


class Roommate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    move_in_date = models.DateField()
    gender = models.CharField(max_length=10, choices=(('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')))
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name