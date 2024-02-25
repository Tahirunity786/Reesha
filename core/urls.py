from django.urls import path
from core.views import (Register, Login, Logout, create_list, update_list, list_del, list_marked, list_unmarked, marked_as_completed, search_list, social_data, account)

urlpatterns = [
    path('public', social_data, name="post"),
    path('public/account', account, name="account"),
    path('public/m/list/search', search_list, name="l-search"),
    path('public/m/list', marked_as_completed, name="m-completed"),
    path('public/u/register', Register, name="Register"),
    path('public/u/login', Login, name="Login"),
    path('public/u/logout', Logout, name="Logout"),
    path('public/create_list', create_list, name="Logout"),
    path('public/lists/<int:id>/', update_list, name="Update"),
    path('public/lists/marked/<int:id>/', list_marked, name="Marked"),
    path('public/lists/del/<int:id>/', list_del, name="Marked"),
    path('public/lists/unmark/<int:id>/', list_unmarked, name="Marked"),
    
]
