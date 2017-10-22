from django.conf.urls import url

from .views import control_view

app_name = 'Workflow'

urlpatterns = [
    url(r'^$', control_view, name='skripte'),
]
