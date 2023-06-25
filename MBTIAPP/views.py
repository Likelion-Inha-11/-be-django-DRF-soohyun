from rest_framework import generics,mixins
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer,PostBaseModelSerializer
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from MBTIAPP.forms import Signupform,MbtiForm,CommentForm
from .models import Post, Profile, Comment, Category
from rest_framework.decorators import api_view
# from django.urls import reverse


# Create your views here.
def main(request):
    
    return render(request, 'MBTIAPP/main.html')

def detail(request, pk):
    post_detail = get_object_or_404(Post, pk=pk)
    comments = post_detail.comment_set.all()
    context = {
        'post' : post_detail,
        'comments' : comments,
    }
    return render(request, 'MBTIAPP/detail.html', context)

def edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.save()  
        return redirect('MBTIAPP:detail', pk)
    else:
        context = {
            'post' : post
        }
        return render(request, 'MBTIAPP/edit.html', context), render(request, 'MBTIAPP/blog.html', context)
    
def delete(pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('MBTIAPP:blog')


class PostListGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostBaseModelSerializer
    template_name= 'MBTIAPP/blog.html'



@api_view(['GET'])
def category(request, category_id):
    posts = Post.objects.filter(category=category_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def my_posts(requsest):
    user_id=requsest.user.id
    posts = Post.objects.filter(poster=user_id)
    serializer = PostSerializer(posts, many=True)
    serialized_data= serializer.data
    return Response(serialized_data)

@api_view(['GET'])
def user_post(request, poster_id):
    posts =  Post.objects.filter(poster = poster_id)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_my_comments(request):
    user_id = request.user.id
    comments = Comment.objects.filter(poster = user_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

def new(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'MBTIAPP/postcreate.html', context)

def postcreate(request):
    if(request.method == 'POST'):
        post = Post()
        post.title=request.POST['title']
        post.content=request.POST['content']
        post.poster = request.user
        post.save()     
        categories = request.POST.getlist('category')
        if categories: 
            post.categories.set(categories)
    return redirect('MBTIAPP:blog')


def comment_create(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        form = CommentForm()
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.commenter = request.user
                comment.save()
                return redirect('MBTIAPP:detail', pk)
        else:
            form = CommentForm()
        return render(request, 'MBTIAPP/detail.html', {'post':post, 'form': form})



def comment_delete(request, post_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.commenter:
            comment.delete()
    return redirect('MBTIAPP:detail', post_pk) 

def comment_edit(request, post_pk, comment_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST':
            comment.content=request.POST['content']
            comment.save()  
            return redirect('MBTIAPP:detail', post_pk)
    else:
        context = {
            'comment' : comment,
            'post' : post,
            'comment_content' : comment.content
        }
        return render(request, 'MBTIAPP/comment_edit.html', context)   

def mbtitest(request):
    form = MbtiForm()
    return render(request, 'MBTIAPP/mbti_test.html', {'form':form})

def result(request):
    if request.method == 'POST':
        form = MbtiForm(request.POST)
        if form.is_valid():
            EI = form.cleaned_data['EI']
            NS = form.cleaned_data['NS']
            TF = form.cleaned_data['TF']
            PJ = form.cleaned_data['PJ']
            arr=[EI, NS, TF, PJ]
            my_mbti = ''.join(arr)
            user = request.user
            user.user_mbti = my_mbti
            user.save()
            context = {'mymbti':my_mbti}
            return render(request, 'MBTIAPP/result.html', context)
    else:
        form = MbtiForm()
        context = {'form': form}
        return render(request, 'MBTIAPP/result.html',context)





def signup(request):
    if request.method == "POST":
        form = Signupform(request.POST)
        if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('MBTIAPP:main')
    else:
        form = Signupform()
    return render(request, 'MBTIAPP/signup.html', {'form' : form})
