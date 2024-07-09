from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Recipe,Profile
from .forms import RecipeForm,CommentForm,RatingForm,ProfileForm
from django.db.models import Avg
from django.views.generic.edit import FormView
from django.views.generic import ListView,UpdateView
from django.views import View
from django.urls import reverse_lazy



# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator



class RegisterView(FormView):
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/home/'

    def form_valid(self, form):
        user = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            self.request.session['user_id'] = user.id
        return redirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})




    
class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['user_id'] = user.id  # Store user ID in session
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')

        return render(request, 'login.html', {'form': form})



class ProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        self.created = created  # Store the created flag to use in form_valid
        return profile

    def form_valid(self, form):
        profile = form.save(commit=False)
        if self.created:
            messages.success(self.request, 'Profile has been created and saved in the database.')
        elif 'bio' in form.changed_data:
            messages.success(self.request, 'Profile has been updated.')
        else:
            messages.info(self.request, 'No changes detected.')
        profile.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('profile_view')



class HomeView(ListView):
    model = Recipe
    template_name = 'home.html'
    context_object_name = 'page_obj'
    paginate_by = 10  # 10 recipes per page

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search_query')

        if search_query:
            queryset = queryset.filter(title__icontains=search_query) | \
                       queryset.filter(ingredients__icontains=search_query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.object_list
        return context



class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Clear user-related session variables upon logout
            request.session.flush()

            # Alternatively, clear specific session keys if needed:
            # if request.user.is_authenticated: 
            #     del request.session['user_id']

            logout(request)
            messages.info(request, "You have been logged out.")
        return redirect(reverse_lazy('profile')) # Redirect to the home page or any other page


class CreateRecipeView(LoginRequiredMixin,View): # Login Required Mixin page will not show create receipe page directly untill the user is not logged in 

    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        form = RecipeForm()
        return render(request, 'recipe_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe_detail', pk=recipe.pk)
        return render(request, 'recipe_form.html', {'form': form})


    
class UpdateRecipeView(LoginRequiredMixin,View):

    login_url = '/login/'

    def get(self, request,pk): #this is needed other wise the page is not visible 
        recipe = get_object_or_404(Recipe,pk=pk)
        form = RecipeForm(instance=recipe)
        return render(request, 'recipe_form.html', {'form': form})

    def post(self, request,pk):
        recipe = get_object_or_404(Recipe,pk=pk)
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
        return render(request, 'recipe_form.html', {'form': form})


class DeleteRecipeView(LoginRequiredMixin, View):
    login_url = '/login/'  # Ensures redirect to login page if not logged in

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.user == recipe.author:
            recipe.delete()
            return redirect('user_recipes')
        else:
            # Optionally, you can add a message if the user tries to delete someone else's recipe
            return redirect('recipe_detail', pk=pk)


# def recipe_detail(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     comments = recipe.comments.all()
#     new_comment = None
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.recipe = recipe
#             new_comment.save()
#             return redirect('recipe_detail', pk=recipe.pk)
#     else:
#         comment_form = CommentForm()
#     return render(request, 'recipe_detail.html', {'recipe': recipe, 'comments': comments, 'comment_form': comment_form})


@login_required(login_url='/login/')
def user_recipes(request):
    recipes = Recipe.objects.filter(author=request.user)
    return render(request, 'user_recipes.html', {'recipes': recipes})


@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.comments.all()
    ratings = recipe.ratings.all()

    # Calculate average rating
    average_rating = ratings.aggregate(Avg('score'))['score__avg'] if ratings.exists() else 'No ratings yet'

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        rating_form = RatingForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.recipe = recipe
            new_comment.save()
            return redirect('recipe_detail', pk=recipe.pk)
        
        if  rating_form.is_valid():
            new_rating = rating_form.save(commit=False)
            new_rating.author = request.user
            new_rating.recipe = recipe
            new_rating.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        comment_form = CommentForm()
        rating_form = RatingForm()

    # Render template with recipe details, comments, and comment form
    return render(request, 'recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'ratings': ratings,
        'average_rating': average_rating,
        'rating_form': rating_form
    })



