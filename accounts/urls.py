from django.urls import path
from .views import SignUpView, EditSettingsView, ShowProfileView, EditProfileView, CreateProfileView, AddStudentView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', EditSettingsView.as_view(), name='edit_settings'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('<int:pk>/profile/', ShowProfileView.as_view(), name='show_profile'),
    path('<int:pk>/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('<int:pk>/add_student/', AddStudentView.as_view(), name='add_student'),
]