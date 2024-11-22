from rest_framework import serializers
from .models import Blog
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'user', 'tags','created_at', 'updated_at']
        def create(self, validated_data):
            tags_data = validated_data.pop('tags')  # Extract tags data
            blog = Blog.objects.create(**validated_data)  # Create the Blog object

            # Loop through each tag data
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name'])  # Get or create the tag
                blog.tags.add(tag)  # Add tag to blog's tags

            return blog
            

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        # Authenticate the user
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        return data

    def get_user(self, data):
        # Authenticate the user and return the user instance
        return authenticate(username=data['username'], password=data['password'])

class RegisterSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is taken')
        return data

    def create(self,validated_data):
        user=User.objects.create(first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],username=validated_data['username'])
        user.set_password(validated_data['password'])
        return validated_data

from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
