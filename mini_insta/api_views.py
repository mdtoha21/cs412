from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Photo, Post, Profile
from .serializers import CreatePostSerializer, PostSerializer, ProfileSerializer


def _profile_for_user(user):
    profile = Profile.objects.filter(user=user).first()
    if profile:
        return profile

    profile = Profile.objects.filter(username=user.username).first()
    if profile:
        profile.user = user
        profile.save(update_fields=["user"])
        return profile

    return Profile.objects.create(username=user.username, display_name=user.username, user=user)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    base = request.build_absolute_uri(request.path)
    if not base.endswith("/"):
        base = f"{base}/"
    return Response(
        {
            "login": f"{base}login/",
            "profiles": f"{base}profiles/",
            "my_profile": f"{base}me/",
            "my_posts": f"{base}me/posts/",
            "my_feed": f"{base}me/feed/",
            "create_post": f"{base}posts/",
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def api_login(request):
    username = request.data.get("username", "")
    password = request.data.get("password", "")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    profile = _profile_for_user(user)
    return Response(
        {
            "token": token.key,
            "profile": ProfileSerializer(profile).data,
        }
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_profiles(request):
    profiles = Profile.objects.order_by("id")
    return Response(ProfileSerializer(profiles, many=True).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return Response(ProfileSerializer(profile).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_profile_posts(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = profile.get_all_post()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_profile_feed(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    posts = profile.get_post_feed()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_my_profile(request):
    profile = _profile_for_user(request.user)
    return Response(ProfileSerializer(profile).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_my_posts(request):
    profile = _profile_for_user(request.user)
    posts = profile.get_all_post()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_my_feed(request):
    profile = _profile_for_user(request.user)
    posts = profile.get_post_feed()
    return Response(PostSerializer(posts, many=True).data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def api_create_post(request):
    payload = CreatePostSerializer(data=request.data)
    payload.is_valid(raise_exception=True)

    profile = _profile_for_user(request.user)
    post = Post.objects.create(profile=profile, caption=payload.validated_data.get("caption", ""))

    image_url = payload.validated_data.get("image_url", "")
    if image_url:
        Photo.objects.create(post=post, image_url=image_url)

    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
