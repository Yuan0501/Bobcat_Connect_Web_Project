from django.db import models
from django.conf import settings

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
    


class Textbook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(upload_to='textbook_images/')

class CreditCards(models.Model):
    name = models.TextField()
    cardnumber = models.TextField()
    expiry = models.TextField()
    cvv = models.IntegerField()
    limitremaining = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.cardnumber}"