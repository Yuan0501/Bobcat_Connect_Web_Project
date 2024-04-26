from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('search_people', views.search_people, name='search_people'),
    path('search_roommates', views.search_roommates, name='search_roommates'),
    path('textbook/search/', views.search_textbook, name='search_textbook'),
    path('checkout/', views.checkout, name='checkout'),
    path('finalize-purchase/', views.finalize_purchase, name='finalize_purchase'),
    path('purchase_confirmation/', views.purchase_confirmation_view, name='purchase_confirmation')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)