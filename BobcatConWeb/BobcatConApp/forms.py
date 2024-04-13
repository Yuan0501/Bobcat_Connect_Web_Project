from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import DateInput


from django import forms
from .models import Department

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        # fields = ['FirstName', 'LastName', 'Address', 'City', 'State', 'Zipcode', 'Email', 'LoginName', 'Password', 'confirmPassword']
        fields = ['username', 'email', 'password1', 'password2']

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)


class RoommateSearchForm(forms.Form):
    move_in_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=(('', 'Any'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), required=False)
    price = forms.DecimalField(required=False, max_digits=7, decimal_places=2)