from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic import TemplateView
from .models import Profile, Post, Photo, Follow
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import CreateProfileForm

# ---------------- Mixins ----------------

class ProfileAccessMixin(LoginRequiredMixin):
    login_url = '/login/'

    def get_profile(self):
        """Return the Profile object of the logged-in user."""
        return Profile.objects.filter(user=self.request.user).first()


# ---------------- Profile Views ----------------

class ProfileListView(ListView):
    """Show all profiles."""
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"


class ProfileDetailView(DetailView):
    """Show any Profile based on the URL pk."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"


class LoggedInProfileDetailView(ProfileAccessMixin, DetailView):
    """Display the Profile page of the logged-in user."""
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_profile()


class UpdateProfileView(ProfileAccessMixin,LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

    def get_object(self):
        # Return the Profile of the logged-in user
        return self.get_profile()

    def get_login_url(self):
        return reverse('login')


# ---------------- Post Views ----------------

class PostDetailView(DetailView):
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"


class CreatePostView(ProfileAccessMixin,LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.profile = self.get_profile()
        post.save()

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(post=post, image_file=f)

        self.object = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_post', args=[self.object.pk])


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('show_post', args=[self.object.pk])
    
    def get_object(self):

        # Example: update the latest post by the logged-in user
        return Post.objects.filter(profile__user=self.request.user).last()


class DeletePostView(ProfileAccessMixin,LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        return reverse('show_profile', args=[self.object.profile.pk])


# ---------------- Followers / Following ----------------

class ShowFollowersDetailView(ProfileAccessMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["followers"] = self.object.get_followers()
        return context


class ShowFollowingDetailView(ProfileAccessMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_object(self):
        return self.get_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["following"] = self.object.get_following()
        return context


# ---------------- Feed / Search ----------------

class PostFeedListView(ProfileAccessMixin, ListView):
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        profile = self.get_profile()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class SearchView(ProfileAccessMixin, ListView):

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_profile()
        self.query = self.request.GET.get('query', None)
        if not self.query:
            return render(request, 'mini_insta/search.html', {'profile': self.profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.filter(caption__icontains=self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        matching_profiles = Profile.objects.filter(
            models.Q(username__icontains=self.query) |
            models.Q(display_name__icontains=self.query) |
            models.Q(bio_text__icontains=self.query)
        )
        context['profile'] = self.profile
        context['query'] = self.query
        context['matching_profiles'] = matching_profiles
        return context
    



class LogoutConfirmationView(TemplateView):
    template_name = "mini_insta/logged_out.html"



class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        # Reconstruct the UserCreationForm from POST data
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()  # creates the User object
            # Log the user in
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            # Attach the user to the Profile instance
            form.instance.user = user
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        # Redirect to the logged-in user's profile page after registration
        return reverse('show_profile',args=[self.object.pk])