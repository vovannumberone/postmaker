from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Msg
from .forms import PostForm, MessageForm, NaviForm

import requests
import json
# Create your views here.
def posting(url, data):
    response = requests.post(url, data)
    return json.loads(response.text)

def make_post(post):
    token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'
    save_photo = {'url': 'https://api.vk.com/method/photos.copy?',
    'data': {'access_token': token, 'v': 3, 'owner_id': post['owner_id'], 'photo_id': post['photo_id']}}
    saved_id = posting(save_photo['url'], save_photo['data'])['response']
    likes_indic = post['likes']
    reposts_indic = post['reposts']
    link = 'photo78767814_' + str(saved_id)

    postt = {'url': 'https://api.vk.com/method/wall.post?',
    'data': {'access_token': token, 'v': 3, 'owner_id': -142223503, 'attachments': link,'from_group': 1,}}
    return posting(postt['url'], postt['data'])

def postmaker(request):#, pk, group):
    response = ''
    form = NaviForm
    one = 1
    from . import postgetter
    post_list = postgetter.sl

    if 'next' in request.GET:
        page = int(request.GET["next"]) + 1
        try:
            link = post_list[page]['full_link']
        except KeyError:
            page = page-1
    elif 'prev' in request.GET:
        page = int(request.GET["prev"]) - 1
        try:
            link = post_list[page]['full_link']
        except KeyError:
            page = page+1
    elif 'make_post' in request.GET:
        page = int(request.GET["make_post"])
        post_data = post_list[page]
        response = make_post(post_data)

    else:
        page = 1

    link = post_list[page]['full_link']
    if post_list[page]['text'] == '':
        text = 'Sample text.'
    else:
        text = post_list[page]['text']
    return render(request, 'blog/postmaker.html', {'request': request,
    'link': link, 'text': text, 'page': page, 'form': form, 'response': response})

def postmakers(request):#, pk, group):
    form = NaviForm
    one = 1
    from . import postgetter
    post_list = postgetter.sl

    if request.method == 'POST':
        page = request.POST["page"]
        page = int(page)
        try:
            link = post_list[page]['full_link']
        except KeyError:
            page = page-1
        if post_list[page]['text'] == '':
            text = 'Sample text.'
        else:
            text = post_list[page]['text']
        return render(request, 'blog/postmaker.html', {'request': request,
        'link': link, 'text': text, 'page': page, 'form': form})

    else:
        page = 1
        link = post_list[page]['full_link']
        if post_list[page]['text'] == '':
            text = 'Sample text.'
        else:
            text = post_list[page]['text']
        return render(request, 'blog/postmaker.html', {'request': request,
        'link': link, 'text': text, 'page': page, 'form': form})

def send(request):
    form = MessageForm
    if request.method == 'POST':
        user = request.POST["user"]
        msg = request.POST["message"]
        token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'
        data={'url': 'https://api.vk.com/method/messages.send?',
        'data': {'access_token': token, 'v': 5.71, 'user_id': user, 'message': msg}}
        response = requests.post(data['url'], data['data'])
        result = str(json.loads(response.text))

        return render (request, 'blog/send_result.html', {'result': result})
    else:
        return render(request, 'blog/send.html', {'form': form})

def index(request):
    return render(request, 'blog/index.html')

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
