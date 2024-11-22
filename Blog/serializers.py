from rest_framework import serializers
from Blog.models import  blog
from django.contrib.auth.models import User

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

class blogserializer(serializers.ModelSerializer):
    class Meta:
        model=blog
        fields='__all__'
        
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model=User
        fields=['id','username','password']