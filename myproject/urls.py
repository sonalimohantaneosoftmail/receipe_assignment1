"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from receipes.views import recipe_detail,user_recipes
from receipes.views import RegisterView,HomeView,LogoutView,CreateRecipeView,LoginView,UpdateRecipeView,DeleteRecipeView
from receipes.views import ProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('home/',HomeView.as_view(),name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('recipe/new/', CreateRecipeView.as_view(), name='create_recipe'),
    path('update_recipe/<int:pk>/', UpdateRecipeView.as_view(), name='update_recipe'),
    path('delete_recipe/<int:pk>/', DeleteRecipeView.as_view(), name='delete_recipe'),
    # path('recipe/new/', create_recipe, name='create_recipe'),
    path('recipe_detail/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('user_recipes/', user_recipes, name='user_recipes'),


]
