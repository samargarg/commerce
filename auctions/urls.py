from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("closebid/<str:listing_id>", views.closebid, name="closebid"),
    path("addcomment/<str:listing_id>", views.addcomment, name="addcomment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addtowatchlist/<str:listing_id>", views.addtowatchlist, name="addtowatchlist"),
    path("removefromwatchlist/<str:listing_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category")
]
