from django.urls import path
from registration.views import activity_log, homepage

app_name = "registration"
urlpatterns = [
    path("", homepage, name="homepage"),
    path("guest/<int:user_id>/activity-log", activity_log, name="activity_log"),
]
