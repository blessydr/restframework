from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Blog,Tag
from .serializers import BlogSerializer,RegisterSerializer,LoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from rest_framework.decorators import api_view

class BlogListCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        search_query = request.query_params.get('search', None)
        blogs = Blog.objects.filter(user=request.user)
        from_date=request.query_params.get('from_date')
        to_date=request.query_params.get('to_date')
        if search_query:
            blogs = blogs.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) | 
                Q(tags__name__icontains=search_query)
            ).distinct()
            
        if from_date and to_date:
            blogs=blogs.filter(created_at__range=[from_date,to_date])
            
        elif from_date:
            blogs=blogs.filter(created_at__range=from_date)
            
        elif from_date:
            blogs=blogs.filter(created_at__range=to_date)
            
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



@api_view(['PUT', 'DELETE'])
def blog_edit_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user != blog.user and not request.user.is_staff:
        return Response({"detail": "You do not have permission to edit or delete this blog."}, status=status.HTTP_403_FORBIDDEN)

    if request.method=='PUT':
        data = request.data
        tags_data = data.get('tags', [])
        if tags_data:
            tags = []
            for tag_name in tags_data:
                # If the tag doesn't exist, create it
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tags.append(tag)
                
            blog.tags.set(tags)
            
            
        serializer = BlogSerializer(blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH' and 'remove_tags' in request.data:
        tags_to_remove = request.data.get('remove_tags', [])
        if tags_to_remove:
            tags = Tag.objects.filter(name__in=tags_to_remove)  # If using names
            blog.tags.remove(*tags) 
            return Response({"message": "Tags removed successfully", "tags": [tag.name for tag in blog.tags.all()]})

        return Response({"detail": "No tags to remove."}, status=status.HTTP_400_BAD_REQUEST)
     
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