from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile, Post, Photo,Follow
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.shortcuts import get_object_or_404

from django.urls import reverse
# Create your views here.


class  ProfileListView(ListView):
    '''Define a view class to show all mini_insta profiles'''
    model=Profile
    template_name="mini_insta/show_all_profiles.html"
    context_object_name="profiles"


class ProfileDetailView(DetailView):
    '''Define a view class to show a single mini_insta profiles'''

    model=Profile
    template_name="mini_insta/show_profile.html"
    context_object_name="profile"



class PostDetailView(DetailView):
    """ Display a single Post, including its caption, timestamp, and photos."""

    model=Post
    template_name="mini_insta/show_post.html"
    context_object_name="post"


class CreatePostView(CreateView):
    '''Allow users to create a new Post associated with a specific Profile.
'''
    model = Post
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"


    def get_context_data(self, **kwargs):

        '''Add the Profile object to the context data
        so the form knows which Profile this Post belongs to.'''

        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        context['profile'] = profile
        return context


    def form_valid(self, form):
        ''' Attaches the Post to the correct Profile and creates an associated Photo.'''
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
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





class UpdatePostView(UpdateView):

    ''''View to update a Post's information.

    Inherits from Django's generic UpdateView.'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        ''' After successfully updating a Post, redirect to the page
        showing that Post.'''

        return reverse('show_post', args=[self.object.pk])
    

class DeletePostView(DeleteView):
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
    

class PostFeedListView(ListView):
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'  # accessible in template as 'posts'


    def get_queryset(self):
        # Retrieve the profile based on the pk in URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context