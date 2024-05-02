from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class LoginPerson(models.Model):
    userID = models.OneToOneField(User, on_delete = models.CASCADE , related_name='person', primary_key=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=100)


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
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.ImageField(upload_to='textbook_images/', null=True, blank=True)

class CreditCards(models.Model):
    name = models.TextField()
    cardnumber = models.TextField()
    expiry = models.TextField()
    cvv = models.IntegerField()
    limitremaining = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.cardnumber}"
    
class TextbookPurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.quantity} of {self.textbook.title}"

class MealplanPurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_plan_name = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    transaction_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.meal_plan_name} plan"
    
class TicketPurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    zones = models.CharField(max_length=100)  # Store selected zones as a comma-separated string
    number_of_tickets = models.IntegerField()
    bus_card_purchase_option = models.BooleanField(default=False)  # True if bus card purchased, False otherwise
    transaction_date = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.number_of_tickets} tickets"