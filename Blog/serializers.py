from rest_framework import serializers
from Blog.models import  blog
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is taken')
        return data

class blogserializer(serializers.ModelSerializer):
    class Meta:
        model=blog
        fields='__all__'
        
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password']