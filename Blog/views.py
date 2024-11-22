from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Blog,Tag
from .serializers import BlogSerializer,RegisterSerializer,LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
class BlogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blogs = Blog.objects.filter(user=request.user)
        serializer = BlogSerializer(blogs, many=True)
        return Response({'data': serializer.data, 'message': 'Blogs fetched successfully'}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id 
        tags_data = data.pop('tags', []) 
        serializer = BlogSerializer(data=data)
        
        if serializer.is_valid():
            blog = serializer.save()
            
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(name=tag_data['name']) 
                blog.tags.add(tag)  # Add the tag to the blog
            
            return Response({'data': serializer.data, 'message': 'Blog created successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({'data': serializer.errors, 'message': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
    
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.get_user(serializer.validated_data)
        
      
        if not user:
            return Response({
                'data': {},
                'message': 'Invalid username or password'
            }, status=status.HTTP_401_UNAUTHORIZED)
     
        return Response({
            'data': {
                'username': user.username,
            },
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
        
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



# @api_view(['POST'])
# def login(request):
#     username= request.data['username']
#     user=get_object_or_404(User,username=username)
#     if not user.check_password(request.data['password']):
#         return Response({"detail":"Not found"},status=status.HTTP_404_NOT_FOUND)
#     token, _=Token.objects.get_or_create(user=user)
#     # print("abcd")
#     serializer=UserSerializer(instance=user)
#     return Response({"token":token.key, "user": serializer.data})

# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save() 
        
#         user.set_password(request.data['password'])
#         user.save()
#         token,_ = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key, "user": serializer.data})
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def test_token(request):
#     return Response({})