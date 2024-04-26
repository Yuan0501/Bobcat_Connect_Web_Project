from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import CreateUserForm, PeopleSearchForm, RoommateSearchForm, TextbookSearchForm
from .models import Student, Faculty, Roommate, Textbook, CreditCards
from datetime import datetime
import json

def home(request):
    return render(request, 'registration/homepage.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        
    context = {'registerform' : form}
    return render(request, 'registration/signup.html', context=context)
 

def logout(request):
    pass


def search_people(request):
    form = PeopleSearchForm(request.GET or None)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results = []
        if form.is_valid():
            name = form.cleaned_data.get('name')
            department = form.cleaned_data.get('department')

            query = Q()
            if name:
                query &= Q(name__icontains=name)
            if department:
                query &= Q(department=department)

            students = Student.objects.filter(query)
            faculty = Faculty.objects.filter(query)
            results = list(students.values('name', 'email', 'department__name')) + list(faculty.values('name', 'email', 'department__name'))

        return JsonResponse({"results": results}, safe=False)
    else:
        return render(request, 'search/peoplesearch.html', {'form': form})
    

def search_roommates(request):
    form = RoommateSearchForm(request.GET or None)
    results = None
    if form.is_valid():
        move_in_date = form.cleaned_data.get('move_in_date')
        gender = form.cleaned_data.get('gender')
        price = form.cleaned_data.get('price')

        queryset = Roommate.objects.all()
        if move_in_date:
            queryset = queryset.filter(move_in_date__lte=move_in_date)
        if gender:
            queryset = queryset.filter(gender=gender)
        if price:
            queryset = queryset.filter(price__lte=price)

        results = queryset

    return render(request, 'search/search_roommates.html', {'form': form, 'results': results})



def search_textbook(request):
    form = TextbookSearchForm(request.GET or None)
    if request.method == 'GET' and form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:  # Check if the query is not empty
            textbooks = Textbook.objects.filter(title__icontains=search_query) | \
                        Textbook.objects.filter(author__icontains=search_query)
        else:  # If no query is entered, fetch all textbooks
            textbooks = Textbook.objects.all()
        return render(request, 'search/textbook_searchresults.html', {'textbooks': textbooks, 'query': search_query})
    return render(request, 'search/textbook_search.html', {'form': form})

def checkout(request):
    if request.method == 'POST':
        cart_data = json.loads(request.POST.get('cartData'))
        return render(request, 'checkout.html', {'cart_data': cart_data})
    return render(request, 'error.html')  # or redirect somewhere appropriate


def finalize_purchase(request):
    if request.method == 'POST':
        # Retrieve payment details from form
        name = request.POST.get('name')
        cardnumber = request.POST.get('cardnumber')
        exp = datetime.strptime(request.POST.get('expiry'), '%Y-%m-%d').date()
        expiry = exp.strftime('%Y-%m')
        cvv = int(request.POST.get('cvv'))
        total = float(request.POST.get('total'))

        # Apply discount if applicable
        if total > 200:
            total *= 0.9  # Apply a 10% discount

        # Check if the card is valid
        try:
            card = CreditCards.objects.get(cardnumber=cardnumber, name=name, expiry=expiry, cvv=cvv)
            if card.limitremaining >= total:
                card.limitremaining -= total
                card.save()
                return render(request, 'purchase_confirmation.html')
            else:
                return render(request, 'error.html', {'message': 'Not enough balance on the card.'})
        except CreditCards.DoesNotExist:
            return render(request, 'error.html', {'message': 'Invalid card details.'})

    return render(request, 'error.html', {'message': 'Invalid request.'})

def purchase_confirmation_view(request):
    return render(request, 'purchase_confirmation.html') 