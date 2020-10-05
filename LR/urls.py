from django.urls import path
from .views import UserRegisterView, homepage, logoutUser, loginpage, add_expense

urlpatterns = [
     path('register/', UserRegisterView.as_view(), name="registered"),
     path('logout/', logoutUser, name="Logout"),
     path('', homepage, name="home"),
     path('login2/', loginpage, name="Login"),
     path('add_expense/', add_expense, name='add_expense'),
]