from django.urls import path, include

from . import views 


urlpatterns = [
    path("", views.Homepage.as_view(), name="index"),
    path("auth/events", views.Events.as_view(), name="events"),
    path("auth/login", views.Login.as_view(), name="login"),
    path("auth/profile/<int:pk>", views.UserProfile.as_view(), name="profile"),
    path("auth/profile/edit/<int:pk>", views.UserProfileEdit.as_view(), name="edit_profile"),
    path("auth/register", views.Register.as_view(), name="register"),
   # path("auth/register",views.Register.as_view(),name= "register")
]

