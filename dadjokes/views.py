from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
app_name = 'dadjokes'
def home(request):
    # show one random joke and one random picture
    joke = Joke.objects.order_by('?').first()
    picture = Picture.objects.order_by('?').first()
    return render(request, 'dadjokes/home.html', {'joke': joke, 'picture': picture})

def random_page(request):
    joke = Joke.objects.order_by('?').first()
    picture = Picture.objects.order_by('?').first()
    return render(request, 'dadjokes/random.html', {'joke': joke, 'picture': picture})

def jokes_list(request):
    jokes = Joke.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/jokes.html', {'jokes': jokes})

def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    return render(request, 'dadjokes/joke_detail.html', {'joke': joke})

def pictures_list(request):
    pictures = Picture.objects.all().order_by('-created_at')
    return render(request, 'dadjokes/pictures.html', {'pictures': pictures})

def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'dadjokes/picture_detail.html', {'picture': picture})
# Create your views here.

class APIRandomJoke(APIView):
    def get(self, request):
        joke = Joke.objects.order_by('?').first()
        if not joke:
            return Response({"detail": "No jokes yet."}, status=status.HTTP_404_NOT_FOUND)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)

class APIJokeListCreate(generics.ListCreateAPIView):
    queryset = Joke.objects.all().order_by('-created_at')
    serializer_class = JokeSerializer

class APIJokeDetail(generics.RetrieveAPIView):
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class APIAllPictures(generics.ListAPIView):
    queryset = Picture.objects.all().order_by('-created_at')
    serializer_class = PictureSerializer

class APIPictureDetail(generics.RetrieveAPIView):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class APIRandomPicture(APIView):
    def get(self, request):
        picture = Picture.objects.order_by('?').first()
        if not picture:
            return Response({"detail": "No pictures yet."}, status=status.HTTP_404_NOT_FOUND)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)