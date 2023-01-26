from django.contrib import admin
from django.urls import include, path

from bacheca.views import BachecaView, CreaPostView

urlpatterns = [
    path('', BachecaView.as_view(), name='bacheca'),
    path("nuovo_post/", CreaPostView.as_view(), name="crea_post")  # new

]
