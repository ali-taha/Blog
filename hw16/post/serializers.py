from rest_framework import serializers
from post.models import Post, Category, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]  

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["slug"]

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title"]        

class PostSerializer(serializers.ModelSerializer):
    writer = UserSerializer()
    class Meta:
        model = Post
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["slug"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["slug"]
        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
