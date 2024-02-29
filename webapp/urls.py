
from django.contrib import admin
from django.urls import path
from newsapp.views import Greet, login_view, logout_view, delete_story, story_handler


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/greet", Greet),
    path("api/login", login_view),
    path("api/logout", logout_view),
    path("api/stories", story_handler),
    path("api/stories/<int:key>", delete_story, name = "delete_story")
]
