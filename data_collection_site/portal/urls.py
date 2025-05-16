from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('form/<str:form_id>/', views.form_view, name='form_view'),
    path('start_forms/', views.start_forms, name='start_forms'),
    path('assigned_form/<int:page_num>/', views.assigned_form_page, name='assigned_form_page'),
    path('download_single_entry/<str:form_id>/', views.download_single_entry, name='download_single_entry'),
    path('download_all_assigned/', views.download_all_assigned, name='download_all_assigned'),
    # Add more as needed
]
