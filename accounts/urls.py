from django.urls import path
from . import views
from .views import SignUpView, EditSettingsView, ShowProfileView, EditProfileView, CreateProfileView, AddStudentView, EditStudentView, DeleteStudentView#, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', EditSettingsView.as_view(), name='edit_settings'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/', ShowProfileView.as_view(), name='show_profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('<int:pk>/edit_student/', EditStudentView.as_view(), name='edit_student'),
    path('<int:pk>/delete_student/', DeleteStudentView.as_view(), name='delete_student'),

    # Path when user wants to change password (Needs to be logged on)
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),

    #path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    # Path when user forgets password (Does not need to be logged on)
    #path('password_reset/', PasswordResetView.as_view(), name='password_reset_form'),
    #path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    #path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]