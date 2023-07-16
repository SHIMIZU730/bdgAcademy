from django.urls import path
from . import views
from devapp.views import IndexTemplateView
from .views import detectBoardgame

app_name = 'devapp'
urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('detectBdg', views.detectBoardgame.as_view(), name='detectBdg'),
]