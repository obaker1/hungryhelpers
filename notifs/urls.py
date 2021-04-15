from django.contrib import admin
from django.urls import path, include
from . import views
import notifications.urls
from django.conf.urls import url

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('message', views.message, name='message'),
    path('inbox/', views.inbox, name='inbox'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),

]