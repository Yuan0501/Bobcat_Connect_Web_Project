from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('update_user', views.update_user, name="update"),  
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_done.html"), name="password_reset_complete"),
    path('search_people', views.search_people, name='search_people'),
    path('search_roommates', views.search_roommates, name='search_roommates'),
    path('textbook/search/', views.search_textbook, name='search_textbook'),
    path('checkout/', views.checkout, name='checkout'),
    path('finalize-purchase/', views.finalize_purchase, name='finalize_purchase'),
    path('purchase_confirmation/', views.purchase_confirmation_view, name='purchase_confirmation'),
    path('meal-plans/', views.meal_plans, name='meal_plans'),
    path('purchase-history/', views.purchase_history, name='purchase_history')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)