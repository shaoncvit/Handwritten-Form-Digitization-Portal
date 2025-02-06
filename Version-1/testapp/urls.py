from django.urls import path
from testapp import views

urlpatterns = [
    path('', views.homePage, name = "home"),
    path('about/', views.aboutPage, name = "about"),
    path('contact/', views.contactPage, name = "contact"),
    path('signup/', views.register, name = "reg"),
    path("check_user/",views.checkUser, name = "check_user"),
    path("login_user/", views.login_user, name = "login_user"),
    path("user_dashboard/",views.user_dashboard, name = "user_dashboard"),
    path("user_logout/", views.user_logout, name = "user_logout"),
    path("edit_profile/", views.edit_Profile, name = "edit_profile"),
    path("change_password/", views.changePassword, name = "change_password"),
    path("add_form/", views.add_form_view, name = "add_form_view"),
    path("myform/", views.my_forms, name = "myform"),
    # path("viewForm/<int:form_id>", views.view_form, name="view_form"),
    path("deleteForm/<int:form_id>", views.delete_form, name="delete_form"),
    path("digitize/<int:form_id>/", views.get_digitize, name = "digitize"),
    path("showDigitizeOutput/<int:form_id>",views.get_digitize, name ="result"),
    path('showDigitizedOutput/<int:form_id>', views.show_digitized_output, name='show_digitized_output'),
    # path("showDigitizeOutput1/", views.digitize_output, name ="result1" ),
    path("download_csv/<int:form_id>", views.download_csv, name = "csvDownload"),
    path('showDigitizedOutput/', views.clear_digitized_data, name='clear_digitized_data'),


]