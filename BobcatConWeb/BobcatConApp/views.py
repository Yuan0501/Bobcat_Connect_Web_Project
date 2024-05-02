from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import CreateUserForm, PeopleSearchForm, RoommateSearchForm, TextbookSearchForm, LoginForm, EventFilterForm, EventSelectionForm
from .models import Student, Faculty, Roommate, Textbook, CreditCards, LoginPerson, Event
from datetime import datetime
import json
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import itertools


def home(request):
    return render(request, 'registration/homepage.html')

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth.login(request, user)
                return redirect("home")
    context = {'loginform' : form}

    return render(request, 'registration/login.html', context=context)


def register(request):
     form = CreateUserForm()

     if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            address = form.cleaned_data.get('address')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            zipCode = form.cleaned_data.get('zipCode')

            person, create = LoginPerson.objects.get_or_create(userID=user)
            person.address = address
            person.city = city
            person.state = state
            person.zipCode = zipCode
            person.save()
            return redirect("login")
        
     context = {'registerform' : form}
     return render(request, 'registration/signup.html', context=context)


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_person = request.user.person
        form_data = {
            'first_name':current_user.first_name,
            'last_name' : current_user.last_name,
            'address' : current_person.address,
            'city' : current_person.city,
            'state' : current_person.state,
            'zipCode' : current_person.zipCode,
            'Email' : current_user.email,
            'username' : current_user.username,
            'password' : current_user.password,
            'password confirmation' : current_user.password,
        }
        update_form = CreateUserForm(request.POST or None, initial=form_data)
        if update_form.is_valid():
            update_form.save()
            return redirect("home")
        context = {'update_form' : update_form}
        return render(request,'registration/update.html',context=context)
    else:
        messages.success(request, ("you must be logged in to website."))
        return redirect("home")
    

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
        purchase_type = request.POST.get('purchase_type')
        items = []
        discount = 0
        revised_total = 0
        total = 0

        if purchase_type == 'meal_plan':
            plan_name = request.POST.get('plan_name')
            # Convert the price to a float here to avoid TypeError
            plan_price = float(request.POST.get('plan_price'))
            total = plan_price
            items = [{'title': plan_name, 'price': plan_price}]
            revised_total = total  # No discount for meal plans
        
        elif purchase_type == 'textbook':
            # Convert prices to floats before summing to avoid TypeError
            cart_data = json.loads(request.POST.get('cartData'))
            items = cart_data.get('items', [])
            # Use a list comprehension to ensure all prices are floats
            total = sum(float(item['price']) for item in items)
            
            if total > 200:
                discount = total * 0.10  # 10% discount
                revised_total = total - discount
            else:
                revised_total = total

        context = {
            'cart_data': {
                'items': items,
                'total': total,
                'purchase_type': purchase_type,
            },
            'total': total,
            'discount': discount,
            'revised_total': revised_total,
        }

        return render(request, 'checkout.html', context)
    else:
        return redirect('home')



def finalize_purchase(request):
    if request.method == 'POST':
        # Retrieve payment details from form
        name = request.POST.get('name')
        cardnumber = request.POST.get('cardnumber')
        exp = datetime.strptime(request.POST.get('expiry'), '%Y-%m-%d').date()
        expiry = exp.strftime('%Y-%m')
        cvv = int(request.POST.get('cvv'))
        total = float(request.POST.get('total'))

        discount = 0
        revised_total = total

        # Apply discount if applicable
        if total > 200:
            discount = total * 0.1  # Calculate 10% discount
            revised_total = total - discount  # Calculate revised total after discount

        # Check if the card is valid
        try:
            card = CreditCards.objects.get(cardnumber=cardnumber, name=name, expiry=expiry, cvv=cvv)
            if card.limitremaining >= revised_total:
                card.limitremaining -= revised_total
                card.save()
                context = {
                    'cart_data': {'total': total, 'items': [], 'discount': discount, 'revised_total': revised_total},
                    # You should actually pass the cart items here too
                }
                return render(request, 'purchase_confirmation.html', context)
            else:
                return render(request, 'error.html', {'message': 'Not enough balance on the card.'})
        except CreditCards.DoesNotExist:
            return render(request, 'error.html', {'message': 'Invalid card details.'})

    return render(request, 'error.html', {'message': 'Invalid request.'})

def purchase_confirmation_view(request):
    return render(request, 'purchase_confirmation.html') 

def meal_plans(request):
    monthly_price = 600
    semester_months = 4
    semester_discount = 0.05
    semester_price = (monthly_price * semester_months) * (1 - semester_discount)

    context = {
        'monthly_plan': {
            'price': monthly_price,
            'duration': '1 Month'
        },
        'semester_plan': {
            'price': semester_price,
            'duration': f'{semester_months} Months',
            'original_price': monthly_price * semester_months,
            'discount_percentage': semester_discount * 100,
        }
    }

    return render(request, 'meals/meal_plan.html', context)

def mealplan_checkout(request):
    if request.method == 'POST':
        plan_name = request.POST.get('plan_name')
        plan_price = request.POST.get('plan_price')

        # Here you can create an order or do whatever is needed with the selected plan

        context = {
            'plan_name': plan_name,
            'plan_price': plan_price,
        }
        return render(request, 'checkout.html', context)
    else:
        # Redirect to meal plans or an error page if this view is accessed without POST data
        return redirect('meal_plans')
    
def events_list(request):
    # Handle event filtering
    form = EventFilterForm(request.GET)
    party_events = Event.objects.filter(category='party')
    activity_events = Event.objects.filter(category='activity')

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        if start_date and end_date:
            party_events = party_events.filter(date__range=[start_date, end_date])
            activity_events = activity_events.filter(date__range=[start_date, end_date])
        
    # Handle event selection
    if request.method == 'POST':
        print("POST data:", request.POST)
        selection_form = EventSelectionForm(request.POST)
        if selection_form.is_valid():
            print("here")
            print("Selection form is valid")
            print("Selected event IDs:", selection_form.cleaned_data.get('selected_events'))
            selected_event_ids = selection_form.cleaned_data.get('selected_events')
            selected_events = Event.objects.filter(id__in=selected_event_ids)
            print(selected_events)
            # Process selected events here
            # For example, you can mark them as selected in the database
            for event in selected_events:
                event.selected = True
                event.save()
            # Redirect to the page displaying selected events
            return redirect('selected_events')
        else:
            print(selection_form.errors)
            return render(request, 'events.html', {
                'party_events': party_events,
                'activity_events': activity_events,
                'form': form,
                'selection_form': selection_form
            })
    else:
        selection_form = EventSelectionForm()

    return render(request, 'events.html', {
        'party_events': party_events,
        'activity_events': activity_events,
        'form': form,
        'selection_form': selection_form
    })


def selected_events(request):
    selected_events = Event.objects.filter(selected=True).order_by('date')  # Assuming you have a 'selected' field in your Event model
    grouped_events = {}

    # Group selected events by month
    for month, events_in_month in itertools.groupby(selected_events, key=lambda event: event.date.strftime('%B %Y')):
        grouped_events[month] = list(events_in_month)

    return render(request, 'selected_events.html', {'grouped_events': grouped_events})