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
    path('admin-portal/', views.admin_portal, name='admin_portal'),
    path('admin-download-user/<int:user_id>/', views.admin_download_user_txts, name='admin_download_user_txts'),
    path('admin/delete_filled_form/<int:filled_form_id>/', views.admin_delete_filled_form, name='admin_delete_filled_form'),
    # path('admin/delete_all_filled_forms/<int:user_id>/', views.admin_delete_all_filled_forms, name='admin_delete_all_filled_forms'),
    path('admin/delete_user_and_all_data/<int:user_id>/', views.admin_delete_user_and_all_data, name='admin_delete_user_and_all_data'),
    path('assigned_forms_list/', views.assigned_forms_list, name='assigned_forms_list'),  # Now paginated, use ?page=1 etc.
    # Add more as needed
]
