from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Profile, Post, Photo, Follow, Like
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.shortcuts import get_object_or_404
from django.db import models
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class UserProfileMixin(LoginRequiredMixin):
    def get_login_url(self):
        return reverse('login')

    def get_user_profile(self):
        user = self.request.user
        profile = Profile.objects.filter(user=user).first()
        if profile:
            return profile

        profile = Profile.objects.filter(username=user.username).first()
        if profile:
            profile.user = user
            profile.save(update_fields=['user'])
            return profile

        return None


class ProfileListView(ListView):
    '''Define a view class to show all mini_insta profiles'''
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"



class ProfileDetailView(DetailView):
    '''Define a view class to show a singlr mini_insta profiles'''
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile = None
        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user=self.request.user).first()
        context['current_profile'] = current_profile
        context['can_edit'] = bool(current_profile and current_profile.pk == self.object.pk)
        context['can_follow'] = bool(current_profile and current_profile.pk != self.object.pk)
        context['is_following'] = bool(current_profile and current_profile.is_following(self.object))
        return context

class PostDetailView(DetailView):
    model=Post
    template_name="mini_insta/show_post.html"
    context_object_name="post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile = None
        if self.request.user.is_authenticated:
            current_profile = Profile.objects.filter(user=self.request.user).first()
        context['current_profile'] = current_profile
        context['can_edit_post'] = bool(current_profile and current_profile.pk == self.object.profile.pk)
        context['can_like'] = bool(current_profile and current_profile.pk != self.object.profile.pk)
        context['has_liked'] = bool(current_profile and self.object.is_liked_by(current_profile))
        return context


class CreatePostView(UserProfileMixin, CreateView):
    '''Allow users to create a new Post associated with a specific Profile.
'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"


    def get_context_data(self, **kwargs):

        '''Add the Profile object to the context data
        so the form knows which Profile this Post belongs to.'''

        context = super().get_context_data(**kwargs)
        profile = self.get_user_profile()
        if not profile:
            return context
        context['profile'] = profile
        return context


    def form_valid(self, form):
        ''' Attaches the Post to the correct Profile and creates an associated Photo.'''
        profile = self.get_user_profile()
        if not profile:
            return redirect('create_profile')
        post = form.save(commit=False)
        post.profile = profile
        post.save()

 
        #image_url = self.request.POST.get('image_url')
        #if image_url:
            #Photo.objects.create(post=post, image_url=image_url)
        
        #self.object = post 
        files = self.request.FILES.getlist('files')

        for f in files:
            Photo.objects.create(post=post, image_file=f)

        self.object=post

        return super().form_valid(form)
    
    def get_success_url(self):

        '''     Redirect the user to the new Post's detail page after creation.'''
        return reverse('show_post', args=[self.object.pk])

class UpdateProfileView(UpdateView):
    '''View to update a user's profile information.

    Inherits from Django's generic UpdateView.'''

    model=Profile
    form_class=UpdateProfileForm
    template_name="mini_insta/update_profile_form.html"

    def get_login_url(self):
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not self.get_object():
            return redirect('create_profile')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        profile = Profile.objects.filter(user=self.request.user).first()
        if not profile:
            profile = Profile.objects.filter(username=self.request.user.username).first()
            if profile:
                profile.user = self.request.user
                profile.save(update_fields=['user'])
        return profile

    def get_success_url(self):
        return reverse('show_my_profile')


class UpdatePostView(UserProfileMixin, UpdateView):

    ''''View to update a Post's information.

    Inherits from Django's generic UpdateView.'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        profile = self.get_user_profile()
        if not profile or post.profile_id != profile.id:
            return redirect('show_post', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        ''' After successfully updating a Post, redirect to the page
        showing that Post.'''

        return reverse('show_post', args=[self.object.pk])
    
class DeletePostView(UserProfileMixin, DeleteView):
    ''' View to delete a Post.

    Inherits from Django's generic DeleteView.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        '''Add extra context to the template: the Post object and the Profile
        of the user who created the Post.'''

        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile 
        return context

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        profile = self.get_user_profile()
        if not profile or post.profile_id != profile.id:
            return redirect('show_post', pk=post.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        '''After deleting a Post, redirect to the Profile page of the user
        who created the Post.'''
        
        post = self.get_object()
        profile = post.profile
        return reverse('show_profile', args=[profile.pk])  
    


class ShowFollowersDetailView(DetailView):

    model=Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the followers using the accessor method in the model
        context["followers"] = self.object.get_followers()
        return context
    



class ShowFollowingDetailView(DetailView):
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the following list using the accessor method in the model
        context["following"] = self.object.get_following()
        return context
    

class PostFeedListView(UserProfileMixin, ListView):
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'  # accessible in template as 'posts'


    def get_queryset(self):
        profile = self.get_user_profile()
        if not profile:
            return Post.objects.none()
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_user_profile()
        context['profile'] = profile
        return context
    

class SearchView(UserProfileMixin, ListView):
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_user_profile()
        if not self.profile:
            return redirect('create_profile')
        self.query = self.request.GET.get('query', None)
        if not self.query:
            # If no query, show search form
            return render(request, 'mini_insta/search.html', {'profile': self.profile})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Return Posts whose caption contains the query
        return Post.objects.filter(caption__icontains=self.query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Profiles matching the query in username, display_name, or bio_text
        matching_profiles = Profile.objects.filter(
            models.Q(username__icontains=self.query) |
            models.Q(display_name__icontains=self.query) |
            models.Q(bio_text__icontains=self.query)
        )
        context['profile'] = self.profile
        context['query'] = self.query
        context['matching_profiles'] = matching_profiles
        return context


class MyProfileView(UserProfileMixin, DetailView):
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def dispatch(self, request, *args, **kwargs):
        if not self.get_user_profile():
            return redirect('create_profile')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.get_user_profile()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_profile'] = self.object
        context['can_edit'] = True
        context['can_follow'] = False
        context['is_following'] = False
        return context


class CreateProfileView(CreateView):
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_creation_form'] = kwargs.get('user_creation_form', UserCreationForm())
        return context

    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if not user_form.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, user_creation_form=user_form)
            )

        user = user_form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        form.instance.user = user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_my_profile')


class FollowProfileView(UserProfileMixin, View):
    def post(self, request, pk):
        current_profile = self.get_user_profile()
        other_profile = get_object_or_404(Profile, pk=pk)
        if current_profile and current_profile.pk != other_profile.pk:
            Follow.objects.get_or_create(profile=other_profile, follower_profile=current_profile)
        return redirect('show_profile', pk=pk)


class DeleteFollowProfileView(UserProfileMixin, View):
    def post(self, request, pk):
        current_profile = self.get_user_profile()
        other_profile = get_object_or_404(Profile, pk=pk)
        if current_profile:
            Follow.objects.filter(profile=other_profile, follower_profile=current_profile).delete()
        return redirect('show_profile', pk=pk)


class LikePostView(UserProfileMixin, View):
    def post(self, request, pk):
        current_profile = self.get_user_profile()
        post = get_object_or_404(Post, pk=pk)
        if current_profile and post.profile_id != current_profile.pk:
            Like.objects.get_or_create(post=post, profile=current_profile)
        return redirect('show_post', pk=pk)


class DeleteLikePostView(UserProfileMixin, View):
    def post(self, request, pk):
        current_profile = self.get_user_profile()
        post = get_object_or_404(Post, pk=pk)
        if current_profile:
            Like.objects.filter(post=post, profile=current_profile).delete()
        return redirect('show_post', pk=pk)