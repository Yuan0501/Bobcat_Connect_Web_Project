from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import DateInput
from django import forms
from django.forms.widgets import PasswordInput, TextInput


from django import forms
from .models import Department

class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zipCode = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'zipCode', 'email', 'username', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput)
    password = forms.CharField(widget=PasswordInput)



class PeopleSearchForm(forms.Form):
    name = forms.CharField(required=False)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)


class RoommateSearchForm(forms.Form):
    move_in_date = forms.DateField(required=False, widget=DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=(('', 'Any'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')), required=False)
    price = forms.DecimalField(required=False, max_digits=7, decimal_places=2)


class TextbookSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search', required=False)
