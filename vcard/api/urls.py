from django.urls import path
from .views import vcard

urlpatterns = [
    path('string', vcard)
]