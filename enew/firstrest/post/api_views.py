from .models import Post
from .serializer import PostSerializer
from django.http import Http404 #Get object or 404 직접구현
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class PostList(APIView):

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True) #쿼리셋 넘기기
        return Response(serializer.data)        #직접 Response 리턴해주기
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():   #직접 유효성 검사
            serializer.save()       #문제가 없으면 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST) #오류페이지 보여주기

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):    #정보 읽기
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):    #정보 수정
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_BAD_REQUEST)
    
    def delete(self, request, pk, format=None): #정보 삭제
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        