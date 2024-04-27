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