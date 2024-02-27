from django.urls import path
from base.api.views import Login,UsuarioCreateView,refresh,UserListView,user_list

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('create/', UsuarioCreateView.as_view(), name='create'),
    path('refresh/', refresh.as_view(), name='refresh'),
    
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/', user_list, name='list')
]