from django.urls import path
from .views import SignUpView, EditSettingsView, ShowProfileView, EditProfileView, AddStudentView, EditStudentView, DeleteStudentView, MealPlansView, EditMealPlanView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', EditSettingsView.as_view(), name='edit_settings'),
    #path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/', ShowProfileView.as_view(), name='show_profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('add_student/', AddStudentView.as_view(), name='add_student'),
    path('<int:pk>/edit_student/', EditStudentView.as_view(), name='edit_student'),
    path('<int:pk>/delete_student/', DeleteStudentView.as_view(), name='delete_student'),
    path('meal_plans/', MealPlansView.as_view(), name='meal_plans'),
    #path('create_meal_plan/', CreateMealPlanView.as_view(), name='create_meal_plan'),
    path('<int:pk>/edit_meal_plan/', EditMealPlanView.as_view(), name='edit_meal_plan'),

    # Path when user wants to change password (Needs to be logged on)
    path('change_password/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    # Path when user forgets password (Does not need to be logged on)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
]