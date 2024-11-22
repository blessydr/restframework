from  rest_framework.response import Response
from rest_framework.decorators import api_view
from Blog.models import  blog
from rest_framework.views import APIView
from .serializers import blogserializer,UserSerializer,RegisterSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class RegistrationView(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data':{},
                'message':'your account is created'
                }, status=status.HTTP_201_CREATED
             )

        except Exception as e:
            return Response({
                    'data':serializer.errors,
                    'message':'somthing went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)



def example_view(request):
    data = {
        'message': 'Hello, Blessy!',
        'status': 'success'
    }
    return JsonResponse(data)



@api_view(['GET'])
def getData(request):
    blogs=blog.objects.all()
    serializer=blogserializer(blogs,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_blog(request):
    serializer=blogserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response (serializer.data)

@api_view(['POST'])
def login(request):
    username= request.data['username']
    user=get_object_or_404(User,username=username)
    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
    token, _=Token.objects.get_or_create(user=user)
    # print("abcd")
    serializer=UserSerializer(instance=user)
    return Response({"token":token.key, "user": serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save() 
        
        user.set_password(request.data['password'])
        user.save()
        token,_ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def test_token(request):
    return Response({})