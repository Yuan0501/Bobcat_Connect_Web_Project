from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Department, Student, Faculty, Roommate, Textbook, LoginPerson, Event

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Roommate)
admin.site.register(Textbook)
admin.site.register(LoginPerson)
admin.site.register(Event)
