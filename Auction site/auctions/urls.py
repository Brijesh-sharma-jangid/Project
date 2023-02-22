from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("removelist/<int:id>", views.removelist, name="removelist"),
    path("addlist/<int:id>", views.addlist, name="addlist"),
    path("watchlist", views.displaywatchlist, name="watchlist"),
    path("search", views.search, name="Category"),
    path("close/<int:id>", views.close, name="Close"),
    path("addnewcomment/<int:id>", views.comment, name="Comment")
]
