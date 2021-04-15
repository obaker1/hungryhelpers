from django.urls import path
from .views import SignUpView, EditSettingsView, ShowProfileView, EditProfileView, CreateProfileView, AddStudentView, EditStudentView, DeleteStudentView, Intermediate
from . import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', EditSettingsView.as_view(), name='edit_settings'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('<int:pk>/profile/', ShowProfileView.as_view(), name='show_profile'),
    path('<int:pk>/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('<int:pk>/add_student/', AddStudentView.as_view(), name='add_student'),
    path('<int:pk>/edit_student/', EditStudentView.as_view(), name='edit_student'),
    path('<int:pk>/delete_student/', DeleteStudentView.as_view(), name='delete_student'),
    path('intermediate/', views.Intermediate, name='intermediate'),
]