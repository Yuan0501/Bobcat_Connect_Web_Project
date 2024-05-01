from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import CreateUserForm, PeopleSearchForm, RoommateSearchForm, TextbookSearchForm
from .models import Student, Faculty, Roommate, Textbook


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
    if request.method == 'GET':
        form = TextbookSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            textbooks = Textbook.objects.filter(title__icontains=search_query)
            return render(request, 'search/textbook_searchresults.html', {'textbooks': textbooks, 'query': search_query})
    else:
        form = TextbookSearchForm()
    return render(request, 'search/textbook_search.html', {'form': form})

def search_textbook(request):
    if request.method == 'GET':
        form = TextbookSearchForm(request.GET)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            textbooks = Textbook.objects.filter(title__icontains=search_query) | \
            Textbook.objects.filter(author__icontains=search_query)
            return render(request, 'search/textbook_searchresults.html', {'textbooks': textbooks, 'query': search_query})
    else:
        form = TextbookSearchForm()
    return render(request, 'search/textbook_search.html', {'form': form})
