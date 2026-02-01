from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
# Create your views here.
quotes = [
    "Life is like riding a bicycle. To keep your balance you must keep moving.",
    "Imagination is more important than knowledge.",
    "Try not to become a man of success, but rather try to become a man of value."
]


# List of images
images = [
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    "https://cdn.britannica.com/09/75509-050-86D8CBBF/Albert-Einstein.jpg",
    "https://media.sciencephoto.com/c0/28/65/20/c0286520-800px-wm.jpg"
]





def home(request):

    """Render the home page template with a random quote and image."""

    context = {
        "quote": random.choice(quotes),
        "image": random.choice(images)
    }

    template_name='quotes/home.html'

    return render(request,template_name,context)

def quote(request):

    """Render a page showing a random quote and image."""


    context = {
        "quote": random.choice(quotes),
        "image": random.choice(images)
    }

    template_name='quotes/quote.html'


    return render(request,template_name,context)


def show_all(request):


    """Render a page displaying all quotes and images."""



    context = {
        "quotes": quotes,
        "images": images
    }

    template_name='quotes/show_all.html'


    return render(request,template_name,context)


def about(request):

    """Render the about page with information about the person and creator."""


    template_name='quotes/about.html'


    return render(request,template_name)