from django.contrib import admin
from django.urls import path
from wish_app import views

urlpatterns = [
    path("", views.loginreg),
    path('admin/', admin.site.urls),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('addWish', views.addWish),
    path('createWish', views.createWish),
    path('remove/<item_id>', views.removeitem),
    path('edit/<item_id>', views.showEditPage),
    path('editWish/<item_id>', views.editItem)
]
