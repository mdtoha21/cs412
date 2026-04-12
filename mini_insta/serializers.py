from rest_framework import serializers

from .models import Photo, Post, Profile


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Photo
        fields = ["id", "image", "image_url", "timestamp"]

    def get_image(self, obj):
        return obj.get_image_url()


class PostSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(source="photo_set", many=True, read_only=True)
    profile_id = serializers.IntegerField(source="profile.id", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "profile_id", "caption", "timestamp", "photos"]


class ProfileSerializer(serializers.ModelSerializer):
    num_followers = serializers.SerializerMethodField()
    num_following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "display_name",
            "profile_image_url",
            "bio_text",
            "join_date",
            "num_followers",
            "num_following",
        ]

    def get_num_followers(self, obj):
        return obj.get_num_followers()

    def get_num_following(self, obj):
        return obj.get_num_following()


class CreatePostSerializer(serializers.Serializer):
    caption = serializers.CharField(required=False, allow_blank=True)
    image_url = serializers.URLField(required=False, allow_blank=True)

    def validate(self, attrs):
        caption = attrs.get("caption", "").strip()
        image_url = attrs.get("image_url", "").strip()
        if not caption and not image_url:
            raise serializers.ValidationError("Provide caption or image_url.")
        attrs["caption"] = caption
        attrs["image_url"] = image_url
        return attrs
